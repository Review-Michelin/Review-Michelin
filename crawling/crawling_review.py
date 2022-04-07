from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import csv


# 크롤링 함수 지정
def 리뷰크롤링():
    # 1. 카테고리 변경
    time.sleep(1)
    browser.find_element(by=By.XPATH, value='//*[@id="content"]/div[2]/div[1]/ul/li[2]/a').click()
    time.sleep(1)

    # 2 매장명으로 csv 파일 만들기
    title = browser.find_element(by=By.XPATH, value='//*[@id="content"]/div[2]/div[1]/div[1]/div[1]/span')
    f = "{0}.csv".format(title.text)
    f = open(f, "w", encoding="utf-8-sig", newline="")
    writer = csv.writer(f)

    # 3. 리뷰 페이지 스크롤 내리기
    while True:
        try:
            browser.execute_script("window.scrollTo(0,document.body.scrollHeight)")
            print("더보기 시작")
            time.sleep(1)
            browser.find_element(by=By.XPATH, value='btn-more').click()
            print("더보기 종료")
            time.sleep(1)
        except:
            break

    # 4. 내용만 긁어오기
    count = 1
    maincontent = []

    while True:
        try:
            content = []
            count = count + 1
            score1 = browser.find_element(
                by=By.XPATH, value='//*[@id="review"]/li[' + str(count) + ']/div[2]/div/span[2]/span[3]')

            score2 = browser.find_element(
                by=By.XPATH, value='//*[@id="review"]/li[' + str(count) + ']/div[2]/div/span[2]/span[6]')

            score3 = browser.find_element(
                by=By.XPATH, value='//*[@id="review"]/li[' + str(count) + ']/div[2]/div/span[2]/span[9]')

            total_score = (int(score1.text) + int(score2.text) + int(score3.text))

            con2 = browser.find_element(
                by=By.XPATH, value='//*[@id="review"]/li[' + str(count) + ']/p').text

            if total_score == 15:
                content.append(con2)
                content.append("1")
                maincontent.append(content)
                print("긍정 성공 !")

            if total_score < 10:
                content.append(con2)
                content.append("0")
                maincontent.append(content)
                print("부정 성공 ! ")


        except:
            break

    for i in maincontent:
        writer.writerow(i)

    # 5. 크롤링 종료 및 뒤로가기
    f.close()
    browser.back()
    time.sleep(1)


# 1. 요기요 페이지 접속
browser = webdriver.Chrome()
# browser.maximize_window() # 창 최대화
url = "https://www.yogiyo.co.kr/mobile/#/"
browser.get(url)  # url 로 이동
time.sleep(1)

# 2. 카테고리 선택
print("카테고리를 선택하세요")
a = int(input("1.치킨 2.피자/양식 3.중국집 4.한식 5.일식 6.족발/보쌈 7.분식 8.카페/디저트   "))
if a == 1:
    cg = browser.find_element(by=By.XPATH, value='/html/body/div[7]/div/div[5]/a')
elif a == 2:
    cg = browser.find_element(by=By.XPATH, value='/html/body/div[7]/div/div[6]/a')
elif a == 3:
    cg = browser.find_element(by=By.XPATH, value='/html/body/div[7]/div/div[7]/a')
elif a == 4:
    cg = browser.find_element(by=By.XPATH, value='/html/body/div[7]/div/div[8]/a')
elif a == 5:
    cg = browser.find_element(by=By.XPATH, value='/html/body/div[7]/div/div[9]/a')
elif a == 6:
    cg = browser.find_element(by=By.XPATH, value='/html/body/div[7]/div/div[10]/a')
elif a == 7:
    cg = browser.find_element(by=By.XPATH, value='/html/body/div[7]/div/div[12]/a')
elif a == 8:
    cg = browser.find_element(by=By.XPATH, value='/html/body/div[7]/div/div[13]/a')
else:
    print("올바른 번호를 입력해주세요")
cg_title = cg.text
cg.click()

# 4. 음식점을 리뷰 많은 순으로 정렬
time.sleep(2)
browser.find_element(by=By.XPATH, value='//*[@id="content"]/div/div[1]/div[2]/div/select').click()

time.sleep(1)
browser.find_element(by=By.XPATH, value='//*[@id="content"]/div/div[1]/div[2]/div/select/option[3]').click()

# 4 기준 리뷰수 설정 및 크롤링 시작
time.sleep(1)
i = 1
review_count_input = int(input("기준 리뷰수 설정 (입력 숫자 이상의 리뷰만 크롤링)"))
while True:
    count = browser.find_element(by=By.XPATH, value='//*[@id="content"]/div/div[5]/div/div/div[' + str(
        i) + ']/div/table/tbody/tr/td[2]/div/div[2]/span[2]')
    review_count = int(count.text[3:])
    if review_count < review_count_input:
        break
    browser.find_element(by=By.XPATH, value='//*[@id="content"]/div/div[5]/div/div/div[' + str(i) + ']/div').click()
    i = i + 1
    리뷰크롤링()

print("크롤링종료")
