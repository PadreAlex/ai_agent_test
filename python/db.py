from langchain_community.utilities import SQLDatabase

class AiDbConnection():
    def __init__(self, db_uri: str):
        self.db = SQLDatabase.from_uri(db_uri)

    def run_sql_query(self, sql_query: str) -> str:
        db_response = self.db.run(sql_query)
        return db_response