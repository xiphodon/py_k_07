import pymongo
from bs4 import BeautifulSoup
import requests
import time

# 把爬取的住房信息存储在数据库中


# 获得数据库连接（本地地址，端口号）
client = pymongo.MongoClient("localhost", 27017)
# 连接数据库（若不存在则创建）
first_db = client["first_db"]
# 连接数据库中的表（若不存在则创建）
house_detail = first_db["house_detail"]

# 住房信息列表
urls_house_list = ["http://sh.xiaozhu.com/search-duanzufang-p{}-0/".format(str(i)) for i in range(1,3)]
# 住房信息列表各个详情页链接
data_href_list = []


def saveDataToDB(data):
    house_detail.insert_one(data)


def readDataFromDB():
    for item in house_detail.find():
        print(item)


# 获取当前页所有房屋资源的详情页链接的列表
def get_this_page_house(url):
    soup = get_soup(url)

    href_list = soup.select("a.resule_img_a")

    for href in href_list:
        href_value = href.get("href")
        if(len(href_value)>0):
            data_href_list.append(href.get("href"))

    time.sleep(2)
    return data_href_list

# 获取租房详情
def get_house_detail(url):
    soup = get_soup(url)

    title_list = soup.select("body > div.wrap.clearfix.con_bg > div.con_l > div.pho_info > h4 > em")
    addr_list = soup.select("body > div.wrap.clearfix.con_bg > div.con_l > div.pho_info > p > span")
    price_list = soup.select("#pricePart > div.day_l > span")
    house_img_list = soup.select("#curBigImage")
    ower_img_list = soup.select("#floatRightBox > div.js_box.clearfix > div.member_pic > a > img")
    ower_name_list = soup.select("#floatRightBox > div.js_box.clearfix > div.w_240 > h6 > a")
    ower_sex_list = soup.select("#floatRightBox > div.js_box.clearfix > div.w_240 > h6 > span")

    for title,addr,price,house_img,ower_img,ower_name,ower_sex in zip(title_list,addr_list,price_list,house_img_list,ower_img_list,ower_name_list,ower_sex_list):
        data = {
            "title" : title.get_text(),
            "addr" : addr.get_text(),
            "price" : price.get_text(),
            "house_img" : house_img.get("src"),
            "ower_img" : ower_img.get("src"),
            "ower_name" : ower_name.get_text(),
            "ower_sex" : "男" if ower_sex.get("class")[0]=="member_boy_ico" else "女"
        }

    saveDataToDB(data)
    print(data)

def get_soup(url):
    header = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.101 Safari/537.36"
    }

    response = requests.get(url, headers=header)
    soup = BeautifulSoup(response.text, "lxml")
    return soup

def main_function():
    for each_detail_url in urls_house_list:
        for each_url in get_this_page_house(each_detail_url):
            try:
                get_house_detail(each_url)
            except:
                pass



if __name__ == "__main__":
    # 爬取数据并存入数据库
    # main_function()

    # 从数据库读取存储数据
    readDataFromDB()
"""
detail href:
#page_list > ul > li:nth-child(9) > a
#page_list > ul > li:nth-child(7) > a

"""