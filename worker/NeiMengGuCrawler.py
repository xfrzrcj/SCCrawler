from worker import Crawler
import pymysql
import re

baseUrl = "http://www.nmgjjjc.gov.cn"
indexUrl = "http://www.nmgjjjc.gov.cn/ajcc/"
index2Url = "http://www.nmgjjjc.gov.cn/scdc/"


class NMGAjccCrawler(Crawler.CrawlerInterface):

    def get_num(self):
        soup = self.get_soup(indexUrl)
        a = soup.find("div", class_="z_page").text
        nums = re.findall("/\d+页", a)[0][1:-1]
        return int(nums)

    def get_index(self):
        return indexUrl

    def join_url(self, i):
        url = baseUrl+"/ajcc/index_"+str(i+1)+".shtml"
        return url

    def get_urls(self, url):
        soup = self.get_soup(url)
        lists = soup.find("div", class_="zMain_con")
        tags = lists.find_all("div", "zMain_list")
        urls = []
        for tag in tags:
            info_url = tag.find("a").get("href")
            urls.append(info_url)
        return urls

    def get_info(self, url):
        info_result = Crawler.Info()
        info_result.url = url
        soup = self.get_soup(url)
        detail_tit = soup.find("div", class_="detail_tit")
        info_result.title = detail_tit.find("h2").text
        info_result.time = detail_tit.find("em").text
        info_result.source = detail_tit.find("span").text
        article = soup.find("div", class_="detail_con")
        ps = article.find_all("p")
        text = ""
        for p in ps:
            text = text + p.text + "\n"
        self.get_resum_description_from_text(text, info_result)
        return info_result

    def process_info(self, info):
        info.province = "内蒙古"
        info.source = info.source.replace("来源：", "")
        info.time = info.time.replace("发布时间:", "")
        info.postion = "执纪审查"
        return info


class NMGScdcCrawler(Crawler.CrawlerInterface):

        def get_num(self):
            soup = self.get_soup(index2Url)
            a = soup.find("div", class_="z_page").text
            nums = re.findall("/\d+页", a)[0][1:-1]
            return int(nums)

        def get_index(self):
            return indexUrl

        def join_url(self, i):
            url = baseUrl + "/scdc/index_" + str(i + 1) + ".shtml"
            return url

        def get_urls(self, url):
            soup = self.get_soup(url)
            lists = soup.find("div", class_="zMain_con")
            tags = lists.find_all("div", "zMain_list")
            urls = []
            for tag in tags:
                info_url = tag.find("a").get("href")
                urls.append(info_url)
            return urls

        def get_info(self, url):
            info_result = Crawler.Info()
            info_result.url = url
            soup = self.get_soup(url)
            detail_tit = soup.find("div", class_="detail_tit")
            info_result.title = detail_tit.find("h2").text
            info_result.time = detail_tit.find("em").text
            info_result.source = detail_tit.find("span").text
            article = soup.find("div", class_="detail_con")
            ps = article.find_all("p")
            text = ""
            for p in ps:
                text = text + p.text + "\n"
            self.get_resum_description_from_text(text, info_result)
            return info_result

        def process_info(self, info):
            info.province = "内蒙古"
            info.source = info.source.replace("来源：", "")
            info.time = info.time.replace("发布时间:", "")
            info.postion = "审查调查"
            return info

c = NMGScdcCrawler()
conns = pymysql.connect(host='127.0.0.1', port=3306, user='root', passwd='123456', db='data', charset='utf8')
c.start(conns)
conns.close()
# print(c.get_num())
# print(c.get_urls("http://www.nmgjjjc.gov.cn/ajcc/index_2.shtml"))
# c.get_info("http://www.nmgjjjc.gov.cn/ajcc/9849001.shtml")
