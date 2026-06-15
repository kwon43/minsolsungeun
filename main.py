import streamlit as st

# 각 페이지를 st.Page로 정의
main_page = st.Page(
    "pages/home.py",
    title="홈 - 공정 개요",
    icon="🏠"
)

page1 = st.Page(
    "pages/1_Process_Explorer.py",
    title="공정 탐색기",
    icon="🔍"
)

page2 = st.Page(
    "pages/2_Yield_And_Inspection.py",
    title="중요 공정과 수율",
    icon="📈"
)

# 네비게이션 등록 (이 한 줄이 사이드바를 만들어줌)
pg = st.navigation([main_page, page1, page2])

# 전체 페이지 공통 설정
st.set_page_config(
    page_title="반도체 공정 탐구 앱",
    page_icon="🔬",
    layout="wide"
)

pg.run()
