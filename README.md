# Aurora 2.0

### 目录功能
> * **build** 用于存放pip相关引用，dockerfile 等打包相关的内容
> * **pkg**            项目根目录
> * **blueprints**      蓝图（视图）
> * **cli**             命令行操作接口
> * **model**           数据库定义
> * **query**           SQL 操作接口

## Installation

```shell
$ git clone https://github.com/GKAurora/Aurora2.0-WebAPI.git
$ cd Aurora2.0-WebAPI
```

创建&&安装虚拟环境: with venv/virtualenv + pip:
```shell
$ python -m venv env  # use `virtualenv env` for Python2, use `python3 ...` for Python3 on Linux & macOS
$ .\env\Scripts\activate  # use `env\Scripts\activate` on Windows
$ source env/bin/activate  # use `env\Scripts\activate` on Linux
$ pip install -r requirements.txt # or use pip3 on Linux
```

运行api server:
```
$ flask initdb
$ flask run
* Running on http://127.0.0.1:5000/ # http://127.0.0.1:5000/docs is api docs
```

如果执行`pip install`命令安装依赖耗时太长，你可以考虑使用国内的PyPI镜像源，比如：
```
$ pip install -i https://mirrors.aliyun.com/pypi/simple -r requirements.txt
```

## 项目结构
```shell
├── README.md
├── build
│   ├── Dockerfile
│   └── README.md
├── demo
│   ├── ClassStartMaginc.py
│   └── sysMessage.py
├── pkg
│   ├── __init__.py
│   ├── blueprints
│   │   ├── auth.py
│   │   ├── sdn.py
│   │   ├── server.py
│   │   ├── test
│   │   │   └── __init__.py
│   │   └── users.py
│   ├── crawlers
│   │   ├── base.py
│   │   ├── setting.py
│   │   ├── system
│   │   │   ├── get_all.py
│   │   │   ├── get_single.py
│   │   │   └── speeds.py
│   │   └── users
│   │       ├── get_err.py
│   │       ├── get_floor_device.py
│   │       ├── get_sites.py
│   │       ├── get_token.py
│   │       ├── get_user_location.py
│   │       ├── get_users.py
│   │       └── heatmap.py
│   ├── exceptions
│   │   ├── reqerror.py
│   │   └── token.py
│   ├── extensions.py
│   ├── models
│   │   └── __init__.py
│   ├── schemas
│   │   ├── __init__.py
│   │   ├── auth.py
│   │   ├── auth_test.py
│   │   └── sdn.py
│   ├── setting
│   │   ├── __init__.py
│   │   └── setting.py
│   ├── settings.py
│   ├── storages
│   │   └── redis.py
│   ├── util
│   │   ├── __init__.py
│   │   ├── stamp.py
│   │   └── time_parse.py
│   └── utils.py
├── request_demo
│   └── Python_demo.py
├── requirement.txt
└── wsgi.py
```

## License

This project is licensed under the MIT License (see the
[LICENSE](LICENSE) file for details).
