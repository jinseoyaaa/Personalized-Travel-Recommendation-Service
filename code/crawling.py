import csv
import os
import json
import time
import pandas as pd
import urllib.request
from tqdm import tqdm
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
import random

class NaverCrawling:
    def __init__(self, client_id, client_secret):
        self.client_id = client_id
        self.client_secret = client_secret

    def search_and_save_api_results(self, text, output_file, iterations):
        encText = urllib.parse.quote(text)
        fieldnames = ['title', 'link', 'description', 'bloggername', 'bloggerlink', 'postdate']

        with open(output_file, 'a', newline='', encoding='utf-8-sig') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

            if csvfile.tell() == 0:
                writer.writeheader()

            count = 0

            for _ in tqdm(range(1, iterations + 1), desc="API 호출 및 저장 중"):

                url = "https://openapi.naver.com/v1/search/blog?query=" + encText + f"&display=100&sort=sim"
                request = urllib.request.Request(url)
                request.add_header("X-Naver-Client-Id", self.client_id)
                request.add_header("X-Naver-Client-Secret", self.client_secret)
                response = urllib.request.urlopen(request)
                rescode = response.getcode()

                if rescode == 200:
                    response_body = response.read()
                    data = json.loads(response_body.decode('utf-8'))
                    for item in data['items']:
                        writer.writerow({'title': item['title'], 'link': item['link'], 'description': item['description'], 'bloggername': item['bloggername'], 'bloggerlink': item['bloggerlink'], 'postdate': item['postdate']})
                    count += 1
                    print(f"API 호출 및 {text}에 대한 {count * 100}개의 검색 데이터 저장 완료.")
                else:
                    print(f"API 호출 실패: start={start}, 응답 코드={rescode}")

    def crawl_links(self, csv_file, output_file, i):
        # 쿠키 파일 경로
        cookie_path = fr'C:\Users\art\Desktop\cookie\cookies{i}.txt'
        
        chrome_options = Options()
        chrome_options.add_argument("--lang=ko-KR,ko;q=0.9")
        user = random.choice(user_agents)

        #chrome_options.add_argument("--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36")
        # 쿠키 파일 경로 설정
        chrome_options.add_argument(f"--user-data-dir={cookie_path}")

        # chrome_options.add_argument("--headless") # 크롬 창이 나타나지 않는 설정
        service = Service(executable_path=r"크롬 드라이버 경로")

        driver = webdriver.Chrome(service=service, options=chrome_options)

        df = pd.read_csv(csv_file)
        blog_links = df['link'].tolist()

        contents = []
        count = 0
        
        try:
            for link in tqdm(blog_links, desc="Crawling", unit="link", mininterval=60):
                #start_time = time.time()  # 시작 시간 기록
                driver.get(link)

                time.sleep(2)
                driver.switch_to.frame("mainFrame")
                count += 1
                try:
                    #table_exists = driver.find_elements(By.CSS_SELECTOR, 'table')
                    #if len(table_exists) > 0:
                        #continue
                    a = driver.find_element(By.CSS_SELECTOR, 'div.se-main-container').text
                    contents.append(a)
                except NoSuchElementException:
                    a = driver.find_element(By.CSS_SELECTOR, 'div#content-area').text
                    contents.append(a)
                    continue
                except:
                    print('내용 없음 다음으로 진행')
                    contents.append('')  # 내용이 없을 경우 빈 문자열 추가
                    continue
        finally:
            driver.quit()

            df['content'] = contents
            if os.path.isfile(output_file):
                existing_data = pd.read_csv(output_file)
                combined_data = pd.concat([existing_data, df])
                combined_data.to_csv(output_file, index=False, encoding='utf-8-sig')
            else:
                df.to_csv(output_file, index=False, encoding='utf-8-sig')

            print(f"크롤링 완료: {count} 링크에 대한 본문 내용 추출됨.")
                
#     def preprocess_links(self, csv_file, blacklist_file):
#         # CSV 파일 읽기
#         df = pd.read_csv(csv_file)

#         # 'https://blog.naver.com/'로 시작하지 않는 링크 제거
#         df = df[df['link'].str.startswith('https://blog.naver.com/')]

#         # 중복된 링크 제거
#         df = df.drop_duplicates(subset=['link'], keep='first')
        
#         # 블랙리스트 CSV 파일 읽기
#         blacklist = pd.read_csv(blacklist_file)

#         # 블랙리스트에 포함된 링크 제거
#         df = df[~df['link'].str.startswith(blacklist['link'])]

#         # 수정된 데이터프레임을 새로운 CSV 파일로 저장
#         df.to_csv(csv_file, index=False, encoding='utf-8-sig')

#         print(f"Naver blog 링크의 수: {len(df['link'])}")
#         return len(df['link'])

    def preprocess_links(self, csv_file, blacklist_file):
        # CSV 파일 읽기
        df = pd.read_csv(csv_file)

        # 'https://blog.naver.com/'로 시작하지 않는 링크 제거
        df = df[df['link'].str.startswith('https://blog.naver.com/')]

        # 중복된 링크 제거
        df = df.drop_duplicates(subset=['link'], keep='first')
        
        # 블랙리스트 CSV 파일 읽기
        blacklist = pd.read_csv(blacklist_file)

        # 블랙리스트에 포함된 링크 제거
        blacklist_links = blacklist['link'].tolist()  # 블랙리스트 DataFrame의 'link' 열을 리스트로 변환
        df = df[~df['link'].str.startswith(tuple(blacklist_links))]  # 블랙리스트에 포함된 링크 제거

        # 수정된 데이터프레임을 새로운 CSV 파일로 저장
        df.to_csv(csv_file, index=False, encoding='utf-8-sig')

        print(f"Naver blog 링크의 수: {len(df['link'])}")
        return len(df['link'])

    def extract_columns(self, csv_file):
        print("데이터 정제 시작... 불필요한 열 제거 중...")
        # CSV 파일 읽기
        df = pd.read_csv(csv_file)

        # 필요한 열만 선택
        columns_to_extract = ['시도', '시군구', 'code', 'title', 'content']
        df = df[columns_to_extract]
        df = df[df['content'].str.strip() != '']
        
        # content 값이 없는 행 제거
        df = df.dropna(subset=['content'])        
        
        # 수정된 데이터프레임을 기존 CSV 파일로 덮어씌우기
        df.to_csv(csv_file, mode='w', index=False, encoding='utf-8-sig')
        print('데이터 정제 및 불필요한 열 제거 완료')

    def search(self, search_words, link_file_name, search_count, blacklist_file):
        # 코드 실행
        for word in search_words:
            self.search_and_save_api_results(word, link_file_name, search_count)
        i = self.preprocess_links(link_file_name, blacklist_file)
        print(f'\n{i}개의 링크에 대해서 크롤링 시작.')
  
    def crawling(self,link_file_name, result_file_name):
        start_time = time.time()
        i = 0
        self.crawl_links(link_file_name, result_file_name, i)  
        self.extract_columns(result_file_name)

        # 총 실행 시간 계산
        execution_time = time.time() - start_time

        # 시, 분, 초로 변환
        minutes, seconds = divmod(execution_time, 60)
        hours, minutes = divmod(minutes, 60)

        # 시간을 시, 분, 초 형식으로 출력
        print(f"Total execution time: {int(hours)}시 {int(minutes)}분 {int(seconds)}초")