import pandas as pd
from bs4 import BeautifulSoup

base_url = "https://www.inflearn.com"

account_naver = open("naver.html", "rt", encoding="utf-8").read()
soup = BeautifulSoup(account_naver, "html.parser")

# 강의 정보 추출
course_title = [title.get_text(strip=True) for title in soup.find_all("p", class_="course_title")]
course_link = [base_url + link.find("a")["href"] for link in soup.find_all("div", class_="course-title-wrapper") if link.find("a")]

# 데이터프레임 생성
df = pd.DataFrame({"강의 링크": course_link, "강의명": course_title})

# 필요한 컬럼만 선택
df = df[["강의명", "강의 링크"]]

# 인덱스를 1부터 시작하도록 변경
df.index = df.index + 1

# 엑셀 파일로 저장
df.to_excel("result.xlsx", index_label="인덱스")

print("result.xlsx 파일이 생성되었습니다.")
