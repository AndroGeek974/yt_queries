from urllib.request import *
from html.parser import HTMLParser
import os

# Get data
#query = input('Recherche : ')
query = str(input('Recherche : '))
query = query.replace(' ','+')

key = int(100) #HTML Parsing Helper Key

res = 'https://www.youtube.com/results?search_query='+query
q = urlopen(res)

# Copy data
f = open('workfile.html', 'w')
fi = q.read().decode('utf-8')
f.write(str(fi))
f.close()

d = open('workfile.html','r')
fi = open('final.html','w')


for line in d:
    if '<span class="accessible-description"' in line:
        #print(line)
        #line = line.split('title=',1)[1]
        #line = "'"+line+"'"
        key = key+1
        #fi.write(line.replace('dir="ltr">','dir="ltr"> /'+str(key)+'/'))
        fi.write(line.replace('dir="ltr">','dir="ltr'+str(key)+'">'))

d.close()
fi.close()

fp = open('data.txt','w')

string1 = str("('link : ', ('href', '/watch?v=")
string2 = str("('data  :', ' - Duration: ")
string3 = str("'))")
string4 = str("')")
string5 = str("('link : ', ('href', '/user/")
string6 = str("('data  :', '")
string7 = str("data : ' /")+str(key)+str('/')
string8 = str("('title : ', ('title', ")
string9 = str("('link : ', ('href', '/channel/")
string10 = str("('title : ',")

#including HTMLParser
class MyHTMLParser(HTMLParser):
    def handle_starttag(self, tag, attrs):
        if tag == 'a':
            for name, value in attrs:
                if name == 'href':
                    var1 = "link : ",attrs[0]
                    #print(var1)
                    var1 = str(var1)+'\n'
                    #print(var1)
                    parse = var1.replace(string1,str("url : '"))
                    parse = parse.replace(string3,str("'"))
                    parse = parse.replace(string4,str("'"))
                    parse = parse.replace(string5,str("user : '"))
                    parse = parse.replace(string6,str("data : '"))
                    #parse = parse.replace(string7,str("title : '"))
                    parse = parse.replace(string9,str("channel : '"))
                    if 'http' not in parse and 'channel' not in parse:
                        fp.write(parse)
                else:
                    if name =='title':
                        try:
                            parse2 = "title : ",attrs[3]
                            parse2 = str(parse2)
                            parse3 = parse2.replace(string8,"title : ")
                            parse3 = parse3.replace(string10,"tips : ")
                            parse3 = parse3.replace('))','')
                            if "tips" not in parse3:
                                fp.write(parse3+"\n")
                        except IndexError:
                            fp.write('\n')


    def handle_endtag(self, tag):
        if tag == 'a':
            var2 = "tag :", tag
            var2 = str(var2)+'\n'
            #print(var2)
            #fp.write(str(var2))

    def handle_data(self, data):
            var3 = "data  :", data
            var3 = str(var3)+'\n'
            #print(str(var3))
            parse = var3.replace(string2,str("duration : '"))
            parse = parse.replace(string3,str("'"))
            parse = parse.replace(string4,str("'"))
            parse = parse.replace(string5,str("user : '"))
            parse = parse.replace(string6,str("data : '"))
            parse = parse.replace(string7,str("title : '"))
            if 'data' not in parse:
                fp.write(str(parse))


fpp = open('final.html','r')
parser = MyHTMLParser()

for i in fpp:
    d = parser.feed(i)

fpp.close()
fp.close()

# wipe things
os.system('rm -f final.html && rm -f workfile.html && cat data.txt')
print('\n\n Logs file : data.txt')
