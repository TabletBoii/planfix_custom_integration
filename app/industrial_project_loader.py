import os
import requests
from sqlalchemy import text
from sqlalchemy.orm import Session

from models.models import IndustrialProjects


class IndustrialProjectListLoader:
    def __init__(self, session):
        self.has_db_session: Session = session
        self.PLANFIX_URL = os.getenv("PLANFIX_INDUSTRIAL_URL")
        self.headers = {"Authorization": f"Bearer {os.getenv('PLANFIX_INDUSTRIAL_BEARER_TOKEN')}"}

    def check_directory_table(self):
        pass

    def get_project_list(self) -> list:
        get_project_list_endpoint = f'project/list'

        get_project_list_url = self.PLANFIX_URL + get_project_list_endpoint
        offset_value = 0
        project_entry_list = []
        while True:
            post_body = {
                "offset": offset_value,
                "pageSize": 100,
                "filters": [

                ],
                "fields": "id,name,description"
            }

            project_entries_response = requests.post(get_project_list_url, headers=self.headers, json=post_body).json()["projects"]
            if len(project_entries_response) == 0:
                break
            print(project_entries_response)
            for project_entry in project_entries_response:
                project_entry_list.append(
                    IndustrialProjects(
                        project_id=project_entry["id"],
                        project_name=project_entry["name"],
                        description=project_entry["description"]
                    )
                )
            offset_value += 100

        return project_entry_list

    def load_project_table(self):
        project_entries = self.get_project_list()
        self.has_db_session.add_all(project_entries)
        self.has_db_session.commit()

    def run(self):
        self.has_db_session.execute(text('TRUNCATE industrial_projects'))
        self.load_project_table()

