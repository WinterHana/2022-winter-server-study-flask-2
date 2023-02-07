import pymysql

db = pymysql.connect(host='15.164.250.155', port=3306, user='Winter_Hana', password='980920', db='serverStudy', charset='utf8')

print(db)