pip freeze >  packegas.txt
pip install -r  packages.txt  

# scrapy使用指南
## 1.虚拟环境配置
### 安装虚拟环境相关的包
+ ***pip install virtualenv***
+ ***pip install virtualenvwrapper-win***
### 使用豆瓣源
+ ***https://pypi.douban.com/simple***
### 查看虚拟环境
+ ***workon***
### 配置虚拟环境默认路径
+ 环境变量中新建<u>***WORKON_HOME***</u>
+ 输入默认环境<u>***E:\ENVS***</u>
### 创建删除使用虚拟环境
+ 创建虚拟环境：***mkvirtualenv***
+ 删除虚拟环境：***rmvirtualenv***
+ 使用虚拟环境：***workon***
## 2.使用安装scrapy
### 安装scrapy
+ pip install ***scrapy***`
### 创建scrapy项目
```
scrapy startproject 项目名称
```
### 创建scrapy工程
+ 需要在项目根目录下
```
    scrapy genspider 【工程名】 【爬取域名】
```
## 3.使用Pycharm/scrapy shell进行Debug
### 使用Pycharm进行测试
+ 新建main函数，引入相关的包
+ 获取项目路径
+ 执行启动scrapy
```
    from scrapy.cmdline import execute
    import sys
    
    //引入项目根路径
    sys.path.append(os.path.dirname(os.path.abspath(__file__)))
    execute(['scrapy','crawl','项目名称'])
```
+ 注：使用前需要在setting中关闭ROBOTSTXT协议
```
//setting中设置
ROBOTSTXT_OBEY=False
```
+ 注：需要提前安装pypiwin32的包
```
pip install pypiwin32
```
### 使用scrapy shell进行测试
+ 进入命令行，workon到指定虚拟环境，通过**scrapy shell 测试地址**进行测试
```
scrapy shell https://blog.jobbole.com/
```
## 4.Xpath的使用
### Xpath语法实例

| 表达式 | 说明  |
| --- | --- |
| article | 选取所有article元素的所有子节点 |
| /article | 选取根元素article |
| article/a | 选组所有属于article的子元素的a元素 |
| //div | 选取所有div子元素（无论出现在文档任何地方） |
| article//div | 选取所有属于article元素的后代的div元素， 不管它出现在article之下的任何位置 |
| //@class | 选取所有名为class的属性 |
| /article/div[1] | 选取属于article子元素的第一个div元素 |
| /article/div[last()] | 选取属于article子元素的最后一个div元素 |
| /article/div[last()-1] | 选取属于article子元素的倒数第二个div元素 |
| //div[@lang] | 选取所有有lang属性的div元素 |
| //div[@lang='eng'] | 选取所有lang属性为eng的div元素 |
| /div/* | 选取属于div元素的所有子节点 |
| //* | 选取所有元素 |
| //div[@* ]  | 选取所有带属性的title元素 |
| /div/a&#124;//div/p | 选取所有div元素的a和p元素  |
| //span&#124; //ul | 选取文档中所有的span和ul元素 |
| article/div/p&#124; //span | 选取所有属于article元素的div元素的P元素以及文档中所有SPAN元素 |

## 5.CSS选择器
### CSS选择器样例

| 表达式 | 说明 |
| --- | --- |
| * | 所有节点 |
| #container | id为container的节点 |
| .container | 所有class包含container的节点 |
| li a | 所有li下的所有a节点 |
| ul+p | ul后面第一个p元素 |
| div#container>ul | id为container的div的第一个ul子元素 |
| ul~p | 选取与ul相邻的所有p元素 |
| a[title] | 选取所有有title属性的a元素 |
| a[href="http://jobbole.com"] | 选取所有href属性为jobbole.com值得a元素 |
| a[href*="jobble"] | 选取所有href属性包含jobbole的a元素 |
| a[href^="http"] | 选取所有href属性以http开头的a元素 |
| a[href$=".jpg"] | 选取所有href属性以.jpg结尾的a元素 |
| input[type=radio]:checked | 选取选中的radio元素 |
| div:not(#container) | 选取所有id非container的div属性 |
| li:nth-child(3) | 选取第三个li元素 |
| tr:nth-child(2n) | 选取第偶数个tr |

## 6.爬取伯乐在线文章
### 1.建立项目
```
scrapy jobbole www.jobbole.com
scrapy genspider jobbole
```
### 2.主程序中设置debug的main
```
from scrapy.cmdline import execute import sys //引入项目根路径 sys.path.append(os.path.dirname(os.path.abspath(__file__))) 
execute(['scrapy','crawl','jobbole'])
```
##### 爬虫主程序生成的代码为
```
import scrapy
class JobboleSpider(scrapy.Spider): 
    name = 'jobbole'   
    allowed_domains = ['jobbole.com']    //允许域名
    start_urls = ['http://blog.jobbole.com']    //开始网址
    
    def parse(self, response): 
        pass       

