import mysql.connector # importing mysql-connector library to connect database

# using try & except block to catch error
try:
    mydb = mysql.connector.connect(host='localhost', user='root', password='1234', db='userdb')
    if(mydb):
        print("connection successful...")

except Exception as error:
    print("Error connecting : ",error.__context__)

import pandas as pd # using pandas library we'll be able to store data from db into csv format

df = pd.read_sql("SELECT * FROM users", mydb) # returns selected data from users table into dataframe object df
df.to_csv("usersData.csv", index=False) # exporting users data into csv file

df = pd.read_sql("SELECT * FROM post", mydb) # returns selected data from post table into dataframe object df
df.to_csv("postData.csv", index=False) # exporting post data into csv file