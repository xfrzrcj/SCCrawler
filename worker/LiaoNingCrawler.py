from worker import Crawler
import pymysql

baseUrl = "http://www.lnsjjjc.gov.cn/"
indexUrl = baseUrl + "jlsc/"


class LiaoNingCrawler(Crawler.CrawlerInterface):

    def get_num(self):
        soup = self.get_soup(indexUrl)
        a = soup.find("p", class_="tC")
        href = a.find("a").get('href')
        href = href[83:90]
        return int(href)

    def get_index(self):
        return indexUrl

    def join_url(self, i):
        page = "%08d" % i
        url = indexUrl + "system/more/1400000000000000/0000/1400000000000000_" + page + ".shtml"
        return url

    def get_urls(self, url):
        soup = self.get_soup(url)
        lists = soup.find("div", class_="picList clearall")
        tags = lists.find_all("p")
        urls = []
        for tag in tags:
            info_url = tag.find("a").get("href")
            urls.append(info_url)
        return urls

    def get_info(self, url):
        info_result = Crawler.Info()
        soup = self.get_soup(url)
        real_url = soup.find("meta").get("content")
        if real_url != "text/html; charset=UTF-8":
            url = real_url.replace("0; url=", "")
        info_result.url = url
        soup = self.get_soup(url)
        title = soup.find("h1")
        info_result.title = title.text
        time_source = soup.find("div", class_="infoLine")
        ts = time_source.text.replace("\r", "").replace("\n", "").split("     ")
        info_result.time = ts[0]
        info_result.source = ts[1]
        img = soup.find("img", id="no_img")
        if img is None:
            article = soup.find("div", class_="content")
            ps = article.find_all("p")
            text = ""
            for p in ps:
                text = text + p.text + "\n"
            self.get_resum_description_from_text(text, info_result)
        else:
            info_result.description = img.get("src")
        return info_result

    def process_info(self, info):
        info.province = "辽宁省"
        info.source = info.source.replace("来源：", "")
        info.time = info.time.replace("发布时间：", "")
        info.postion = "审查调查"
        return info

c = LiaoNingCrawler()
conns = pymysql.connect(host='127.0.0.1', port=3306, user='root', passwd='123456', db='data', charset='utf8')

c.start(conns)
conns.close()
# print(c.get_num())
#print(c.join_url(1))
# print(c.get_urls("http://www.lnsjjjc.gov.cn/jlsc/system/more/1400000000000000/0000/1400000000000000_00000014.shtml"))
# c.get_info("http://www.lnsjjjc.gov.cn/gktb/system/2018/06/01/010026037.shtml")
