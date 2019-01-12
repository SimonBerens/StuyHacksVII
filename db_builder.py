# creates tables for database stored in DB_FILE: alright.db
# field names created; no records
import sqlite3  # enable control of an sqlite database

DB_FILE = "cyber.db"
db = sqlite3.connect(DB_FILE, check_same_thread=False)  # open if file exists, otherwise create
c = db.cursor()


def createTable(tableName, fieldNames, *foreignKeys):
    '''creates new table with list of parameters to be taken in'''
    commandArgs = "("
    colTypes = []
    for name in fieldNames:
        commandArgs += name + " " + fieldNames[name] + ","
        colTypes.append(fieldNames[name])
    # print(colTypes)
    for fk in foreignKeys:
        commandArgs += f"FOREIGN KEY ({fk[0]}) REFERENCES {fk[1]}({fk[2]}),"
    commandArgs = commandArgs[:-1]
    commandArgs += ")"
    print("CREATE TABLE " + tableName + " " + commandArgs)

    c.execute("CREATE TABLE " + tableName + " " + commandArgs)


def closeDB():
    db.commit()  # save changes
    db.close()  # close database


profilesHeader = {
    "UserID": "INTEGER PRIMARY KEY",
    "Username": "TEXT UNIQUE",
    "Password": "TEXT",
    "ActiveSession": "TEXT"
}
createTable("profiles", profilesHeader)

messagesHeader = {
    "MessageID": "INTEGER PRIMARY KEY",
    "FromUserID": "INTEGER",
    "ToUserID": "INTEGER",
    "Message": "TEXT"
}
createTable("messages", messagesHeader, ("FromUserID", "profiles", "UserID"))

closeDB()
# creates tables for database stored in DB_FILE: alright.db
# field names created; no records
import sqlite3  # enable control of an sqlite database

DB_FILE = "cyber.db"
db = sqlite3.connect(DB_FILE, check_same_thread=False)  # open if file exists, otherwise create
c = db.cursor()


def createTable(tableName, fieldNames, *foreignKeys):
    '''creates new table with list of parameters to be taken in'''
    commandArgs = "("
    colTypes = []
    for name in fieldNames:
        commandArgs += name + " " + fieldNames[name] + ","
        colTypes.append(fieldNames[name])
    # print(colTypes)
    for fk in foreignKeys:
        commandArgs += f"FOREIGN KEY ({fk[0]}) REFERENCES {fk[1]}({fk[2]}),"
    commandArgs = commandArgs[:-1]
    commandArgs += ")"
    print("CREATE TABLE " + tableName + " " + commandArgs)

    c.execute("CREATE TABLE " + tableName + " " + commandArgs)


def closeDB():
    db.commit()  # save changes
    db.close()  # close database


profilesHeader = {
    "UserID": "INTEGER PRIMARY KEY",
    "Username": "TEXT UNIQUE",
    "Password": "TEXT",
    "ActiveSession": "INTEGER"
}
createTable("profiles", profilesHeader)

messagesHeader = {
    "MessageID": "INTEGER PRIMARY KEY",
    "FromUserID": "INTEGER",
    "ToUserID": "INTEGER",
    "Message": "TEXT",
    "Flagged": "INTEGER"
}
createTable("messages", messagesHeader, ("FromUserID", "profiles", "UserID"))

closeDB()
