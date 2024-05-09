import requests
from bs4 import BeautifulSoup

# 타겟 URL을 읽어서 HTML를 받아오고,
headers = {'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'}
data = requests.get('https://serieson.naver.com/v3/broadcasting/ranking/realtime', headers=headers)

# HTML을 BeautifulSoup이라는 라이브러리를 활용해 검색하기 용이한 상태로 만듦
# soup이라는 변수에 "파싱 용이해진 html"이 담긴 상태가 됨
# 이제 코딩을 통해 필요한 부분을 추출하면 된다.
soup = BeautifulSoup(data.text, 'html.parser')


dramas = soup.select('#container > div.RankingPage_ranking_wrap__GB855 > ol')


for drama in dramas:
# get an attribute from a tag
    tag_element = drama.select(' * > img') 
    for i in range(len(tag_element)):
        name = tag_element[i].get('alt')
        print(name)
        #   find('img').get('alt'))
    




    # if not tag_element:
    #     continue
    # print(tag_element)
    
    # title = tag_element.string.strip()

