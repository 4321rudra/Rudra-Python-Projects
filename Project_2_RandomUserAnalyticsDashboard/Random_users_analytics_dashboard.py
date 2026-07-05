import requests
import pandas as pd
import json
import matplotlib.pyplot as plt 
n=int(input("How many users data you want to process : "))
rows=[]
url = f"https://randomuser.me/api/?results={n}"
r=requests.get(url)
if r.status_code!=200:
    print("Error!")
    exit()
data=r.json()
# print(data["results"][0].keys())
# print(json.dumps(data,indent=4))
i=0
domains=[]
for user in data['results']:
    rows.append({'Name':f"{user['name']['first']} {user['name']['last']}",
                 'Gender':user["gender"],
                 'Email':user['email'],
                 'Age':user["dob"]["age"],
                 'Registration Year':int(user['registered']['date'][:4]),
                 'Country':user['location']['country'],
                 'City':user['location']['city'],
                 'Username':user['login']['username']
                 })
    domains.append(user['email'].split('@')[1])
df=pd.DataFrame(rows)
df['domains']=domains
print(df.head())
df.to_csv("Random_users_data.csv",index=False)
df.to_excel("Random_users_data.xlsx", index=False)
print(f"Total Users : {len(df)}")
print(f"Male vs Female count\n{df["Gender"].value_counts()}")
print(f"Average Age : {df['Age'].mean()}")
idx=df["Age"].idxmin()
print(f"Youngest User \n{df.loc[idx,["Name","Age","Country"]]}")
idx=df["Age"].idxmax()
print(f"Oldest User \n{df.loc[idx,["Name","Age","Country"]]}")
counts=df["Country"].value_counts()
# print(type(counts))
# print(counts)
print("Country:", counts.index[0])
print("Users:", counts.iloc[0])
print(f"Top 5 countries and their Users:\n {counts.iloc[:5]}")
print(df["domains"].value_counts()) #since it only contain email of domain type @example.com i didn't bother to just print the top one
print(f"Average Registration Year : {df['Registration Year'].mean()}")
users_above_40=df[df["Age"]>40]
print(users_above_40)
print(f"Number of users above 40 : {len(users_above_40)}")
print(df.groupby("Country")["Age"].mean())
gender_counts=df["Gender"].value_counts()
gender_counts.plot(kind="bar")
plt.title("Gender Distribution")
plt.show()
plt.hist(df["Age"], bins=10)
plt.xlabel("Age")

plt.ylabel("Users")

plt.title("Age Distribution")

plt.show()
top = df["Country"].value_counts().head(10)

top.plot(kind="bar")

plt.show()