```
### 3.简单的css选择器使用
+ 根据页面信息，使用简单的response的css方法，选取目标内容，
```
title = response.css('.entry-header h1::text').extract_first('')

create_date = response.css('.entry-meta-hide-on-mobile::text').extract_first('').strip().replace(' ·', '')

praise_nums = response.css('.vote-post-up h10::text').extract_first('')

fav_nums = response.css('.bookmark-btn::text').extract_first('')

match_num = re.match('.*?(\d+).*?', fav_nums)

if match_num:
    fav_nums = match_num.group(1)
    
comment_nums = response.css("a[href='#article-comment'] span::text").extract_first('')
match_num = re.match('.*?(\d+).*?', comment_nums)

if match_num:    
    comment_nums = match_num.group(1)
    
content = response.css('.entry').extract_first('')

tags = response.css('.entry-meta-hide-on-mobile a')
tag_list = []
for tag in tags:    
    tag = tag.css('::text').extract_first('')   
        if '评论' not in tag: 
            tag_list.append(tag)
```
### 4.使用scrapy进行多线程多页面爬取
+ parse：由于有的页面，给的url是相对路径，为了保证路径的一直性，我们使用urllib库中的parse对url进行拼接，保证路径为带有域名的绝对路径
```
parse.urljoin(response.url,url)
```
+ 获取url后，通过yiled关键字和Request方法中的callback函数，进行下载，解析
```
yiled Request(url=post_url,callback=self.parse_detail)
```
+ 例：三步对伯乐在线进行多页面爬取
1. 提取详情页url
2. 将每页url页面下载后，交给scrapy进行解析
3. 获取下一页url，下载后重新交给parse函数循环开始
### 5.Items类的使用
##### Items类的作用是将非结构化的数据结构化，类似字典的方式储存爬取到的数据，Item中字段的类型为`Item.Field()`
+ 在Item类中创建jobbole文章的item类
```
class ArticleItem(scrapy.Item): 
    title = scrapy.Field()
    create_date = scrapy.Field() 
    url = scrapy.Field()
    url_obj_id = scrapy.Field()  
    front_image_url = scrapy.Field() 
    front_image_path = scrapy.Field() 
    praise_nums = scrapy.Field() 
    comment_nums = scrapy.Field()
    fav_nums = scrapy.Field()   
    tags = scrapy.Field()   
    content = scrapy.Field()


```
#### 加餐1：Request通过meta传递参数
+ 再Request将url传递给parse_detail解析时，通过meta传递从第一页url获取的数据
+ 例：将封面图url传递到Requests的meta中
+ meta是个字典的形式，通过response.meta.get方式获取
```
yield Request(url=parse.urljoin(response.url, post_url), meta={'front_image_url':parse.urljoin(response.url, front_image_url)},callback=self.parse_detail)

articleItem['front_image_url'] = response.meta.get('front_img_url', '')
```

#### 加餐2：使用MD5格式化url
+ 创建utils包，新建common.py，并写通用的get_md5()方法
+ 注：因为python3中的字符串都是Unicode，需要将字符类型修改为``utf-8``
```
def get_md5(url):  
    if isinstance(url, str):     
        url = url.encode('utf-8')  
    m = hashlib.md5() 
    m.update(url)   
    return m.hexdigest()
