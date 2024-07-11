from abc import abstractmethod, ABC
from sqlalchemy.orm import Session
import requests
from sqlalchemy import insert
from models.models import Expenses


class HasExpensesLoader(ABC):

    def __init__(self, session, url, token, start_date):
        self.has_db_session: Session = session
        self.PLANFIX_URL = url
        self.PLANFIX_BEARER_TOKEN = token
        self.headers = {"Authorization": f"Bearer {self.PLANFIX_BEARER_TOKEN}"}
        self.task_list = []
        self.get_task_list_endpoint = 'task/list'
        self.get_task_list_url = self.PLANFIX_URL + self.get_task_list_endpoint
        self.start_date = start_date

    def get_planfix_expenses_query(self):
        return

    @abstractmethod
    def fetch_planfix_tasks(self, current_date: str, current_offset: int, get_task_list_url: str) -> None:
        pass

    def get_task_list(self):
        current_date = self.start_date
        # current_date = f"01-06-2024"
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