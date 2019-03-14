# -*- coding:utf-8 -*-

import urllib2
from lxml import etree
from selenium import webdriver
import requests
import os
import random
import time
driver = webdriver.Chrome("C:\chromedriver_win32\chromedriver.exe")
year_month_link_dict = {}

def transfer(str):
    month_list=['01','02','03','04','05','06','07','08','09','10','11','12']
    return month_list[int(str)-1]

# 得到一年中的所有期链接
def getStageUrlList(url_year,year):
        pattern = '../volumn/(.*?).shtml'
        # 获取主页内容
        headers = {
            'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.80 Safari/537.36 QQBrowser/9.3.7269.400',
        }
        req = urllib2.Request(url_year,headers=headers)
        content = urllib2.urlopen(req).read()
        page = etree.HTML(content)


        path='//div[@class="level"]/ul[@id="pi-'+year+'"]/li/a/@href'
        url_abstract_list = page.xpath(path)#pi-2016代表2016年

        path='//div[@class="level"]/ul[@id="pi-'+year+'"]/li/a/text()'
        text_list = page.xpath(path)#pi-2016代表2016年



        host = r'http://ieeexplore.ieee.org'


        for i in range(len(url_abstract_list)):
            url=host+url_abstract_list[i]
            #url_list.append(url)
            year_month=year+transfer(text_list[i][50:53])
            #year_month_list.append(year_month)
            year_month_link_dict[int(year_month)] =url

        return 1

        #return year_month_link_dict

#获取某一期所有页面链接
def getAllPageUrl(issur_url):
    #driver = webdriver.Chrome("C:\chromedriver_win32\chromedriver.exe")
    driver.get(issur_url)
    strs={"//a[@aria-label='Pagination Page 1']","//a[@aria-label='Pagination Page 2']","//a[@aria-label='Pagination Page 3']"}
    #strs={"//a[@aria-label='Pagination Page 1']"}

    links =[]
    for str in strs:
        try:
            driver.find_element_by_xpath(str).click()
            links.append(driver.current_url)
            #links = driver.current_url
            print 1
        except:
            print 0
    return links

#获取某一页面所有pdf链接
def getPdfUrl(url_stage):
    pattern = r'href="../abstract/(.*?).shtml" '
    # 获取主页内容
    headers = {
        'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.80 Safari/537.36 QQBrowser/9.3.7269.400',
    }
    req = urllib2.Request(url_stage,headers=headers)
    content = urllib2.urlopen(req).read()
    page = etree.HTML(content)
    url_list = page.xpath('//div[@class="controls"]/a[@aria-label]/@href')
    url_list_=[]
    for url in url_list:
        if "/stamp/stamp.jsp" in url:
              url="http://ieeexplore.ieee.org"+url
              url_list_.append(url)

    url_list =url_list_

    return url_list

def getRealPdfUrl2(posturl):
    driver.get(posturl)
    #strs={"//a[@aria-label='Pagination Page 1']","//a[@aria-label='Pagination Page 2']","//a[@aria-label='Pagination Page 3']"}
    str="/html/frameset/frame[2]"

    link=driver.find_element_by_xpath(str).get_attribute('src')
    return link

def downLoadFile(fileName,downloadUrl):
    print "downloading with requests"
    #url = 'http://ieeexplore.ieee.org/ielx7/36/7529247/07493651.pdf?tp=&arnumber=7493651&isnumber=7529247'
    r = requests.get(downloadUrl)
    with open(fileName, "wb") as code:
     code.write(r.content)

if __name__ == "__main__":
    url_mostRecent="http://ieeexplore.ieee.org/xpl/mostRecentIssue.jsp?punumber=36"#raw_input("请输入期刊最新一期链接：")#示例"http://ieeexplore.ieee.org/xpl/mostRecentIssue.jsp?punumber=36"
    start_time=201603#raw_input("请输入开始年月：")#示例,201501
    end_time=201603#raw_input("请输入结束年月：")#示例,201702

    #是否包含最新一期,进行判断
    flag=True
    while(flag):
        input='no'#raw_input("结束年月是否是最新一期,是输入yes,不是输入no:")
        if input=='yes':
            year_month_link_dict[int(end_time)]=url_mostRecent
            flag=False
        elif input=='no':
            flag=False
        else:
            print "输入错误，请重新输入！"
    start_year=str(start_time)[0:4]
    end_year=str(end_time)[0:4]
    for year in range(int(start_year),int(end_year)+1):
        getStageUrlList(url_mostRecent,str(year))
    _year_month_link_dict=year_month_link_dict.copy()
    for key in year_month_link_dict.keys():
        if key<start_time or key>end_time:
            del _year_month_link_dict[key]
    #print 1

    for key in _year_month_link_dict.keys():
        folderName=str(key)[0:4]+'.'+str(key)[4:6]
        if not (os.path.exists(folderName)): #判断是否存在目录，不存在则创建。
            os.makedirs(folderName)
        fileName=folderName+'/'+folderName
        issue_url=_year_month_link_dict[key]
        page_url_list=getAllPageUrl(issue_url)
        for page_url in page_url_list:
            pdf_url_list=getPdfUrl(page_url)
            for pdf_url in pdf_url_list:
                real_pdf_url=getRealPdfUrl2(pdf_url)
                tempName=fileName+'.'+real_pdf_url[44:56]
                if not(os.path.exists(tempName)):
                    num=random.randint(0, 10)
                    time.sleep(num)
                    downLoadFile(tempName,real_pdf_url)


                  #print 1




    #输入为某种期刊最新一期的链接，开始年月，结束年月,结束年月是否为最新一期的判断
    #输出为按期刊年月文件夹存储的所有pdf文件

