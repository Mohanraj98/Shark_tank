import mysql.connector
from flask import Flask, render_template, request

class Shark_tank:

    #Database Connectivity
    def db_connect(self):
        try:
            self.mydb = mysql.connector.connect(
            host="remotemysql.com",
            user="7eumJKSEFG",
            passwd="jfu62wjCyE",
            database="7eumJKSEFG",
            port=3306
            )
            return "Success"
        except:
            return "Failure"


    #Database Query and Result
    def find_result(self,season=0, episode=0, investors="All", investor_amount=0,product="All",status="Funded",gender="Both"):
        print(season, episode, investors, investor_amount)
        cursor = self.mydb.cursor()
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
        try:
            cursor.execute(loginquery)
            records = cursor.fetchall()
            return records
        except:
            return "Enter a valid value"

    def rendres(self,records):
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

    def db_close(self):
        self.mydb.close()


#FLASK APPLICATION
app = Flask(__name__)


#OBJECT FOR CLASS
s=Shark_tank()


#RENDER WEB PAGE
@app.route('/')
def index():
    return render_template('index.html')


#RENDER RESULT ALONG WEB PAGE
@app.route('/', methods=['POST'])
def page():
    #Fetch details from webpage
    season = request.form['Seasons']
    episode = request.form['episode']
    investor_amount = request.form['amount']
    gender = request.form['gender']
    investors = request.form['investors']

    #call database connection
    status=s.db_connect()
    if(status=="Failure"):
        return render_template('index.html',Result="Error in connecting to the database!! \nPlease try again later.")
    else:
        #Get the results from the database
        records= s.find_result(season=season,episode=episode,investors=investors,gender=gender,investor_amount=investor_amount)
        if(records=="Enter a valid value"):
            return render_template('index.html',Result=records)

        #Render resullt to the web page
        res=s.rendres(records)
        return render_template('index.html',Result=res)


#CALLING FLASK APPLICATION
if __name__ == '__main__':
    app.run(debug=True)

#Closing Database Connection
s.db_close()