import requests
from bs4 import BeautifulSoup
from pyecharts import Bar

def parse_page(url):
    headers={
        'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:62.0) Gecko/20100101 Firefox/62.0',
        'Referer':'http://www.weather.com.cn/textFC/xn.shtml'
    }

    resp=requests.get(url,headers=headers)
    resp.encoding='utf-8'
    # 在分析港澳台的天气页面的时候，由于有一个table没有结束标签，造成用lxml无法正确解析html
    # 因此改用html5lib解析器，该解析器的容错性更强，对于没有结束标签的情况，解析器会自动加入结束标签，只不过速度稍慢
    bs=BeautifulSoup(resp.text,"html5lib")
    conMidtab_tag=bs.find(class_="conMidtab")
    tables_tag=conMidtab_tag.find_all('table')
    result=[]
    for child in tables_tag:
        trs=child.find_all('tr')[2:]
        for index,tr in enumerate(trs):
            infos={}
            tds=tr.find_all('td')
            if index==0:
                city_td = tds[1]
            else:
                city_td = tds[0]
            city=list(city_td.stripped_strings)[0]
            temp_td = tds[-2]
            temp=list(temp_td.stripped_strings)[0]
            temp_int=int(temp)
            infos['city']=city
            infos['temp']=temp_int
            result.append(infos)
    return result

def main():
    urls=[
        'http://www.weather.com.cn/textFC/hb.shtml',
        'http://www.weather.com.cn/textFC/db.shtml',
        'http://www.weather.com.cn/textFC/hd.shtml',
        'http://www.weather.com.cn/textFC/hz.shtml',
        'http://www.weather.com.cn/textFC/hn.shtml',
        'http://www.weather.com.cn/textFC/xb.shtml',
        'http://www.weather.com.cn/textFC/xn.shtml',
        'http://www.weather.com.cn/textFC/gat.shtml'
    ]

    result=[]
    for url in urls:
        result_perpage=parse_page(url)
        result.extend(result_perpage)

    # 分析数据
    # 1、先进行排序，sort方法为数组[]拥有的方法
    result.sort(key=lambda data:data['temp'])
    print(result)

    # 2、获取前10个元素，存到一个新的数组里
    data=result[0:10]

    # 3、使用pyechars的Bar实现可视化
    chart= Bar("中国天气最低温排行榜")
    # map方法返回一个map对象，需要用list()方法将其转化为列表
    # 另外，对于 lambda 的含义和使用方法还不是很理解
    cities=list(map(lambda x:x['city'],data))
    temps=list(map(lambda x:x['temp'],data))
    chart.add('',cities,temps)
    chart.render("temp.html")

if __name__ == '__main__':
    main()