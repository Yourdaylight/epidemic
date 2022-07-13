import traceback

import pandas as pd
import json
import pymysql
from sqlalchemy import create_engine
from conifg import CONFIG

class utils:
    def __init__(self):
        config = CONFIG
        self.db_name = config["db_name"]
        self.user = config["user"]
        self.password = config["password"]
        self.host = config["host"]
        self.port = config["port"]
        self.data = None

    def get_conn(self):
        '''

        :return:连接
        '''
        # 创建连接
        conn = pymysql.connect(host=self.host, port=self.port, user=self.user, password=self.password,
                               db=self.db_name, charset="utf8")
        cursor = conn.cursor()
        return conn, cursor

    def close_conn(self, conn, cursor):
        cursor.close()
        conn.close()

    def query(self, table_name, use_sql=None):
        """
        :param sql:
        :return:epidemic: DataFrame
        """
        # 使用pandas从数据库中读取疫情数据
        try:
            conn = create_engine('mysql://{}:{}@{}:3306/{}?charset=utf8'.format(self.user, self.password, self.host,self.db_name))
            sql = use_sql if use_sql else "select * from {}".format(table_name)
            epidemic = pd.read_sql(sql, con=conn)
            return epidemic
        except Exception as e:
            traceback.print_exc(e)
            return None

    def get_c1_data(self, region="china"):
        '''
        获取c1的四个数据：累计确诊、累计治愈、累计死亡、新增死亡
        :return:
        '''
        table_name = "china_day" if region == "china" else "world_day"
        sql = "select * from {} order by date desc limit 1".format(table_name)
        df = self.query("china_day", sql)
        confirm = int(df["confirm"][0])
        heal = int(df["heal"][0])
        dead = int(df["dead"][0])
        now_confirm = int(df["nowConfirm"][0])
        res = [confirm, heal, dead, now_confirm]
        if region == "china":
            res.append(int(df["importedCase"][0]))
            res.append(int(df["noInfectH5"][0]))

        return res

    def get_c2_data(self, region="china"):
        '''
        获取中国各省的疫情数据
        :return:
        '''
        # 将地区-确诊人数以键值对的形式保存
        dict = {}

        # 获取最新数据
        # 从数据库中获取最近一次更新的数据
        region = "china_total_epidemic" if region == "china" else "world_epidemic"
        sql = "select distinct 疫情地区,日期,确诊 from {} order by 日期".format(region)
        df = self.query(region, sql)
        for p, v in zip(df.疫情地区, df.确诊):
            dict[p] = v
        return dict

    def get_l1_data(self, region="china"):
        '''
        获取疫情期间每日累计数据
        :return:
        '''
        table_name = "%s_day" % region
        if region == "china":
            sql = "select date, confirm, heal,dead from {} order by date".format(table_name)
        else:
            sql = "select lastUpdateTime, confirm, heal,dead from {} order by lastUpdateTime".format(table_name)
        df = self.query("", sql)
        return df

    def get_l2_data(self, region="china"):
        '''
        获取疫情期间每日新增数据
        :return:
        '''
        table_name = "china_day_add" if region == "china" else "world_day"
        if region == "china":
            sql = "select date, confirm,heal,dead from {} order by date".format(table_name)
        else:
            sql = "select lastUpdateTime, confirmAdd, healAdd,deadAdd from {} order by lastUpdateTime".format(table_name)
        df = self.query("", sql)
        return df

    def get_r1_data(self, region="china"):
        '''
        获取确诊人数最多的省份
        :return:
        '''
        region = "china_total_epidemic" if region == "china" else "world_epidemic"
        sql = "select 疫情地区,确诊 from {} order by 日期 desc,确诊 desc limit 10".format(region)
        df = self.query("", sql)
        return df

    def get_r2_data(self, region="china"):
        '''
        获取最新的疫情新闻数据
        :return:
        '''
        table_name = "%s_news" % region
        sql = "select eventDescription, eventUrl from {table_name} order by eventTime desc".format(table_name=table_name)
        df = self.query(region, sql)
        df = df.drop_duplicates()
        return df[:15]


if __name__ == "__main__":
    u = utils()

    u.get_c1_data()
