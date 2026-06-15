import streamlit as st

st.set_page_config(
    page_title="반도체 공정 탐구 앱",
    page_icon="🔬",
    layout="wide"
)

# pages 폴더 안의 두 파일을 명시적으로 등록
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

# 사이드바 네비게이션 생성
pg = st.navigation([page1, page2])
pg.run()
