# -*- coding: utf-8 -*-
# @Time    :2021/7/30 23:34
# @Author  :lzh
# @File    : new_spider.py
# @Software: PyCharm
import datetime

import pandas as pd
import requests
from sqlalchemy import create_engine

from translate import COUNTRIES_CH_EN_DICT
from conifg import CONFIG

def traslate(word):
    '''
    将世界各国的中文名转化为英文
    '''
    return COUNTRIES_CH_EN_DICT.get(word, "未知地区")


# %%
def save_data(df, table_name, if_exists="append", need_translate=False):
    if need_translate:
        df['name'] = df['疫情地区'].apply(traslate)
    conn = create_engine(f'mysql://{CONFIG["user"]}:{CONFIG["password"]}@{CONFIG["host"]}:3306/{CONFIG["db_name"]}?charset=utf8')
    pd.io.sql.to_sql(df, table_name, con=conn, if_exists=if_exists, index=None)


def crawl_china_data():
    url = "https://api.inews.qq.com/newsqa/v1/query/inner/publish/modules/list?modules=chinaDayList,chinaDayAddList,nowConfirmStatis,provinceCompare"
    data = requests.get(url)
    data = data.json().get("data", {})
    provinceCompare = data.get("provinceCompare")  # 每个省份的总数据（每日更新）
    chinaDayList = data.get("chinaDayList")  # 最近一个月的全国疫情的总数据
    chinaDayAddList = data.get("chinaDayAddList")  # 最近一个月的全国疫情的新增数据
    return provinceCompare, chinaDayList, chinaDayAddList

# %%
def crawl_countries_data():
    url = "https://api.inews.qq.com/newsqa/v1/automation/modules/list?modules=FAutoCountryConfirmAdd,WomWorld,WomAboard"
    data = requests.get(url)
    data = data.json().get("data")
    foreignList = data.get("WomAboard", [])
    foreignTotal = data.get("WomWorld",{})
    df = pd.DataFrame(foreignTotal,index=[0])
    save_data(df,"world_day")
    return foreignList


def parse_china_daily_data(day_list, day_add_list):
    """
    解析每日新增、每日累计数据
    :param api_rtn_data:
    :return:
    """
    day_df = pd.DataFrame(day_list)
    day_df["date"] = pd.to_datetime(day_df["y"] + "." + day_df["date"])
    day_add_df = pd.DataFrame(day_add_list)
    day_add_df["date"] = pd.to_datetime(day_add_df["y"] + "." + day_add_df["date"])
    save_data(day_df, "china_day", "append")
    save_data(day_add_df, "china_day_add", "append")


def parse_countries_total_data(api_rtn_data):
    """
    解析每个国家的新增数据
    :param api_rtn_data:
    :return:
    """
    dates = []
    countries = []
    dignose = []
    heal = []
    dead = []
    add = []
    for country in api_rtn_data:
        countries.append(country.get("name", ""))
        month, day = country.get("date").split(".")
        month = month if "0" not in month else month[-1]
        date = datetime.date(int(country.get("y")), int(month), int(day))
        dates.append(date)
        dignose.append(country.get("confirm", 0))
        heal.append(country.get("heal", 0))
        dead.append(country.get("dead", 0))
        add.append(country.get("confirmAdd", 0))
    df = pd.DataFrame({
        "疫情地区": countries,
        "日期": dates,
        "确诊": dignose,
        "治愈": heal,
        "死亡": dead,
        "新增死亡": add
    })
    df.to_csv("world_epidemic.csv",encoding="gbk")
    save_data(df, "world_epidemic", "replace", True)
    return df


def parse_provinces_total_data(api_rtn_data):
    dates = []
    provinces = []
    dignose = []
    heal = []
    dead = []
    add = []
    for province, total_data in api_rtn_data.items():
        provinces.append(province)
        date = datetime.datetime.now()
        dates.append(date)
        dignose.append(total_data.get("nowConfirm", 0))
        heal.append(total_data.get("heal", 0))
        dead.append(total_data.get("dead", 0))
        add.append(total_data.get("confirmAdd", 0))
    df = pd.DataFrame({
        "疫情地区": provinces,
        "日期": dates,
        "确诊": dignose,
        "治愈": heal,
        "死亡": dead,
        "新增死亡": add
    })
    df.to_csv("china_total_epidemic.csv",encoding="gbk")
    save_data(df, 'china_total_epidemic',"replace")
    return df

def crawl_news():
    def __get_data(region_type, table_name):
        url = "https://opendata.baidu.com/data/inner?tn=reserved_all_res_tn&dspName=iphone&from_sf=1&dsp=iphone&resource_id=28565&alr=1&query={}".format(region_type)
        news = requests.get(url).json()
        if isinstance(news,dict) and news.get("Result",[]):
            data = news.get("Result")[0].get("items_v2")[0].get("aladdin_res").get("DisplayData").get("result").get("items")
            data = pd.DataFrame(data)
            save_data(data, table_name)
    __get_data("国内新型肺炎最新动态","china_news")
    __get_data("国外新型肺炎最新动态","world_news")


# %%
def main():
    crawl_news()
    provinceCompare, chinaDayList, chinaDayAddList = crawl_china_data()
    parse_china_daily_data(chinaDayList, chinaDayAddList)
    parse_provinces_total_data(provinceCompare)
    foreignList = crawl_countries_data()
    parse_countries_total_data(foreignList)



if __name__ == '__main__':
    main()
    print("爬取完成")
    # url = "https://news.qq.com/zt2020/page/feiyan.htm#/"
    # df = pd.read_html(url)
    # table = df[2]
