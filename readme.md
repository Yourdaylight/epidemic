# python 疫情大数据可视化
## 启动方式
1、打开config.py文件，配置mysql数据库的用户名和密码。db_name换成一个数据库中存在的数据库名称，
或者去自己本地数据库建立一个名称叫myspider的数据库。
2、运行app.py。运行完成后浏览器输入http://127.0.0.1访问界面
## 要求
基于python的新冠疫情数据的采集与可视化展示
①从腾讯新闻网获取中国、全球的疫情数据
②对获取的数据进行数据清洗与数据解析
③将获取的全国各省与全球各国的数据导出Excel表进行查看，
 并将获取的中国各省各地的现有确诊，累计确诊，当日确诊，无症状感染者，境外输入，累计死亡的数据以及
 全球各国的现有确诊，累计确诊，累计治愈，累计死亡的数据存储在mysql数据库中
④利用vue、flask框架对数据进行可视化的展示，可以实现两个页面，中国页面与全球页面，
在中国页面展示出累计确诊、现有确诊、累计死亡、无症状感染者、境外输入的人数，
在中国地图上点击某省可以查看现有确诊人数，在中国页面展示出全国现有确诊趋势的折线图，全国疫情新增趋势的折线图，全国疫情各累计趋势的折线图，治愈率与病死率趋势图，
以及腾讯新闻百度新闻中相关的每天的疫情热点新闻，点击某相关热点新闻可以进行查看相关文章，展示国内现有确诊前十各省确诊数据的排行。
在全球页面点击全球地图可以查看各国现有确诊人数，在国外页面显示现有确诊、累计确诊、累计治愈、累计死亡的人数，展示国外目前确诊的前十排行国家，全球现有确诊的趋势图，累计确诊的趋势图。