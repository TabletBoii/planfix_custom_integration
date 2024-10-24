import re

from enums.planfix_task_fields_enum import HasGlobalTaskFieldsEnum, HasGlobalTaskTemplateEnum, \
    HasChinaTaskFieldsEnum, HasIndustrialTaskFieldsEnum


class Utils:

    @staticmethod
    def extract_first_6_digits(text: str) -> int:
        all_digits = re.findall(r'\d', text)

        digits_str = ''.join(all_digits)

        if len(digits_str) == 0:
            return 0

        claim_id = digits_str[:6]

        return claim_id

    @staticmethod
    def china_from_request_body(current_date: str, offset: int, page_offset: int = 100) -> dict:
        fields = ""
        templates = []

        for enum_index, field_enum in enumerate(HasChinaTaskFieldsEnum):
            if enum_index == len(HasChinaTaskFieldsEnum):
                fields += str(field_enum.value)
            else:
                fields += str(field_enum.value) + ","

        for field_enum in HasChinaTaskFieldsEnum:
            templates.append(field_enum.value)

        request_body = {
            "offset": offset,
            "pageSize": page_offset,
            "filters": [
                {
                    "type": 103,
                    "operator": "gt",
                    "value": {
                        "dateType": "otherDate",
                        "dateValue": current_date
                    },
                    "field": 104770
                }
            ],
            "fields": "id,name,object," + fields
        }

        return request_body

    @staticmethod
    def industrial_from_request_body(current_date: str, offset: int, page_offset: int = 100) -> dict:
        fields = ""
        templates = []

        for enum_index, field_enum in enumerate(HasIndustrialTaskFieldsEnum):
            if enum_index == len(HasIndustrialTaskFieldsEnum):
                fields += str(field_enum.value)
            else:
                fields += str(field_enum.value) + ","

        for field_enum in HasIndustrialTaskFieldsEnum:
            templates.append(field_enum.value)

        request_body = {
            "offset": offset,
            "pageSize": page_offset,
            "filters": [
                {
                    "type": 103,
                    "operator": "gt",
                    "value": {
                        "dateType": "otherDate",
                        "dateValue": current_date
                    },
                    "field": 22905
                }
            ],
            "fields": "id,name,object,project," + fields
        }

        return request_body

    @staticmethod
    def global_form_request_body(current_date: str, offset: int, page_offset: int = 100) -> dict:
        fields = ""
        templates = []

        for enum_index, field_enum in enumerate(HasGlobalTaskFieldsEnum):
            if enum_index == len(HasGlobalTaskFieldsEnum):
                fields += str(field_enum.value)
            else:
                fields += str(field_enum.value) + ","

        for field_enum in HasGlobalTaskTemplateEnum:
            templates.append(field_enum.value)

        request_body = {
            "offset": offset,
            "pageSize": page_offset,
            "filters": [
                {
                    "type": 103,
                    "operator": "gt",
                    "value": {
                        "dateType": "otherDate",
                        "dateValue": f"{current_date}"
                    },
                    "field": 85856
                },
                # Шаблоны
                {
                    "type": 51,
                    "operator": "equal",
                    "value": templates
                },
            ],
            "fields": f"id,name," + fields
        }

        return request_body

    @staticmethod
    def generate_task_dict(task_item: dict, organization: str, planfix_org: str) -> dict:
        splited_task_name = task_item["name"].split(" ")
        if "object" in task_item.keys():
            claim_id = splited_task_name[0]
        else:
            claim_result = Utils.extract_first_6_digits(task_item["name"])
            claim_id = claim_result if claim_result != 0 else task_item["id"]
            # claim_id = splited_task_name[1] if splited_task_name[0] == "Согласование" and splited_task_name[1] != "ведомости" else task_item["id"]
            organization = ""
        try:
            task_dict = {
                "claim_name": task_item["name"],
                "claim_id": claim_id,
                "pay_date": "",
                "subitem": "",
                "turnover_date": "",
                "currency": "",
                "subitem_id": None,
                "amount_to_pay": None,
                "paid": None,
                "acquisition_cost": None,
                "payment_type": "",
                "project": "",
                "project_id": task_item["project"]["id"] if organization == 'ТОО "HAS Industrial"' else None,
                "provider": "",
                "organization": organization,
                "has_photo_confirmation": True,
                "initiator": "",
                "supplier": "",
                "planfix_org": planfix_org
            }

        except Exception as e:
            print(e)
            print(splited_task_name)
            return

        for field in task_item["customFieldData"]:
            match field["field"]["name"]:

                case "Дата оплаты":
                    task_dict["pay_date"] = field["stringValue"]
                case "Статья расхода" | "Статья бюджета":
                    task_dict["subitem"] = field["value"] if isinstance(field["value"], str) else \
                        field["value"]["value"]
                    task_dict["subitem_id"] = field["stringValue"]
                case "Дата совершения оборота":
                    task_dict["turnover_date"] = field["stringValue"]
                case "Валюта приобретения" | "Валюта":
                    task_dict["currency"] = field["value"]
                case "Сумма к оплате":
                    try:
                        task_dict["amount_to_pay"] = field["value"]
                    except Exception as e:
                        task_dict["amount_to_pay"] = 0
                case "Оплаченная сумма" | "Оплачено" | "Сумма предоплаты перевозчику":
                    try:
                        task_dict["paid"] = field["value"]
                    except Exception as e:
                        task_dict["paid"] = 0
                case "Стоимость приобретения":
                    task_dict["acquisition_cost"] = field["value"]
                case "Вид платежа":
                    task_dict["payment_type"] = field["stringValue"]
                case "Проект (целевое назначение)":
                    task_dict["project"] = "" if isinstance(field["value"], str) else field["value"]["value"]
                    task_dict["project_id"] = None if isinstance(field["value"], str) else field["value"]["id"]
                case "Организация":
                    task_dict["organization"] = field["stringValue"]
                case "Заказчик" "Наименование банка" | "Контрагент (наименование)":
                    task_dict["provider"] = field["stringValue"] if isinstance(field["stringValue"], str) else field["value"]["name"]
                case "Поставщик" | "Контрагент/поставщик":
                    task_dict["supplier"] = field["stringValue"] if isinstance(field["stringValue"], str) else field["value"]["name"]
                case "Прикрепить фотоподтверждение":
                    task_dict["has_photo_confirmation"] = True if field["stringValue"] != "" else False
                case "Инициатор":
                    task_dict["initiator"] = field["stringValue"]
        return task_dict

    @staticmethod
    def exclude_incorrect_claims_by_name(task_name: str) -> bool:
        excluded_claim_names = [
            "{{Задача.Номер}}",
            "тест"
        ]

        for excluded_name in excluded_claim_names:
            if excluded_name in task_name:
                return False
        return True
