True s85ptyww42zrjkv2uf34pswricujjwoo Bearer s85ptyww42zrjkv2uf34pswricujjwoo
r= [{'subcategories': '[Android,YouTube] ', 'category': 'Technology', 'id': 1}, {'subcategories': None, 'category': 'Docs Required', 'id': 2}]
Sample answers= []
127.0.0.1 - - [15/Jul/2017 20:31:12] "GET / HTTP/1.1" 200 -
Shubham1
http://data.c100.hasura.me/v1/query
{'Content-Type': 'application/json', 'Authorization': 'Bearer s85ptyww42zrjkv2uf34pswricujjwoo'}
r===== [{'email': 'sa126@snu.edu.in', 'name': 'Shubham', 'profilepic': None, 'mobile': None, 'username': 'Shubham1', 'id': 1}]
127.0.0.1 - - [15/Jul/2017 20:31:18] "GET /profile HTTP/1.1" 200 -
session['logged_in']=  True
r===== {'message': 'You have to be user to access this endpoint'}
127.0.0.1 - - [15/Jul/2017 20:31:19] "GET /logout HTTP/1.1" 302 -
User is not logged in
r= [{'subcategories': '[Android,YouTube] ', 'category': 'Technology', 'id': 1}, {'subcategories': None, 'category': 'Docs Required', 'id': 2}]
Sample answers= []
127.0.0.1 - - [15/Jul/2017 20:31:19] "GET / HTTP/1.1" 200 -
FORM ===========  <__main__.RegistrationForm object at 0x7fa6d4b585f8>  


GET
127.0.0.1 - - [15/Jul/2017 20:31:22] "GET /register HTTP/1.1" 200 -
FORM ===========  <__main__.RegistrationForm object at 0x7fa6d4b118d0>  


POST
Read username chomu inside register endpoint successfully.
r for register======= {'hasura_roles': ['user'], 'auth_token': 'ij15s0fb71yjrsyaebfqo52tsem5qen1', 'hasura_id': 6}
http://data.c100.hasura.me/v1/query {'type': 'insert', 'args': {'objects': [{'email': 'sanchit@gmail.com', 'username': 'chomu', 'name': 'sanchit'}], 'table': 'profile'}}
r======= {'affected_rows': 1}
127.0.0.1 - - [15/Jul/2017 20:31:53] "POST /register HTTP/1.1" 302 -
FORM FOR LOGIN ENDPOINT IS  <__main__.LoginForm object at 0x7fa6d4b11358>
127.0.0.1 - - [15/Jul/2017 20:31:53] "GET /login HTTP/1.1" 200 -
sanchit123
{'password': 'sanchit123', 'username': 'chomu'}
http://auth.c100.hasura.me/login
{'Content-Type': 'application/json'}
r inside try===== {'hasura_roles': ['user'], 'auth_token': 'a718y18aoug0b22hh31bz56b8rghwd5l', 'hasura_id': 6}
{'type': 'update', 'args': {'$set': {'uid': 6}, 'returning': ['*'], 'table': 'profile', 'where': {'username': 'chomu'}}}
{'Content-Type': 'application/json', 'Authorization': 'Bearer a718y18aoug0b22hh31bz56b8rghwd5l'}
http://data.c100.hasura.me/v1/query
r======= {'path': '$.args.$set', 'error': 'role "user" does not have permission to update column "uid"'}
Redirecting...
127.0.0.1 - - [15/Jul/2017 20:32:04] "POST /login HTTP/1.1" 302 -
True a718y18aoug0b22hh31bz56b8rghwd5l Bearer a718y18aoug0b22hh31bz56b8rghwd5l
r= [{'subcategories': '[Android,YouTube] ', 'category': 'Technology', 'id': 1}, {'subcategories': None, 'category': 'Docs Required', 'id': 2}]
Sample answers= []
127.0.0.1 - - [15/Jul/2017 20:32:04] "GET / HTTP/1.1" 200 -
chomu
http://data.c100.hasura.me/v1/query
{'Content-Type': 'application/json', 'Authorization': 'Bearer a718y18aoug0b22hh31bz56b8rghwd5l'}
r===== [{'email': 'sanchit@gmail.com', 'name': 'sanchit', 'profilepic': None, 'mobile': None, 'username': 'chomu', 'id': 4}]
127.0.0.1 - - [15/Jul/2017 20:32:11] "GET /profile HTTP/1.1" 200 -
Entered qANDa endpoint
{'type': 'count', 'args': {'table': 'questions'}} http://data.c100.hasura.me/v1/query
4
[{'title': 'How to get my business\xa0online ??\xa0'}]
[{'title': 'How to save videos online on YouTube.'}]
[{'title': 'How to link my adhaar card with PAN card??'}]

 ['How to get my business\xa0online ??\xa0', 'How to save videos online on YouTube.', 'How to link my adhaar card with PAN card??'] 

127.0.0.1 - - [15/Jul/2017 20:32:28] "GET /QandA HTTP/1.1" 200 -
chomu
0
/usr/lib/python3/dist-packages/bs4/__init__.py:166: UserWarning: No parser was explicitly specified, so I'm using the best available HTML parser for this system ("lxml"). This usually isn't a problem, but if you run this code on another system, or in a different virtual environment, it may use a different parser and behave differently.

To get rid of this warning, change this:

 BeautifulSoup([your markup])

to this:

 BeautifulSoup([your markup], "lxml")

  markup_type=markup_type))

question= Why am I called chomu??? 
 category=   
 subcategory=   

request.form===== ImmutableMultiDict([('Category', ''), ('subCategory', ''), ('questa', '<p>Why am I called chomu???</p>\r\n')])


 {
  "type": "insert",
  "args": {
    "objects": [
      {
        "title": "Why am I called chomu???",
        "asked_by": "chomu",
        "question": "<p>Why am I called chomu???</p>\r\n",
        "category": "Miscellaneous"
      }
    ],
    "table": "questions"
  }
} 

<Response [200]>
