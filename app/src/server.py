
#This is not the complete server.py file
#To view it, contact me at 



from flask import Flask,jsonify, request,redirect,url_for,render_template,flash, session, logging
import requests
import json
from wtforms import *
from passlib.hash import sha256_crypt
from functools import wraps	
from bs4 import BeautifulSoup
import random,os,sys

import config

app = Flask(__name__)

data_url = None
auth_url= None
headers = {
    'Content-Type': 'application/json'
}

data_url = 'http://data.HowTo.hasura.me'
auth_url = 'http://auth.HowTo.hasura.me'


query_url = data_url + '/v1/query'
print("Config.Development=====",config.DEVELOPMENT)
print("config.PROJECT_NAME=====",config.PROJECT_NAME)


class RegistrationForm(Form):
	name=StringField('Name',[validators.Length(min=1 ,max=50)])
	username=StringField('Username',[validators.Length(min=4,max=25)])
	email=StringField('email',[validators.Length(min=6,max=50)])
	#mobile=StringField('Mobile',[validators.Length(min=6, max=15)])
	password=PasswordField('Password',[
			validators.DataRequired(),
			validators.Length(min=8,max=15),
			validators.EqualTo('confirm',message="Password should match Confirm Password")
		])
	confirm=PasswordField('Confirm',[validators.Length(min=8,max=15)])

class ForgotForm(Form):
	email=StringField('Email',[validators.Length(min=4)])


class LoginForm(Form):
	username=StringField('Username',[validators.Length(min=4,max=25)])
	password=PasswordField('Password',[
			validators.DataRequired(),
			validators.Length(min=8,max=15),
		])


def ripOff(s):
	while not s[0].isalnum():
		s=s[1:]
	while not s[-1].isalnum():
		s=s[:-2]
	return s.strip().lower()


def ripOff2(s):
	while not s[0].isalnum():
		s=s[1:]
	while not s[-1].isalnum():
		s=s[:-1]
	return s.strip()	

@app.context_processor
def override_url_for():
    return dict(url_for=dated_url_for)

def dated_url_for(endpoint, **values):
    if endpoint == 'static':
        filename = values.get('filename', None)
        if filename:
            file_path = os.path.join(app.root_path,
                                     endpoint, filename)
            values['q'] = int(os.stat(file_path).st_mtime)
    return url_for(endpoint, **values)

