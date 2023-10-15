# -*- coding: utf-8 -*-
"""
Created on Sat Jul 25 09:08:21 2020

@author: prady
"""

from flask import Flask,render_template,request,redirect,url_for
import mysql.connector
import pandas as pd
from datetime import datetime
import io
from io import StringIO
import schedule
import time


mydb = mysql.connector.connect(host = "localhost",user="root",passwd="root",database="test")
mycursor = mydb.cursor()
app = Flask(__name__)

@app.route("/login",methods=['GET','POST'])
def validation():
    mycursor.execute("Select * from admin")
    myResult1= mycursor.fetchone()
    print(myResult1)
    if 'username' in request.form and 'password' in request.form:
        username = request.form['username']
        password = request.form['password']
        if myResult1['username']==username and myResult1['password']==password:
            return "login successful"
        else:
            return "login unsuccessful"
    
    
    return render_template("auth.html",result=myResult1)




@app.route("/")
def index():
            a=datetime.now().time()
            mydb = mysql.connector.connect(host = "localhost",user="root",passwd="root",database="test")
            mycursor = mydb.cursor()
            mycursor.execute("SELECT * FROM data order by time")
            myResult1= mycursor.fetchall()
            
            
            #moving average part
            mycursor.execute("SELECT distinct name FROM dummy")
            myResult2= mycursor.fetchall()          
            mycursor.execute("SELECT * FROM dummy ")
            myResult3= mycursor.fetchall()
          
            sqls=[]
            jaar=[]
            for i in range(len(myResult2)):
                for j in range(len(myResult3)):
                    if(myResult2[i][0]==myResult3[j][1]):
                        sqls.append(myResult3[j])
                df = pd.DataFrame(sqls,columns=["Time","Name","frequency"])
                df['SMA_3'] = df.iloc[:,2].rolling(window=3).mean()
                jaar.append([])
                jaar[i].append(myResult2[i])
                jaar[i].append(df['SMA_3'][len(df)-1])
                sqls.clear()
                        
                        
            def myFunc(e):
                return e[1]
                            
            trending=sorted(jaar,key=myFunc,reverse=True)
                            
            sort=[]
            for i in range(len(trending)):
                if(trending[i][1]>1): 
                    sort.append(trending[i])
                            
                            
                          
            bo=[]
            for i in range(len(sort)):
                bo.append([])
                bo[i].append(trending[i][0][0])
            words=[]
            for i in range(len(bo)):
                words.append(bo[i][0])
            
            lastwords=[]
            if len(words)>100:
                for i in range(100):
                    lastwords.append(words[i])
            else:
                lastwords=words
                            
                            
            topwords=[]
            for i in range(100):
                topwords.append(words[i])    
                
                
            topNews=[]
            global finalNews
            finalNews=[]
            mycursor.execute("SELECT distinct title FROM data order by time desc ")
            myResult4= mycursor.fetchall()
                            
                            
            for i in range(len(myResult4)):
                for j in range(len(topwords)):
                    index1 = myResult4[i][0].lower().find(topwords[j])    
                    if(index1 != -1):
                        topNews.append(myResult4[i][0])
                        break
                                         
            for i in range(len(topNews)):
                for j in range(len(myResult1)):
                    if(topNews[i]==myResult1[j][1]):
                        finalNews.append(myResult1[j]) 
                        break
        
            last=[]
            if(len(finalNews)>50):
                for i in range(50):
                    last.append(finalNews[i])
            else:
                last=finalNews
                 
    
    #if request.method == "POST":
    #         user= request.form["project"]
    #         return redirect(url_for("handle", usr=user))
    #else:
            a=render_template("template.html",words=lastwords,news=last)
            with io.open("index.html","w", encoding="utf-8") as file:
                 file.write(a)
            return a    
                
               
@app.route("/<usr>")
            
def handle(usr): 
    handles=[]
    if(usr!="ALL" and usr!= "EXIT"):
        for i in range(len(finalNews)):
            out=finalNews[i][1].lower().find(usr)
            if(out!= -1):
                handles.append(finalNews[i])
                
            elif(usr=="ALL"):
                for i in range(len(finalNews)):
                    handles.append(str(finalNews[i][0])+"----"+str(finalNews[i][1])+"----"+str(finalNews[i][3]))
    return render_template("handle.html",result=handles)   




if __name__ =="__main__":
    app.run(debug=True)    


  
                    
                    
                    