```
### 6.pipeline的使用
##### pipeline是scrapy处理类的关键，item通过pipeline进行存储等操作
#### a.图片下载
##### 使用自带的ImagePipeline进行图片下载
1. 建立image下载目录
2. 配置setting文件
```
import os
//item中图片路径url
IMAGES_URLS_FIELD = 'front_image_url'
image_path = os.path.abspath(os.path.dirname(__file__))
IMAGES_STORE = os.path.join(image_path, 'images')
```
3. 自定义pipeline下载读取图片下载路径
```
class ArticlePipeline(ImagesPipeline): 
    def item_completed(self, results, item, info):  
        for ok, value in results:       
            image_file_path = value['path'] 
            item['front_image_path'] = image_file_path
            # 一定要将item返回回去    
            return item


```
### 7.数据存储
#### a.json方式
1. 使用文件codecs方式
    + 使用codecs打开文件，并且设置encoding为utf-8 
    ```
    def __init__(self):   
        self.json_file = codecs.open('AtricleJson.json', 'w', encoding='UTF-8')
    ```
    + 将item转为json，并写入文件
    ```
    def process_item(self, item, spider): 
        lines = json.dumps(dict(item), ensure_ascii=False) + '\n' 
        self.json_file.write(lines) 
        return item
    ```
    + 在close_spider方法中，关闭文件流
    ```
    def close_spider(self, spider): 
        print('spiderclose')  
        self.json_file.close()
    ```
2. 使用exporter方式
    + 使用open方法打开文件，并导入JsonItemExporter包
    + __init__方法初始化文件，export
    + process_item方法中，利用export的export_item方法，将数据导出到指定JSON文件中
    + 在close_spider方法中关闭文件流
 ```
 def __init__(self): 
    self.file = open('ArticlaExporterJson.json', 'wb')  
    self.exporter = JsonItemExporter(self.file, encoding='utf-8', ensure_ascii=False)    
    self.exporter.start_exporting()
    
def close_spider(self, spider):  
    self.file.close()
    
def process_item(self, item, spider): 
    self.exporter.export_item(item)    
    return item
 ```
#### b.数据库方式
1. 普通mysql存储方式
+ 安装mysql-client包``如果不能安装，需要在pypi中下载mysql-client相关库``
```
    pip instll mysql-client
```
+ 导入MysqlDB库
+ 在__init__函数中初始化数据库连接和cursor
+ 在process_item函数中进行item的插入``注意excute后需要commit``
+ 在close_spider后关闭conn连接
+ ``注：如果出现1366, "Incorrect string value: '\\xF0\\x9F\\x8C\\xB0\\xE3\\x80...' for column 'content' at row 1")报错，需要将数据库调整为的数据集调整utf-8mb4`，同时将数据库以及表的charset设置为ubf8mb4``
```
def __init__(self):
    self.conn = MySQLdb.connect('主机', '用户名', '密码', '表',charset='utf8mb4', use_unicode=True) 
    self.cursor = self.conn.cursor()
    
def process_item(self, item, spider): 
    insert_sql = '''
    insert into jobbole_article(title,...)  values (%s,%s)
    '''    
    self.cursor.execute(insert_sql, ( item['title'], ','.join(item['tags'])))
    self.conn.commit()
    
def close_spider(self, spider):
    self.conn.close()
```
2. 异步插入mysql数据库方式---``连接池``
+ 如果插入速度比scrap解析慢的话就会出现阻塞
+ 在setting中设置数据库连接相关参数----``不必要为了增加可修改性``
```
MYSQL_HOST = 'localhost'
MYSQL_DBNAME = 'jobbole_spider'
MYSQL_USER = 'root'
MYSQL_PWD = '50122294'
```
+ 在pipeline中，使用内部类方法，使用from_settings方法读取setting中相关参数
+ 导入twisted中的adbapi方法，MySQLdb中的cursors
+ 自定义数据库连接参数，注意需要增加``cursorclass=MySQLdb.cursors.DictCursor``
+ 使用adbapi的ConnectionPool连接池方法，参数（数据库驱动名称，数据库连接参数）
```
@classmethod
def from_settings(cls, settings):
    db_params = dict( host=settings['MYSQL_HOST'],
                    db=settings['MYSQL_DBNAME'], 
                    user=settings['MYSQL_USER'], 
                    passwd=settings['MYSQL_PWD'],
                    charset='utf8mb4',    
                    use_unicode=True, 
                    cursorclass=MySQLdb.cursors.DictCursor )
     dbpool = adbapi.ConnectionPool('MySQLdb', **db_params)    return cls(dbpool)
```
+ 在__init__方法中初始化dbpool
```
def __init__(self, dbpool): 
    self.dbpool = dbpool
```
+ 在process_item方法中指定数据插入以及异常处理方法----``runInteraction--插入回调函数，addErrback--异常错误函数``
```
def process_item(self, item, spider): 
    # 使用twisted将mysql变成异步操作   
    query = self.dbpool.runInteraction(self.do_insert, item) 
    query.addErrback(self.handle_error, item, spider)
```
+ 插入函数和同步方式一致，但是不需要commit
+ 异常处理函数可以输出failure，同时可以输出item
```
#数据插入函数
def do_insert(self, item, spider):  
    insert_sql = ''' 
    insert into jobbole_article(title,...) values (%s,%s)
    '''    
    self.cursor.execute(insert_sql, ( item['title'], ','.join(item['tags'])))
    
#错误处理函数
def handle_error(self, failure, item, spider):  
    print(failure)
```
### ``后续可以使用Djangoitem进行数据库管理``
#### ``github地址：https://github.com/scrapy-plugins/scrapy-djangoitem``

