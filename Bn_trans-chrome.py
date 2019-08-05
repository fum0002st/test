# -*- coding: utf_8 -*-  
import requests
import os, sys, codecs, time
sys.path.append(os.path.join(os.path.dirname(os.path.abspath(sys.argv[0])), 'site-packages'))
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import chromedriver_binary


detail_url_list = []
next_page_url = 'https://proposal-service.azurewebsites.net/api/TrainData/'


sys.stdout = codecs.getwriter("utf-8")(sys.stdout)

options = Options()

driver = webdriver.Chrome(options=options)

#google翻訳ページを展開
driver.get("https://translate.google.com/?hl=ja&tab=TT#view=home&op=translate&sl=ja&tl=ko")

time.sleep(5)


for i in range(1,300) :

    #BIDnavi登録情報取得
    target_url = str(next_page_url) + str(i)
    req = requests.get(target_url)
    req.encoding = req.apparent_encoding
    soup = BeautifulSoup(req.content, "lxml")
    soup_find = soup.find('p')
    if soup_find != None :
        soup_list = soup_find.get_text('p')
        soup_list = soup_list.split(',')
    
        soup_rep = soup_list[5]

        #日本語->韓国語
        driver.get("https://translate.google.com/?hl=ja&tab=TT#view=home&op=translate&sl=ja&tl=ko")

        time.sleep(1)

        #翻訳対象日本語文字列入力
        driver.find_element_by_xpath("//*[@id='source']").send_keys(soup_list[5])

        time.sleep(1)

        #確認
        print(driver.find_element_by_class_name("tlid-translation").text)

        trans_ko = driver.find_element_by_class_name("tlid-translation").text

        #韓国語->日本語
        driver.get("https://translate.google.com/?hl=ja&tab=TT#view=home&op=translate&sl=ko&tl=ja");

        time.sleep(3)

        #翻訳対象韓国語文字列入力
        driver.find_element_by_xpath("//*[@id='source']").send_keys(trans_ko)
        
        #driver.find_element_by_xpath("//*[@id='source']").clear()
        
        soup_list[5] = driver.find_element_by_class_name("tlid-translation").text

        soup_ivr = soup_list[0] + ',' + soup_list[1] + ',' + soup_list[2] + ',' + soup_list[3] + ',' + soup_list[4] + ',' + soup_ins + ',' + soup_list[6] + ',' + soup_list[7] + ',' + soup_list[8] + ',' + soup_list[9] + ',' + soup_list[10] + ',' + soup_list[11] + ',' + soup_list[12] + ',' + soup_list[13]

        #[テスト用]ファイル保存
        filename = 'bn_contents-coja' + str(i) + '.txt'
    
        file = codecs.open(filename, 'a', 'utf_8')

        file.write(soup_ivr)
        file.close()

        print('clear : ' + str(i))

        #except:

            #print('error : ' + str(i))

            #pass

            
    else :
        
        print('page not defined : ' + str(i))
