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
from app.global_loader import HasGlobalExpensesLoader
from app.industrial_loader import HasIndustrialExpensesLoader


def main():
    dotenv_path = os.path.join(os.path.dirname(__file__), ".env")

    load_dotenv(
        dotenv_path=dotenv_path
    )
    HAS_DB_CONNECTION_STRING = f'postgresql+psycopg2://{os.getenv("HAS_DB_USERNAME")}:{quote_plus(os.getenv("HAS_DB_PASSWORD"))}@{os.getenv("HAS_DB_SERVER")}/{os.getenv("HAS_DB_NAME")}'

    has_db_engine = create_engine(
        HAS_DB_CONNECTION_STRING
    )

    HasSession = sessionmaker(has_db_engine)
    session_121 = HasSession()

    # directory_loader = DirectoryLoader(session_121)
    # directory_loader.run()

    session_121.execute(text("TRUNCATE planfix_expenses_data;"))
    session_121.commit()

    has_global_loader = HasGlobalExpensesLoader(session_121)
    has_global_loader.get_task_list()

    has_industrial_loader = HasIndustrialExpensesLoader(session_121)
    has_industrial_loader.get_task_list()


if __name__ == '__main__':

    main()



