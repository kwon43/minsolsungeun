import streamlit as st
import pandas as pd
import os

# 페이지 설정
st.set_page_config(
    page_title="반도체 공정 탐구 앱",
    page_icon="🔬",
    layout="wide"
)

# 데이터 로드 함수
@st.cache_data
def load_data():
    file_name = "한국나노기술원_공정 정보_20260226.csv"
    if not os.path.exists(file_name):
        st.error(f"'{file_name}' 파일이 존재하지 않습니다. 파일을 프로젝트 루트 폴더에 넣어주세요.")
        return None
    try:
        # 인코딩 오류가 발생할 수 있으므로 utf-8-sig 또는 cp949 시도
        df = pd.read_csv(file_name, encoding='utf-8-sig')
    except UnicodeDecodeError:
        df = pd.read_csv(file_name, encoding='cp949')
    
    # 깨진 열 이름을 표준 한글 열 이름으로 강제 변환
    df.columns = ['기관명', '공정코드', '공정명', '공정그룹코드', '공정그룹']
    return df

# 데이터 불러오기
df = load_data()

# 메인 화면 구성
st.title("🔬 한국나노기술원 데이터를 활용한 반도체 공정 탐구")
st.subheader("당곡고등학교 학생들을 위한 반도체 공정 학습 가이드")

st.markdown("""
반도체는 현대 과학기술의 정점입니다. 모래(규소)에서 시작해 우리가 사용하는 스마트폰과 컴퓨터의 두뇌인 칩이 되기까지, 수백 가지의 정밀한 공정을 거치게 됩니다.

이 웹앱은 **한국나노기술원의 실제 공정 데이터**를 바탕으로, 반도체 제조 공정의 구조를 이해하고 수율을 높이기 위해 어떤 기술들이 사용되는지 스스로 분석해 볼 수 있도록 설계되었습니다.
""")

if df is not None:
    st.info(f"📊 현재 데이터베이스에 등록된 총 공정 수: **{len(df)}개**")
    
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
    왼쪽 사이드바의 메뉴를 통해 원하는 분석 페이지로 이동할 수 있습니다.
    
    1. **`1 Process Explorer` (공정 탐색기)**: 포토공정, 식각공정 등 반도체 핵심 8대 공정과 관련된 다양한 실제 세부 공정들을 찾아보고 비교해보세요.
    2. **`2 Yield And Inspection` (중요 공정과 수율)**: 제공된 공정 데이터에서 '수율(Yield)'을 지키기 위해 활용하는 계측, 검사, 신뢰성 테스트 공정이 무엇이 있는지 확인하고 수율 관리에 대해 고민해 봅시다.
    """)
else:
    st.warning("데이터를 불러오지 못했습니다. CSV 파일명을 다시 한번 확인해주세요.")
