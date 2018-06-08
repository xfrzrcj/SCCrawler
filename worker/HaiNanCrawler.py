from worker import Crawler
import pymysql
from selenium import webdriver
import time
import re


baseUrl = "http://www.hnlzw.net"
indexUrl = "http://www.hnlzw.net/jlsc_sggb.php"
djcf_sggbUrl = "http://www.hnlzw.net/djcf_sggb.php"
jlsc_sxgbUrl = "http://www.hnlzw.net/jlsc_sxgb.php"
djcf_sxgbUrl = "http://www.hnlzw.net/djcf_sxgb.php"
browser = webdriver.Chrome("d:/chromedriver.exe")


class HN_jlsc_sggb_Crawler(Crawler.CrawlerInterface):

    def get_num(self):
        soup = self.get_soup(indexUrl)
        a = soup.find("a", text="末页").get("href")
        pages = a.replace('/jlsc_sggb.php?ncount=8&nbegin=', "")
        return int(pages)//8+1

    def get_index(self):
        return indexUrl

    def join_url(self, i):
        url = baseUrl+"/jlsc_sggb.php?ncount=8&nbegin="+str(i*8)
        return url

    def get_urls(self, url):
        soup = self.get_soup(url)
        lists = soup.find("div", id="mainrconlist")
        tags = lists.find_all("li")
        urls = []
        for tag in tags:
            ss = tag.find("a").get("href")
            if ss.startswith("http"):
                urls.append(tag.find("a").get("href"))
            else:
                urls.append(baseUrl + "/" + tag.find("a").get("href"))
        return urls

    def get_info(self, url):
        if url == "http://www.hnlzw.net/page.php?xuh=44175" or url == \
                "http://www.hnlzw.net/page.php?xuh=39496":
            return None
        info_result = Crawler.Info()
        info_result.url = url
        soup = self.get_soup(url)
        title = soup.find("div", id="arttitl")
        info_result.title = title.text
        time_source = soup.find("div", id="artdes").text
        ts = time_source.split("  ")
        info_result.time = ts[0]
        info_result.source = ts[1]
        article = soup.find("div", id="artcon")
        ps = article.find_all("p")
        text = ""
        for p in ps:
            text = text + p.text + "\n"
        self.get_resum_description_from_text(text, info_result)
        return info_result

    def process_info(self, info):
        info.province = "海南"
        info.source = info.source.replace("来源：", "")
        info.time = info.time.replace("发布时间：", "")
        info.postion = "审查调查(省一级党和国家机关、国企干部)"
        return info


class HN_djcf_sggb_Crawler(Crawler.CrawlerInterface):

    def get_num(self):
        soup = self.get_soup(djcf_sggbUrl)
        a = soup.find("a", text="末页").get("href")
        pages = a.replace('/djcf_sggb.php?ncount=8&nbegin=', "")
        return int(pages)//8+1

    def get_index(self):
        return djcf_sggbUrl

    def join_url(self, i):
        url = baseUrl+"/djcf_sggb.php?ncount=8&nbegin="+str(i*8)
        return url

    def get_urls(self, url):
        soup = self.get_soup(url)
        lists = soup.find("div", id="mainrconlist")
        tags = lists.find_all("li")
        urls = []
        for tag in tags:
            ss = tag.find("a").get("href")
            if ss.startswith("http"):
                urls.append(tag.find("a").get("href"))
            else:
                urls.append(baseUrl + "/" + tag.find("a").get("href"))
        return urls

    def get_info(self, url):
        info_result = Crawler.Info()
        info_result.url = url
        browser.get(url)
        time.sleep(0.5)
        title = browser.find_element_by_id("arttitl").text
        info_result.title = title
        time_source = browser.find_element_by_id("artdes").text
        tt = re.findall("\d{4}-\d{2}-\d{2}\s+\d{2}:\d{2}:\d{2}",
                        time_source)
        if len(tt) != 0:
            info_result.time = tt[0]
        source = re.findall("来源：.*?作者", time_source)
        if len(source) == 0:
            source = re.findall("来源：.*?编辑", time_source)
        if len(source) > 0:
            info_result.source = source[0]
        article = browser.find_element_by_id("artcon")
        ps = article.find_elements_by_tag_name("p")
        text = ""
        for p in ps:
            text = text + p.text + "\n"
        self.get_resum_description_from_text(text, info_result)
        return info_result

    def process_info(self, info):
        info.province = "海南"
        info.source = info.source.replace("来源：", "").replace("作者", "").replace("编辑", "")
        info.time = info.time.replace("发布时间：", "")
        info.postion = "纪律处分(省一级党和国家机关、国企干部)"
        return info


