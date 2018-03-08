# # 这是分析一页的url
# import requests
# import re
# data={"User-Agent":"Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.186 Safari/537.36"}
# response=requests.get("http://maoyan.com/board/4?offset=0",headers=data)
# # start_url="http://maoyan.com/board/4?offset=0"
# html=response.text
# dianyings=re.compile('<p class="star">(.*?)</p><p class="releasetime">(.*?)</p>',re.S)
# dianying=re.findall(dianyings,html)
# # print(dianying)
# # <p class="star">(.*?)</p><p class="releasetime">(.*?)</p>',re.S
# # yanyuans=re.compile('<p class="star">(.*?)</p>', re.S)
# # yanyuan=re.findall(yanyuans,html)
# # for i in yanyuan:
# #     print(i.strip().split("：")[1])
# # shijians=re.compile('<p class="releasetime">(.*?)</p>')
# # shijian=re.findall(shijians,html)
# # print(shijian)
from multiprocessing import Pool
import requests
import json
import re


def get_one_page(url):
    response = requests.get(url)
    if response.status_code == 200:
        return response.text


def parse_one_page(html):  # 分析页面
    pattern = re.compile('<dd>.*?board-index.*?>(\d+)</i>.*?data-src="(.*?)".*?name"><a'
                         + '.*?>(.*?)</a>.*?star">(.*?)</p>.*?releasetime">(.*?)</p>'
                         + '.*?integer">(.*?)</i>.*?fraction">(.*?)</i>.*?</dd>', re.S)
    items = re.findall(pattern, html)
    for item in items:
        yield {
            "index": item[0],
            "image": item[1],
            "title": item[2],
            "actor": item[3].strip()[3:],  # 去掉主演
            "time": item[4].strip()[5:],  # 去掉上映时间aa
            "score": item[5] + item[6]
        }  # 用字典去存储


def write_to_file(content):
    with open("maoyan.txt", "a") as f:
        f.write(json.dump(content, ensure_ascii=False + "\n"))  # 转换成字符串
        # 这是因为json.dumps 序列化时对中文默认使用的ascii编码.想输出真正的中文需要指定ensure_ascii=False：
        f.close()


def main(offset):
    url = "http://maoyan.com/board/4?offset=" + str(offset)
    html = get_one_page(url)
    for item in parse_one_page(html):
        print(item)
        write_to_file(item)


if __name__ == "__main__":
    pool = Pool()
    pool.map(main, [i * 10 for i in range(10)])
    print("ok")
