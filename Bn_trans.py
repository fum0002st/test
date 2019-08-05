# -*- coding: utf_8 -*-  
import requests
import os, sys, codecs, time
sys.path.append(os.path.join(os.path.dirname(os.path.abspath(sys.argv[0])), 'site-packages'))
from googletrans import Translator
from bs4 import BeautifulSoup


detail_url_list = []
next_page_url = 'https://proposal-service.azurewebsites.net/api/TrainData/'

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
        
        #print(soup_rep)

        try:

            time.sleep(3)
        
            translator = Translator()

            #日本語->韓国語
            soup_trans = translator.translate(soup_rep, src='ja' ,dest='co').text
            
            #韓国語->日本語
            soup_tra =  translator.translate(soup_trans, src='co' ,dest='ja').text

            #改行文字置換
            soup_ins = soup_tra.replace(' \\ n','\\n')
    
            soup_ins = soup_ins.replace(' \\ N','\\n')
    
            soup_ins = soup_ins.replace('\\ n','\\n')
    
            soup_ins = soup_ins.replace('\\ N','\\n')
    
            soup_list[5] = soup_ins

            soup_ivr = soup_list[0] + ',' + soup_list[1] + soup_list[2] + soup_list[3] + soup_list[4] + soup_ins + soup_list[6] + ',' + soup_list[7] + ',' + soup_list[8] + ',' + soup_list[9] + ',' + soup_list[10] + ',' + soup_list[11] + ',' + soup_list[12] + ',' + soup_list[13]

            #[テスト用]ファイル保存
            filename = 'bn_contents-coja' + str(i) + '.txt'
    
            file = codecs.open(filename, 'a', 'utf_8')  #追加書き込みモードでオープン

            soup_ivrs = soup_ivr
    
            file.write(soup_ivrs)
            file.close()

            print('clear : ' + str(i))

        except:

            #エラー時 メッセージを出力して次へ
            print('error : ' + str(i))

            pass

            
    else :
        
        print('page not defined : ' + str(i))
