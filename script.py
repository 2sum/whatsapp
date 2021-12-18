import re
import numpy as np
import pymysql
h=''
s=''
u=''
p=''
d=''
mon=''
day=''
tm=''
err_cnt=0
start='''<html>
  <head>
    <script type="text/javascript" src="https://www.gstatic.com/charts/loader.js"></script>
    <script type="text/javascript">
      google.charts.load("current", {packages:["corechart"]});
      google.charts.setOnLoadCallback(drawChart);
      function drawChart() {
        var data = google.visualization.arrayToDataTable([
            ['Name', 'MessageCount'],
            '''
end=''']);

        var options = {
          title: 'Whatsapp Daily Report',
          is3D: true,
        };

        var chart = new google.visualization.PieChart(document.getElementById('piechart_3d'));
        chart.draw(data, options);
      }
    </script>
  </head>
  <body>
    <div id="piechart_3d" style="width: 900px; height: 500px;"></div>
  </body>
</html>'''
with open ('/Users/malaybiswal/malay_procore/python/projects/arkk/my.conf','r') as r:
    reader=r.readlines()
    for lines in reader:
        l=lines.split(':')
        if l[0]=='host':
            h=l[1].strip()
        elif l[0]=='sock':
            s=l[1].strip()
        elif l[0]=='uid':
            u=l[1].strip()
        elif l[0]=='pwd':
            p=l[1].strip()
        elif l[0]=='db':
            d=l[1].strip()
conn = pymysql.connect(host=h, unix_socket=s, user=u, passwd=p, db=d,use_unicode=True, charset="utf8mb4")
cur=conn.cursor()
sql="""insert into whatsapp (created_date, name ,text, textlen) values(%s,%s,%s,%s)"""
cnt=0
tm=0
i=0
d={}
participant=[TWFsYXksQ2h1bmlhLE1hbmFzIERhcyxTaWRoYXJ0aGEgVHJpcGF0aHksUHJhZGlwdGEgU2FyYW5naSxOYW5kYW4gTW9oYW50eSxTYXR5YSBBY2hhcnlhLFN1Ymhhc2hpcyBTYWhvbyxMb2thIFBhbmRhLEJpcGxhYiAgTmF5YWssQXJvb3AsRGViaSxLdWt1ZGEsUGFoYWxhLFBhcmVzaCxTcmluaWJhcyBTYXRwYXRoeSxTdW1hbnRhLFN1cmFuamFuIFBhbmRhLERlZXBhayBQYXRuYWlrLEFzaXMgUGF0bmFpayxEZWVwYWsgTW9oYXBhdHJhLFJhdGlrYW50YSBKZW5hLEJpYmh1LFNoYWt0aSBNb2hhbnR5LFN3YWluLFNpYnUgVGFyaWEsUHJhZHl1bW5hIFRyaXBhdGh5LEFya2EgTmFuZGksSGFyYSBNaXNocmEsRGViYXNpcyBLaHVudGlhCg==]
#fl='/Users/malaybiswal/Downloads/whatsapp/investor.txt'
fl='/Users/malaybiswal/Downloads/whatsapp/_chat.txt'
with open (fl,'r') as r:
    reader=r.readlines()
    for lines in reader:
        data = re.findall(r'^(.*?\d+\/\d+\/\d+).*?',lines)
        #print("*******",data,type(data))
        #print("*******",data,type(data),data[0][1],type(data[0][1]))
        if len(data)>0 and data[0][1].isdigit():
            cnt+=1
            line=lines.split(']')
            i=line[1].find(':')
            id=line[1][1:i+1]
            id=id.strip()
            eid=id.encode("ascii", "ignore")
            id=eid.decode()
            id=id[:len(id)-1]
            dts=line[0][1:len(line[0])].split(',')
            dt1s=dts[0].split('/')
            dt2s=dts[1].split()
            if len(dt1s[1])==1:
                day='0'+dt1s[1]
            else:
                day=dt1s[1]
            if len(dt1s[0])==1:
                mon='0'+dt1s[0]
            else:
                mon=dt1s[0]
            dt1='20'+dt1s[2]+'-'+mon+'-'+day
            #dt=dt1+" "+dts[1]
            if dt2s[1].strip()=='PM':
                #print("***********************YUPPPY",dt2s[1],dt2s[0])
                tms=dt2s[0].split(':')
                if tms[0].strip()=='12':
                    hr=tms[0]
                else:
                    hr=int(tms[0].strip())+12
                if int(hr)>=24:
                    hr=hr-24
                hr=str(hr)
                if len(hr)==1:
                    hr='0'+hr
                tm=hr+':'+tms[1]+':'+tms[2]
            else:
                #print("#######################HMMMMM",dt2s[1])
                tm=dt2s[0].strip()
            #dt=dt1+' '+dt2s[0].strip()
            dt=dt1+' '+tm
            #print(dt,'--',tm,'--',dt2s[0])
            if ':' in line[1]:
                text=line[1].split(':')
            

           # print(id,line[0],"***",line[1],'-',dt2s[0],'-',dt2s[1],'-',dts,'-',dt)
            try:
                if len(text[1])>0:
                    l=len(text[1])
                    cur.execute(sql, (dt,id,text[1],int(l)))
                    
                else:
                    l=len(line[1])
                    cur.execute(sql, (dt,id,line[1],int(l)))

            except Exception as e:
                #print(e,dt,id,line[1])
                #print(e,dt,id,text[1])
                err_cnt+=1
            if cnt==1:
                tm=line[0]
            if id =='Investors:' or id=="F95UCE:" or len(id)<1:
                continue
            #if len(line[1])>30:
            #     break
            if id not in d:
                d[id]=1
            else:
                d[id]+=1
            #print(id)
        conn.commit()
conn.close()
cur.close()
s=sorted(d.items(),key=lambda x:x[1], reverse=True)
print(s)
temp=[]
for names in s:
    temp.append(names[0])
#print(temp)
print("-------Chat Time started from",tm[1:len(tm)]," CST----------")
#intersection_set = set.intersection(set(temp), set(participant))
#print(intersection_set)
main_list = np.setdiff1d(participant,temp)
print("*****THIS IS PIP LIST:*****\n",main_list)
print("ERROR COUNT:",err_cnt)
graphstr=''
for details in s:
    name=details[0]
    cnt=details[1]
    graphstr+='['+'\''+name+'\','+str(cnt)+'],'

print (graphstr[0:len(graphstr)-1])
html_page=start+graphstr+end
with open ('/Users/malaybiswal/Downloads/res.html','w') as f:
    f.write(html_page)



