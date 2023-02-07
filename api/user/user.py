from flask import request, jsonify
from flask_restx import Resource, Namespace
import pymysql, requests
from database.database import Database

user = Namespace('user')
database = Database()

# 전체 테이블 보기 / DELETE
def select_all():
    sql = "SELECT * FROM user"
    rows = database.execute_all(sql)
    list = []
    for row in rows:
        list.append(row)
    print(list)
    return list    

# id와 비밀번호로 찾기 / PUT
def find_id_password(user):
    sql = "SELECT nickname FROM user WHERE id = %s AND pw = %s"
    val = (user["id"], user["password"])
    row = database.execute_all(sql, val)
    if len(row) == 0:
        return None
    else:
        return row[0]

@user.route('', methods = ['GET', 'POST', 'PUT', 'DELETE'])
class UserManagement(Resource):
    # 1. GET : 특정한 아이디의 닉네임 가져오기
    def get(self):
        # param으로 받아와서 다른 것과 문법이 좀 다름...
        id = request.args.get("id")
        pw = request.args.get("pw")
        
        # 1. 아이디가 불일치할 때 : 필요없으면 지워도 무방
        sql = "SELECT * FROM user WHERE id = %s"
        val = (id)
        row = database.execute_all(sql, val)
        if len(row) == 0:
            result = {            
                    "is_success" : False,
                    "message" : "해당 유저가 존재하지 않음"
                }
            return jsonify(result)
        
        # 2. 비밀번호가 불일치할 때  
        sql = "SELECT nickname FROM user WHERE id = %s AND pw = %s"
        val = (id, pw)
        row = database.execute_all(sql, val)
        print(row)
        if len(row) == 0:
            result = {            
                    "is_success" : False,
                    "message" : "아이디나 비밀번호 불일치"
                }
            return jsonify(result)
        # 3. nickname 찾기 성공
        else:
            return row[0]
        
    # 2. POST : 유저 추가하기. 단, 중복된 ID는 불허
    def post(self):
        try:
            user = request.get_json()
            sql = "INSERT INTO user VALUES (%s, %s, %s)"
            val = (user["id"], user["password"], user["nickname"])
            database.execute_all(sql, val)
            database.commit()
        except pymysql.err.MySQLError as e:     # id는 primary key이기 때문에 중복 추가 시 오류 발생
            result = {
                "is_success" : False,
                "message" : "이미 있는 유저"
            }
            return jsonify(result)
        
        result = {            
            "is_success" : True,
            "message" : "유저 생성 성공"
        }
        return jsonify(result)
    # 3. PUT : 유저 닉네임 변경하기
    def put(self):
        user = request.get_json()
        before = find_id_password(user)
        
        sql = "UPDATE user SET nickname = %s WHERE id = %s AND pw = %s"
        val = (user["nickname"], user["id"], user["password"])
        rows = database.execute_all(sql, val)
        database.commit()
        
        after = find_id_password(user)
        # 1. 아이디나 비밀번호가 틀릴 때
        if before == None or after == None:
            result = {            
                    "is_success" : False,
                    "message" : "아이디와 비밀번호 불일치"
                }
            return jsonify(result)
        # 2. 현재 닉네임과 같아서 변경이 되지 않을 때
        elif before["nickname"] == after["nickname"]:
            result = {            
                    "is_success" : False,
                    "message" : "현재 닉네임과 같음"
                }
            return jsonify(result)
        # 3. 성공
        else:
            result = {            
                    "is_success" : True,
                    "message" : "유저 닉네임 변경 성공"
                }
            return jsonify(result)
    # 4. DELETE : 유저 내용 삭제하기
    def delete(self):
        user = request.get_json()
        before = select_all()       # 삭제 전 테이블과 삭제 후 테이블을 비교해서 다르면 삭제 성공, 같으면 삭제 실패
        
        sql = "DELETE FROM user WHERE id = %s AND pw = %s"
        val = (user["id"], user["password"])
        database.execute_all(sql, val)    
        database.commit()
        
        after = select_all()
        # 1. 실패
        if len(before) == len(after):
            result = {
                "is_success" : False,
                "message" : "아이디나 비밀번호 불일치"
            }
            return jsonify(result)
        # 2. 성공
        else:
            result = {            
                "is_success" : True,
                "message" : "유저 삭제 성공"
            }
            return jsonify(result)