import requests
from bs4 import BeautifulSoup
import json
import re
import pandas
import openpyxl

unreadnewsurl1='http://api.roll.news.sina.com.cn/zt_list?channel=news&cat_1=gnxw&cat_2==gdxw1||=gatxw||=zs-pl||=mtjj&level==1||=2&show_ext=1&show_all=1&show_num=22&tag=1&format=json&page={}'


#定义获取内文评论数的函数，返回评论数
def getCommentCount(newsurl):
    newsid=newsurl.split('/')[-1].rstrip('.shtml').lstrip('/doc-i') #rstrip为删除右侧内容，lstrip为删除左侧内容。该条为获取评论数的信息做url准备,也可以用正则表达式来匹配抽取

    #有两类channel，需要用if-else结构选择，假定为是gn channel，然后判断status标签下的msg是不是捕捉错误
    commentsurl_gn='http://comment5.news.sina.com.cn/page/info?version=1&format=json&channel=gn&newsid=comos-{}&group=undefined&compress=0&ie=utf-8&oe=utf-8&page=1&page_size=3&t_size=3&h_size=3&thread=1'
    commentsurl_sh='http://comment5.news.sina.com.cn/page/info?version=1&format=json&channel=sh&newsid=comos-{}&group=undefined&compress=0&ie=utf-8&oe=utf-8&page=1&page_size=3&t_size=3&h_size=3&thread=1'

    comments=requests.get(commentsurl_gn.format(newsid),timeout = 5000) #timeout参数用来设置响应超时时间，防止因为网络延迟他自行判断为连接超时
    jd=json.loads(comments.text)
    if jd['result']['status']['msg']=='':
        return jd['result']['count']['total']
    else:
        comments=requests.get(commentsurl_sh.format(newsid))#format()函数用于填补在字符串中用{}挖出的空格
        jd=json.loads(comments.text)


#定义获取内文详细信息的函数，返回包含不同子标题的字符串
def getNewsDetail(newsurl):
    #通过request获取请求，返回页面的HTML文本
    result={}
    res=requests.get(newsurl,timeout = 5000)
    res.encoding='utf-8'
    soup=BeautifulSoup(res.text,'html.parser')#构建DOM模型

   
    if len(soup.select('.main-title'))!=0:
        #获取内文题目
        result['title']=soup.select('.main-title')[0].text
        print(result['title'])

        #获取内文时间
        result['date']=soup.select('.date')[0].text

        #获取内文来源
        result['source']=soup.select('.source')[0].text

        #获取每一段的文本
        articleGroup=[]
        for p in soup.select('#article p')[:-1]:#[:-1]是不获取最后一行，即不显示编辑了
            articleGroup.append(p.text.strip())#strip函数用于在字符串中删除指定字符
        result['article']='\n'.join(articleGroup) #为各段之间加一个换行符号,将一个字符数组合并为一个字符串

        #获取内文编辑作者
        result['editor']=soup.select('.show_author')[0].text

        #调用内文评论数的函数
        result['commentsNumber']=getCommentCount(newsurl)

    return result

#定义获取一个分页面中包含的新闻信息的函数，返回一个字符串数组包含分页中所有详细信息
def parseListLinks(unreadnewsurl):
    newsdetails=[]
    unreadnews=requests.get(unreadnewsurl,timeout = 5000)
    jd_unreadnews=json.loads(unreadnews.text)
    for ent in jd_unreadnews['result']['data']:
        newsdetails.append(getNewsDetail(ent['url']))
    return newsdetails

#主程序，获取所有分页包含的新闻信息
allResult=[]
for j in range(1,2):
    print(j)
    resultList=parseListLinks(unreadnewsurl1.format(j))
    allResult.extend(resultList)

#andas将数据存入EXCEL
df=pandas.DataFrame(allResult)
df.to_excel('222.xlsx')

print('--------------------end--------------------')


