import requests
from lxml import etree
import pandas
import openpyxl

#获取页面的HTML文本，并返回
def getResponseText(url):
    header = {
        'Cookie': 'pgv_pvi=8770966528; PHPSESSID=681omihjt3pdsldkvk0kgpap75; pgv_si=s1532389376',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:61.0) Gecko/20100101 Firefox/61.0',
        'Host': 'hr.tencent.com',
        'Upgrade-Insecure-Requests': '1'
    }
    resp = requests.get(url, headers=header)
    text = resp.text
    return text

#传入职业列表每一页的HTML文本，获取这个文本的列表中职位对应的详情url
def getUrlsPerPage(text):
    list_page_HTML = etree.HTML(text)
    result = list_page_HTML.xpath("//tr[@class='even']//a/@href | //tr[@class='odd']//a/@href")
    url_per_page = []
    for item in result:
        real_url="http://hr.tencent.com/"+item
        url_per_page.append(real_url)
    return url_per_page

#逐个访问传入的url数组中的元素，并抽取关键信息，一个职位的信息用一个position字典包含，
#直接用positions数组追加这个职位信息的字典即可
def getInfoPerPage(urls):
    for url in urls:
        info_text=getResponseText(url)
        model = etree.HTML(info_text)
        position = {}
        #获取职位名称
        position_name = model.xpath(".//td[@id='sharetitle']//text()")[0]
        position['position_name'] = position_name
        #获取职位城市、分类、人数
        position_fundamental_info = model.xpath(".//tr[@class='c bottomline']//td//text()")
        position_place = position_fundamental_info[1]
        position_category = position_fundamental_info[3]
        position_number = position_fundamental_info[5]
        position['position_place'] = position_place
        position['position_category'] = position_category
        position['position_number'] = position_number

        #获取职位介绍和要求
        position_introduction = model.xpath(".//ul[@class='squareli']")
        position_duty_model = position_introduction[0].xpath(".//text()")
        position_demand_model = position_introduction[1].xpath(".//text()")

        position_duty = ''
        for item in position_duty_model:
            position_duty = position_duty + item + "/"

        position_demand = ''
        for item in position_demand_model:
            position_demand = position_demand + item + "/"

        position['position_duty'] = position_duty
        position['position_demand'] = position_demand
        positions.append(position)
        print(position)
    return

#主函数，主要包括如下步骤：
#1、获取职位列表展示页面（for循环提供指定页面遍历功能）
#2、获取当前页面的职位列表中的职位详情url，以数组封装
#3、遍历访问详情url数组，获取某一页列表中所展示的职位的所有详细信息，并以数组形式表示“该页的所有职位信息”
base_url='https://hr.tencent.com/position.php?&start={}#a'
base_inform='开始获取第{}页职位列表'
positions=[]
for x in range(0,2):
    inform = base_inform.format(x)
    x *= 10
    url = base_url.format(x)
    print(inform)
    #第1步
    list_page_text=getResponseText(url)
    #第2步
    url_per_page=getUrlsPerPage(list_page_text)
    #第3步
    positions_per_page=getInfoPerPage(url_per_page)

#将这个数组存入excel表中，不过目前这种方式有一个缺陷，
# 一旦某一页的网络断开连接，之前所有爬取的信息会随着程序中断而丢失
df = pandas.DataFrame(positions)
df.to_excel('temp.xlsx')
