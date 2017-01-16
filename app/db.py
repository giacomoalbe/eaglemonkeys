# -*- coding: utf-8 -*-

# DB Instance (file based)
import os

def read_file(name, mode='r'):
    __location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__))) 

    fopen = open(os.path.join(__location__,'db/{0}.csv'.format(name)), mode)

    return fopen

def getFields():
    fopen = read_file('fields') 
    fields = []
    content = fopen.read()  

    for row in content.split("\n")[:-1]:
        fields.append(row.split(','))

    fopen.close()

    return fields

def checkFields(fieldsToCheck):
    fopen = read_file('fields') 
    correctFields = fopen.read().split("\n")[:-1] 

    isFormCorrect = True

    for cor_field in correctFields:
        check_field = fieldsToCheck.get(cor_field.split(',')[0], None) 
        print "CheckF: {0} == CorrectF: {1}".format(check_field, cor_field.split(',')[1])
        if not check_field or check_field != cor_field.split(',')[1]:
            isFormCorrect = False
            break

    return isFormCorrect


def readTable(tablename):
    # Function for easily reading a table
    # which is included

    fopen = read_file(tablename)

    content = fopen.read().split('\n')[:-1]

    table_header = content[0].split(',')
    rows = content[1:]

    table_rows = []

    for row in rows:
        fields = row.split(',')
        obj = {}
        for index,field in enumerate(table_header):
            obj[field] = fields[index]  
        table_rows.append(obj)

    fopen.close()
    return table_rows

def insert(obj, tablename):
    fread = read_file(tablename) 

    content = fread.read().split('\n')[:-1]
    newId = len(content) - 1
    table_header = content[0].split(',')

    tableheader = ['id'] + table_header
    obj['id'] = newId

    fread.close()

    fopen = read_file(tablename, 'ab+') 

    rowtowrite = ""

    for field in table_header: 
        rowtowrite += "{0},".format(obj[field]) 

    # Remove last comma       
    rowtowrite = rowtowrite[:-1] + "\n"

    fopen.write(rowtowrite)
    fopen.close()

def insertTry(time, date, user=-1):
    obj = {
        "user": user,
        "time": time,
        "date": date
    }

    insert(obj, 'try')

def insertUser(name, mail, password):
    obj = {
        "name": name,
        "mail": mail,
        "password": password
    }

    insert(obj, 'user')

def loginUser(mail, pwd):
    users = readTable('user')

    for user in users:
        if user['mail'] == mail and user['password'] == pwd:
            user.pop('password', None)
            return user
    return False


def getUser(userId):
    users = readTable('user') 
    returnUser = None

    for user in users:
        if user['id'] == userId:
            returnUser = user

    return returnUser

def populateUser(tryList):
    for index in range(len(tryList)):
        tryList[index]['user'] = getUser(tryList[index]['user'])
        print tryList[index]['date'].split('T')[1]
        tryList[index]['hour'] = tryList[index]['date'].split("T")[1]
        tryList[index]['date'] = tryList[index]['date'].split("T")[0]

    return tryList

def getRanking():
    preList = populateUser(readTable('try'))
    return sorted(preList, key=lambda x: float(x['time']))

def getUserTries(userId):
    tries = readTable('try')
    userTries = []

    for userTry in tries:
        if userTry['user'] == userId:
            userTry['hour'] = userTry['date'].split("T")[1]
            userTry['date'] = userTry['date'].split("T")[0]
            userTries.append(userTry)
    userTries = sorted(userTries, key=lambda x: float(x['time'])) 
    return userTries 

def test():
    #insertTry(10.2, "16-01-17")
    #insertUser("Giacomo", "giacomoalbe@gmail.com","1234")
    for elem in readTable('try'):
        print elem

if __name__ == "__main__":
    test()


