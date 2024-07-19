import requests
from utils import Utils
from enums.planfix_task_fields_enum import HasChinaObjectsEnum
from abstraction.abstract_loader import HasExpensesLoader


class HasChinaExpensesLoader(HasExpensesLoader):

    def __init__(self, session, url, token, start_date):
        super().__init__(session, url, token, start_date)

    def get_planfix_expenses_query(self):
        return

    def fetch_planfix_tasks(self, current_date: str, current_offset: int, get_task_list_url: str) -> None:
        object_list = [object_enum.value for object_enum in HasChinaObjectsEnum]
        while True:
            preprocessed_task_list = []
            print("Выгружаются данные с оффсетом: ", current_offset)
            post_body = Utils.china_from_request_body(
                current_date=current_date,
                offset=current_offset
            )

            response = requests.post(get_task_list_url, headers=self.headers, json=post_body).json()
            if len(response["tasks"]) == 0:
                break
            for task in response["tasks"]:
                try:
                    if task["object"]["id"] in object_list:
                        preprocessed_task_list.append(task)
                except KeyError as e:
                    continue

            for task_item in preprocessed_task_list:
                is_claim_name_excluded = Utils.exclude_incorrect_claims_by_name(
                    task_name=task_item["name"]
                )
                if not is_claim_name_excluded:
                    continue
                task_dict = Utils.generate_task_dict(
                    task_item=task_item,
                    organization='China'
                )
                self.task_list.append(task_dict)

            current_offset += 100
