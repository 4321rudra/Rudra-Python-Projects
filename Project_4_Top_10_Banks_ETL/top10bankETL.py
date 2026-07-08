import pandas as pd 
from bs4 import BeautifulSoup
import requests
import sqlite3
from datetime import datetime
def extract(url,table_attr):
    headers={
        "User-Agent":"Mozilla/5.0"
    }
    results=requests.get(url,headers=headers)
    results.raise_for_status()
    soup=BeautifulSoup(results.text,"html.parser")
    tables=soup.find_all('table',class_='wikitable')
    # print(len(tables))
    table=tables[0]
    rows=table.find_all('tr')
    rows_list=[]
    for row in rows[1:11]:
        col=row.find_all('td')
        if len(col)!=0:
            Rank=col[0].text.strip()
            Bank_Name=col[1].text.strip()
            assets=col[2].text.strip()
            data_dict={'Rank':Rank,'Bank Name':Bank_Name,'Assets(USD)':assets}
            rows_list.append(data_dict)
        else :
            continue
    df=pd.DataFrame(rows_list)

    return df
def transform(df):
    df1=pd.read_csv(r"C:\Users\chauh\.vscode\Rudra Python Projects\Project_4_Top_10_Banks_ETL\exchange_rate.csv")
    

    USD_INR=df1.loc[df1["Currency"]=="INR","Rate"].iloc[0]
    USD_EUR=df1.loc[df1["Currency"]=="EUR","Rate"].iloc[0]
    USD_GBP=df1.loc[df1["Currency"]=="GBP","Rate"].iloc[0]
    df["Assets(USD)"]=round(df["Assets(USD)"].str.replace(",","").astype(float),2)
    df["Assets(INR)"]=round(df["Assets(USD)"]*USD_INR,2)
    df["Assets(GBP)"]=round(df["Assets(USD)"]*USD_GBP,2)
    df["Assets(EUR)"]=round(df["Assets(USD)"]*USD_EUR,2)
    return df

def load_to_csv(df,path_):
    df.to_csv(path_,index=False)
def load_to_db(df,conn,Table_name):
    df.to_sql(Table_name,conn,if_exists='replace',index=False)
def run_query(query_statement,conn):
    print(query_statement)
    query_result=pd.read_sql(query_statement,conn)
    print(query_result)
def log_progress(message):
    timestamp_format="%Y-%b-%d-%H:%M:%S"
    now=datetime.now()
    timestamp=now.strftime(timestamp_format)
    with open(r'C:\Users\chauh\.vscode\Rudra Python Projects\Project_4_Top_10_Banks_ETL\code_log.txt','a') as f:
        f.write(f"{timestamp} : {message}\n")

url=r'https://en.wikipedia.org/wiki/List_of_largest_banks'
table_attr=['Rank','Bank Name', 'Assets']
db_name="Banks.db"
table_name="Largest_banks"
output_csv_path='./Largest_banks_data.csv'
log_progress("Preliminaries complete. Initiating ETL process")
df=extract(url,table_attr)
print(df)
log_progress("Data extraction complete. Initiating Transformation process")
df=transform(df)
print(df)
log_progress("Data transformation complete. Initiating Loading process")
load_to_csv(df,output_csv_path)
log_progress("Data saved to CSV file")
conn=sqlite3.connect(db_name)
log_progress("SQL Connection initiated")
load_to_db(df,conn,table_name)
log_progress("Data loaded to Database as a table, Executing queries")
qry_sttment=f"SELECT * from {table_name}"
run_query(qry_sttment,conn)
qry_sttment = f'SELECT AVG("Assets(GBP)") FROM {table_name}'
run_query(qry_sttment,conn)
qry_sttment=f'SELECT [Bank Name] from {table_name} LIMIT 5'
run_query(qry_sttment,conn)
log_progress("Process Complete")
conn.close()
log_progress("Server Connection closed")
