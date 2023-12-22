from sqlalchemy import text
from sqlalchemy import create_engine
import csv

# CSV PATH and TABLE NAME
# ========================= #
CSV_PATH = "/Users/soeun-uhm/yonsei/GDSC/resume-ai-chat/input/question/behav_q.csv"
TABLE_NAME = "behavior_question"
# ========================= #

SQLALCEMY_DATABASE_URL = 'sqlite:///./resume_ai_chat.db'

engine = create_engine(SQLALCEMY_DATABASE_URL,connect_args={'check_same_thread':False})

def insert_data(db, table, rows):
    for row in rows:
        db.execute(text(f"INSERT INTO {table} (question, criteria ) VALUES (:question, :criteria)"), row)
    db.commit()



def csv_to_database(CSV_PATH, TABLE_NAME):
    with open(CSV_PATH, 'r', encoding='utf-8-sig') as file:
        csv_reader = csv.DictReader(file)
        data = [row for row in csv_reader]

    with engine.connect() as connection:
        insert_data(connection, TABLE_NAME , data)
        
if __name__ == "__main__":
    csv_to_database(CSV_PATH, TABLE_NAME)
    print("database update done!")

