import requests
import json
from pyquery import PyQuery as pq

headers = {
    'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36'
}
proxies = {
    "http": "http://127.0.0.1:64795",
    "https": "https://127.0.0.1:64795",
}

def GetPageList(index):
    rtn = []
    try:
        response = requests.get("https://www.t66y.com/thread0806.php?fid=2&search=&page=%d"%index, proxies = proxies, headers=headers, timeout=5)
        response.encoding='gbk'
        #print(response.text)
        doc = pq(response.text)
        #需要找两个tr2
        tr2_index = 0
        for item in doc('tbody:nth-child(2) tr').items():
            if "tr2" in str(item.attr("class")):
                tr2_index += 1
            if tr2_index >= 2:
                stu = {}
                stu["title"] = item("td:nth-child(2) h3:nth-child(1) a:nth-child(1)").text()
                stu["href"] = str(item("td:nth-child(2) h3:nth-child(1) a:nth-child(1)").attr("href"))
                stu["author"] = str(item("td:nth-child(3) a:nth-child(1)").text())
                stu["time"] = str(item("td:nth-child(3) div .s3").attr('title'))[-10:]+" "+str(item("td:nth-child(3) div .s3").text())[-5:]
                if stu["title"] != '':
                    rtn.append(stu)
    except:
        print("error")
        pass
    return rtn

def GetOnePage(url):
    rtn = {"imgs":[],"magnet":""}
    try:
        response = requests.get("https://www.t66y.com/%s"%url, proxies = proxies, headers=headers, timeout=10)
        response.encoding='gbk'
        doc = pq(response.text)
        #需要找两个tr2
        tr2_index = 0
        for item in doc('img').items():
            rtn["imgs"].append(item.attr("ess-data"))
        for item in doc('a').items():
            if item.text().startswith('http://www.rmdown.com'):
                rtn["magnet"] = "magnet:?xt=urn:btih:%s"%item.text()[-40:]
    except:
        print("error")
        pass
    return rtn

def GetImage(url):
    #open(file, mode='r')
    try:
        file_name_start = url.rfind('/')
        if file_name_start == -1 or url.endswith("gif"):
            print("file name get error!!!")
            return
        file_name = url[file_name_start+1:]
        response = requests.get(url, proxies = proxies, headers=headers, timeout=10)
        #print(response.content)magnet:?xt=urn:btih:4123d0652898be01b593e7dc24f16ad6318e44ed
        f = open(file_name, mode='wb')
        f.write(response.content)
        f.close()
    except:
        print("error")
        pass


if __name__ == "__main__":
    result = GetPageList(0)
    idx = 0
    for item in result:
        item_result = GetOnePage(item["href"])
        idx += 1
        print(idx)
        for sub_item in item_result:
            item[sub_item] = item_result[sub_item]

    print(json.dumps(result, sort_keys=True, indent=4 ,ensure_ascii=False))

    #GetImage("http://img599.net/images/2020/10/02/index-541402.th.jpg")
    #GetDownloadUrl('http://www.rmdown.com/link.php?hash=2034123d0652898be01b593e7dc24f16ad6318e44ed')