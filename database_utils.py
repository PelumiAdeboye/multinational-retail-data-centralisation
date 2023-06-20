import yaml
import sqlalchemy
import psycopg2

class DatabaseConnector():

    def read_db_creds(self):
        with open('db_creds.yaml', 'r') as file:
            creds = yaml.safe_load(file)
        return creds
    
    def init_db_engine(self):
        # Read the credentials from the YAML file
        creds = self.read_db_creds()

        # Extract the necessary credentials
        database_type = 'postgresql'
        host = creds['RDS_HOST']
        username = creds['RDS_USER']
        password = creds['RDS_PASSWORD']
        database = creds['RDS_DATABASE']
        port = creds['RDS_PORT']

        # Construct the database connection URL
        db_conn_url = f"{database_type}://{username}:{password}@{host}:{port}/{database}"

        # Create and return the SQLAlchemy engine
        engine = sqlalchemy.create_engine(db_conn_url)
        return engine

    def list_db_tables(self):
        engine = self.init_db_engine()
        with engine.connect() as connection:
            # Get the metadata of the database
            metadata = sqlalchemy.MetaData()
            metadata.reflect(bind=connection)

            # Get the table names from the metadata
            table_names = metadata.tables.keys()

            return table_names

    def upload_to_db(self, df, table_name):

        DATABASE_TYPE = 'postgresql'
        DBAPI = 'psycopg2'
        HOST = 'localhost'
        USER = 'postgres'
        PASSWORD = 'Adaobi31'
        DATABASE = 'sales_data'
        PORT = 5432
        local_engine = sqlalchemy.create_engine(f"{DATABASE_TYPE}+{DBAPI}://{USER}:{PASSWORD}@{HOST}:{PORT}/{DATABASE}")
        df.to_sql(table_name, local_engine, if_exists='replace')




if __name__ == '__main__':
    print('Tables in Database:', DatabaseConnector().list_db_tables())
   
    from data_cleaning import DataCleaning
    from data_extraction import DataExtractor
    #DatabaseConnector().upload_to_db(DataCleaning().clean_user_data(),'dim_users')    
    #DatabaseConnector().upload_to_db(DataCleaning().clean_card_data(),'dim_card_details')
    #DatabaseConnector().upload_to_db(DataClean().clean_store_data(),'dim_store_details' )
    #DatabaseConnector().upload_to_db((DataClean().clean_products_data(DataExtractor().extract_from_s3('s3://data-handling-public/products.csv'))), 'dim_products')
    #DatabaseConnector().upload_to_db(DataClean().clean_orders_data(), 'orders_table')
    #DatabaseConnector().upload_to_db((DataClean().clean_date_times()), 'dim_date_times')