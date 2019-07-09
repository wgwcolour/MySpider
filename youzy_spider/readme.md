### 代码说明

1. 结构说明

   [youzy_schoolScoreLine](https://github.com/wgwcolour/MySpider/tree/master/youzy_spider/youzy_schoolScoreLine) 是基于Scrapy的[优志愿](<https://www.youzy.cn/> )爬虫代码，入库mongodb

   `js`文件是优志愿网站的js加密代码。

   [parseAll.py](https://github.com/wgwcolour/MySpider/blob/master/youzy_spider/parseAll.py) 是解析解密数据的代码。因为数据加密较多，采集的过程中同时解析的话，速度非常慢，所以决定先采集数据入库，然后再解析数据。

2. 数据说明

   数据分为五个表：

   ```
   SchoolScoreLine：学校分数线
   MajorComparedData：专业招生对比数据
   MajorScoreLine：专业历年分数线
   Plan2019：2019年学校招生计划
   MONGO_TB5：采集过程中未采集到数据的学校入库此表
   ```

3. 使用说明

   - 爬虫代码说明

     需要安装的第三方库：

   ```
   scrapy
   sqlalchemy
   pymongo
   lxml
   ```

   ​	因爬虫运行过程中要模拟运行js加密代码，需要安装`node.js`：

   ```
   请先安装 node.js: https://nodejs.org/
   ```

   - 解析解密代码说明

     使用多线程分页读取mongodb的数据，防止一次读取太多内存占满，然后解析入sqlserver库。

     同爬虫代码一样，需要执行js进行数据解密。

     