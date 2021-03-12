from flask import Flask, request,jsonify,Response
import mysql.connector
from passlib.hash import sha256_crypt

app = Flask(__name__)

mydb = mysql.connector.connect(
   host = "localhost",
   user = "book",
   password = "book",
   database = "mydb"
)

mycursor = mydb.cursor()

def login(givenEmail,Enterpwd):
   getpwd = "select password from user where email = '{}'".format(str(givenEmail))
   mycursor.execute(getpwd)
   result = mycursor.fetchone() # result is a tuple ex = ('135463',)
   givenpwd = sha256_crypt.encrypt(Enterpwd)
   existpwd = sha256_crypt.encrypt(result)
   loged = sha256_crypt.verify(result,Enterpwd)
   if loged == True:
      return Response(status=200)
   else:
      return Response(status=404)



@app.route('/users/<emailid>',methods = ['GET'])
def CheckEmail(emailid):
   check = "SELECT * FROM user WHERE email = '{}'".format(str(emailid))
   mycursor.execute(check)
   myresult = mycursor.fetchall()
   if len(myresult) == 0:
      return Response(status=202)
   else:
      return Response(status=409)

def register(userID,name,email,longitude,latitude,password,role,active):
   signup = 'INSERT INTO user VALUES ({},"{}","{}",{},{},"{}","{}",{})'.format(str(userID),name,email,longitude,latitude,password,role,active)
   mycursor.execute(signup)
   mydb.commit()

@app.route('/users/<int:id>',methods = ['DELETE'])
def deleteuser(id):
   mycursor.execute("DELETE FROM user where userID = {}").format(id)
   mydb.commit()
   

@app.route('/users_id/<id>',methods = ['GET'])
def get_userid(id):
   query = 'select * from user where userID = {}'.format(id)
   mycursor.execute(query)
   data = mycursor.fetchone()
   mydb.commit()
   return "ok"
   

@app.route('/users', methods = ['POST'])
def user():
   userID = int(request.json['userID'])
   name = request.json['name']
   email = request.json['email']
   longitude = request.json['longitude']
   latitude = request.json['latitude']
   password = request.json['password']
   role = request.json['role']
   active = request.json['active']
   register(userID,name,email,longitude,latitude,password,role,active)
   
   return Response(status=201)

if __name__ == '__main__':
   app.run(debug = True)