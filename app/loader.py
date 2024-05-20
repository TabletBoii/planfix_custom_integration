import requests
from datetime import datetime, timedelta

from sqlalchemy import insert

from models.models import Expenses
from sqlalchemy.orm import Session

PLANFIX_URL = 'https://hasglobal.planfix.ru/rest/'
PLANFIX_BEARER_TOKEN = '03a35ecbd1b914d535e0d81408053573'
headers = {"Authorization": f"Bearer {PLANFIX_BEARER_TOKEN}"}


class HasDBLoader:
    def __init__(self, session):
        self.has_db_session: Session = session

    def get_task_list(self):
        # поставил с 3 до 4, потому что в planfix нет >=
        current_date = (datetime.today() - timedelta(days=4)).strftime("%d-%m-%Y")
        print(current_date)

        get_task_list_endpoint = 'task/list'
        get_task_list_url = PLANFIX_URL + get_task_list_endpoint
        post_body = {
            "offset": 0,
            "pageSize": 100,
            "filters": [
                {
                    "type": 12,
                    "operator": "gt",
                    "value": {
                        "dateType": "otherDate",
                        "dateValue": f"{current_date}"
                    }
                },
                {
                    "type": 5,
                    "operator": "equal",
                    "value": [
                        128
                    ]
                },
                {
                    "type": 51,
                    "operator": "equal",
                    "value": 125
                },
            ],
            "fields": "id,name,85850,86190,87018,67632,85874,85856,67630,85858,86392,67636,85874"
        }

        response = requests.post(get_task_list_url, headers=headers, json=post_body).json()
        print(response)
        # print(len(response["tasks"]))
        # print(response["tasks"])
        task_list = []
        for task in response["tasks"]:
            task_dict = {
                "claim_name": task["name"]
            }
            key_checkout = [
                "pay_date",
                "subitem",
                "turnover_date",
                "currency",
                "subitem_id",
                "amount_to_pay",
                "paid",
                "acquisition_cost",
                "payment_type",
                "project",
                "project_id"
            ]

            for field in task["customFieldData"]:
                match field["field"]["name"]:
                    case "Дата оплаты":
                        task_dict["pay_date"] = field["stringValue"]
                        key_checkout.remove("pay_date")
                    case "Статья расхода":
                        task_dict["subitem"] = field["value"] if isinstance(field["value"], str) else field["value"]["value"]
                        print(field)
                        task_dict["subitem_id"] = field["stringValue"]
                        key_checkout.remove("subitem")
                        key_checkout.remove("subitem_id")
                    case "Дата совершения оборота":
                        task_dict["turnover_date"] = field["stringValue"]
                        key_checkout.remove("turnover_date")
                    case "Валюта приобретения":
                        task_dict["currency"] = field["value"]
                        key_checkout.remove("currency")
                    case "Сумма к оплате":
                        task_dict["amount_to_pay"] = field["value"]
                        key_checkout.remove("amount_to_pay")
                    case "Оплаченная сумма":
                        task_dict["paid"] = field["value"]
                        key_checkout.remove("paid")
                    case "Стоимость приобретения":
                        task_dict["acquisition_cost"] = field["value"]
                        key_checkout.remove("acquisition_cost")
                    case "Вид платежа":
                        task_dict["payment_type"] = field["stringValue"]
                        key_checkout.remove("payment_type")
                    case "Проект (целевое назначение)":
                        task_dict["project"] = "" if isinstance(field["value"], str) else field["value"]["value"]
                        task_dict["project_id"] = None if isinstance(field["value"], str) else field["value"]["id"]
                        key_checkout.remove("project")
                        key_checkout.remove("project_id")

            if len(key_checkout) != 0:
                for key in key_checkout:
                    task_dict[key] = ""
            task_list.append(task_dict)
        self.has_db_session.execute(
            insert(Expenses),
            task_list
        )
        self.has_db_session.commit()
        # print(task_list)


