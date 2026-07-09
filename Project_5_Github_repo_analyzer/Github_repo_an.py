import requests
import pandas as pd 
import matplotlib.pyplot as plt 
def extract(user_name):
    url=f"https://api.github.com/users/{user_name}/repos"
    r=requests.get(url)
    try:
        r.raise_for_status()
    except requests.HTTPError:
        print("User not found.")
        return pd.DataFrame()
    repositories=r.json()
    rows_list=[]
    for repository in repositories:
        # print(repository.keys())
        row={'Repository Name':repository.get('name'),
             'Owner':repository.get('owner',{}).get("login"),
             'Language':repository.get('language'),
             'Stars':repository.get('stargazers_count') or 0,
             'Forks Count':repository.get('forks_count') or 0,
             'Open Issues':repository.get('open_issues_count'),
             'Size(KB)':repository.get('size'),
             'Created Date':repository.get('created_at'),
             'Updated Date':repository.get('updated_at'),
             'Visibility':repository.get('visibility'),
             'Default Branch':repository.get('default_branch')}
        rows_list.append(row)
    df=pd.DataFrame(rows_list)
    return df
def transform(df):
    df["Created Date"]=pd.to_datetime(df["Created Date"])
    df["Updated Date"]=pd.to_datetime(df["Updated Date"])
    return df
def analysis(df):
    if df.empty:
        print("No repositories found.")
        return
    print(f"Total Repositories : {len(df)}")
    print(f"Total Stars : {df['Stars'].sum()}")
    print(f"Average Stars : {df['Stars'].mean()}")
    print(f"Average Forks : {df['Forks Count'].mean()}")
    print(f"Largest Repository : {df.loc[df['Size(KB)'].idxmax(),"Repository Name"]}")
    idx=df['Stars'].idxmax()
    print(f"Repository with most stars : {df.loc[idx,'Repository Name']}\tStars : {df.loc[idx,'Stars']}")
    idx=df['Forks Count'].idxmax()
    print(f"Repository with most stars : {df.loc[idx,'Repository Name']}\tForks : {df.loc[idx,'Forks Count']}")
    language_count=df["Language"].value_counts()
    print("Most Used Language:", language_count.index[0])
    print("Repositories:", language_count.iloc[0])
    visibility_count=df['Visibility'].value_counts()# This question is absurd as one can only see public repositories in a profile
    print(visibility_count)
    print(f"Average Repository Size : {df['Size(KB)'].mean()}")

    idx=df["Created Date"].idxmax()
    print(f"Newest Repository : \n{df.loc[idx,"Repository Name"]}")
    idx=df["Created Date"].idxmin()
    print(f"Oldest Repository : \n{df.loc[idx,"Repository Name"]}")
    print(df.groupby("Language")["Stars"].mean())

    
    print(df.groupby("Owner")["Stars"].sum())
    

def visualization(df):
    plf=df['Language'].value_counts()
    plf.plot(kind='bar')
    plt.title("Programming Language Frequency")
    plt.show()
    df2=df.sort_values("Stars",ascending=False).head(10)
    plt.barh(df2["Repository Name"],df2["Stars"])
    plt.gca().invert_yaxis()
    plt.xlabel("Stars")
    plt.ylabel("Repositories Name")
    plt.title("Repositories by Stars")
    plt.show()
    plt.scatter(df["Stars"],df["Forks Count"])
    plt.xlabel("Stars")
    plt.ylabel("Forks")
    plt.title("Stars vs Forks")
    plt.show()
def load_to_csv(df):
    df.to_csv("./Github_Repository_Analysis.csv", index=False)
n=int(input("Enter number of users : "))
all_rows=[]
for i in range(n):
    user_name=input("Enter username : ")
    df1=extract(user_name)
    all_rows.append(df1)
df=pd.concat(all_rows,ignore_index=True)
print(df)

df=transform(df)
analysis(df)
visualization(df)
load_to_csv(df)
