import requests
import pandas as pd 
import sqlite3
from bs4 import BeautifulSoup
import numpy as np
from datetime import datetime

def extract(url, table_attr):
    headers = {
    "User-Agent": "Mozilla/5.0"
    }
    results=requests.get(url,headers=headers)
    results.raise_for_status()
    soup=BeautifulSoup(results.text,'html.parser')
    tables=soup.find_all('table',class_="wikitable")
    table=tables[0]
    rows=table.find_all('tr')
    col= rows[1].find_all("td")
    rows_list=[]
    for row in rows[1:51]:
        
        col=row.find_all('td')
        if len(col)!=0:
            gdp_million=col[1].text.strip()
            # gdp_million=float(gdp_million.replace(',',''))
            country=col[0].text.strip().split('[')[0]
            data_dict={"Country":country,"GDP_USD_MILLION":gdp_million}
            rows_list.append(data_dict)
            
        else:
            continue
        

    df=pd.DataFrame(rows_list)
    # print(df)
    return df
def transform(df):
    df['GDP_USD_MILLION']=(round(df['GDP_USD_MILLION'].str.replace(",","").astype(float)/1000,2))
    df.rename(columns={"GDP_USD_MILLION":"GDP_USD_BILLION"},inplace=True)
    print(df)
    return df
def load_to_csv(df,csv_path):
    df.to_csv(csv_path)
def load_to_db(df, conn,file_name):
    df.to_sql(file_name,conn,if_exists='replace',index=False)
def run_query(query_statement,sql_connection):
    print(query_statement)
    query_result=pd.read_sql(query_statement,sql_connection)
    print(query_result)
def log_progress(message):
    timestamp_format="%Y-%b-%d-%H:%M:%S"
    now=datetime.now()
    timestamp=now.strftime(timestamp_format)
    with open(r"C:\Users\chauh\.vscode\Rudra Python Projects\Project_3_ETL_GDP\etl_project_log.txt",'a') as f:
        f.write(f"{timestamp} : {message}\n")

db_name="World_economies.db"
table_name="Countries_by_GDP"
csv_path='Countries_by_GDP.csv'
url = 'https://en.wikipedia.org/wiki/List_of_countries_by_GDP_(nominal)'
table_attr=["Country","GDP_USD_MILLION"]
log_progress('Preliminaries complete. Initiating ETL process')

df = extract(url, table_attr)

log_progress('Data extraction complete. Initiating Transformation process')

df = transform(df)

log_progress('Data transformation complete. Initiating loading process')

load_to_csv(df, csv_path)

log_progress('Data saved to CSV file')

sql_connection = sqlite3.connect('World_Economies.db')

log_progress('SQL Connection initiated.')

load_to_db(df, sql_connection, table_name)

log_progress('Data loaded to Database as table. Running the query')

query_statement = f"SELECT * from {table_name} WHERE GDP_USD_BILLION >= 100"
run_query(query_statement, sql_connection)

log_progress('Process Complete.')

sql_connection.close()
