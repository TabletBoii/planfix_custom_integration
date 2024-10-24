import os

import requests

from abstraction.abstract_loader import HasExpensesLoader
from sqlalchemy.orm import Session

from utils import Utils


class HasGlobalExpensesLoader(HasExpensesLoader):

    def __init__(self, session, url, token, start_date, planfix_org):
        super().__init__(session, url, token, start_date, planfix_org)
        self.has_db_session: Session = session
        self.PLANFIX_URL = os.getenv('PLANFIX_URL')
        self.PLANFIX_BEARER_TOKEN = os.getenv('PLANFIX_BEARER_TOKEN')
        self.headers = {"Authorization": f"Bearer {self.PLANFIX_BEARER_TOKEN}"}
        self.task_list = []
        self.get_task_list_endpoint = 'task/list'
        self.get_task_list_url = self.PLANFIX_URL + self.get_task_list_endpoint

    def get_planfix_expenses_query(self):
        return

    def fetch_planfix_tasks(self, current_date: str, current_offset: int, get_task_list_url: str) -> None:
        while True:
            print("Выгружаются данные с оффсетом: ", current_offset)
            post_body = Utils.global_form_request_body(
                current_date=current_date,
                offset=current_offset
            )

            response = requests.post(get_task_list_url, headers=self.headers, json=post_body)
            try:
                response_json = response.json()
            except Exception as e:
                print(e)
                print(response.text)
                return
            if len(response_json["tasks"]) == 0:
                break

            for task_item in response_json["tasks"]:
                is_claim_name_excluded = Utils.exclude_incorrect_claims_by_name(
                    task_name=task_item["name"]
                )
                if not is_claim_name_excluded:
                    continue
                task_dict = Utils.generate_task_dict(
                    task_item=task_item,
                    organization="",
                    planfix_org="global"
                )
                self.task_list.append(task_dict)

            current_offset += 100
