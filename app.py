import os
from flask import Flask
from flask import jsonify
from flask import render_template
from flask import request
from translate import COUNTRIES_CH_EN_DICT
from apscheduler.schedulers.background import BackgroundScheduler
import utils

app = Flask(__name__)

# 工具类，初始化参数为数据库名，数据库表名，数据库账号，数据库密码
u = utils.utils()


def crawl_daily_data():
    """
    定时任务，每天爬取一次数据
    :return:
    """
    cur_path = os.path.dirname(os.path.abspath(__file__))
    os.system("python {}".format(os.path.join(cur_path, "spider.py")))


@app.route('/')
def hello_world():
    return render_template("main.html")


@app.route('/c1')
def get_c1_data():
    """大屏中间，数字累计"""
    region = request.args.get("region")
    data = u.get_c1_data(region)
    return jsonify(
        {
            "dignose": data[0],
            "heal": data[1],
            "dead": data[2],
            "newly_add": data[3],
            "imported_case": data[4] if region == "china" else 0,
            "no_infect": data[5] if region == "china" else 0
        })


@app.route('/c2')
def get_c2_data():
    """
    大屏中国地图
    """
    region = request.args.get("region", "china")
    res = []
    data = u.get_c2_data(region)
    for key, value in data.items():
        if region == "world":
            # 事件地图数据这里需要查询一次中国的累计确诊数据加入
            data = u.get_c1_data()
            if data:
                res.append({"name": "China", "value": data[0]})
            res.append({"name": COUNTRIES_CH_EN_DICT.get(key, key), "value": value})
        else:
            res.append({"name": key, "value": value})
    return jsonify({"data": res})


@app.route('/l1')
def get_l1_data():
    """全国/全球累计趋势"""
    region = request.args.get("region")
    data = u.get_l1_data(region)

    day = data.date.tolist() if region == "china" else data.lastUpdateTime.tolist()
    dignose = data.confirm.tolist()
    heal = data.heal.tolist()
    dead = data.dead.tolist()
    return jsonify({"days": day, "dignose": dignose, "heal": heal, "dead": dead})


@app.route('/l2')
def get_l2_data():
    """全国/全球新增趋势"""
    region = request.args.get("region")
    data = u.get_l2_data(region)
    day = data.date.tolist() if region == "china" else data.lastUpdateTime.tolist()
    dignose = data.confirm.tolist() if region == "china" else data.confirmAdd.tolist()
    heal = data.heal.tolist() if region == "china" else data.healAdd.tolist()
    dead = data.dead.tolist() if region == "china" else data.deadAdd.tolist()
    return jsonify({"days": day, "dignose": dignose, "heal": heal, "dead": dead})


@app.route('/r1')
def get_r1_data():
    """全球/全国地区top5"""
    region = request.args.get("region")
    data = u.get_r1_data(region)
    keys = data.疫情地区.tolist()
    values = data.确诊.tolist()
    return jsonify({"keys": keys, "values": values})


@app.route('/r2')
def get_r2_data():
    region = request.args.get("region")
    res = []
    data = u.get_r2_data(region)
    for key, value in zip(data.eventDescription, data.eventUrl):
        res.append({"name": key, "value": value})
    return jsonify({"data": res})


if __name__ == '__main__':
    # 定时任务 ,间隔一天执行
    scheduler = BackgroundScheduler()
    scheduler.add_job(crawl_daily_data, 'interval', days=1)
    scheduler.start()
    app.run(host="0.0.0.0")
