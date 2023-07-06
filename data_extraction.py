from database_utils import DatabaseConnector
import sqlalchemy
import pandas as pd
import requests
import tabula
import boto3 

class DataExtractor():

    def __init__(self):
        self.db = DatabaseConnector()
        self.rds_database = self.db.init_db_engine()
        self.api_key ={'x-api-key':'yFBQbwXe9J3sd6zWVAMrK6lcxxr0q1lr2PT6DDMX'}


    def read_rds_table(self, table_name):
      return pd.read_sql_table(table_name, self.rds_database)
    

    def retrieve_pdf_data(self, pdf_link):
        pdf_dataframes = tabula.read_pdf(pdf_link, pages="all", multiple_tables=True)

        return pd.concat(pdf_dataframes,ignore_index=True)
    

    def list_number_of_store(self):
        stores = requests.get('https://aqj7u5id95.execute-api.eu-west-1.amazonaws.com/prod/number_stores',headers=self.api_key)
        number_of_stores = stores.json()
        return number_of_stores["number_stores"]
    

    def retrieve_stores_data(self):
        number_of_stores = self.list_number_of_store()
        stores_list = []
        for store_number in range(0, number_of_stores):
            stores_list.append(requests.get('https://aqj7u5id95.execute-api.eu-west-1.amazonaws.com/prod/store_details/'+str(store_number), headers=self.api_key).json())
        return pd.json_normalize(stores_list)
    

    def extract_from_s3(self,address):
        s3 = boto3.client('s3')
        bucket = 'data-handling-public'
        object = 'products.csv'
        file = 'products.csv'
        s3.download_file(bucket,object,file)
        table = pd.read_csv('./products.csv')
        return table
    

    def extract_from_s3_json(self):
        #https://data-handling-public.s3.eu-west-1.amazonaws.com/date_details.json
        s3 = boto3.client('s3')
        bucket = 'data-handling-public'
        object = 'date_details.json'
        file = 'date_details.json'
        s3.download_file(bucket,object,file)
        table = pd.read_json('./date_details.json')
        # print(table)
        return table
    

if __name__ == "__main__":
    isinstance = DataExtractor()


