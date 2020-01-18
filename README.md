# EasyRequest 

> ##### 这是一个极易使用的异步爬虫框架



### 创建一个工程
> EasyRequest CreateProject xxx (xxx is your project name)

### 进入工程目录
> cd xxx

### <u>创建一个爬虫</u>

> EasyRequest CreateSpider xxx (xxx is your spider name)

### 启动一个爬虫
> EasyRequest RunSpider xxx (xxx is your spider name)

### 关闭一个爬虫
> EasyRequest StopSpider xxx (xxx is your spider name)



------




## 关于配置文件的说明

- CONCURRENT_REQUESTS 

  - 允许同时运行的爬虫数量
- RECORD_PID
  - 是否记录本次爬虫pid,可以通过命令行随时终止爬虫


- DEFAULT_REQUEST_TIMEOUT
  
  - 每次请求的超时时间,单位是秒,超过后进行重试
- RETRY_TIMES

  - 请求失败后重新请求次数
- DEFAULT_REQUEST_VERIFY

  - 请求是否验证证书
- REQUEST_DELAY

  - 每次请求需要等待多久
- ~~PROCESS_NUM~~(已弃用)

  - ~~开启进程数量~~


- ~~PER_REQUEST_MIN_TIME~~(已弃用)

  - ~~每次请求最少花费时间~~
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

    > 如果开启了记录pid,则会生成此文件




## 关于爬虫书写的说明

- Request()相关参数说明
  
  - is_filter:是否开启url过滤,过滤标准是url+参数,默认开启
  
  - method:请求方式,默认get
  
  - url:请求的url
  
  - data_pass:传递值到下一个callback函数
  
  - callback:下一个需要执行的函数名,默认是parse_response
  
  - proxies:设置代理
  
  - timeout:请求超时时间
  
  - headers:添加请求头
  
  - params:请求参数,多用于get
  
  - data:请求参数,字典格式,多用于post
  
  - json:请求参数,多用于post
  
    
  
- Request相关使用说明

  - 除了parse_response函数,其他所有**callback**函数**必须返回Request的实例对象**

  - callback可以使用生成器返回多次,也可返回一次

  - ```python
        for i in range(2):
            yield Request(method='GET',
                          url=self.start_urls[1],
                          data_pass='传给callback2'
                         )
    ```

    ```python
    return Request(method='GET',
                   url=self.start_urls[1],
                   data_pass='传给callback2'
                  )
    ```

    

- 中间件相关说明
  - 只有request中间件和parse中间件,通过类名很好区分
  - before:
    - 请求/解析之前需要的操作,无需返回任何值
  - after:
    - 请求/解析成功之后需要的操作,无需返回任何值,如果没有执行成功,则不执行,自动进入exception中间件
  - exception:
    - request中:无需返回任何值
    - parser中:
      - 返回None,放弃本次解析数据
      - 返回item,则会继续执行,存储这个item
- 数据存储相关说明
  - clean:
    - 如果需要清洗数据,可以在这里进行
    - **必须返回一个items.**
  - save:
    - 存储的相关逻辑写在这里