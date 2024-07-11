import os

import requests
from datetime import datetime, timedelta

from sqlalchemy import insert

from models.models import Expenses
from sqlalchemy.orm import Session

from utils import Utils
from enums.planfix_task_fields_enum import HasGlobalTaskTemplateEnum
from enum import Enum


class HasGlobalExpensesLoader:

    def __init__(self, session):
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

            response = requests.post(get_task_list_url, headers=self.headers, json=post_body).json()
            if len(response["tasks"]) == 0:
                break

            for task_item in response["tasks"]:
                is_claim_name_excluded = Utils.exclude_incorrect_claims_by_name(
                    task_name=task_item["name"]
                )
                if not is_claim_name_excluded:
                    continue
                task_dict = Utils.generate_task_dict(
                    task_item=task_item
                )
                self.task_list.append(task_dict)

            current_offset += 100

    def get_task_list(self):

        current_date = f"16-05-2024"
        current_offset = 0
        print(current_date)
        # for template in TaskTemplateEnum:
        #     print(f"Template name: {template.name}")
        self.fetch_planfix_tasks(
            current_date=current_date,
            current_offset=current_offset,
            get_task_list_url=self.get_task_list_url
        )
        print("Database insertion started")
        self.has_db_session.execute(
            insert(Expenses),
            self.task_list
        )
        self.has_db_session.commit()
        print("Script finished successfully")
        # print(task_list)

    # def set_tasks(self):
    #
    # def initial_database_fill(self):

