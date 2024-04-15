#!/usr/bin/env python
# coding: utf-8

# In[ ]:



from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By

import geocoder
import re
import time
import sys 

global driver2 

#식당목록찾기 함수
def Find_Restaurants(lat, lon):
    
    global Rest_name
    Rest_name = []
    global Rest_score_f
    Rest_score_f= []
    global Rest_score
    Rest_score= []
    global Rest_review
    Rest_review= []
    global Rest_review_n
    Rest_review_n= []
    global Rest_open
    Rest_open= []
    
    #url 설정(구글맵)
    url = 'https://www.google.co.kr/maps/place/{},{}'.format(lat, lon)
    
    #driver 선언, 브라우저 실행
    driver = webdriver.Chrome()
    driver.get(url)
    time.sleep(4)
    #식당 카테고리로 검색
    btn = driver.find_element(By.CLASS_NAME, 'e2moi')
    btn.click()
    time.sleep(4)
    a = driver.find_element(By.CSS_SELECTOR, '#QA0Szd > div > div > div.w6VYqd > div:nth-child(2) > div > div.e07Vkf.kA9KIf > div > div > div.m6QErb.DxyBCb.kA9KIf.dS8AEf.ecceSd > div.m6QErb.DxyBCb.kA9KIf.dS8AEf.ecceSd')
    for k in range(30):
        a.send_keys(Keys.PAGE_DOWN)
        time.sleep(0.12)
    time.sleep(0.3)
    
    table = driver.find_element(By.CSS_SELECTOR, '#QA0Szd > div > div > div.w6VYqd > div:nth-child(2) > div > div.e07Vkf.kA9KIf > div > div > div.m6QErb.DxyBCb.kA9KIf.dS8AEf.ecceSd > div.m6QErb.DxyBCb.kA9KIf.dS8AEf.ecceSd')
    Restaurants = table.find_elements(By.CLASS_NAME, 'Z8fK3b')
    for i, Restaurant in enumerate(Restaurants):
        Rest_name.append(Restaurant.find_element(By.CLASS_NAME, 'NrDZNb').text)
        Rest_score_t = Restaurant.find_element(By.CLASS_NAME, 'AJB7ye')
        temp = re.findall('\d\.\d',Rest_score_t.text)
        if temp != []:
            Rest_score_f.append(float(temp[0]))
            temp2 = '평점 : ' + temp[0]
            Rest_score.append(temp2) 
        else:
            Rest_score_f.append(0)
            Rest_score.append('평가 없음')


        temp = re.findall('\((\d+)\)',Rest_score_t.text)
        if temp != []:
            Rest_review_n.append(int(temp[0]))
            temp2 = '리뷰 수 : ' + temp[0]
            Rest_review.append(temp2) 
        else:
            Rest_review_n.append(0)
            Rest_review.append('리뷰 없음')

        Rest_info = Restaurant.find_elements(By.CLASS_NAME, 'W4Efsd')[1]
        if '영업 중' in Rest_info.text:
            Rest_open.append('영업 중')
        else:
        #elif '영업 종료' in Rest_info.text:
            Rest_open.append('영업 종료')
    time.sleep(1)
    driver.close

#자세한 정보를 얻는 함수
def info_about_Restaurant(lat, lon, Rest_name):
    #url 설정(구글맵)
    url = 'https://www.google.co.jp/maps/place/{},{}'.format(lat, lon)
    global driver2
    #driver 선언, 브라우저 실행
    driver2 = webdriver.Chrome()
    driver2.get(url)
    time.sleep(3)
    btn = driver2.find_element(By.CSS_SELECTOR, '#searchboxinput')
    btn.clear()
    btn.send_keys(Rest_name+'\n')
    time.sleep(2)
    btn2 = driver2.find_elements(By.CLASS_NAME, 'hh2c6 ')
    btn2[len(btn2)-1].click()
    info = driver2.find_elements(By.CLASS_NAME, 'hpLkke ')
    for i in range(len(info)):
        print(info[i].text)
        
        
        

Rest_list = []

#사용자 좌표 산출
g = geocoder.ip('me')
lat, lon = g.latlng
#건대
#lat, lon = (37.541, 127.071)
#안성
#lat, lon = (37.024, 127.225)
#후쿠오카 탠진
#lat, lon = (33.5916437356679, 130.39878136093628)
#식당찾기
Find_Restaurants(lat,lon)

#점수 측정하기
for j in range(len(Rest_open)):
    if not '영업 중' in Rest_open[j]:
        Rest_final_score =  0
    else:
        temp = (Rest_review_n[j]+15)*(Rest_score_f[j]-2.5)+1
        temp = round(temp,2)
        Rest_final_score = temp
    Rest_list.append((j,Rest_name[j],Rest_final_score))

#점수별로 정렬하기
sorted_list = sorted(Rest_list, key=lambda x: x[2], reverse=True)

#결과 출력
for i in range(len(sorted_list)):
    if sorted_list[i][2] > 20:
        print('Ranking ',i+1,' : ',sorted_list[i][1])
        print('점수 : ', sorted_list[i][2])
        print('고유 번호 : ', sorted_list[i][0])
        print(' ')

#사용자 상호작용
while True:
    user_input = input("자세한 정보 = 고유 번호를 입력하기 / Q : 나가기")
    if user_input == 'Q' or user_input == 'q':
        driver2.close
        break;
    elif user_input.isdigit():
        input_num = int(user_input)
        if input_num > len(Rest_open):
            print('잘못된 고유번호')
        else:
            print(Rest_name[input_num])
            print(Rest_score[input_num])
            print(Rest_review[input_num])
            info_about_Restaurant(lat, lon, Rest_name[input_num])
    else:
        print('잘못된 입력')


# In[2]:



# In[ ]:




