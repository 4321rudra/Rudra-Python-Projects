import requests
import pandas as pd 
from bs4 import BeautifulSoup
import matplotlib.pyplot as plt
from datetime import datetime
def log_progress(message,logfile):
    timestamp_format="%Y-%b-%d-%H:%M:%S"
    now=datetime.now()
    timestamp=now.strftime(timestamp_format)
    with open(logfile,'a') as f:
        f.write(f"{timestamp} : {message}\n")


def extract_data(url,logfile):
    headers={
        "User-Agent":"Mozilla/5.0"
    }
    
    rows_list=[]

    for i in range(1,51):
        page_url=f"{url}-{i}.html"
        r=requests.get(page_url,headers=headers,timeout=10)

        if r.status_code!=200:
            break
        soup=BeautifulSoup(r.text,"html.parser")
        # print(soup.prettify())
        books_container=soup.find("ol",class_="row")
        if books_container is None:
            print(f"Could not find books on page {i}")
            continue
        books=books_container.find_all("li")
        # print(books[0])
        # a=rows[0].find("h3").find("a")
        # print(a["title"])
        for book in books:
            # print(row.find("p"))
            # print(row)
            data_dict={"Title":book.find("h3").find("a")["title"],
                    "Price":book.find("p",class_="price_color").text,
                    "Rating":book.find("p")["class"][1].strip(),
                    "Availability":book.find("p",class_="instock availability").text.strip(),
                    "Product URL":book.find("h3").find("a")["href"]}
            rows_list.append(data_dict)
    df=pd.DataFrame(rows_list)
    log_progress("Data Extraction completed . Initiating Transformation Process !",logfile)
    return df
def transform_data(df,logfile):
    df["Price"] = df["Price"].str.replace("Â£", "").astype(float)
    # df["Rating"]=df["Rating"].replace({
    #     "One":1,
    #     "Two":2,
    #     "Three":3,
    #     "Four":4,
    #     "Five":5
    # })
    RATING_MAP={
        "One":1,
        "Two":2,
        "Three":3,
        "Four":4,
        "Five":5  
    }
    df["Rating"]=df["Rating"].map(RATING_MAP)
    log_progress("Data Transformation completed . Initiating Data Analysis",logfile)

    #it only gives in stock and out of stock ,and not any number
    return df
def data_analysis(df,logfile):
    print(f"Total Books : {len(df)}")
    print(f"Average Price : {df['Price'].mean()}")
    idx=df['Price'].idxmin()
    print(f"Cheapest Book :\n{df.loc[idx][["Title","Price"]]}")
    idx=df["Price"].idxmax()
    print(f"Most expensive book : \n{df.loc[idx][["Title","Price"]]}")
    print(f"Average Rating : {df['Rating'].mean()}")
    # print(f"Books with 5 Stars : {len(df[df["Rating"]==5])}")
    # print(f"Books with 5 Stars : {df['Rating'].value_counts()[5]}")
    print(f"Books with 5 Stars : {(df["Rating"] == 5).sum()}")
    print(f"Average Price by Rating \n{df.groupby("Rating")["Price"].mean()}")
    print(f"Books Costing more than £50 \n{df.loc[df["Price"]>=50 ,["Title",'Rating']]}")
    log_progress("Data Analysis Completed . Moving to Visualization",logfile)

def data_visualization(df,logfile):
    ratings_graph=df['Rating'].value_counts()
    ratings_graph.plot(kind="bar")
    plt.title("Ratings")
    plt.show()
    plt.hist(df["Price"],bins=10)
    plt.xlabel("Price")
    plt.ylabel("Number of books")
    plt.show()
    avg_price_by_rating=df.groupby("Rating")["Price"].mean()
    avg_price_by_rating.plot(kind="bar")
    plt.xlabel("Rating")
    plt.ylabel("Average Price")
    plt.title("Average Price by Rating Graph")
    plt.show()
    plt.scatter(df["Price"],df["Rating"])
    plt.xlabel("Price")
    plt.ylabel("Rating")
    plt.show()
    log_progress("Visualization done. Loading data into csv now ",logfile)

def load_to_csv(df,file_path,logfile):
    df.to_csv(file_path,index=False)
    log_progress("Loading Completed . Program successfully executed\n\n------------------------------------------------------------------\n\n",logfile)

logfile=r'C:\Users\chauh\.vscode\Rudra Python Projects\Project_6_Book_Scraping\Log_Progress.txt'
url=r"https://books.toscrape.com/catalogue/page"
file_path=r"C:\Users\chauh\.vscode\Rudra Python Projects\Project_6_Book_Scraping\Books_Scraping.csv"
log_progress("\nPreliminaries complete. Initiating ETL process",logfile)
df=extract_data(url,logfile)
print(df)
df=transform_data(df,logfile)
# print(df)

data_analysis(df,logfile)
data_visualization(df,logfile)
load_to_csv(df,file_path,logfile)


##THIS IS MY STAR PROJECT TILL NOW