class HN_jlsc_sxgb_Crawler(Crawler.CrawlerInterface):

    def get_num(self):
        soup = self.get_soup(jlsc_sxgbUrl)
        a = soup.find("a", text="末页").get("href")
        pages = a.replace('/jlsc_sxgb.php?ncount=8&nbegin=', "")
        return int(pages)//8+1

    def get_index(self):
        return indexUrl

    def join_url(self, i):
        url = baseUrl+"/jlsc_sxgb.php?ncount=8&nbegin="+str(i*8)
        return url

    def get_urls(self, url):
        soup = self.get_soup(url)
        lists = soup.find("div", id="mainrconlist")
        tags = lists.find_all("li")
        urls = []
        for tag in tags:
            ss = tag.find("a").get("href")
            if ss.startswith("http"):
                urls.append(tag.find("a").get("href"))
            else:
                urls.append(baseUrl + "/" + tag.find("a").get("href"))
        return urls

    def get_info(self, url):
        info_result = Crawler.Info()
        info_result.url = url
        browser.get(url)
        time.sleep(0.5)
        title = browser.find_element_by_id("arttitl").text
        info_result.title = title
        time_source = browser.find_element_by_id("artdes").text
        tt = re.findall("\d{4}-\d{2}-\d{2}\s+\d{2}:\d{2}:\d{2}",
                        time_source)
        if len(tt) != 0:
            info_result.time = tt[0]
        source = re.findall("来源：.*?作者", time_source)
        if len(source) == 0:
            source = re.findall("来源：.*?编辑", time_source)
        if len(source) > 0:
            info_result.source = source[0]
        article = browser.find_element_by_id("artcon")
        ps = article.find_elements_by_tag_name("p")
        text = ""
        for p in ps:
            text = text + p.text + "\n"
        self.get_resum_description_from_text(text, info_result)
        return info_result

    def process_info(self, info):
        info.province = "海南"
        info.source = info.source.replace("来源：", "").replace("作者", "").replace("编辑", "")
        info.time = info.time.replace("发布时间：", "")
        info.postion = "审查调查(市县干部)"
        return info


class HN_djcf_sxgb_Crawler(Crawler.CrawlerInterface):

    def get_num(self):
        soup = self.get_soup(djcf_sxgbUrl)
        a = soup.find("a", text="末页").get("href")
        pages = a.replace('/djcf_sxgb.php?ncount=8&nbegin=', "")
        return int(pages)//8+1

    def get_index(self):
        return indexUrl

    def join_url(self, i):
        url = baseUrl+"/djcf_sxgb.php?ncount=8&nbegin="+str(i*8)
        return url

    def get_urls(self, url):
        soup = self.get_soup(url)
        lists = soup.find("div", id="mainrconlist")
        tags = lists.find_all("li")
        urls = []
        for tag in tags:
            ss = tag.find("a").get("href")
            if ss.startswith("http"):
                urls.append(tag.find("a").get("href"))
            else:
                urls.append(baseUrl + "/" + tag.find("a").get("href"))
        return urls

    def get_info(self, url):
        info_result = Crawler.Info()
        info_result.url = url
        browser.get(url)
        time.sleep(0.5)
        title = browser.find_element_by_id("arttitl").text
        info_result.title = title
        time_source = browser.find_element_by_id("artdes").text
        tt = re.findall("\d{4}-\d{2}-\d{2}\s+\d{2}:\d{2}:\d{2}",
                        time_source)
        if len(tt) != 0:
            info_result.time = tt[0]
        source = re.findall("来源：.*?作者", time_source)
        if len(source) == 0:
            source = re.findall("来源：.*?编辑", time_source)
        if len(source) > 0:
            info_result.source = source[0]
        article = browser.find_element_by_id("artcon")
        ps = article.find_elements_by_tag_name("p")
        text = ""
        for p in ps:
            text = text + p.text + "\n"
        self.get_resum_description_from_text(text, info_result)
        return info_result

    def process_info(self, info):
        info.province = "海南"
        info.source = info.source.replace("来源：", "").replace("作者", "").replace("编辑", "")
        info.time = info.time.replace("发布时间：", "")
        info.postion = "纪律处分(市县干部)"
        return info


c = HN_djcf_sxgb_Crawler()
conns = pymysql.connect(host='127.0.0.1', port=3306, user='root', passwd='123456', db='data', charset='utf8')
c.start(conns)
conns.close()
browser.quit()
# print(c.get_num())
# print(c.join_url(1))
# print(c.get_urls("http://www.hnlzw.net/jlsc_sggb.php?ncount=8&nbegin=8"))
# c.get_info("http://www.hnlzw.net/page.php?xuh=45930")
