"""from flask import Flask,jsonify, request,redirect,url_for,render_template
import requests
import json

app=Flask(__name__)

class users():
	name="shubham"
	username="bumbum"
	email="sa21asd"
	url="https://avatars1.githubusercontent.com/u/18347915?v=3&s=40"

@app.route("/")
def hello():
    return render_template('home.html')
    #return json.dumps({"message":"Hello World!"})

@app.route("/register")
@app.route("/login")
def login():
	return render_template('LoginPage.html')
	#return "You have logged in successfully"
	
@app.route("/profile")
def profile():
	return render_template('Profile.html', user=users())

@app.route("/QandA")
def QandA():
	return render_template('Q&A.html')


if __name__=='__main__':
	app.secret_key='secret123'
	app.run(debug=True)



from flask import Flask,jsonify, request,redirect,url_for,render_template
import requests
import json

import config

app = Flask(__name__)

data_url = None
headers = {
    'Content-Type': 'application/json'
}

#if not config.DEVELOPMENT:
if 1==1:
    data_url = 'http://auth.c100.hasura.me:80'
    
else:
    # Make a request to the data API as the admin role for full access
    data_url = 'http://data.hasura'
    headers['X-Hasura-Role'] = 'admin'
    headers['X-Hasura-User-Id'] = '1'

query_url = data_url + '/login'

@app.route("/")
def home():
	return render_template('home.html')

@app.route("/login")
def hello():
    query={"username":"shubhma","password":"WhyShouldItellYou"}
    print("data_url= \n",data_url,"\n","query_url=\n",query_url,"\n headers=\n",headers,"\n data=\n",json.dumps(query))
    r=requests.post(query_url, data=json.dumps(query) ,headers=headers)
    print("r=",r)
    return jsonify(r.json())
    query ={
            		"type": "select",
            		"args": {
            			"table": "Users",
            			"columns": ["*"]
            			}
            		}
            
            
                r = requests.post(query_url, data=json.dumps(query), headers=headers)
                if r.status_code != 200:
                    return "Error fetching current schema: %s" % r.text
            
                return jsonify(r.json())
         
@app.route("/<string:role>")
def get_role(role):
    roles = request.headers['X-Hasura-Allowed-Roles']

    if role in roles:
        return "Hey you have the %s role" % role

    return ('DENIED: Only a user with %s role can access this endpoint' % role, 403)

@app.route("/register")
@app.route("/login")
def login():
	return render_template('LoginPage.html')
	#return "You have logged in successfully"
	
	
if __name__ == '__main__':
    app.run(debug=True)
"""






#THE ERROR THAT FRUSTATED ME FOR 3 DAYS WAS THE AUTHORIZATION TOKEN AND was using https which is not supported by hasura






from flask import Flask,jsonify, request,redirect,url_for,render_template,flash, session, logging
import requests
import json
from wtforms import *
from passlib.hash import sha256_crypt
from functools import wraps	

import config

data_url = None
auth_url= None
headers = {
    'Content-Type': 'application/json'
}

if config.DEVELOPMENT:
    data_url = 'http://data.{}.hasura-app.io'.format(config.PROJECT_NAME)
    auth_url = 'http://auth.{}.hasura-app.io'.format(config.PROJECT_NAME)
    headers['Authorization'] = 'Bearer ' + config.ADMIN_TOKEN
else:
    # Make a request to the data API as the admin role for full access
    data_url = 'http://data.hasura'
    headers['X-Hasura-Role'] = 'admin'
    headers['X-Hasura-User-Id'] = '1'


data_url='http://data.c100.hasura.me'
auth_url='http://auth.c100.hasura.me'


query_url = data_url + '/v1/query'

class RegistrationForm(Form):
	name=StringField('Name',[validators.Length(min=1 ,max=50)])
	username=StringField('Username',[validators.Length(min=4,max=25)])
	email=StringField('email',[validators.Length(min=6,max=50)])
	mobile=StringField('Mobile',[validators.Length(min=6, max=15)])
	password=PasswordField('Password',[
			validators.DataRequired(),
			validators.Length(min=6,max=15),
			validators.EqualTo('confirm',message="Password should match Confirm Password")
		])
	confirm=PasswordField('Confirm',[validators.Length(min=4,max=25)])


app=Flask(__name__)
@app.route("/")
def home():
    query={"type": "select", "args": {"table": "categories" ,"columns":["*"] }}
    r=requests.post(query_url, data=json.dumps(query) ,headers=headers).json()
    #print("r=",r)
    return render_template('home.html', categories=r, session=session)
    #return json.dumps({"message":"Hello World!"})


@app.route('/register',methods=['GET','POST'])
def register():
	form=RegistrationForm(request.form)
	print("FORM =========== ",form," \n\n")
	if request.method=='POST' and form.validate():
		name=form.name.data
		username=form.username.data
		email=form.email.data
		mobile=form.mobile.data
		password=sha256_crypt.encrypt(str(form.password.data))

		query_url=auth_url+'/signup'
		query={
			"username": username,
			"password": password,
			"email":email,
			"mobile":mobile
		}
		r=requests.post(query_url, data=json.dumps(query) ,headers=headers).json()
		print("r=======" ,r)
		redirect(url_for('home'))
	return render_template('LoginPage.html', form=form, endpoint="reg")
	

@app.route("/login" , methods=['GET','POST'])
def login():
	if request.method=='POST':
		query_url= auth_url+'/login'
		username=request.form['username']
		password=request.form['password']
		query={'username': username , "password": password}
		r=requests.post(query_url, data=json.dumps(query) ,headers=headers).json()
		print("r=====" ,r)
		if(r['auth_token']):
			session['auth_token']=r['auth_token']
			session['hasura_id']=r['hasura_id']
		else:
			return jsonify(r)
		print("Redirecting...")
		return redirect(url_for('home'))
		#render_template('home.html')   
	return render_template('LoginPage.html' , form=form, endpoint="login")
	#return "You have logged in successfully"
	
@app.route("/profile")
def profile():	
	query={"type":"select" , "args": {"table":"profile", "columns":["*"] ,"where": {"uid": 3}}}
	r=requests.post(query_url, data=json.dumps(query) ,headers=headers).json()
	print("r=====" ,r)
	return render_template('Profile.html', user=r)

@app.route("/QandA")
def QandA():
	return render_template('Q&A.html')


if __name__=='__main__':
	app.secret_key='secret123'
	app.run(debug=True)