def is_logged_in(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'logged_in' in session and auth_token in session and 'Authorization' in headers:
            return f(*args, **kwargs)
        else:
        	flash("Unauthorised, Please Login", 'danger')
        	return redirect(url_for('login'))
    return wrap

@app.route("/")
def home():
	print("Config.Development=====",config.DEVELOPMENT)
	query_url=data_url+"/v1/query"
	print(headers,"\n\n",query_url)
	print(session)
	#print('logged_in' in session)
	if 'logged_in' in session:
		headers['Authorization'] = 'Bearer ' + session['auth_token']
		query={"type":"select", "args":{"table":"profile", "columns":["profilepic"], "where":{"username":session['username']}}}
		print(json.dumps(query,indent=2))
		print(query_url)
		PP=requests.post(query_url, data=json.dumps(query), headers=headers).json()
		print(PP,"\n\n\n\n")
		print(session['logged_in'],session['auth_token'], headers['Authorization'])

	else:
		print("User is not logged in")
		session.clear()
		if('Authorization') in headers.keys():
			headers.pop('Authorization')

	query={"type": "select", "args": {"table": "categories" ,"columns": ["*"] }}
	r=requests.post(query_url, data=json.dumps(query) ,headers=headers).json()
	print("r=",r)

	#selecting sample answers for home page
	query={"type":"select", "args":{"table":"answers", "columns":["*"], }}
	SampleAns=requests.post(query_url, data=json.dumps(query) ,headers=headers).json()
	random.shuffle(SampleAns)
	print("Sample answers=",len(SampleAns))

	SampQues=[]
	for i in SampleAns:
		q=i['question']
		query={
		  "args": {
		   
		    "columns": [
		      "title"
		    ],"where":{"id":q},
		    "table": "questions"
		  },
		  "type": "select"
		}
		temp=requests.post(query_url, json.dumps(query, indent=2), headers=headers).json()
		SampQues.append(temp[0]['title'])	
	print("SampQues",SampQues)

	x=SampleAns[0]['answer'];
	# print(x)
	#print(PP[0]['profilepic'])
	try:
	    return render_template('home.html',headers=headers, categories=r, ripOff=ripOff2, str=str, len=len, session=session, articles=SampleAns ,SampQues=SampQues ,noOfArticle=len(SampleAns), ProfilePic=PP[0]['profilepic']) 
	except:
		return render_template('home.html',headers=headers, categories=r, ripOff=ripOff2, str=str, len=len, session=session, articles=SampleAns ,SampQues=SampQues ,noOfArticle=len(SampleAns)) 
	#return json.dumps({"message":"Hello World!"})


def is_logged_in(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
            return f(*args, **kwargs)
        else:
        	flash("Unauthorised, Please Login", 'danger')
        	return redirect(url_for('login'))
    return wrap


@app.route('/register',methods=['GET','POST'])
def register():
	print("Config.Development=====",config.DEVELOPMENT)
	form=RegistrationForm(request.form)
	print("FORM =========== ",form," \n\n")
	print(request.method)
	#print(form.validate())
	if request.method=='POST' and form.validate():
	
		name=form.name.data
		username=form.username.data
		email=form.email.data 
		#mobile=form.mobile.data
		#password=sha256_crypt.encrypt(str(form.password.data))
		password=form.password.data
		print("Read username %s inside register endpoint successfully."%(username))
		query_url="http://auth.HowTo.hasura.me/signup"
		query={
			"username": username,
			"password": password,
			"email":email,
			#"mobile":mobile
		}
		print("headers for Registration== " ,headers)
		try:
			print(query_url,"\n",query)
			r=requests.post(query_url, data=json.dumps(query) ,headers={'Content-Type': 'application/json'})
			if r.status_code==200:
				print("r for register=======" ,r)
				# return redirect(url_for('login'))
			else:
				print(r.json())
				return json.dumps(r.json())
		except:
			print("ERROR")
			print("r for register=======" ,r)


		query_url=data_url+'/v1/query'
		query={
			"type":"insert",
			"args":{
				"table":"profile",
				 "objects":[{
					"username": username, 
					"name": name,
					"email": email,
					#"mobile": mobile,
				}]
			}
		}
		print(query_url,query)
		r=requests.post(query_url, data=json.dumps(query) ,headers=headers)
		if r.status_code==200:
			print("r=======" ,r)
			return redirect(url_for('login'))
		else:
			return json.dumps(r.json() ,indent=2)
	"""	else:
						print("failed")
						flash("Error in Registering. Make sure your email is valid")
				"""
	return render_template('LoginPage.html', form=form, endpoint="reg")
	

@app.route("/login" , methods=['GET','POST'])
def login():
	print("Config.Development=====",config.DEVELOPMENT)
	print("This is login endpoint")
	print(headers)
	try:
		if('Authorization') in headers.keys():
			headers.pop('Authorization')
		session.clear()
	except Exception as e:
		print("error=",e)

	form=LoginForm(request.form)
	if request.method=='POST':
		query_url= auth_url+'/login'
		username=request.form['username']
		password=request.form['password']
		ps=form.password.data
		print(ps)
		query={'username': username , "password": password}
		try:
			print(query)
			print(query_url)
			print(headers)
			#Set the headers to correct  values
			r=requests.post(query_url, data=json.dumps(query) ,headers=headers).json()
			print("r inside try=====" ,r)
			if(r['auth_token']):
				session['logged_in']=True
				session['auth_token']=r['auth_token']
				session['hasura_id']=r['hasura_id']
				session['username']=username
				headers['Authorization'] = 'Bearer ' + session['auth_token']
				query={
					"type":"update","args":{
						"table":"profile",
						"$set": {"id": session['hasura_id']},
						"where": {"username": username},
						"returning": ["id"]
						}
					}
				query_url=data_url+'/v1/query'
				print(query)
				print(headers)
				print(query_url)
				r=requests.post(query_url, data=json.dumps(query) ,headers=headers)
				print("r=======" ,r)
				if r.status_code!=200:
					print("Not Found PP")
				else:
					r=r.json()
				
			else:
				return jsonify(r)
			print("Redirecting...")
		except Exception as e:
			print(e)
			incor=True
			flash("Invalid Credentials","warning")
			return redirect(url_for('login',incor="True"))
		print("Sessions====",session)
		return redirect(url_for('home'))		
		#render_template('home.html')   
	print("FORM FOR LOGIN ENDPOINT IS ",form)
	return render_template('LoginPage.html' , form=form, endpoint="login")
	#return "You have logged in successfully"
	

@app.route('/forgotPass' ,methods=["GET","POST"])
def forgotPass():
	form=ForgotForm(request.form)
	#form=request.form
	if request.method=="POST":
		print("POST Method Used...")
		email=request.form['email']
		print("Email= ",email)
		query_url=data_url+"/v1/query"
		query={
		"type":"count",
		"args":{
		"table":"profile",
		"where":{"email":email}
		}
		}
		validEmail=requests.post(query_url, data=json.dumps(query), headers=headers)

		query={"type":"insert",
			"args":{
			"table":"ForgotPass",
			"objects":[
				{
					"email":email
				}
			]
			}
		}
		print("query=",query)
		print("headers=",headers)
		r=requests.post(query_url,data=json.dumps(query),headers=headers).json()
		print(r)
		#print(type(email))
		#print(email['value'])
		return redirect(url_for('login'))
	return render_template('ForgotPassword.html' , form=form)


@app.route('/logout')
@is_logged_in
def logout():
	print("session['logged_in']= ",session['logged_in'])
	session.clear()
	if 'Authorization' in headers:
		headers.pop('Authorization')
	query_url= auth_url+'/user/logout'
	r=requests.post(query_url ,headers=headers).json()
	print("r=====" ,r)	
	flash("Successfully Logged Out", "Success")
	return redirect(url_for('home'))


@app.route("/profile")
@is_logged_in
def profile():
	print(session['username'])
	print(headers)
	if 'logged_in' in session:
		headers['Authorization'] = 'Bearer ' + session['auth_token']
	#query={"type":"select" , "args": {"table":"Users", "columns":["*"] ,"where": {"uid": 3}}}	
	query={"type":"select" ,
		"args": {
		"table":"profile",
		"columns":["*"] ,
		"where": {"username": session['username']}
	}}
	print(query)
	print(query_url)
	print(headers)
	r=requests.post(query_url, data=json.dumps(query) ,headers=headers).json()
	print("r=====" ,r)

	print(session)
	query={
	"type":"select" ,
		"args": {
		"table":"questions",
		"columns":["title"] ,
		"where": {"asked_by": session['username'] }
		}
	}
	print(query_url)
	print(headers)
	qasked=requests.post(query_url, data=json.dumps(query) ,headers=headers).json()
	print("qasked=====" ,qasked)
	#qasked of type [{'title':"abc"},{...}]

	print(session)
	query={
	"type":"select" ,
		"args": {
		"table":"answers",
		"columns":["question"] ,
		"where": {"answered_by": session['username'] }
		}
	}
	print(query_url)
	print(headers)
	qanswered=requests.post(query_url, data=json.dumps(query) ,headers=headers).json()
	print("qanswered=====" ,qanswered)


	temp=[]
	for i in qanswered:
		query={
		"type":"select" ,
			"args": {
			"table":"questions",
			"columns":["title"] ,
			"where": {"id": i['question'] }
			}
		}
		print(query_url)
		print(headers)
		titl=requests.post(query_url, data=json.dumps(query) ,headers=headers).json()
		print("qanswered=====" ,titl)
		temp.append(titl[0]['title'])

	print("Questions Answered=====" ,temp)
	return render_template('Profile.html', user=r[0], Qans=temp, Qask=qasked, len=len)




@app.route("/QandA")
@is_logged_in
def QandA():
	print("Entered qANDa endpoint")
	query_url=data_url+"/v1/query"

	query={"type":"count" , "args":{
		"table":"questions"
		#  "where":{
		# 	"category":"Technology"
		# }
	}}
	print(query,query_url,)
	noOfQues=requests.post(query_url, data=json.dumps(query) ,headers=headers).json()
	noOfQues=noOfQues['count']
	print(noOfQues)
	title_list=[]
	temp=[]
	
	# try:
	# 	for i in range(min(noOfQues,3)):
	# 		randomId=random.randint(1,noOfQues)
	# 		while(randomId in temp):
	# 			randomId=random.randint(1,noOfQues)
	# 		temp.append(randomId)
	# 		#print(temp)
	mappedSubs={}

	query={"type":"select" ,
	"args":{
		"table":"categories",
		"columns":["category","subcategories"],
		}
	}
	categories=[]
	subcategs=[]
	categs=requests.post(query_url, data=json.dumps(query) ,headers=headers)
	if categs.status_code == 200:
		categs=categs.json()
		print("categs===== ",categs,"\n")
		for i in categs:
			categories.append(ripOff2(i['category']))
			subcategs.append(i['subcategories'])
			mappedSubs[ripOff2(i['category'])]=i['subcategories']
	print("categories===== ",categories,"\n")
	print("subcategories ===== ",subcategs,"\n")
	print("Mapped subcategories====",mappedSubs)
	# 		#print("type(i)= ",type(i))
	# 		title_list.append(r[0]['title'])
	# 		#print("titleList= ",title_list)
	# except Exception as e:
	# 	print(e)

	try:
		query={
		"type":"select",
			"args": {
			"table":"answers",
			"columns":["question"],
			}
		}
		Qids=requests.post(query_url, data=json.dumps(query) , headers=headers)
		print(Qids.json())
		ids=set()
		for i in Qids.json():
			ids.add(i['question'])



		query={
		"type":"select",
			"args": {
			"table":"questions",
			"columns":["title","id"] ,
			}
		}
		r1=requests.post(query_url, data=json.dumps(query) ,headers=headers)
		titles=set()
		for i in r1.json():
			if i['id'] not in ids:
				titles.add(i['title'].strip())


	except Exception as e:
		return str(e)
		print(e)

	titles=list(titles)
	PopQues=[]
	if len(titles)<4:
		PostQues=list(titles)
	else:
		while len(PopQues)<4:
			ran=random.randint(1,len(titles))
			if ran<len(titles) and len(titles[ran].strip())>0:
				PopQues.append(titles[ran])

	#print(query_url)
	print("\n",titles,"\n")
	#r=requests.post(query_url, data=json.dumps(query) ,headers=headers).json()
	#print("r=====" ,r)
	return render_template('Q&A.html', Titles=titles, PopQues=PopQues, Categories=categories, subcategories=subcategs, mappedSubs=mappedSubs)


@app.route('/PostQues', methods=["GET","POST"])
@is_logged_in
def PostQues():
	query_url=data_url+"/v1/query"
	question=request.form['questa']
	category=request.form['Category']
	subcategory=request.form['subCategory']
	
	print(session['username'])
	print(len(subcategory))
	soup=BeautifulSoup(question)
	ques=soup.p.text
	print("\nquestion=",ques,"\n category= ",category,'\n subcategory= ',subcategory,"\n")
	print("request.form=====",request.form)
	
	if category=="":
		category="Miscellaneous"
	if subcategory=="" or str(subcategory).strip()=="":
		subcategory="None"
	
	query={"type":"select" ,
		"args":{
			"table":"categories",
			"columns":["*"]
			}
		}
	print("\n\n",json.dumps(query, indent=2),"\n")
	print(query_url)
	categories=requests.post(query_url, json.dumps(query), headers=headers).json()
	print("categories= ",categories,"\n\n")

	query={"type":"insert" , "args":{
				"table":"questions", "objects": [{
					"question": question,
					"category": category,
					"subcategory": subcategory,
					"asked_by": session['username'],
					"title": ques
				}]
	}}

	# if subcategory!="":

	print("\n\n",json.dumps(query, indent=2),"\n")
	r=requests.post(query_url, json.dumps(query), headers=headers)

	print(r)
	if r.status_code == 200:
		flash("Question Asked successfully. Hold on tight. We'll be back with an answer soon.", "success")
	else:
		flash("Error in asking question","error")


	#Append the category if not already present
	cats=[]
	for i in categories:
		print(i)
		cats.append(i['category'].lower().strip())
	if(category.lower().strip("'") not in cats):
		query={"type":"insert",
			"args":{
				"table":"categories",
				 "objects":[{ "category":category }]
				 }
		}
		tee=[]
		# if subcategory!="":
		tee.append(subcategory)
		print("tee",tee)
		query["args"]["objects"][0]["subcategories"]=ripOff(subcategory)+','
		print(json.dumps(query,indent=2))
		r=requests.post(query_url, json.dumps(query), headers=headers)
		print(r,"\n\n")
	else:
		if subcategory!="":
			l=[]
			for i in categories:
				if(i['category'].lower().strip("'")==category.lower().strip("'")):
					l=i['subcategories']
					print(type(l))
					print(l)
					temp=set()
					if l!=None and len(l)>0 and l!="['None']": 
						#Splitting subcategories
						for j in l.split(','):
							temp.add(ripOff(j))
					temp.add(subcategory)
					print("temp=",temp)
					# flag=0
					# for i in temp:
					# 	if(subcategory in ripOff(i)):
					# 		flag=1
					# 		break
					# print(flag)
					# if flag==0:
					print("New subcats=",",".join(temp))
					query={
					"type":"update",
					"args":{
						"table":"categories",
						"$set": {"subcategories": ",".join(temp)},
						"where": {"category": category},
						"returning": ["category","subcategories"]
						}
					}
					print(query)
					print(headers)
					updatedCategs=requests.post(query_url, json.dumps(query), headers=headers).json()
					print("updates=",updatedCategs,"\n\n")
					# break
	
	query={"type":"select" ,
		"args":{
			"table":"questions",
			"columns":["id"],
			"where":{"question":question}
			}
		}
	QaskedId=requests.post(query_url, json.dumps(query), headers=headers)
	Qid=QaskedId.json()[0]['id']
	print("Id for the article inserted is:- ",Qid)
	omit=["what","what's","how","is","it","the","a","an",""]
	tags=[]
	for i in set(question.split(' ')):
		if not omit.__contains__(i):
			tags.append(i)
	print("Tags == ",tags," \n")
	for i in tags:
		query={"type":"insert" , "args":{
				"table":"Tags", 
				"objects": [{
					"tags":ripOff(i).lower(),
					"question":Qid
					}]
				}}
		insertedTag=requests.post(query_url, json.dumps(query), headers=headers)
		print(insertedTag.status_code, "\n", insertedTag.json())
	query={"type":"insert" , "args":{
			"table":"Tags", 
			"objects": [{
				"tags":ripOff(category),
				"question":Qid
				}]
			}}
	insertedTagCat=requests.post(query_url, json.dumps(query), headers=headers)
	print(insertedTagCat.status_code, "\n", insertedTagCat.json())
	if subcategory != "":
		query={"type":"insert" , "args":{
			"table":"Tags", 
			"objects": [{
				"tags": ripOff(subcategory),
				"question":Qid
				}]
			}}
		insertedTagScat=requests.post(query_url, json.dumps(query), headers=headers)
		print(insertedTagScat.status_code, "\n", insertedTagScat.json())
		
	return redirect(url_for('QandA'))

@app.route('/PostAns', methods=["GET","POST"])
@is_logged_in
def PostAns():
	#print(question)
	
	query_url=data_url+"/v1/query"
	print("username=",session['username'])
	tempo=request.form
	print(tempo)
	#print(type(tempo))
	print(tempo['answer'])
	# print(request.form[0])
	# print(request.form[0]['answer'])
	username=session['username']
	print("username= ",username)
	answer=request.form['answer']
	print("answer= ",answer)
	question=request.form['que']
	print("question=",question)
	#print(username,answer,question)

	#fetching the Question Id
	query={
		"type":"select",
		"args":{
			"table":"questions",
			"columns":["id"],
			"where": {"title": question},
		}
	}
	print(json.dumps(query, indent=2))
	qid=requests.post(query_url, json.dumps(query) , headers=headers).json()
	print("qid=",qid)



	# print(len(subcategory))
	# soup=BeautifulSoup(question)
	# ques=soup.p.text
	# print("\nquestion=",ques,"\n category= ",category,'\n subcategory= ',subcategory,"\n")
	print("request.form=====",request.form)
	
	# if category=="":
	# 	category="Miscellaneous"
	# # if subcategory=="":
	# 	subcategory=null 
	
	
	#print(CKEDITOR.instances.editor1.getData());
	#question=request.form.ques
	query={"type":"insert" , "args":{
				"table":"answers", "objects": [{
					"answer": answer,
					"answered_by": username,
					"question": qid[0]['id']
				}]
	}}
	
	print("\n\n",json.dumps(query, indent=2),"\n")
	r=requests.post(query_url, json.dumps(query), headers=headers)

	print(r,"\n",r.json())
	if r.status_code == 200:
		r=r.json()
		print(json.dumps(r, indent=2))
		flash("Successfully Posted your answer", "success")
	else:
		flash("Error in asking question","error")	

	query={
		"type": "select",
		"args": {
			"table":"answers",
			"columns":["id"],
			"where":{"answer": answer,
					"answered_by": username,
					"question": qid[0]['id']
			}
		}
	}
	print(json.dumps(query, indent=2))
	print(headers)
	ansId=requests.post(query_url, json.dumps(query), headers=headers)
	print(ansId,"\n",ansId.json())

	query={
		"type":"update",
		"args":{
			"table":"questions",
			"$set": {"answer": ansId.json()[0]['id']},
			"where": {"id":qid[0]['id']},
			"returning": ["id","answer"]
			}
		}
	print(json.dumps(query, indent=2))
	Qid=requests.post(query_url, json.dumps(query), headers=headers)
	print(Qid,"\n",Qid.json())
	return redirect(url_for('home'))



@app.route('/insertImg', methods=["GET","POST"])
@is_logged_in
def insertImg():
	print(request.form['ImageUrl'])
	query={
		"type":"update",
		"args":{
			"table":"profile",
			"$set": {"profilepic": request.form['ImageUrl']},
			"where": {"username": session['username']},
			"returning": ["profilepic","username"]
			}
		}
	query_url=data_url+'/v1/query'
	print(json.dumps(query, indent=2))
	print(headers)
	print(query_url)
	r=requests.post(query_url, data=json.dumps(query) ,headers=headers).json()
	print("r=======" ,r)
	
	return redirect(url_for('profile'))



#get the data from the form
#for rendering an article you get a category and fetch the corresponding article ie from question table and answer table as done in home
#Pass these articles to the home endpoint with comm=2


@app.route('/renderArticle' ,methods=["POST"])
def renderArticle():
	query_url=data_url+'/v1/query'
	x=request.form
	print(x)
	print(dict(x))
	categs=[]	
	for i in request.form:
		print(ripOff(i)," is ",x[i])
		categs.append(i)
	print("categs = ",categs,"\n\n")

	qids=[]
	questions=[]
	for i in categs:
		print(i)
		print(ripOff(i))
		query={
			"type": "select",
			"args": {
				"table":"questions",
				"columns":["*"],
				"where":{"subcategory": ripOff2(i)} 
			}
		}
		print(query)
		subques=requests.post(query_url, json.dumps(query), headers=headers)
		if(len(subques.json())>0):
			for j in subques.json():
				qids.append(j['id'])
				questions.append(j['title'])
	
	print("QUIDs = ",qids)
	print("Questions= ",questions)

	#print('logged_in' in session)
	if 'logged_in' in session:
		headers['Authorization'] = 'Bearer ' + session['auth_token']
		query={"type":"select", "args":{"table":"profile", "columns":["profilepic"], "where":{"username":session['username']}}}
		print(query)
		PP=requests.post(query_url, data=json.dumps(query), headers=headers).json()
		print(PP,"\n\n\n\n")
		print(session['logged_in'],session['auth_token'], headers['Authorization'])

	else:
		print("User is not logged in")
		session.clear()
		if('Authorization') in headers.keys():
			headers.pop('Authorization')


	query={"type": "select", "args": {"table": "categories" ,"columns": ["*"] }}
	categs=requests.post(query_url, data=json.dumps(query) ,headers=headers)
	print("categories=",categs.json(),"\n\n")

	#selecting answers to be rendered
	questionsFinal=[]
	answers=[]
	for i in range(len(qids)):
		query={"type":"select", "args":{"table":"answers", "columns":["*"], "where": {"question":qids[i]}}}
		print(query)
		Ans=requests.post(query_url, data=json.dumps(query) ,headers=headers).json()
		print("Answer= ",Ans)
		if (len(Ans)>0):
			answers.append(Ans[0])
			print(i)
			questionsFinal.append(questions[i])
		# else:
		# 	questions.pop(0)
		#random.shuffle(SampleAns)
	print("Answers= ",answers,"\n\n")
	print("Question= ",questionsFinal)
	try:
	    return render_template('home.html', headers=headers, categories=categs.json(), ripOff=ripOff2, str=str, len=len, session=session, answers=answers, questions=questionsFinal, comm=2, noOfArticle=len(answers), ProfilePic=PP[0]['profilepic']) 
	except:
		return render_template('home.html', headers=headers, categories=categs.json(), ripOff=ripOff2, str=str, len=len, session=session, answers=answers, questions=questionsFinal, comm=2 , noOfArticle=len(answers),) 
	#return json.dumps({"message":"Hello World!"})



	# return "rendered"




@app.route('/search', methods=["GET","POST"])
def search():
	x=dict(request.form)
	Query=x['searchQuery'][0].lower()
	#tags=set(Query.split(' '))
	omit=["what","what's","how","is","it","the","a","an",""]
	tags=[]
	for i in set(Query.split(' ')):
		if not omit.__contains__(i):
			tags.append(i)
	print(tags)
	query_url=data_url+'/v1/query'
	titles=[]
	for i in range(min(15,len(tags))):
		query={"type":"select", "args":{
			"table":"Tags",
			"columns":["*"],
			"where": {"tags": ripOff(tags[i]) }
		}}
		print(query)
		r=requests.post(query_url, data=json.dumps(query) ,headers=headers)
		print("r=======" ,r,"\n",r.json())
		questions=set()
		if r.status_code == 200 and len(r.json())>0:
			print("successfully retrieved some questions")
			print(type(questions))
			for i in r.json():
				questions.add(i['question'])
			questions=list(questions)
			
			print("Questions===",questions)
			for i in questions:
				query={
				  "args": {
				    "columns": [
				      "title"
				    ],"where":{"id": i},
				    "table": "questions"
				  },
				  "type": "select"
				}
				title=requests.post(query_url, json.dumps(query, indent=2), headers=headers).json()
				print("title=",title)
				for i in title:
					titles.append(i['title'])
			print("titles=",titles)
		else:
			print("failed")
	#print('logged_in' in session)
	if 'logged_in' in session:
		headers['Authorization'] = 'Bearer ' + session['auth_token']
		query={"type":"select", "args":{"table":"profile", "columns":["profilepic"], "where":{"username":session['username']}}}
		print(query)
		PP=requests.post(query_url, data=json.dumps(query), headers=headers).json()
		print(PP,"\n\n\n\n")
		print(session['logged_in'],session['auth_token'], headers['Authorization'])
	else:
		print("User is not logged in")
		session.clear()
		if('Authorization') in headers.keys():
			headers.pop('Authorization')

	query={"type": "select", "args": {"table": "categories" ,"columns": ["*"] }}
	r=requests.post(query_url, data=json.dumps(query) ,headers=headers).json()
	print("r=",r)

	#selecting sample answers for home page
	query={"type":"select", "args":{"table":"answers", "columns":["*"], }}
	SampleAns=requests.post(query_url, data=json.dumps(query) ,headers=headers).json()
	random.shuffle(SampleAns)
	#print("Sample answers=",SampleAns)
	SampQues=[]
	for i in SampleAns:
		q=i['question']
		query={
		  "args": {
		   
		    "columns": [
		      "title"
		    ],"where":{"id":q},
		    "table": "questions"
		  },
		  "type": "select"
		}
		temp=requests.post(query_url, json.dumps(query, indent=2), headers=headers).json()
		SampQues.append(temp[0]['title'])	
	print("SampQues",SampQues)
	x=SampleAns[0]['answer'];
	print(x)
	#print(PP[0]['profilepic'])
	try:
	    return render_template('home.html',headers=headers, categories=r, ripOff=ripOff2, len=len, str=str, session=session, articles=SampleAns ,SampQues=SampQues ,noOfArticle=len(SampleAns), ProfilePic=PP[0]['profilepic'], comm=1, searchRes=titles) 
	except:
		return render_template('home.html', headers=headers,categories=r, ripOff=ripOff2, len=len, str=str, session=session, articles=SampleAns ,SampQues=SampQues ,noOfArticle=len(SampleAns), comm=1, searchRes=titles) 
	#return json.dumps({"message":"Hello World!"})


	#You have words that have to be matchec
	#You have a tags table with questions mapped to tags
	#Search tags table for each tag in the query
	#if tag is present in tags table select it

	#search code is 1





@app.route('/renderSearch', methods=["GET","POST"])
def renderSearch():
	query_url=data_url+'/v1/query'
	x=request.form
	print(dict(x))
	print(x['renArt'])
	# print(x)
	# categs=[]	
	# for i in request.form:
	# 	print(ripOff(i)," is ",x[i])
	# 	categs.append(i)
	# print("categs = ",categs,"\n\n")
	titl=x['renArt']
	query={"type":"select", "args":{"table":"questions", "columns":["answer"], "where":{"title":titl} }}
	print(query)
	answers=requests.post(query_url, data=json.dumps(query) ,headers=headers).json()
	print(json.dumps(answers ,indent=2))
	# if(len(answers)==0):
	# 	return "Not Answered Yet"
	# else:
	# 	# for i in answers:
	query={"type":"select", "args":{"table":"answers", "columns":["*"], "where": {"id":answers[0]['answer']} }}
	print(query)
	SampleAns=requests.post(query_url, data=json.dumps(query) ,headers=headers).json()
	print(SampleAns)
	# return "Rendered"
	nf=0
	if(len(SampleAns)==0):
	 	nf=1

	query={"type": "select", "args": {"table": "categories" ,"columns": ["*"] }}
	r=requests.post(query_url, data=json.dumps(query) ,headers=headers).json()
	print("r=",r)
	lis=[]
	lis.append(titl)
	print("noOfArticle=",len(SampleAns))
	try:
	    return render_template('home.html',headers=headers, categories=r, ripOff=ripOff2, str=str, len=len, session=session, articles=SampleAns ,SampQues=lis ,noOfArticle=len(SampleAns), NotFound=nf, ProfilePic=PP[0]['profilepic']) 
	except:
		return render_template('home.html',headers=headers, categories=r, ripOff=ripOff2, str=str, len=len, session=session, articles=SampleAns ,SampQues=lis ,noOfArticle=len(SampleAns), NotFound=nf,) 
	#return json.dumps({"message":"Hello World!"})


# @app.route("/<string:role>")
# def get_role(role):
#     roles = request.headers['X-Hasura-Allowed-Roles']
#     if role in roles:
#         return "Hey you have the %s role" % role

#     return ('DENIED: Only a user with %s role can access this endpoint' % role, 403)


if __name__ == '__main__':

	app.run(debug=True)



