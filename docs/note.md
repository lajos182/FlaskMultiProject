# Note

# spider
- 爬虫
    - 数据获取
        - 麻烦
    - 数据提取
    - 数据清洗

# 反馈
- 数据加密反爬
- 在服务端对数据急性特算法的加密
- 在客户端进行数据的解密
    - 浏览器还是可破解的
    - Android或IOS移动端, 破解率基本为0
    
## 钩子函数
- 面向切片编成
- 动态介入请求流程
    - before_request
    - after_request
    
## Django的请求流程
- urls -> views -> models -> views -> response
- 添加中间件
    - client -> process_request[], 逐一进行process_request
    - process_request -> urls
    - urls -> process_view[], 逐一进行process_view
    - process_view -> views
    - views -> models
    - models -> views
    - views -> response
    - response ->  process_response[], 逐一进行process_response
    
 ## 四大内置对象
 - request
 - session
 - g
    - 跨函数传度数据
    - 间接传递数据
 - config(app)
    - python  current_app
    - 一定是在项目启动之后