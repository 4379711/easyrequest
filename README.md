# EasyRequest

### 创建一个工程
> EasyRequest CreateProject xxx (xxx is your project name)

### 进入工程目录
> cd xxx

### 创建一个爬虫

> EasyRequest CreateSpider xxx (xxx is your spider name)

### 启动一个爬虫
> EasyRequest RunSpider xxx (xxx is your spider name)

### 关闭一个爬虫
> 如果同一个爬虫启动多次,只会关闭最后一个启动的爬虫

> EasyRequest StopSpider xxx (xxx is your spider name)



------




## 关于配置文件的说明

- PROCESS_NUM

  - 需要开启进程数,只在linux下起作用

- CONCURRENT_REQUESTS 

  - 允许同时运行的爬虫数量
- DEFAULT_REQUEST_TIMEOUT
  
  - 每次请求的超时时间,单位是秒,超过后进行重试
- RETRY_TIMES

  - 请求失败后重新请求次数
- DEFAULT_REQUEST_VERIFY

  - 请求是否验证证书
- REQUEST_DELAY

  - 每次请求需要等待多久

- DEFAULT_REQUEST_HEADERS

  - 默认请求头
- LOG_CONFIG

  - 日志配置
    - LOG_PATH
      - 日志存放位置,必须使用相对位置
    - DEBUG
      - 是否记录debug日志
    - INFO
      - 是否记录info日志
    - WARNING
      - 是否记录warning日志
    - ERROR
      - 是否记录error日志,建议开启,不然神仙也帮不了你
    - INTERVAL
      - 每隔多少天进行日志压缩
- TIMER_TASK
  - 定时启动爬虫,列表格式,每个字典对应一个定时任务
    - SpiderName(字符串)
      - 
    - every(整形),默认是1
      - 启动频率
    - unit
      - 只有两种格式(字符串)
        - 'days.at("10:00")' 表示在每天10点启动,只适用于日期间隔大于天的情况
        - minutes,seconds,hours 表示每隔every个minutes/seconds/hours启动

## 关于项目文件的说明

- myproject 项目根目录

  - Apps 

    > 存放爬虫文件,每个爬虫一个文件,如果需要改名,必须把项目中相关文件全部改名
    >
    > start_urls :列表格式,存放需要请求的url
    >
    > run:返回Request类型,此处配置请求参数
    >
    > parse_response:解析响应

    - spider1.py 
    - spider2.py

  - DataPersistence 

    > 爬虫结果存储
    >
    > clean:如果需要清洗数据,可以在这里进行
    >
    > save:数据持久化

    - spider1_data_persistence.py
    - spider2_data_persistence.py

  - Middlewares 

    > 定义中间件
    >
    > RequestMiddleware:请求中间件
    >
    > ParserMiddleware:请求中间件
    >
    > before:定义请求/解析之前的操作.
    >
    > after:定义请求/解析之后的操作.
    >
    > exception:定义请求/解析发生错误时的操作

    - spider1_middleware.py
    - spider2_middleware.py

  - Models 

    > 需要存储数据的结构,每个Filed有对应类型检查功能,如StringFiled只能接受字符串类型数据,如果使用同种类型多次,name属性必须不同

    - spider1_items.py
    - spider2_items.py

  - logs 

    > 默认日志存放位置

  - manage.py 

    > 定时任务启动入口,可改为脚本启动,无需命令行启动

  - settings.py

    > 配置文件

  - spider.pid 

    > 启动爬虫后产生,结束后消失,用来记录爬虫状态,无需关心此文件




