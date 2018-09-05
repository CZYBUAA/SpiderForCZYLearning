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

#获取1到7页，不包含第7页的所有电影详情url
result_urls=getUrls(1,7)
#先试验，尝试获取第一个url对应电影的详情信息片段
detail_url = result_urls[0]
text=getText(detail_url)
print(text) #注意，这里能够无乱码输出是因为第十行用了gbk作为解码，但是实际resp对应的encoding方式应该是ISO-8859-1，疑问在这



#for detail_url in result_urls:
#    resp = requests.get(detail_url, headers=header, timeout=50000)
#    print(resp.content.decode('gbk'))

#这里编码格式明明是ISO-8859-1，为什么用这个解码在控制台会输出乱码，但是用gbk解码就不会出现乱码？
#print(resp.encoding)
#print(resp.content.decode('gbk'))


#同样的问题
#print(text.encode('ISO-8859-1').decode('gbk'))
#detail_imformation_HTML=etree.HTML(text)
#list_p=detail_imformation_HTML.xpath("//p")
#print(etree.tostring(list_p[4],encoding='ISO-8859-1').decode('gbk'))