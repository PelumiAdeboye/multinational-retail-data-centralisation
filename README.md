# Multinational-Retail-Data-Centralisation

The context of this project is that I work for a multinational company that sells various goods across the globe. Currently, their sales data is spread across many different data sources making it not easily accessible or analysable by current members of the team. In an effort to become more data-driven, my organisation would like to make its sales data accessible from one centralised location. My first goal will be to produce a system that stores the current company data in a database so that it's accessed from one centralised location and acts as a single source of truth for sales data. I will then query the database to get up-to-date metrics for the business.

The following milestones will outline the steps I took when going through the project.
## Milestone 1: Set up the environment

- Used GitHub to track changes to my code and save them online in a GitHub repo

## Milestone 2: Extract and clean the data from the data sources

- Initialised a new database locally called Sales_database to store the extracted data through pgadmin4 and Created three Python scripts for data extraction, data cleaning, and database connector each with its own class.

- The data extraction methods within the data extraction class are fit to extract data from sources including CSV files, an API, and an S3 bucket.
 
- Within Dataextractor and Databaseconnector I developed methods to clean and extract the user data, including creating and reading credentials from a yaml file, in order to extract the information from an AWS RDS database.

- Within the Datacleaning I performed the cleaning of the user data.
Looking out for NULL values, errors with dates, incorrectly typed values, and rows filled with the wrong information.
 
 - Used data extractor to extract user card details stored in AWS S3 bucket from a pdf document. I then cleaned the card details to remove any erroneous values. Once cleaned I uploaded it to the database using a database utils method.

 - Retrieved store data through the use of an API. The API has two GET methods. One will return the number of stores in the business and the other to retrieve a store given a store number. I used the API key to connect to the API in the method header. I then cleaned the store data and uploaded the dataframe to the database named Sales_data in pgadmin.

 - Extracted information for each product the company currently sells stored in CSV format in an S3 bucket on AWS. I created a method in DataExtractor  that uses the boto3 package to download and extract the information returning a pandas dataframe. I then cleaned the data frame and uploaded it to the data base.

 - I extracted and cleaned the orders table which acts as the single source of truth for all orders the company has made in the past and is stored in a database on AWS RDS. I extracted it by using earlier methods I created in data extraction. I then uploaded the dataframe to the database.

 - The final source of data was a JSON file containing the details of when each sale happened, as well as related attributes. The file is currently stored on S3, I then extracted the file and performed any necessary cleaning, then uploaded the data to the database.

 ## Milestone 3: Create the database schema

 - In this milestone, I ensured that all of the tables within my sales_database had the correct columns and were cast of the correct type. 

 - I then added primary keys to all dimension tables. With the primary keys created in the tables prefixed with dim, I then created the foreign keys in the orders_table to reference the primary keys in the other tables. 

- I Used SQL to create the foreign key constraints that reference the primary keys of the other table. This made the star-based database schema complete.

## Milestone 4 Querying the Data

- In this final milestone After I had gathered the data into one database, I used SQL to get up-to-date metrics from the data. The business can then start to make more data-driven decisions and get a better understanding of its sales. I answered the following questions:

- How many stores does the business have and in which countries?

- Which locations currently have the most stores?

- Which months produce the most sales typically?

- How many sales are coming from online?

- What percentage of sales come through each type of store?

- Which month in each year produced the most sales?

- What is our staff headcount?

- Which German store type is selling the most?

- How quickly is the company making sales?


