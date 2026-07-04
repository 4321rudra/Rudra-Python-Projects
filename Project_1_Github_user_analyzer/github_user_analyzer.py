import requests
import pandas as pd 
n=int(input("How many users do you want to search? "))
usernames=[]
for i in range(n):
    usernames.append(input(f"Enter username {i+1} : "))
rows=[]
for username in usernames:
    url=f"https://api.github.com/users/{username}"
    
    r=requests.get(url)
    if r.status_code!=200:
        print(f"{username} Not Found !")
        continue
    data=r.json()
    row = {
    "Name": data.get('name') or "Not Available",
    "Login": data.get('login') ,
    "Followers": data.get('followers') ,
    "Following": data.get('following'),
    "Public Repositories": data.get("public_repos") ,
    "Company": data.get("company") or "Not Available",
    "Location": data.get("location") or "Not Available",
    "Created At": data.get("created_at") or "Not Available"
    }
    rows.append(row)
    
df=pd.DataFrame(rows)
df.to_csv("users_data.csv",index=False)
print(df)
df2=df.sort_values("Followers",ascending=False)
print(f"Most followed user \n{df2.iloc[0]["Name"]}\nFollowers : {df2.iloc[0]["Followers"]} ")
print(f"Average Followers : {df["Followers"].mean()}")
idx = df["Public Repositories"].idxmax()
print(f"User having maximum puplic repositories \n{df.loc[idx, "Name"]}\nTotal Repositories :{df.loc[idx,"Public Repositories"]}")

df.to_excel("github_users.xlsx",index=False)

