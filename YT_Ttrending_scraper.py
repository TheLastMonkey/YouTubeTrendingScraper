from selenium import webdriver
import time
import re
import datetime

driver = webdriver.Chrome(executable_path="/home/iPad/PycharmProjects/selenium_tests_lean/sel_driver/chromedriver")
driver.set_page_load_timeout(60)
driver.get("https://www.youtube.com/feed/trending")

k = ','
datetime_now=datetime.datetime.now()
fileN='vid{}.csv'.format(datetime_now)

print("RANK",k ,"CH NAME",k ,"VIEWS",k , "VIDEO TITLE", k, "RAW VIDEO META DATA",
      k, "YT CH", k, "CUT META DATA", k, "VIDEO LINK", k, 'Yr', k, 'month',
      k, 'week', k, 'day', k, 'hr', k, 'min', k, 'sec', file = open(fileN, "a"))



time.sleep(3)
rank=0
print('Working...')

try:
    for meta in driver.find_elements_by_id('meta'):
        rank+=1
        ranks=str(rank)

        vid_dat = meta.find_element_by_id('video-title')
        aria = vid_dat.get_attribute('aria-label')
        aria=str(aria).replace(',',"")
        title=vid_dat.get_attribute('title')
        title=str(title).replace(','," ")
        title=title.lstrip()
        vid_link=vid_dat.get_attribute('href')

        chan_dat = meta.find_element_by_xpath('''.//*[@id="byline"]/a''')
        ch_link = chan_dat.get_attribute('href')
        ch_text = chan_dat.text
        ch_text=ch_text.strip().lstrip().replace(',',' ')

        metasplit=aria.replace(','," ")
        meta_str=str(metasplit).strip().lstrip().replace(',',' ')
        met=meta_str.split(' by ')

        viwe_split=aria.replace(',',".")
        viwe_s=str(viwe_split)
        vi=viwe_s.split()
        views=vi[-2]
        views=views.replace(',',"")
        ####################################
        reg = r"\d{1,}\s\w{1,3}"
        cut = aria.split('by')
        string = str(cut[-1])
        matches = re.findall(reg, string)
        matches_trimed = matches[0:-1]
        time_list = []

        for t in matches_trimed:
            time = str(t)
            tl = time.split()
            time_list.append(tl)

        time_dic = {'yea': 0, 'mon': 0, 'wee': 0, 'day': 0, 'hou': 0, 'min': 0, 'sec': 0}

        for i in range(len(time_list)):
            d = {time_list[i][1]: time_list[i][0]}
            time_dic.update(d)

        if views in ("hour","hours", "minutes", "seconds"):
            views="LIVE"
        else:
            pass

        print(ranks+k+ch_text+k+views+k+title+k+aria+k+ch_link+k+met[1]+k+vid_link+
              k, time_dic['yea'], k, time_dic['mon'], k, time_dic['wee'],
              k, time_dic['day'], k, time_dic['hou'], k,
              time_dic['min'], k, time_dic['sec'], file=open(fileN, "a"))



except:
    print('End')

driver.close()
