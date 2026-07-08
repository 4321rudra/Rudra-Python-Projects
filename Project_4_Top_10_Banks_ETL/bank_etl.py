import pandas as pd
from bs4 import BeautifulSoup
import requests
import sqlite3
from datetime import datetime

# -----------------------------
# Configuration
# -----------------------------

URL = "https://en.wikipedia.org/wiki/List_of_largest_banks"

TABLE_ATTR = ["Rank", "Bank Name", "MC_USD_Billion"]

DB_NAME = "Banks.db"
TABLE_NAME = "Largest_banks"

CSV_OUTPUT_PATH = "Largest_banks_data.csv"
EXCHANGE_RATE_PATH = r"C:\Users\chauh\.vscode\Rudra Python Projects\Project_4_Top_10_Banks_ETL\exchange_rate.csv"
LOG_FILE = "code_log.txt"


# -----------------------------
# Logging Function
# -----------------------------

def log_progress(message):
    """Log progress messages with timestamp."""

    timestamp = datetime.now().strftime("%Y-%b-%d-%H:%M:%S")

    with open(LOG_FILE, "a") as file:
        file.write(f"{timestamp} : {message}\n")


# -----------------------------
# Extract Function
# -----------------------------

def extract(url, table_attr):
    """Extract bank data from Wikipedia."""

    headers = {
        "User-Agent": "Mozilla/5.0"
    }

    response = requests.get(url, headers=headers)
    response.raise_for_status()

    soup = BeautifulSoup(response.text, "html.parser")

    table = soup.find_all("table", class_="wikitable")[0]

    rows = table.find_all("tr")

    rows_list = []

    for row in rows[1:11]:

        columns = row.find_all("td")

        if len(columns) == 0:
            continue

        rows_list.append({

            "Rank": columns[0].text.strip(),

            "Bank Name": columns[1].text.strip(),

            "MC_USD_Billion": columns[2].text.strip()

        })

    df = pd.DataFrame(rows_list, columns=table_attr)

    return df


# -----------------------------
# Transform Function
# -----------------------------

def transform(df,EXCHANGE_RATE_PATH):
    """Convert assets into multiple currencies."""

    df1 = pd.read_csv(EXCHANGE_RATE_PATH)

    usd_to_inr = df1.loc[df1["Currency"] == "INR", "Rate"].iloc[0]
    usd_to_eur = df1.loc[df1["Currency"] == "EUR", "Rate"].iloc[0]
    usd_to_gbp = df1.loc[df1["Currency"] == "GBP", "Rate"].iloc[0]

    df["MC_USD_Billion"] = (
        df["MC_USD_Billion"]
        .str.replace(",", "")
        .astype(float)
        .round(2)
    )

    df["MC_GBP_Billion"] = round(df["MC_USD_Billion"] * usd_to_gbp, 2)
    df["MC_EUR_Billion"] = round(df["MC_USD_Billion"] * usd_to_eur, 2)
    df["MC_INR_Billion"] = round(df["MC_USD_Billion"] * usd_to_inr, 2)

    return df


# -----------------------------
# Load Functions
# -----------------------------

def load_to_csv(df, output_path):
    """Save dataframe as CSV."""
    df.to_csv(output_path, index=False)


def load_to_db(df, connection, table_name):
    """Load dataframe into SQLite database."""
    df.to_sql(table_name, connection, if_exists="replace", index=False)


# -----------------------------
# SQL Query Function
# -----------------------------

def run_query(query_statement, connection):
    """Execute SQL query and print results."""

    print("\nQUERY:")
    print(query_statement)

    query_result = pd.read_sql(query_statement, connection)

    print(query_result)
    log_progress("Query executed successfully")

# -----------------------------
# ETL Pipeline
# -----------------------------

log_progress("Preliminaries complete. Initiating ETL process")

df = extract(URL, TABLE_ATTR)

print(df)

log_progress("Data extraction complete. Initiating Transformation process")

df = transform(df, EXCHANGE_RATE_PATH)

print(df)

log_progress("Data transformation complete. Initiating Loading process")

load_to_csv(df, CSV_OUTPUT_PATH)

log_progress("Data saved to CSV file")

connection = sqlite3.connect(DB_NAME)

log_progress("SQL Connection initiated")

load_to_db(df, connection, TABLE_NAME)

log_progress("Data loaded to Database as a table. Executing queries")

run_query(f'SELECT * FROM {TABLE_NAME}', connection)

qry_sttment = f'SELECT AVG("MC_GBP_Billion") FROM {TABLE_NAME}'
run_query(qry_sttment, connection)
run_query(f'SELECT [Bank Name] FROM {TABLE_NAME} LIMIT 5', connection)

log_progress("Process Complete")

connection.close()

log_progress("Server Connection closed")