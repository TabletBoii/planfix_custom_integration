import datetime
from urllib.parse import quote_plus

import requests
import os
from dotenv import load_dotenv
from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine, text, event
from app.directory_loader import DirectoryLoader
from app.loader import HasDBLoader


def get_task_list():
    current_date = (datetime.today() - timedelta(days=3)).strftime("%d-%m-%Y")
    print(current_date)

    get_task_list_endpoint = 'task/list'
    get_task_list_url = PLANFIX_URL + get_task_list_endpoint
    post_body = {
      "offset": 0,
      "pageSize": 100,
      "filters": [
        {
          "type": 12,
          "operator": "gtAndEqual",
          "value": {
            "dateType": "otherDate",
            "dateValue": f"{current_date}"
          }
        },
        {
            "type": 5,
            "operator": "equal",
            "value": "128"
        }
      ],
      "fields": "id,name,85850,86190,87018,67632,85874,85856"
    }

    response = requests.post(get_task_list_url, headers=headers, json=post_body).json()
    print(len(response["tasks"]))
    print(response["tasks"])
    # print("id: ", response["tasks"][0])


def test_api():
    response = requests.get(PLANFIX_URL, headers=headers)


def main():
    dotenv_path = os.path.join(os.path.dirname(__file__), ".env")
    load_dotenv(
        dotenv_path=dotenv_path
    )
    HAS_DB_CONNECTION_STRING = f'postgresql+psycopg2://{os.getenv("HAS_DB_USERNAME")}:{quote_plus(os.getenv("HAS_DB_PASSWORD"))}@{os.getenv("HAS_DB_SERVER")}/{os.getenv("HAS_DB_NAME")}'

    has_db_engine = create_engine(
        HAS_DB_CONNECTION_STRING
    )

    Session = sessionmaker(has_db_engine)
    session_121 = Session()

    # directory_loader = DirectoryLoader(session_121)
    # directory_loader.run()

    hasDBLoader = HasDBLoader(session_121)
    hasDBLoader.get_task_list()


if __name__ == '__main__':

    main()



