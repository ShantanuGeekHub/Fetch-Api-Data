#Collecting Data

import requests #Import request library in order to interact with api

headers={'app-id' : "6247181c8d483c4a2f3c61f9"} #creating dictionary which consist of app-id and it'll be passed as a parameter in request.get() method

#using get() method which takes url and headers as a parameter, further it authenticates app-id from headers dict and if it's valid then it returns object of response class which consists of all data we've fetched through api
response = requests.get("https://dummyapi.io/data/v1/user", headers=headers)

data = response.json() #this method returns all the data in the form of dictionary 

#Storing Data using MySql

import mysql.connector #importing mysql-connector library in order to interact with mysql database

#Using try & except block to catch error while connecting to database
try:
    #connecting to database
    mydb = mysql.connector.connect(host='localhost', user='root', password='1234')
    if(mydb):
        print("Database connection successful...")
    

except Exception as error:
    print(f"Error Connecting to Database :- {error.__context__}")

myCursor = mydb.cursor() #creating cursor to execute queries and perform CRUD operations on database

myCursor.execute("CREATE DATABASE userdb") #Creating database named userdb

myCursor.execute("USE userdb") #selecting database named userdb

#creating table user
createTable = "CREATE TABLE users(userId varchar(50) NOT NULL, title varchar(4), firstname varchar(50), lastname varchar(50), picture varchar(255), PRIMARY KEY (userID))"
myCursor.execute(createTable)

# creating values list to pass into executemany() method while inserting values into users table
value_list = []
for dic in data['data']:
    temp_list = []
    for key, val in dic.items():
        temp_list.append(val)
    value_list.append(temp_list)

# inserting values inside users table with the help of executemany() method
insertQuery = "INSERT INTO users(userId, title, firstname, lastname, picture) VALUES(%s, %s, %s, %s, %s)"
myCursor.executemany(insertQuery, value_list)
mydb.commit()

# fetching post data from particular user-id

post_val_list = [] # creating values list to pass into executemany() method while inserting values into post table

for dic in data['data']:
    
    userId = dic['id']
    url = f"https://dummyapi.io/data/v1/user/{userId}/post" #Fetching posts from particular user with the help of UserId
    response = requests.get(url, headers=headers)
    postData = response.json()
    
    for dic in postData['data']:
        temp_list = []
        for key, val in dic.items():
            if key == 'owner':
                temp_list.append(dic['owner']['id'])
            
            elif key == 'tags':
                str_temp = ""
                for item in val:
                    str_temp+=(item+", ")
                str_temp = str_temp[:len(str_temp)-2]
                temp_list.append(str_temp)
            else:
                temp_list.append(val)
        post_val_list.append(temp_list)

# creating post table with userId as foreign key refrencing to userId of users table
createTable = "CREATE TABLE post(postID VARCHAR(50) NOT NULL, image VARCHAR(255), likes int, tags VARCHAR(50), text VARCHAR(255), date VARCHAR(50), userId VARCHAR(50) NOT NULL, PRIMARY KEY(postID), FOREIGN KEY(userID) REFERENCES users(userID))"
myCursor.execute(createTable)

# inserting values inside post table with the help of executemany() method
insertQuery = "INSERT INTO post(postID, image, likes, tags, text, date, userID) VALUES(%s,%s,%s,%s,%s,%s,%s)"
myCursor.executemany(insertQuery, post_val_list)
mydb.commit()