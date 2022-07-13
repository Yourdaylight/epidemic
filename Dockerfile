# 基于的基础镜像
FROM python:3.8.8

# 设置app文件夹是工作目录
WORKDIR /usr/src/app

# Docker 避免每次更新代码后都重新安装依赖
# 先将依赖文件拷贝到项目中
COPY requirements.txt /usr/src/app

# 执行指令，安装依赖
RUN pip install -i https://pypi.doubanio.com/simple/ -r requirements.txt
# RUN pip install --no-cache-dir -r requirements.txt

# COPY指令和ADD指令功能和使用方式类似。只是COPY指令不会做自动解压工作。
# 拷贝项目文件和代码
COPY . /usr/src/app

# 执行命令
CMD [ "python", "/usr/src/app/app.py" ]
