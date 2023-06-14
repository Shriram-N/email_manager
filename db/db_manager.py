import psycopg2
import psycopg2.extras
import json

class DbManager:
    def __init__(self):
        with open('db/db_config.json') as f:
            db_config = json.load(f)
        self.conn = psycopg2.connect(host=db_config["host"], database=db_config["database"],
                                     user=db_config["user"], password=db_config["password"],
                                     port=db_config["port"])
        self.cursor = self.conn.cursor(cursor_factory=psycopg2.extras.DictCursor)

    def insert_emails(self, emails):
        query = """INSERT INTO email_table (email_id, thread_id, received_at, from_email, to_email, subject)
                   VALUES (%s, %s, %s, %s, %s, %s)"""
        try:
            psycopg2.extras.execute_batch(self.cursor, query, emails)
            self.conn.commit()
        except psycopg2.DatabaseError as e:
            print(f"Failed to insert data into the database. Error: {e}")

    def get_emails(self):
        self.cursor.execute("SELECT * FROM email_table")
        desc = self.cursor.description
        column_names = [col[0] for col in desc]
        rows = [dict(zip(column_names, row))
                for row in self.cursor.fetchall()]
        return rows

    def update_email(self, email_id, read):
        self.cursor.execute("UPDATE email_table SET read = %s WHERE email_id = %s", (read, email_id))
        self.conn.commit()

    def __del__(self):
        if self.conn is not None:
            self.cursor.close()
            self.conn.close()
