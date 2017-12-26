crawl_anjuke_v1.311.py 说明


本脚本实现爬取安居客二手房信息。可实现将爬取下来的信息存储到本地和导入mysql数据库。
但需要注意两点：

1、ip_collecter_original_test。
是mysql数据库中的代理ip地址和port表。从该表中读取代理信息。如果不需要代理，可以修改代码即可。

2、配置和设置mysql数据库的链接信息。
hosts = 
users = 
passwords = 
databases = 