"""
File:           dbhandler.py
Author:         Dibyaranjan Sathua
Created on:     14/01/21, 8:04 pm
"""
import mysql.connector
import config


class DBHandler:
    """ Connect to DB and execute the SQL """

    def __init__(self):
        self.db_conn = None
        self.db_host = config.DBCred.HOST
        self.db_user = config.DBCred.USERNAME
        self.db_pass = config.DBCred.PASSWORD
        self.db_name = config.DBCred.DBNAME
        self.open_connection()

    def open_connection(self):
        self.db_conn = mysql.connector.connect(
            host=self.db_host,
            user=self.db_user,
            password=self.db_pass,
            database=self.db_name,
        )

    def close_connection(self):
        self.db_conn.close()

    def execute_sql(self, sql, args=None):
        with self.db_conn:
            with self.db_conn.cursor(dictionary=True) as cursor:
                cursor.execute(sql, args)
                query_result = cursor
        return query_result

    def get_all_potential_records(self):
        sql = "SELECT * FROM vw_Deal ORDER BY PotentialDealID DESC"
        cursor = self.db_conn.cursor(dictionary=True)
        cursor.execute(sql)
        return cursor.fetchall()

    def get_all_make_models(self):
        sql = "SELECT * FROM vauto_make_model"
        cursor = self.db_conn.cursor(dictionary=True)
        cursor.execute(sql)
        return cursor.fetchall()

    def update_by_id(self, deal_id, action, comments):
        if action is None:
            action = "NULL"
        else:
            action = f"'{action}'"
        sql = f"UPDATE PotentialDeal SET action = {action}, comment = '{comments}' " \
              f"WHERE PotentialDealID = {deal_id}"
        cursor = self.db_conn.cursor(dictionary=True)
        cursor.execute(sql)
        self.db_conn.commit()


if __name__ == "__main__":
    db_handler = DBHandler()
    results = db_handler.get_all_potential_records()
    for x in results:
        print(x)
    # results = db_handler.get_all_make_models()
    # for x in results:
    #     print(x)
    # db_handler.update_by_id(2, "Test comment456")
