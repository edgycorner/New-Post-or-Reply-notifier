board="2.0" #Enter Board ID here
type=1 #Enter 1 for NEW Post notifier, 2 for Reply notifier
keywords=["keyword/topic 1","keyword/topic 2"] #Enter title of the post if using reply notifier.
token='o.Gyzsad342errafasfae23' #Pushbullet api token

#Do not edit anything from below here:

import requests

from bs4 import BeautifulSoup

from datetime import datetime

from pushbullet import Pushbullet

from time import sleep

url="https://bitcointalk.org/index.php?board="+board

headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.157 Safari/537.36'}

pb= Pushbullet(token)


while True:

 page = requests.get(url, headers=headers)

 soup=BeautifulSoup(page.content, 'html.parser')
 tr=soup.find_all('tr')
 i=0
 check=1
 total=len(tr)
 while check:
  td=list(tr[i].children)
  if len(td)==15:
   ti2=td[13].get_text()
   ti2=ti2.split('by',1)[0]
   if 'Today' in ti2:
    s=ti2.split('at',1)[1].strip()
    today = datetime.today().strftime('%Y-%m-%d')
    s=today+' '+s
    t=datetime.strptime(s, "%Y-%m-%d %I:%M:%S %p")
    c=datetime.utcnow()
    sec=int((c-t).total_seconds())
    if sec<300:
     title=td[5].find_all('span')
     title=title[0].get_text()
     if type==1:
      if any(word in title for word in keywords):
       count=td[9].get_text()
       count=int(count)
       if count<10:
        ptitle="New topic found with title: "+title
        count=str(count)
        ptext="No. of replies: "+count
        push = pb.push_note(ptitle,ptext)
     if type==2:
      if title in keywords:
       count=td[9].get_text()
       count=int(count)
       ptitle="New reply on topic: "
       ptext=title
       push = pb.push_note(ptitle,ptext)

  i+=1
  if i==len(tr):
   break
 sleep(300)
