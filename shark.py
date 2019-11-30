import mysql.connector
from flask import Flask, jsonify, render_template, request



mydb = mysql.connector.connect(
    host="remotemysql.com",
    user="7eumJKSEFG",
    passwd="jfu62wjCyE",
    database="7eumJKSEFG",
    port=3306
)



def find_result(season=0, episode=0, investors="All", investor_amount=0,product="All",status="Funded",gender="Both"):
    print(season, episode, investors, investor_amount)
    cursor = mydb.cursor()
    loginquery= "select c.Company, c.Amount, p.product, p.season, p.episode from products as p, company_info as c "
    if (season==0 and episode==0 and investors=="All" and investor_amount==0):
        #print("Default")
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
    tstr=""
    for x in records:
        c=0
        for y in x:
            if(c==0):
                tstr=tstr+str(y)+"\t\t"
                c+=1
            else:
                tstr=tstr+str(y)+"\t"
        tstr+="\n"
    print(tstr)
    return tstr




def f1(text):
    return text.upper()


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
    code=str("<h1>Hello<h1>")
    return render_template('index.html',Result=res)
    return render_template('index.html',Result=res)


if __name__ == '__main__':
    app.run(debug=True)

####################################################################################



# find_result(season=1,status="Funded",investors="Barbara Corcoran",gender="Female")
mydb.close()
# season=1, ,status="Funded" investors="Barbara Corcoran"