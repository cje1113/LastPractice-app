import streamlit as st

# 페이지 설정
st.set_page_config(
    page_title = '기후변화 대시보드',  # 페이지 tab 타이틀
    page_icon = '🌐',   # 페이지 tab의 아이콘
    layout = 'wide',    # 페이지 전체 폭: centered(기본값, 콘텐츠가 가운데 정렬), wide(화면 전체 폭을 넓게 사용)
    # 사이드바 초기 상태(스트림릿 실행 시 사이드바를 기본으로 어떻게 표시): auto, collapsed(실행 시 접혀 있음), expanded(실행하자마자 사이드바가 펼쳐짐)
    initial_sidebar_state = 'expanded'
)

st.title("🌍 이슈파인더: 기후 변화 여론 분석 대시보드")

st.markdown("""
**이슈파인더(Issue Finder)**는  
기후 변화와 관련된 뉴스 데이터를 분석하여  
사회적 이슈에 대한 여론의 전반적인 흐름과 핵심 키워드를  
한눈에 탐색할 수 있도록 설계된 여론 분석 대시보드입니다.

이 대시보드는 텍스트 데이터 분석을 기반으로  
기후 변화와 함께 자주 언급되는 주요 키워드를 시각화하고,  
키워드 간의 관계를 네트워크 형태로 표현하여  
이슈 구조를 직관적으로 이해할 수 있도록 돕습니다.
""")

st.divider()

import pandas as pd
@st.cache_data
def load_data():
    df = pd.read_csv("data/news.csv")
    return df

df = load_data()

st.subheader("📊 데이터 개요")

st.markdown("""
본 분석에 사용된 데이터는  
**네이버 뉴스 검색 API**를 통해 수집한  
기후 변화 관련 뉴스 기사 텍스트입니다.
""")

st.write("- **수집 키워드**: 기후 변화")
st.write("- **데이터 출처**: 네이버 뉴스")
st.write(f"- **총 기사 수**: {len(df)}건")
st.write(
    f"- **기사 발행 기간**: "
    f"{df['pubDate'].min()} ~ {df['pubDate'].max()}"
)
st.write('- **데이터 구성**: 기사 발행 시각, 기사 제목, 기사 요약/본문')

st.markdown("### 🔍 데이터 미리보기")
st.dataframe(df.head())

st.divider()

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from wordcloud import WordCloud
import re
import os

# -----------------------------
# 1️⃣ 분석 텍스트 준비
# -----------------------------
text_title = ' '.join(df['title'].astype(str).tolist())

def cleanString(text):
    # 한글 자음/모음 제거
    text = re.sub(r'[ㄱ-ㅎㅏ-ㅣ]+', '', text)
    # HTML 태그 제거
    text = re.sub(r'<[^>]*>', '', text)
    # 특수문자 제거
    text = re.sub(r'[^\w\s]', '', text)
    return text

text_title = cleanString(text_title)

# -----------------------------
# 2️⃣ 불용어 로드 + 추가
# -----------------------------
with open('data/korean_stopwords.txt', 'r', encoding='utf-8') as f:
    stopwords = set(f.read().splitlines())

stop_str = """
기후 변화 기후변화 문제 영향 대응 위기 관련 분야 상황 사회 정부 정책
전문가 연구 발표 최근 이날 이번 가능성 필요 강조
에 가 이은 을 를 의 도 또한 더 위해 에게 에게서 에게로 부터
어 우선 간 이후 하는 입니다 할 예정
"""
stopwords.update(stop_str.split())

# -----------------------------
# 3️⃣ 한글 폰트 설정 (Streamlit Cloud 대응)
# -----------------------------
font_path = None
if os.path.exists("fonts/NotoSansKR-Regular.ttf"):
    font_path = "fonts/NotoSansKR-Regular.ttf"

# -----------------------------
# 4️⃣ 워드클라우드 생성
# -----------------------------
wc = WordCloud(
    font_path=font_path,        # 로컬/클라우드 모두 안전
    max_words=50,
    width=800,
    height=800,
    stopwords=stopwords,
    background_color='black',
    colormap='coolwarm'
).generate(text_title)

# -----------------------------
# 5️⃣ Streamlit 출력
# -----------------------------
st.subheader("🔑 기후 변화 뉴스 핵심 키워드 워드클라우드")
st.markdown("""
본 워드클라우드는 기후 변화 관련 뉴스 기사 텍스트에서
자주 등장하는 핵심 키워드를 빈도 기반으로 시각화한 결과이다.
단어의 크기는 기사 내 등장 빈도를 의미하며,
이를 통해 기후 변화 이슈와 함께 반복적으로 언급되는 주요 개념을
직관적으로 파악할 수 있다.
""")
st.markdown("""
불용어 제거 및 텍스트 정제 과정을 거쳐
의미가 중복되거나 정보량이 낮은 단어를 제외함으로써,
기후 변화 이슈의 핵심 주제가 보다 명확히 드러나도록 구성하였다.
""")

fig, ax = plt.subplots(figsize=(7, 7))
ax.imshow(wc)
ax.axis("off")
st.pyplot(fig)

st.divider()

st.subheader("🕸️ 기후 변화 키워드 네트워크")
st.markdown("""
본 키워드 네트워크 그래프는 기후 변화 관련 뉴스 기사에서
함께 등장한 키워드 간의 관계를 동시 출현 빈도를 기반으로
네트워크 형태로 시각화한 결과이다.
각 노드는 키워드를 의미하며,
엣지는 동일 기사 내에서 두 키워드가 함께 언급된 관계를 나타낸다.
""")
st.markdown("""
엣지의 두께는 키워드 간 동시 등장 빈도를 의미하며,
이를 통해 기후 변화 이슈 내에서
서로 밀접하게 연결된 주제 군집을 파악할 수 있다.
""")

st.image(
    "data/keyword_network.png",
    caption="기후 변화 뉴스 키워드 동시 출현 네트워크",
    use_column_width=True
)
st.markdown("""
네트워크 시각화는 분석 환경의 제약을 고려하여
사전에 생성된 시각화 결과 이미지를 활용하였으며,
분석 결과의 전달과 해석에 초점을 맞추어 웹 애플리케이션에 포함하였다.
""")