### 8.使用Itemloader
#### 1.Itemloader
+ 三个方法``add_css,,add_value,add_xpath``
    + add_css(),通过css获取为item读取数据
    + add_value() 直接为item字段赋值
    + add_xpath() 通过xpath获取为item读取数据
```
item_loader.add_css('title', '.entry-header h1::text')
item_loader.add_css('create_date', '.entry-meta-hide-on-mobile::text')
item_loader.add_value('url', response.url)
item_loader.add_value('url_obj_id', get_md5(response.url)
)item_loader.add_value('front_image_url', [front_image_url])
item_loader.add_css('praise_nums', '.vote-post-up h10::text')
item_loader.add_css('comment_nums', "a[href='#article-comment'] span::text")
tem_loader.add_css('fav_nums', '.bookmark-btn::text')
item_loader.add_css('tags', '.entry-meta-hide-on-mobile a::text')
item_loader.add_css('content', '.entry')
articleItem = item_loader.load_item()
```
+ 在item中，通过process方式，对数据进行处理
    +  ``input_processor`` 输入时数据处理
    + ``output_processor`` 输出时数据处理
    + 处理时，通过``MapCompose``方法，指定处理函数
+ 自定义ItemLoader，设置默认处理方法,使用前导入ItemLoader类
```
from scrapy.loader import ItemLoder 
class ArticleItemLoader(ItemLoader): 
    default_output_processor = TakeFirst()
```
+ scrapy.processor中自带的TakeFirst方法，Join方法，MapCompose方法
    + MappCompose方法，指定回调函数
    + TakeFirst方法，输出时，选择list中第一个
    + Join方法，对list中的数据，通过Join方法拼接
```
def get_datetime(value):  
    value = value.strip().replace('·', '').strip() 
    try:      
        create_date = datetime.strptime(value, '%Y%M%D').date()   
    except Exception as e:    
        create_date = datetime.now().date()   
    return create_date
    
    
def image_filter(value):
    return value
    
    
def num_filter(value):  
    pattern = r'.*?(\d+).*?' 
    match_re = re.match(pattern, value)  
    if match_re:   
        nums = int(match_re.group(1))  
    else:  
        nums = 0  
    return nums
    
    
def tag_filter(value):  
    if '评论' in value:   
        return ''
    else: 
        return value
        
        
class ArticleItem(scrapy.Item):
    title = scrapy.Field()  
    create_date = scrapy.Field( 
        input_processor=MapCompose(get_datetime)
    )
    url = scrapy.Field()
    url_obj_id = scrapy.Field()  
    front_image_url = scrapy.Field(
        output_processor=MapCompose(image_filter) 
    )   
    front_image_path = scrapy.Field()
    praise_nums = scrapy.Field(
        input_processor=MapCompose(num_filter)   
    )
    comment_nums = scrapy.Field( 
        input_processor=MapCompose(num_filter) 
    )
    fav_nums = scrapy.Field(   
        input_processor=MapCompose(num_filter)    
    )
    tags = scrapy.Field(     
        input_processor=MapCompose(tag_filter),
        output_processor=Join(',') 
    )
    content = scrapy.Field()


```
