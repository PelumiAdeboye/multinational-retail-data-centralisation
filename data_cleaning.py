import pandas as pd
from data_extraction import DataExtractor
import numpy as np
import yaml

class DataCleaning():


    def clean_user_data(self): 
        df = DataExtractor().read_rds_table('legacy_users')#extract the legacy users table from data extractor class
        df['date_of_birth'] = pd.to_datetime(df['date_of_birth'],  infer_datetime_format=True, errors='coerce')#inferes date time as many different forms
        df['join_date'] = pd.to_datetime(df['join_date'], infer_datetime_format=True, errors='coerce')#inferes date time as many different forms
        df.dropna(subset=['date_of_birth','join_date'], inplace=True)#removes rows that contain null values spcifically looking in columns date_of_birth and join_date
        
        return df #cleaned data frame
    

    def clean_card_data(self):
        data_frame = DataExtractor().retrieve_pdf_data("https://data-handling-public.s3.eu-west-1.amazonaws.com/card_details.pdf")#extract pdf data using link from method in data extractor

        data_frame['date_payment_confirmed'] = pd.to_datetime(data_frame['date_payment_confirmed'],  infer_datetime_format=True, errors='coerce')#inferes date time as many different forms
        data_frame['card_number'] = data_frame['card_number'].astype(str)#converts card_number column to type string
        data_frame['card_number'] = data_frame['card_number'].str.replace('\W', '', regex=True)#replaces all special charactes in this case ? from column card_number
        data_frame['card_number'] = data_frame['card_number'].apply(lambda x: np.nan if x=='NULL' else x)#not a number or nan replaces the null values
        data_frame.dropna(subset=['card_number', 'date_payment_confirmed'], inplace=True)#removes rows that contain null values spcifically looking in columns date_payment_confirmed and card_number
            
        card_data = pd.DataFrame(data_frame) #concatinates list of dataframes to make one dataframe
        
        return card_data
    

    def clean_store_data(self):
        store_data = DataExtractor().retrieve_stores_data()#data frame from store data strated from the api
        store_data.replace({'continent': ['eeEurope', 'eeAmerica']}, {'continent': ['Europe', 'America']}, inplace=True)#replaces erreneous strings with correct strings in column continent
        store_data.drop( columns='lat', inplace=True)#drops column names lat as there are two
        store_data['opening_date']=pd.to_datetime(store_data['opening_date'], infer_datetime_format=True, errors='coerce')#inferes date time as many different forms
        store_data['store_type']=store_data['store_type'].astype(str)
        store_data['store_type'] = store_data['store_type'].apply(lambda x: np.nan if x=='NULL' else x)# if store type has null value replace with np.nan value so 
        store_data.dropna(subset=['opening_date', 'store_type'], inplace=True)
        store_data['staff_numbers'] = store_data['staff_numbers'].str.replace(r'\D', '')# replaces special characters in staff numbers column with empty space
        
        return store_data
    

    def convert_product_weights(self, products_dataframe):
        products_dataframe['weight'] = products_dataframe['weight'].apply(str)#turns weight cloumn into type string
        products_dataframe.replace({'weight':['12 x 100g', '8 x 150g']}, {'weight':['1200g', '1200g']}, inplace=True)#replaces values with entries with correct ones
        filter_letters = lambda x: ''.join(y for y in x if not y.isdigit())#lambda function returns units/letters in each row
        products_dataframe['units'] = products_dataframe['weight'].apply(filter_letters)#applies function to filter letters only
        products_dataframe["weight"] = products_dataframe['weight'].str.extract('([\d.]+)').astype(float)#filters numbers from letters and turns them into floating point
        products_dataframe['weight'] = products_dataframe.apply(lambda x: x['weight']/1000 if x['units']=='g' or x['units']=='ml' else x['weight'], axis=1)#ensures the weight column has standar unit of kg
        products_dataframe.drop(columns='units', inplace=True)#drops column named units

        return products_dataframe
    

    def  clean_products_data(self, products_dataframe):
        products_df=self.convert_product_weights(products_dataframe)#sets the rpoducts dataframe from the cleaned weights dataframe in the previous method
        products_df.dropna(subset=['uuid', 'product_code'], inplace=True)
        products_df['date_added']=pd.to_datetime(products_df['date_added'], format='%Y-%m-%d', errors='coerce')
        drop_prod_list=['S1YB74MLMJ','C3NCA2CL35', 'WVPMHZP59U']# list of strings to drop rows for in the next line
        products_df.drop(products_df[products_df['category'].isin(drop_prod_list)].index, inplace=True)# drop the rows where the category column has entries equal to thouse in the list above
        
        return products_df
    

    def clean_orders_data(self):
        orders_dataframe = DataExtractor().read_rds_table('orders_table') #reads orders table from AWS RDS database extracted in the dataextractor class
        orders_dataframe.drop(columns=['1', 'first_name', 'last_name', 'level_0'], inplace=True) #drops rows where the columns are '1', 'first_name' and 'last_name'
        return  orders_dataframe
    

    def clean_date_times(self):
        date_time_dataframe = DataExtractor().extract_from_s3_json()# sets date time dataframe to dataframe converted from json file from dataextractor
        date_time_dataframe['day'] = pd.to_numeric(date_time_dataframe['day'], errors='coerce')
        date_time_dataframe.dropna(subset=['day', 'year', 'month'], inplace=True)#drops any rown which contain null values in the following columns
        date_time_dataframe['timestamp'] = pd.to_datetime(date_time_dataframe['timestamp'], format='%H:%M:%S', errors='coerce')# timestamp in form hour minute and seconds
        return date_time_dataframe
