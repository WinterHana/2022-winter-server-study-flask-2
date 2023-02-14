from flask import Flask, request, jsonify, json, Response, make_response
from flask_restx import Resource, Namespace
import pymysql
from database.database import Database

user = Namespace('user')
database = Database()

# 에러 코드와 메시지 전달
def errer_message(message):
    '''
    json_dic = json.dumps({
        "is_success" : False,
        "message" : message
    })
    
    result = Response(json_dic, mimetype = "application/json", status = 400)
    return make_response(result)
    '''
    json_dic = {
        "is_success" : False,
        "message" : message
    }
    return jsonify(json_dic)

# 성공 시 메시지 전달
def success_message(message):
    json_dic = {
        "is_success" : True,
        "message" : message
    }
    return jsonify(json_dic)

@user.route('', methods = ['POST'])
class UserManagement(Resource):
    def post(self):
        user = request.get_json()
        
        sql = "SELECT * FROM user WHERE id = %s AND pw = %s"
        val = (user["id"], user["password"])
        row = database.execute_all(sql, val)
    
        if len(row) == 0:
            # return errer_message("Login Failed")
            return "Login Failed"

        else:
            # return success_message("Login Success")
            return "Login Success"