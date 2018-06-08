# -*- coding: utf-8 -*-
from abc import abstractclassmethod, ABCMeta
import hashlib
import urllib.request
from bs4 import BeautifulSoup
import re


def genearte_md5(strs):
    # 创建md5对象
    hl = hashlib.md5()

    # Tips
    # 此处必须声明encode
    # 否则报错为：hl.update(str)    Unicode-objects must be encoded before hashing
    hl.update(strs.encode(encoding='utf-8'))
    return hl.hexdigest()


class CrawlerInterface(metaclass=ABCMeta):
    connection = None

    def __init__(self): pass

    def start(self, mysql_conn):
        self.connection = mysql_conn
        pages = self.get_num()
        urls = []
        index = self.get_index()
        if index is not None:
            urls = [self.get_index()]
        for i in range(1, pages):
            urls.append(self.join_url(i))
        all_urls = []
        for url in urls:
            lls = self.get_urls(url)
            for ll in lls:
                all_urls.append(ll)
        for ul in all_urls:
            print(ul)
            info = self.get_info(url=ul)
            if info is not None:
                info.hash = genearte_md5(info.url)
                result = self.process_info(info=info)
                self.insert_mysql(result=result)

    def insert_mysql(self, result):
        con = self.connection
        cursor = con.cursor()
        cursor.execute(self.get_sql(result))
        con.commit()
        cursor.close()

    @staticmethod
    def get_resum_description_from_text(text, info):
        lines = text.split("\n")
        flag = True
        resume_content = ""
        plen = len(lines)
        nu = 1
        name = ""
        content = ""
        for p in lines:
            if p.strip() == '':
                nu = nu + 1
                continue
            if flag:
                resume = re.match("(^.*简历$)|(^.*简历：$)", p.strip(), flags=0)
                if resume is None:
                    content = content + p + "\r\n"
                else:
                    flag = False
                    name = p.replace("　　", "").replace("：", "").replace("简历", "").replace(" ", "")\
                        .replace("　", "").replace("    ", "").replace("个人", "").strip()
                    resume_content = resume_content + p + "\r\n"
            else:
                st = p.replace("　　", "").replace("    ", "").strip()
                if st.startswith("1") or st.startswith("2") or st.startswith(name) or st.startswith("历任") or \
                        st.startswith("（") or st.startswith("曾任") or st.startswith("("):
                    if plen == nu and re.match("(.*?监委)", p) is not None:
                        content = content + p + "\r\n"
                    else:
                        resume_content = resume_content + p + "\r\n"
                else:
                    content = content + p + "\r\n"
                    flag = True
            nu = nu + 1
        info.description = content
        info.resume = resume_content

    @staticmethod
    def get_soup(url, opener=None):
        for i in range(0, 10):
            if opener is None:
                try:
                    res_data = urllib.request.urlopen(url)
                    break
                except Exception as e:
                    print(e)
            else:
                try:
                    res_data = opener.open(urllib.request.Request(url), timeout=2)
                    break
                except Exception as e:
                    print(e)
        res = res_data.read()
        soup = BeautifulSoup(res, "lxml")
        return soup

    @staticmethod
    def get_sql(result):
        sql = "INSERT INTO info SET `hash`= '"+result.hash+"', `url`='"+result.url+"',`time`='"+result.time\
              + "', `title`='"+result.title+"',`source`='"+result.source+"', `description`='"\
              + result.description.replace("'", "\\'") + "',`resume`='"+result.resume+"',`province`='"+result.province\
              + "',`postion`='" + result.postion + "' ON DUPLICATE KEY UPDATE "+" `url`='"+result.url+"',`time`='"\
              + result.time + "', `title`='"+result.title+"',`source`='"+result.source+"', `description`='"\
              + result.description.replace("'", "\\'") + "',`resume`='"+result.resume+"',`province`='"\
              + result.province+"',`postion`='" + result.postion+"'"
        print(sql)
        return sql

    @abstractclassmethod
    def get_num(self): pass

    @abstractclassmethod
    def get_urls(self, url): pass

    @abstractclassmethod
    def get_index(self): pass

    @abstractclassmethod
    def join_url(self, i): pass

    @abstractclassmethod
    def get_info(self, url): pass

    @abstractclassmethod
    def process_info(self, info): pass


class Info(object):
    def __init__(self):
        self.postion = ""
        self.time = ""
        self.source = ""
        self.title = ""
        self.url = ""
        self.description = ""
        self.resume = ""
        self.province = ""
        self.hash = ""
