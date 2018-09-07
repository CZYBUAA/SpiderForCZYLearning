import requests
from lxml import etree

#获取对应url的响应页面信息，并返回起HTML文本
def getText(url):
    header = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:61.0) Gecko/20100101 Firefox/61.0'
    }
    resp = requests.get(url,headers=header,timeout=50000)
    print(resp.encoding)                                                    #这里输出的响应页面的编码格式是ISO-8859-1
    text = resp.content.decode(encoding="gbk", errors="ignore")             #但是这里只有用gbk解码，控制台输出才不会乱码，反而用ISO-8859-1解码就会乱码
    return text

#获取列表页的HTML文本，并用lxml获取该页中列表内的所有电影详情url
def getDetailUrl(text):
    ahtml=etree.HTML(text)
    list = ahtml.xpath("//table[@class='tbspan']")
    url_lists=[]
    for item_list in list:
        detail_url = item_list.xpath(".//a[@class='ulink']/@href")[0]
        url="http://www.dytt8.net"+detail_url
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

def getMovieDetails(text):
    information_html=etree.HTML(text)
    result_list=information_html.xpath("//div[@id='Zoom']//p")
    result=[]
    if result_list!=[]:               #有一些详情页故意不用p标签包含，造成该数组为空，于是产生错误中断程序，需要做一些处理，必要时做一些断点记录
        result=result_list[0]
    return result

#获取1到7页，不包含第7页的所有电影详情url
result_urls=getUrls(1,7)
for item in result_urls:
    detail_url = item
    text = getText(detail_url)
    detail=getMovieDetails(text)
    if detail!=[]:
        print(etree.tostring(detail,encoding='utf-8').decode())
        print(detail.xpath(".//text()"))
    print("-------------------------------------------------------------------")
    break
