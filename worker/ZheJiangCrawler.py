import re
from worker import Crawler
import pymysql

baseUrl = "http://www.zjsjw.gov.cn"
indexUrl = baseUrl + "/ch112/jlsc/index.shtml"


class ZjscCrawler(Crawler.CrawlerInterface):

    def get_num(self):
        return 8

    def get_index(self):
        return indexUrl

    def join_url(self, i):
        url = baseUrl+"/ch112/system/count//0112003/000000000000/000/000/c0112003000000000000_00000000" + \
              str(i) + ".shtml"
        return url

    def get_urls(self, url):
        soup = self.get_soup(url)
        lists = soup.find("ul", class_="listUl cf")
        tags = lists.find_all("a")
        urls = []
        for tag in tags:
            info_url = baseUrl + tag.get('href')
            urls.append(info_url)
        return urls

    def get_info(self, url):
        info_result = Crawler.Info()
        info_result.url = url
        soup = self.get_soup(url)
        title = soup.find("h1", class_="artTitle")
        info_result.title = title.text
        time = soup.find("span", id="pubtime_baidu")
        info_result.time = time.text.replace('\r', '').replace("\n", "")
        source = soup.find("span", id="source_baidu")
        info_result.source = source.text.replace('\r\n', '')
        article = soup.find("div", class_="artCon")
        ps = article.find_all("p")
        content = ""
        if len(ps) == 0:
            content = article.text
            info_result.description = content.replace("\n", "").replace("\r", "")
            return info_result
        flag = True
        resume_content = ""
        plen = len(ps)
        nu = 1
        name = ""
        for p in ps:
            if flag:
                resume = p.find(text=re.compile("(^.*简历$)|(^.*简历：$)"))
                if resume is None:
                    content = content + p.text + "\r\n"
                else:
                    flag = False
                    name = resume.replace("　　", "").replace("：", "").replace("简历", "").replace(" ", "").replace("　", "")
                    resume_content = resume_content + p.text + "\r\n"
            else:
                st = p.text.replace("　　", "")
                if st.startswith("1") or st.startswith("2") or st.startswith(name):
                    if plen == nu and re.match("(.*?监委)", p.text) is not None:
                        content = content + p.text + "\r\n"
                    else:
                        resume_content = resume_content + p.text + "\r\n"
                else:
                    content = content + p.text + "\r\n"
                    flag = True
            nu = nu + 1
        info_result.description = content
        info_result.resume = resume_content
        return info_result

    def process_info(self, info):
        info.province = "浙江"
        info.source = info.source.replace("来源：", "")
        info.time = info.time.replace("发布时间：", "")
        info.postion = "审查调查"
        return info

c = ZjscCrawler()
conns = pymysql.connect(host='127.0.0.1', port=3306, user='root', passwd='123456', db='data', charset='utf8')

c.start(conns)
conns.close()

