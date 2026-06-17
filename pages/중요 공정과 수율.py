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
st.subheader("당곡고등학교 - 데이터를 활용한 가상 반도체 제조 공정 수율 시뮬레이션")

if df is not None:
    # 1. 데이터 현황 요약 카드
    yield_groups = ['INSPECTION', 'PROBE TEST', 'RELIABILITY TEST', 'FAILURE', 'MEASUREMENT&ANALYSIS', 'SURFACE']
    yield_df = df[df['공정그룹'].isin(yield_groups)]
    
    st.success(f"📌 한국나노기술원 전체 공정 중 **품질 및 수율 관리용 특수 공정**은 총 **{len(yield_df)}개**가 정의되어 있습니다.")

    st.markdown("---")
    st.markdown("## ⚙️ 나만의 반도체 공정 라인 설계하기")
    st.write("실제 데이터에 등록된 공정을 순서대로 선택하여 가상의 반도체를 생산해 보세요. **공정 설계 결과에 따른 정량적 수율 분석 보고서가 즉시 출력됩니다.**")

    # 선택 단계 구성 (실제 CSV의 공정코드와 공정명을 연동)
    col1, col2, col3, col4, col5 = st.columns(5)
    
    # 선택을 돕기 위해 원본 데이터 슬라이싱
    wafer_steps = df[df['공정그룹'].isin(['MATERIAL PROPERTY', 'EPITAXY(MOCVD)', 'EPITAXY(MBE)', 'LIFT-OFF'])]
    photo_steps = df[df['공정그룹'].isin(['COAT/DEVELOP', 'EXPOSURE'])]
    etch_steps = df[df['공정그룹'].isin(['ICP', 'RIE', 'WET-BENCH'])]
    insp_steps = df[df['공정그룹'].isin(['INSPECTION', 'MEASUREMENT&ANALYSIS', 'SURFACE'])]
    test_steps = df[df['공정그룹'].isin(['PROBE TEST', 'RELIABILITY TEST', 'ETC'])]

    with col1:
        st.write("**1단계: 소자/웨이퍼 준비**")
        step1_opt = wafer_steps['공정명'].tolist()
        step1 = st.selectbox("공정 선택", step1_opt if step1_opt else ["Epitaxy"], key="s1")
        
    with col2:
        st.write("**2단계: 패턴 형성 (포토)**")
        step2_opt = photo_steps['공정명'].tolist()
        step2 = st.selectbox("공정 선택", step2_opt if step2_opt else ["PR Coating"], key="s2")
        
    with col3:
        st.write("**3단계: 물리 가공 (식각)**")
        step3_opt = etch_steps['공정명'].tolist()
        step3 = st.selectbox("공정 선택", step3_opt if step3_opt else ["wet etching"], key="s3")
        
    with col4:
        st.write("**4단계: 품질 계측 (검사)**")
        step4_opt = insp_steps['공정명'].tolist()
        # 사용자가 검사를 건너뛰는 상황(무검사)도 수율 리스크 분석을 위해 추가
        step4 = st.selectbox("공정 선택", ["검사 없음 (생략)"] + step4_opt, key="s4")
        
    with col5:
        st.write("**5단계: 최종 품질 검증 (테스트)**")
        step5_opt = test_steps['공정명'].tolist()
        step5 = st.selectbox("공정 선택", ["테스트 없음 (생략)"] + step5_opt, key="s5")

    # ==========================================================
    # 🚨 [데이터 기반 핵심 수학 모델링] 수율 리스크 연산 알고리즘
    # ==========================================================
    # 기본 물리적 가공 수율 (식각, 패턴의 난이도에 따라 기본 수율 설정)
    base_yield = 0.96  # 기본 96%
    yield_penalty = 0.0
    defect_detect_rate = 0.0
    shipped_reliability = 0.0
    report_logs = []

    # 1단계 분석
    if "Epitaxy" in step1:
        base_yield -= 0.01  # 에피성장은 난이도가 있어 초기 수율 95% 시작
        report_logs.append("• [에피택시] 화학적 증착 특성으로 인해 초기 미세 결정 결함 유발 가능성 존재 (+1% 결함 발생)")

    # 2단계 포토 분석
    if "KrF Stepper" in step2:
        base_yield += 0.02  # 고성능 정밀 장비 사용으로 불량 감소
        report_logs.append("• [KrF 노광] 미세 패턴 안정성 확보로 인한 수율 향상 효과 반영")
    elif "i-Line" in step2:
        report_logs.append("• [i-Line 노광] 범용 장비 사용으로 표준 오차 수준 수율 유지")

    # 3단계 식각 분석
    if "Dry Etch" in step3 or "ICP" in step3:
        base_yield -= 0.02  # 건식 식각은 플라즈마 충격(Plasma Damage) 리스크 존재
        report_logs.append("• [건식 식각] 이온 물리 충격에 의한 박막 표면 물리 결함(Plasma Damage) 리스크 발생")
    elif "wet etching" in step3:
        base_yield -= 0.04  # 습식은 등방성 식각에 의한 패턴 무너짐 리스크가 더 큼
        report_logs.append("• [습식 식각] 등방성 가공 성질로 인한 회로 선폭 패턴 정밀도 하락 리스크 반영 (+4% 결함 가능성)")

    # 4단계 검사(INSPECTION) 유무에 따른 수율 추적 결과
    if step4 == "검사 없음 (생략)":
        defect_detect_rate = 10.0  # 검사가 없으므로 불량을 잡아낼 확률이 거의 없음
        shipped_reliability = 40.0 # 불량 칩이 그대로 시장에 나가므로 신뢰성 최악
        base_yield -= 0.05         # 결함을 피드백하여 장비를 개선하는 단계가 없으므로 수율 하락
        report_logs.append("• [⚠️ 경고: 검사 생략] 공정 중간 계측 부재로 불량 칩의 원인 식별 불가능 (피드백 제어 상실)")
    else:
        defect_detect_rate = 85.0
        shipped_reliability = 80.0
        report_logs.append(f"• [계측 완료] '{step4}' 수행을 통한 실시간 패턴 두께/선폭 측정 완수. 제조 리스크의 조기 차단 제어 확보")

    # 5단계 테스트(TEST) 유무에 따른 검증 결과
    if step5 == "테스트 없음 (생략)":
        shipped_reliability -= 20.0 # 전기 및 신뢰성 테스트 안 하면 최종 수명 보장 불가능
        report_logs.append("• [⚠️ 경고: 최종 테스트 생략] 미세 회로의 전기적 동작 여부를 가려내지 못해 완성품 품질 리스크 극대화")
    else:
        defect_detect_rate += 10.0
        shipped_reliability = 98.0 if step4 != "검사 없음 (생략)" else 75.0
        report_logs.append(f"• [최종 테스트 완료] '{step5}' 단계의 정밀 칩 스크리닝 진행. 불량 칩의 실시간 격리 및 포장 조립 예방 성공")

    final_yield = max(0, min(100, int(base_yield * 100)))

    # ==========================================================
    # 📊 명확한 수율 시뮬레이션 결과 리포트 출력
    # ==========================================================
    st.markdown("---")
    st.markdown("## 📊 가상 반도체 라인 수율 분석 및 품질 보고서")
    
    col_res1, col_res2, col_res3 = st.columns(3)
    
    with col_res1:
        st.metric(
            label="📈 최종 예상 공정 수율 (Yield)", 
            value=f"{final_yield}%", 
            delta=f"{final_yield - 85}% (기준수율 85% 대비)"
        )
        st.progress(final_yield / 100.0)
        
    with col_res2:
        st.metric(
            label="🔍 불량 칩 사전 감지율 (Defect Detection)", 
            value=f"{int(defect_detect_rate)}%", 
            delta="위험 수준" if defect_detect_rate < 50 else "안전 수준"
        )
        st.progress(defect_detect_rate / 100.0)
        
    with col_res3:
        st.metric(
            label="🔒 최종 출하 제품 품질 신뢰성 (Reliability)", 
            value=f"{int(shipped_reliability)}%", 
            delta="품질 경보" if shipped_reliability < 70 else "최우수 품질"
        )
        st.progress(shipped_reliability / 100.0)

    # 텍스트 기반 정밀 분석 보고서 출력
    st.markdown("### 📋 제조 결함 추적 로그 (Data-Driven Process Logs)")
    for log in report_logs:
        st.write(log)

    st.markdown("---")
    st.markdown("### 🔬 실제 데이터를 통한 공정 결함 해결 토론")
    st.info("""
    💡 **당곡고 토론 리포트 작성 가이드**
    1. **검사와 계측의 중요성**: 왜 공정 단계 중 `INSPECTION`이나 `MEASUREMENT`가 빠졌을 때 최종 수율과 제품 신뢰성이 수직 낙하하는지 위 시뮬레이터 수치 변화를 보며 서술해 보세요.
    2. **공정 복잡도**: 공정 스텝이 추가될수록(식각, 박막 등 물리 공정이 많아질수록) 전체 칩 수율은 각 단계 수율의 곱($Y_{total} = Y_1 \\times Y_2 \\times Y_3 ...$)으로 결정됩니다. 이를 극복하기 위해 검사 장비의 해상도는 왜 끊임없이 올라가야 할까요?
    """)

else:
    st.error("데이터를 불러오지 못했습니다.")
