import numpy as np
import pymysql
from flask_cors import CORS
from animation_recommand import recommand, animation_vector
from joblib import dump,load
from animatin_prediction import animation_tezheng
from flask import Flask, jsonify, request

# 构建后端应用程序
server = Flask(__name__)

# 先把后端的跨域问题解决了
CORS(server,resources={r"/*": {"origins": "*"}})
# 预测薪资函数
model1 = load("animatin_prediction/model.joblib")
c = model1.intercept_
d = model1.coef_
# 定义一个提供动漫数据的后端函数
@server.route("/animations")
def animations():
    connect = pymysql.connect(host="localhost",port=3306,user="root",passwd="",db="animation",charset="utf8",cursorclass=pymysql.cursors.DictCursor)
    sql = "select * from clean_animations"
    cursor = connect.cursor()
    cursor.execute(sql)
    animations = cursor.fetchall()
    return animations

@server.route("/query_animations")
def query_animations():
    connect = pymysql.connect(host="localhost",port=3306,user="root",passwd="",db="animation",charset="utf8",cursorclass=pymysql.cursors.DictCursor)
    animation_name = request.args.get("animation_name")
    sql = f"select * from animations where animation_name like '%{animation_name}%'"
    cursor = connect.cursor()
    cursor.execute(sql)
    animations = cursor.fetchall()
    return animations

@server.route("/eduBar")
def eduBar():
    connect = pymysql.connect(host="localhost",port=3306,user="root",passwd="",db="animation",charset="utf8",cursorclass=pymysql.cursors.DictCursor)
    sql = "select * from edu_statistics"
    cursor = connect.cursor()
    cursor.execute(sql)
    datas = cursor.fetchall()
    returndatas = []
    for data in datas:
        returndatas.append({"value":data['edu_count'],"name":data['edu_range']})
    return returndatas

@server.route("/scoreBar")
def scoreBar():
    connect = pymysql.connect(host="localhost",port=3306,user="root",passwd="",db="animation",charset="utf8",cursorclass=pymysql.cursors.DictCursor)
    sql = "select * from score_statistics"
    cursor = connect.cursor()
    cursor.execute(sql)
    datas = cursor.fetchall()
    returndatas = []
    for data in datas:
        returndatas.append({"value":data['animation_count'],"name":data['score']})
    return returndatas

# 定义后端路由，用来接受前端的推荐请求
@server.route('/recommandAnimatins', methods=['GET'])
def recommandAnimations():
    # 从请求中获取参数，提供默认值
    redu = request.args.get('redu')
    score = request.args.get('score')

    # 准备参数数组
    param_array = []

    animation_tezheng.score_vec(score, param_array)
    animation_tezheng.redu_vec(redu, param_array)

    # 获取推荐的动画列表
    result = recommand.recommand(param_array)

    # 返回动画列表作为JSON响应
    return jsonify(result), 200

@server.route('/prediction')
def prediction():

    param_array = []
    # 岗位类型维度的向量值进入数组
    animation_tezheng.score_vec(request.args.get('score'),param_array)
    animation_tezheng.redu_vec(request.args.get('redu'), param_array)
    redu_vec = np.array(param_array)
    result = redu_vec.dot(d) + c
    result = round(result, 2)
    return {"result": result}


server.run()
