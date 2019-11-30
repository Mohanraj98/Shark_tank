import mysql.connector
from flask import Flask, render_template, request


#Database Connectivity
mydb = mysql.connector.connect(
    host="remotemysql.com",
    user="7eumJKSEFG",
    passwd="jfu62wjCyE",
    database="7eumJKSEFG",
    port=3306
)

#Database Query and Result
def find_result(season=0, episode=0, investors="All", investor_amount=0,product="All",status="Funded",gender="Both"):
    print(season, episode, investors, investor_amount)
    cursor = mydb.cursor()
    loginquery= "select p.company_link,c.Company, p.investors, p.product, c.Amount, p.season, p.episode from products as p, company_info as c "
    if (season==0 and episode==0 and investors=="All" and investor_amount==0):
        loginquery+=''

    else:
        count=0
        loginquery+="where p.company_title=c.Company and("
        if(season!='0'):
            loginquery+=" p.season='"+str(season)+"'"
            count+=1
        if(episode!=''):
            if(count!=0):
                loginquery+=" and"
            loginquery+=" p.episode='"+str(episode)+"'"
            count+=1
        if(investors!="All"):
            if(count!=0):
                loginquery+=" and"
            loginquery+=" p.investors like '%"+investors+"%'"
            count+=1
        if(investor_amount!=0):
            if(count!=0):
                loginquery+=" and"
            loginquery+=" c.Amount<"+str(investor_amount)
            count+=1
        if(product!="All"):
            if(count!=0):
                loginquery+=" and"
            loginquery+=" p.product="+"'"+product+"'"
            count+=1
        if(status!="All"):
            if(count!=0):
                loginquery+=" and"
            loginquery+=" p.status="+"'"+status+"'"
            count+=1
        if(gender!='both'):
            if(count!=0):
                loginquery+=" and"
            loginquery+=" c.Entrepreneur_Gender="+"'"+gender+"'"
            count+=1
        loginquery+=")"
    #print(loginquery)
    cursor.execute(loginquery)
    records = cursor.fetchall()
    #print(records)
    tstr=str('<table style="width:100%"><tr><th>Company</th><th>Investors</th><th>Product</th><th>Amount($)</th><th>Season</th><th>Episode</th></tr>')
    for x in records:
        count=0
        tstr+="<tr>"
        for y in x:
            if count==0:
                tstr+="<td><a href='"+str(y)+"'>"
                count+=1
            elif count==1:
                tstr+=str(y)+"</a></td>"
                count+=1
            else:
                tstr+="<td>"+str(y)+"</td>"
        tstr+="</tr>"
    tstr+="</table>"
    print(tstr)
    return tstr


#FLASK APPLICATION
app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/', methods=['POST'])
def page():
    season = request.form['Seasons']
    episode = request.form['episode']
    investor_amount = request.form['amount']
    gender = request.form['gender']
    investors = request.form['investors']
    res= find_result(season=season,episode=episode,investors=investors,gender=gender,investor_amount=investor_amount)
    return render_template('index.html',Result=res)

#CALLING FLASK APPLICATION
if __name__ == '__main__':
    app.run(debug=True)

#Closing Database Connection
mydb.close()