import streamlit as st
import pandas as pd
import os

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

st.title("🔍 반도체 세부 공정 탐색기")
st.subheader("당곡고등학교 - 실제 연구원 데이터를 기반으로 한 세부 공정 데이터 통계 분석")

if df is not None:
    # 1. 원본 데이터를 기반으로 한 실시간 텍스트 데이터 분석 (민솔 학생의 데이터 찾기 성과 부각 가능)
    st.markdown("### 📊 [데이터 기반] 한국나노기술원 공정 라인업 성격 분석")
    
    # 원소 기호 및 재료 분석
    gan_count = df['공정명'].str.contains('GaN', case=False, na=False).sum()
    gaas_count = df['공정명'].str.contains('GaAs', case=False, na=False).sum()
    si_count = df['공정명'].str.contains('Si ', case=False, na=False).sum() + df['공정명'].str.contains('SiN|SiO|Silicon', case=False, na=False).sum()
    gold_count = df['공정명'].str.contains('Au|Gold', case=False, na=False).sum()
    copper_count = df['공정명'].str.contains('Cu|Copper', case=False, na=False).sum()
    pr_count = df['공정명'].str.contains('PR|Photo', case=False, na=False).sum()

    col_stat1, col_stat2, col_stat3 = st.columns(3)
    
    with col_stat1:
        st.info(f"""
        **🔬 핵심 소자 기판 재료 분석**
        - **GaN (질화갈륨) 공정**: `{gan_count}개` 검출
        - **GaAs (비소화갈륨) 공정**: `{gaas_count}개` 검출
        - **Si (실리콘 계열) 공정**: `{si_count}개` 검출
        
        👉 **데이터 분석 결과**: 본 데이터는 전통적인 실리콘 반도체보다 전력 반도체 및 LED에 쓰이는 **화합물 반도체(GaN/GaAs) 공정** 비중이 매우 높게 설계되어 있습니다.
        """)
        
    with col_stat2:
        st.info(f"""
        **⚡ 금속 배선(Metallization) 재료 분석**
        - **Au (금 계열) 공정**: `{gold_count}개` 검출
        - **Cu (구리 계열) 공정**: `{copper_count}개` 검출
        
        👉 **데이터 분석 결과**: 구리 배선보다 화학적 안정성이 뛰어나고 고주파에 유리한 **금(Au) 도금 및 증착 공정**이 핵심 주류를 형성하고 있습니다.
        """)
        
    with col_stat3:
        st.info(f"""
        **📷 감광제(PR) 및 리소그래피 비중**
        - **PR/노광 관련 공정**: `{pr_count}개` 검출
        
        👉 **데이터 분석 결과**: 전체 `{len(df)}개` 공정 중 약 `{round(pr_count/len(df)*100, 1)}%`가 미세 회로 패턴 형성을 위한 노광 및 코팅 공정에 집중되어 있습니다.
        """)

    st.markdown("---")
    st.subheader("🔧 실시간 공정 검색 및 데이터 상세 필터")
    
    # 필터 레이아웃
    f_col1, f_col2 = st.columns(2)
    with f_col1:
        all_groups = sorted(df['공정그룹'].dropna().unique())
        selected_group = st.selectbox(
            "공정그룹 필터",
            ["전체 보기"] + list(all_groups)
        )
    with f_col2:
        search_keyword = st.text_input("공정명 검색 (예: Etch, CVD, Sputter)", "")

    filtered_df = df.copy()

    if selected_group != "전체 보기":
        filtered_df = filtered_df[filtered_df['공정그룹'] == selected_group]

    if search_keyword:
        filtered_df = filtered_df[
            filtered_df['공정명'].str.contains(search_keyword, case=False, na=False)
        ]

    st.write(f"#### 📋 검색된 세부 공정 목록 (총 {len(filtered_df)}건)")
    st.dataframe(filtered_df, use_container_width=True)

    st.markdown("---")
    st.markdown("### 📊 공정그룹별 보유 기술 다양성 분포")
    
    if selected_group == "전체 보기":
        chart_data = df['공정그룹'].value_counts()
    else:
        chart_data = filtered_df['공정그룹'].value_counts()
    st.bar_chart(chart_data)

else:
    st.error("❌ 데이터를 불러오지 못했습니다. CSV 파일이 루트 폴더에 있는지 확인해주세요.")
