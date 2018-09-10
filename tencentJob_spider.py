import requests
from lxml import etree

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

def getUrlsPerPage(text):
    list_page_HTML = etree.HTML(text)
    result = list_page_HTML.xpath("//tr[@class='even']//a/@href | //tr[@class='odd']//a/@href")
    url_per_page = []
    for item in result:
        real_url="http://hr.tencent.com/"+item
        url_per_page.append(real_url)
    return url_per_page

def getInfoPerPage(urls):
    positions=[]
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
    return positions

base_url='https://hr.tencent.com/position.php?&start={}#a'
positions=[]
for x in range(0,2):
    x *= 10
    url = base_url.format(x)
    list_page_text=getResponseText(url)
    url_per_page=getUrlsPerPage(list_page_text)
    positions_per_page=getInfoPerPage(url_per_page)
    positions.append(positions_per_page)

print(positions)

