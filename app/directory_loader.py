import os
import requests
from sqlalchemy import insert
from sqlalchemy.orm import Session

from models.models import FofExpenses


class DirectoryLoader:
    def __init__(self, session):
        self.has_db_session: Session = session
        self.PLANFIX_URL = os.getenv("PLANFIX_URL")
        self.headers = {"Authorization": f"Bearer {os.getenv("PLANFIX_BEARER_TOKEN")}"}
        self.directory_id = 17112

    def check_directory_table(self):
        pass

    def get_directory_list(self) -> list:
        get_task_list_endpoint = f'directory/{self.directory_id}/entry/list'

        get_task_list_url = self.PLANFIX_URL + get_task_list_endpoint
        offset_value = 0
        directory_entry_list = []
        while True:
            post_body = {
                "offset": offset_value,
                "pageSize": 100,
                "fields": "48054,48064,48066,48068,48060,48062,key",
                "filters": [

                ]
            }
            directory_entries_response = requests.post(get_task_list_url, headers=self.headers, json=post_body).json()["directoryEntries"]
            if len(directory_entries_response) == 0:
                break
            print(directory_entries_response)
            for directory_entry in directory_entries_response:
                directory_entry_list.append(
                    FofExpenses(
                        item=directory_entry['customFieldData'][1]['value'] if isinstance(directory_entry['customFieldData'][1]['value'], str) else directory_entry['customFieldData'][1]['value']['value'],
                        subitem=directory_entry['customFieldData'][0]['value'] if isinstance(directory_entry['customFieldData'][0]['value'], str) else directory_entry['customFieldData'][0]['value']['value'],
                        activity_type=directory_entry['customFieldData'][3]['value'] if isinstance(directory_entry['customFieldData'][3]['value'], str) else directory_entry['customFieldData'][3]['value']['value'],
                        activity_kind=directory_entry['customFieldData'][2]['value'] if isinstance(directory_entry['customFieldData'][2]['value'], str) else directory_entry['customFieldData'][2]['value']['value'],
                        cost_type=directory_entry['customFieldData'][4]['value'] if isinstance(directory_entry['customFieldData'][4]['value'], str) else directory_entry['customFieldData'][4]['value']['value'],
                        code=directory_entry['customFieldData'][5]['value'] if isinstance(directory_entry['customFieldData'][5]['value'], str) else directory_entry['customFieldData'][5]['value']['value'],
                        planfix_code=directory_entry['key']
                    )
                )
            offset_value += 100


        # print(len(directory_entry_list))
        # print("\n\n\n\n")
        # print(directory_entry_list)

        return directory_entry_list

    def load_directory_table(self):
        directory_entries = self.get_directory_list()
        self.has_db_session.add_all(directory_entries)
        self.has_db_session.commit()

    def run(self):
        self.load_directory_table()

