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

st.title("📈 중요 공정과 수율")

st.warning("""
🚨 **데이터 특징 안내**  
제공해주신 '한국나노기술원 공정 정보' 데이터는 공정 종류를 정의한 마스터 코드 데이터입니다.  
수율 수치(%)나 불량률 등의 구체적인 정량 데이터는 보안상 포함되어 있지 않습니다.  
하지만 수율을 관리하기 위한 **'검사(INSPECTION)'**, **'테스트(PROBE TEST/RELIABILITY TEST)'**,  
**'고장 분석(FAILURE)'**, **'계측(MEASUREMENT)'** 공정이 매우 정밀하게 등록되어 있어 이를 깊이 알아봅니다.
""")

if df is not None:
    st.markdown("---")
    st.markdown("## 1️⃣ 수율(Yield)이란 무엇인가?")

    col1, col2 = st.columns(2)

    with col1:
        st.info("""
        **수율(Yield)의 정의**

        웨이퍼 1장에서 만들어지는 전체 칩 중  
        **정상적으로 작동하는 완성품 칩의 비율**을 뜻합니다.

        > 수율(%) = (양품 칩 수 ÷ 전체 칩 수) × 100
        """)

    with col2:
        st.info("""
        **수율이 왜 중요할까요?**

        반도체 1장의 웨이퍼 가격은 수십만 원에서 수백만 원에 달합니다.  
        수율이 단 1%만 떨어져도 기업에는 막대한 손실이 발생합니다.  
        따라서 가공 중간에 불량을 잡아내어 가치가 없는 칩에 후속 공정 비용이 들어가는 것을 막아야 합니다.
        """)

    st.markdown("---")
    st.markdown("## 2️⃣ 우리 데이터 속 수율 관리 공정 분석")

    yield_related_groups = [
        'INSPECTION',
        'PROBE TEST',
        'RELIABILITY TEST',
        'FAILURE',
        'MEASUREMENT&ANALYSIS',
        'SURFACE'
    ]

    yield_df = df[df['공정그룹'].isin(yield_related_groups)]

    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("수율 관리 관련 공정 수", f"{len(yield_df)}개")
    with col2:
        st.metric("전체 공정 대비 비율", f"{round(len(yield_df)/len(df)*100, 1)}%")
    with col3:
        st.metric("수율 관련 공정그룹 수", f"{len(yield_related_groups)}개")

    st.markdown("---")

    col_a, col_b = st.columns([1, 2])
    with col_a:
        st.write("#### 📊 수율 관련 공정그룹별 공정 수")
        yield_counts = yield_df['공정그룹'].value_counts()
        st.bar_chart(yield_counts)

    with col_b:
        st.write("#### 🔍 세부 수율 관리 공정 목록")
        selected_yield_group = st.selectbox(
            "탐구할 공정 영역을 선택하세요",
            yield_related_groups
        )
        specific_yield_df = yield_df[yield_df['공정그룹'] == selected_yield_group]
        st.dataframe(
            specific_yield_df[['공정코드', '공정명', '공정그룹']],
            use_container_width=True
        )
        
    st.markdown("---")
    st.markdown("## 3️⃣ 각 공정이 수율에 미치는 영향")

    tab1, tab2, tab3 = st.tabs([
        "🧐 계측 및 검사 (INSPECTION)",
        "⚡ 전기 및 신뢰성 테스트 (PROBE/RELIABILITY)",
        "🔬 불량 추적 및 분석 (SURFACE/FAILURE)"
    ])

    with tab1:
        st.markdown("""
        **1. INSPECTION (검사/계측 공정)의 역할**
        - **데이터 속 실제 공정 예시**: `CD Measure` (선폭 측정), `Thickness Measure` (두께 측정)
        - **수율에 미치는 영향**:  
          회로 선폭이 조금이라도 어긋나면 저항이 바뀌어 오작동하거나 회로가 끊어집니다.  
          수시로 크기를 **계측**하여 규격 밖의 결함을 차단함으로써 최종 수율을 보호합니다.
        """)

    with tab2:
        st.markdown("""
        **2. PROBE & RELIABILITY TEST (테스트)의 역할**
        - **데이터 속 실제 공정 예시**: `DC Parametric Test`, `HAST` (고온고습시험), `Thermal Shock` (열충격 시험)
        - **수율에 미치는 영향**:
          - **PROBE TEST**: 가공이 끝난 웨이퍼 상태에서 전기 침으로 찔러 불량 칩을 후속 패키징 공정에 보내는 낭비를 막습니다.
          - **RELIABILITY TEST**: 가혹한 조건(고열, 충격)을 가해 미래에 발생할 잠재 불량을 차단합니다.
        """)

    with tab3:
        st.markdown("""
        **3. SURFACE & FAILURE (표면 및 불량 분석)의 역할**
        - **데이터 속 실제 공정 예시**: `X-ray 3D CT`, `Decapsulation` (칩 개봉)
        - **수율에 미치는 영향**:  
          갑작스러운 수율 하락 시 3D CT나 XPS 같은 분석 장비로 오염 원인을 파악하고 장비를 수정할 수 있는 길을 열어줍니다.
        """)

    st.markdown("---")
    st.markdown("### 🏫 스스로 생각하기 질문")
    st.info("""
    🤔 **당곡고 토론 질문**:  
    `F4B001 GaAs Dry Etch` (건식 식각) 공정을 마친 직후, 깊이가 올바르게 깎였는지 신속히 검증하려면  
    어떤 공정을 연이어 수행하는 것이 수율 모니터링에 가장 효과적일까요?  
    - 힌트: `INSPECTION` 카테고리 중 깊이(Depth)를 재는 공정을 데이터에서 검색해 찾아보세요!
    """)

else:
    st.error("데이터를 불러오지 못했습니다.")
