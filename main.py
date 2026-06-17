import streamlit as st
import pandas as pd
import os

# 💡 페이지 전체 설정은 메인 파일인 main.py에서만 '단 한 번만' 선언합니다.
st.set_page_config(
    page_title="반도체 공정 및 수율 탐구",
    page_icon="🔬",
    layout="wide"
)

# 데이터 로드 함수 (한글 깨짐 해결 포함)
@st.cache_data
def load_data():
    file_name = "한국나노기술원_공정 정보_20260226.csv"
    if not os.path.exists(file_name):
        return None
    try:
        df = pd.read_csv(file_name, encoding='utf-8-sig')
    except UnicodeDecodeError:
        try:
            df = pd.read_csv(file_name, encoding='cp949')
        except Exception:
            return None
    df.columns = ['기관명', '공정코드', '공정명', '공정그룹코드', '공정그룹']
    return df

df = load_data()

st.title("🔬 한국나노기술원 데이터를 활용한 반도체 공정 탐구")
st.subheader("당곡고등학교 학생들을 위한 반도체 공정 학습 가이드")

st.markdown("""
반도체는 현대 과학기술의 정점입니다.  
모래(규소)에서 시작해 우리가 사용하는 스마트폰과 컴퓨터의 두뇌인 칩이 되기까지,  
수백 가지의 정밀한 공정을 거치게 됩니다.

이 웹앱은 **한국나노기술원의 실제 공정 데이터**를 바탕으로,  
반도체 제조 공정의 구조를 이해하고 수율을 높이기 위해 어떤 기술들이 사용되는지  
스스로 분석해 볼 수 있도록 설계되었습니다.
""")

if df is not None:
    st.success(f"✅ 데이터 로드 완료! 현재 데이터베이스에 등록된 총 공정 수: **{len(df)}개**")

    col1, col2 = st.columns(2)

    with col1:
        st.write("### 📌 데이터 미리보기 (상위 10개 행)")
        st.dataframe(df.head(10), use_container_width=True)

    with col2:
        st.write("### 🔍 주요 공정그룹별 등록 분포")
        group_counts = df['공정그룹'].value_counts()
        st.bar_chart(group_counts)

    st.markdown("""
    ### 🧭 탐구 안내
    왼쪽 사이드바에 Streamlit이 자동으로 감지한 페이지 메뉴가 생성되었습니다!
    사이드바의 메뉴를 클릭하여 탐구를 이어가 보세요.
    
    1. **1 Process Explorer (공정 탐색기)**: 포토공정, 식각공정 등 반도체 핵심 공정들을 찾아보세요.
    2. **2 Yield And Inspection (중요 공정과 수율)**: 수율 관리를 위해 실제 현장에서 쓰이는 검사/분석 단계를 확인해보세요.
    """)
else:
    st.error("❌ CSV 데이터를 로드할 수 없습니다. 파일명이 `한국나노기술원_공정 정보_20260226.csv`가 맞는지 확인해 주세요.")
