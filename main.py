import streamlit as st

st.set_page_config(
    page_title="반도체 공정 탐구 앱",
    page_icon="🔬",
    layout="wide"
)

# 💡 중요: pages 폴더 안의 실제 영문 파일명과 100% 일치해야 에러가 나지 않습니다!
page1 = st.Page(
    "pages/1_Process_Explorer.py",  # 실제 파일명
    title="공정 탐색기",             # 화면에 표시될 제목
    icon="🔍"
)

page2 = st.Page(
    "pages/2_Yield_And_Inspection.py", # 실제 파일명
    title="중요 공정과 수율",            # 화면에 표시될 제목
    icon="📈"
)

# 사이드바 네비게이션 설정
pg = st.navigation([page1, page2])
pg.run()
