from urllib.parse import quote_plus
import os
from dotenv import load_dotenv
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine, text
from app.directory_loader import DirectoryLoader
from app.global_loader import HasGlobalExpensesLoader
from app.industrial_loader import HasIndustrialExpensesLoader
from app.china_loader import HasChinaExpensesLoader
from app.industrial_project_loader import IndustrialProjectListLoader


def main(loader_toggle_dict: dict):
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

    """
        Запустить, если необходимо обновить справочник статей расходов
    """
    # directory_loader = DirectoryLoader(session_121)
    # directory_loader.run()

    """
        Запустить, если необходимо обновить справочник проектов HAS Industrial
    """
    # industrial_projects_list_loader = IndustrialProjectListLoader(session_121)
    # industrial_projects_list_loader.run()

    # session_121.execute(text("TRUNCATE planfix_expenses_data;"))
    loader_list = {
        "global": HasGlobalExpensesLoader(
            session=session_121,
            url=os.getenv('PLANFIX_URL'),
            token=os.getenv('PLANFIX_BEARER_TOKEN'),
            # start_date="16-05-2024"
            start_date="01-06-2024",
            planfix_org='global'
        ),
        "industial": HasIndustrialExpensesLoader(
            session=session_121,
            url=os.getenv('PLANFIX_INDUSTRIAL_URL'),
            token=os.getenv('PLANFIX_INDUSTRIAL_BEARER_TOKEN'),
            start_date="01-06-2024",
            planfix_org='industrial'
        ),
        "china": HasChinaExpensesLoader(
            session=session_121,
            url=os.getenv('PLANFIX_CHINA_URL'),
            token=os.getenv('PLANFIX_CHINA_BEARER_TOKEN'),
            start_date="01-06-2024",
            planfix_org='china'
        )
    }
    for key, value in loader_toggle_dict.items():
        if value == "y":
            loader_list[key].get_task_list()


if __name__ == '__main__':
    main(
        loader_toggle_dict={
            "global": "y",
            "industial": "y",
            "china": "n"
        }
    )
