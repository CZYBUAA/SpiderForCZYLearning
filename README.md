# SpiderForCZYLearning
保存一些学习python爬虫过程中的代码片段

dytt_spider.py:
    介绍：这是一个未完成的d爬电影天堂的最新电影列表及详情页的爬虫，目前已经获取到了详细信息，还未做数据清洗
    遗留问题： 1、为什么接收到的响应的encoding是ISO-8859-1，但以ISO-8859-1decode获取的响应页面时却乱码，反而用gbk来decode却不会产生乱码；
              2、获取到了详情页的电影的详细信息，但是这些信息是用一个<p>标签包含的，如何清洗数据还没想好
