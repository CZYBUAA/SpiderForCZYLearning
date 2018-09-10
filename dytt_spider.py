import requests
from lxml import etree

# 1、获取列表页数的所有电影的详情页url，组成一个数组
# 2、遍历这个数组，访问数组中的每个url对应的详情页面
# 3、返回详情页面中的HTML文本，用xpath语言获取包含关键信息的段落
# 4、解析这个段落，将这个段落文本的信息拆解，放入一个“字典”{}，解析完一个电影，就把这个代表这个电影的“字典”放入movie数组中，返回给主函数
# 5、输出这个包含所有电影“字典”信息的数组movie

#获取对应url的响应页面信息，并返回起HTML文本
def getText(url):
    header = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:61.0) Gecko/20100101 Firefox/61.0',
        'Referer':'http://www.dytt8.net/',
        'Connection':'keep-alive',
        'Accept-Language':'zh - CN, zh;q = 0.8, zh - TW;q = 0.7, zh - HK;q = 0.5, en - US;q = 0.3, en;q = 0.2',
        'Host':'www.dytt8.net'
    }
    resp = requests.get(url,headers=header,timeout=50000)                                                 #这里输出的响应页面的编码格式是ISO-8859-1
    text = resp.content.decode(encoding="gbk", errors="ignore")             #但是这里只有用gbk解码，控制台输出才不会乱码，反而用ISO-8859-1解码就会乱码
    return text

#获取列表页的HTML文本，并用lxml获取该页中列表内的所有电影详情url
def getDetailUrl(text):
    ahtml=etree.HTML(text)
    list = ahtml.xpath("//table[@class='tbspan']")
    url_lists=[]
    for item_list in list:
        detail_url = item_list.xpath(".//a[@class='ulink']/@href")[0]
        if item_list.xpath(".//a[@class='ulink']/text()")[0]=='[综合电影]':
            detail_url = item_list.xpath(".//a[@class='ulink']/@href")[1]
        url="http://www.dytt8.net"+detail_url
        print(url)
        url_lists.append(url)
    return url_lists

#获取指定页数区间内的列表内所有电影详情url，返回字符串数组
def getUrls(start,end):
    urls = []
    for i in range(start, end):
        j = str(i)
        print(j)
        dytt_url = 'http://www.dytt8.net/html/gndy/dyzz/list_23_' + j + '.html'
        dytt_text = getText(dytt_url)
        urls.extend(getDetailUrl(dytt_text))
    return urls

#获取详情页中，仅包含关键信息的段落
def getMovieDetails(text):
    information_html=etree.HTML(text)
    result_list=information_html.xpath("//div[@id='Zoom']")
    movie={}
    if result_list!=[]:               #判空
        result=result_list[0]
        info = result.xpath(".//text()")
        for info_item in info:
            if info_item.startswith("◎译　　名"):
                info_item = parse_info(info_item, "◎译　　名")
                movie['translate film name'] = info_item
            elif info_item.startswith("◎片　　名"):
                info_item = parse_info(info_item, "◎片　　名")
                movie['film name'] = info_item
            elif info_item.startswith("◎年　　代"):
                info_item = parse_info(info_item, "◎年　　代")
                movie['year'] = info_item
            elif info_item.startswith("◎产　　地"):
                info_item = parse_info(info_item, "◎产　　地")
                movie['country'] = info_item
            elif info_item.startswith("◎类　　别"):
                info_item = parse_info(info_item, "◎类　　别")
                movie['category'] = info_item
            elif info_item.startswith("◎豆瓣评分"):
                info_item = parse_info(info_item, "◎豆瓣评分")
                movie['douban_rating'] = info_item
            elif info_item.startswith("◎片　　长"):
                info_item = parse_info(info_item, "◎片　　长")
                movie['duration'] = info_item
            elif info_item.startswith("◎导　　演"):
                info_item = parse_info(info_item, "◎导　　演")
                movie['director'] = info_item
    return movie

def parse_info(info,rule):
    return info.replace(rule,"").strip()

def getContents(result_urls):
    movies = []
    #遍历result_urls列表中的所有项，即每一个电影对应的详情页url
    for item in result_urls:
        detail_url = item
        text = getText(detail_url)
        movie=getMovieDetails(text)
        print(movie)
        print("---------------------------------------------")
        movies.append(movie)
    return movies

#获取1到2页，不包含第2页的所有电影详情url，获取7页的时候有bug，还没处理
result_urls=getUrls(1,7)
movies=getContents(result_urls)
print(movies)
