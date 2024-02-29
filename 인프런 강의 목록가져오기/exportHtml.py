import pandas as pd
from bs4 import BeautifulSoup

base_url = "https://www.inflearn.com"

account_naver = open("naver.html", "rt", encoding="utf-8").read()
soup = BeautifulSoup(account_naver, "html.parser")

course_title = [title.get_text(strip=True) for title in soup.find_all("p", class_="course_title")]
course_link = [base_url + link.find("a")["href"] for link in soup.find_all("div", class_="course-title-wrapper") if link.find("a")]
course_thumbnails = [figure.img["src"] for figure in soup.find_all("figure", class_="image is_thumbnail")]

# 데이터프레임 생성
df = pd.DataFrame({"강의 링크": course_link, "강의명": course_title, "Course Thumbnails": course_thumbnails} )

df["강의명"] = df.apply(lambda row: f'<a href="{row["강의 링크"]}"  target="_blank"><p>{row["강의명"]}</p>', axis=1)
df["강의 링크"] = df.apply(lambda row: f'<a href="{row["강의 링크"]}"  target="_blank"><img src="{row["Course Thumbnails"]}"></a>', axis=1)

df = df.drop(["Course Thumbnails"], axis=1)

df.index = df.index + 1

html_table = df.to_html(escape=False)

html_template = f"""
<!DOCTYPE html>
<html lang="ko">
<head>
    <meta charset="UTF-8"/>
    <meta name="viewport" content="width=device-width, initial-scale=1.0"/>
    <title>인프런 강의 구매 목록</title>
    <link rel="stylesheet" href="style.css">
</head>
<body>
    <div class="main">
        {html_table}
    </div>
</body>
</html>
"""

with open("result.html", "w", encoding="utf-8") as file:
    file.write(html_template)

print("result.html 파일이 생성되었습니다.")
