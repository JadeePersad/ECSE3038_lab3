from flask import Flask,jsonify, request, json
from bson.json_util import dumps
from json import loads
import os
from dotenv import load_dotenv
from flask_pymongo import PyMongo
from marshmallow import Schema, fields, ValidationError
import datetime

app=Flask(__name__)

load_dotenv()

app.config["MONGO_URI"]=os.getenv("MONGO_CONNECTION_STRING")
mongo = PyMongo(app)

class TankS(Schema):
    location = fields.String(required=True)
    lat = fields.Float(required=True)
    long = fields.Float(required=True)
    percentage_full = fields.Integer(required=True)

user={}
time=datetime.datetime.now()
array1=[]
id=0
@app.route('/', methods=['GET'])

@app.route('/profile',methods=["POST"])
def profile():
    
    global time
    time =datetime.datetime.now()
    global user
    user = {
        "last_updated" : time,
        "username": request.json["username"],
        "role" : request.json["role"],
        "color" : request.json["color"]
    }

    return {"data":user}

@app.route('/profile', methods=['GET'])
def profile2():
    return {"data":user}

@app.route('/profile', methods=['PATCH'])
def profile3():
    
    global time 
    time = datetime.datetime.now()

    if "username" in request.json:
      user["username"] = request.json["username"]

    if "role" in request.json:
      user["role"] = request.json["role"]

    if "color" in request.json:
      user["color"] = request.json["color"]
      
    return {"data": user}

@app.route('/data', methods=['GET'])    
def tankr2():
    T = mongo.db.lab3tank.find()
    return jsonify(loads(dumps(T)))

    
@app.route('/data',methods=["POST"])
def data():
    
    try:
        tankr=TankS().load(request.json)
        idtankr = mongo.db.lab3tank.insert_one(tankr).inserted_id
        tank = mongo.db.lab3tank.find_one(idtankr)
        return loads(dumps(tank)) 
    except ValidationError as ve:
        return ve.messages, 404
   

@app.route('/data/<ObjectId:id>', methods=['PATCH'])
def tankr3(id):  

    mongo.db.lab3tank.update_one({"_id":id},{"$set":request.json})
    tank = mongo.db.lab3tank.find_one(id)
    return loads(dumps(tank))


@app.route('/data/<ObjectId:id>', methods=["DELETE"])
def tankr4(id):
 
    result = mongo.db.lab3tank.delete_one({"_id":id})
 
    if result.deleted_count == 1:
        return {"success": True}
   
    else:
        return {"success": False }, 404


if __name__ == "__main__":
    app.run(debug=True,
    port=3000,
    host="0.0.0.0"
    )