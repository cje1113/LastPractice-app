import streamlit as st
import pandas as pd
import re

st.title("🧹 데이터 전처리 과정")

st.markdown("""
수집된 뉴스 데이터는 텍스트 분석에 적합하도록  
여러 단계의 전처리 과정을 거쳐 정제하였다.

이 과정은 워드클라우드 및 키워드 네트워크 분석의  
품질을 높이기 위한 필수 단계이다.
""")

st.divider()

st.subheader("📄 데이터 로드")

st.echo()
def load_data():
    df = pd.read_csv("data/news.csv")
    return df

df = load_data()

st.write("데이터 미리보기")
st.dataframe(df.head())

st.divider()

st.subheader("✂️ 텍스트 정제 (Cleaning)")
st.echo()
def clean_text(text):
    # 한글과 공백만 남기기
    text = re.sub(r'[^가-힣\\s]', '', str(text))
    return text

df['clean_description'] = df['description'].apply(clean_text)

st.write("정제된 텍스트 예시")
st.write(df['clean_description'].head())

st.divider()

st.subheader("🚫 불용어 제거")
st.code("""
with open('data/korean_stopwords.txt', 'r', encoding='utf-8') as f:
    stopwords = set(f.read().splitlines())

custom_stopwords = {'기후', '변화', '기후변화', '문제', '영향'}
stopwords.update(custom_stopwords)
""", language="python")

st.markdown("""
- 의미가 약한 조사 및 일반 표현 제거  
- 기후 변화 기사에서 반복적으로 등장하는 도메인 단어 제거  
""")

st.divider()

st.subheader("📊 전처리 결과 요약")

st.markdown("""
위와 같은 전처리 과정을 통해  
텍스트 분석에 불필요한 요소를 제거하고,  
핵심 키워드가 보다 명확히 드러나도록 데이터를 정제하였다.

이후 전처리된 텍스트를 활용하여  
워드클라우드 및 키워드 네트워크 분석을 수행하였다.
""")