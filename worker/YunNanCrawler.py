from worker import Crawler
import pymysql

baseUrl = "http://www.jjjc.yn.gov.cn"
indexUrl = "http://www.jjjc.yn.gov.cn/list-5.html"


class YNCrawler(Crawler.CrawlerInterface):

    def get_num(self):
        soup = self.get_soup(indexUrl)
        a = soup.find("div", class_="total").text
        return int(a.replace("共", "").replace("页", ""))

    def get_index(self):
        return indexUrl

    def join_url(self, i):
        url = baseUrl+"/list-5.html?page="+str(i+1)
        return url

    def get_urls(self, url):
        soup = self.get_soup(url)
        lists = soup.find("div", class_="tList")
        tags = lists.find_all("a")
        urls = []
        for tag in tags:
            info_url = tag.get("href")
            urls.append(info_url)
        return urls

    def get_info(self, url):
        info_result = Crawler.Info()
        info_result.url = url
        soup = self.get_soup(url)
        title = soup.find("div", class_="itit")
        info_result.title = title.text
        time_source = soup.find("div", class_="dt").find_all("span")
        info_result.time = time_source[0].text
        info_result.source = time_source[1].text
        article = soup.find("div", class_="itp")
        ps = article.find_all("p")
        text = ""
        for p in ps:
            text = text + p.text + "\n"
        self.get_resum_description_from_text(text, info_result)
        return info_result

    def process_info(self, info):
        info.province = "云南"
        info.source = info.source.replace("来源:", "")
        info.time = info.time.replace("发布时间:", "")
        info.postion = "审查调查"
        return info

c = YNCrawler()
conns = pymysql.connect(host='127.0.0.1', port=3306, user='root', passwd='123456', db='data', charset='utf8')
c.start(conns)
conns.close()
# print(c.get_num())
# print(c.get_urls("http://www.jjjc.yn.gov.cn/list-5.html?page=2"))
# c.get_info("http://www.jjjc.yn.gov.cn/info-63-51482.html")
