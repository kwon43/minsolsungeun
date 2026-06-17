import streamlit as st

# 1. 페이지 전체 설정 (main.py에서 단 한 번만 선언)
st.set_page_config(
    page_title="반도체 공정 및 수율 탐구",
    page_icon="🔬",
    layout="wide"
)

# 2. 파이썬 표준 임포트 방식으로 다른 파일들로부터 페이지 함수들을 가져옵니다.
# 이 방식은 서버 내 파일 경로 에러를 완벽하게 방지합니다!
try:
    from pages.explorer import show_explorer_page
    from pages.yield_analysis import show_yield_page
except ModuleNotFoundError as e:
    st.error(f"❌ 폴더 구조나 파일 이름이 올바르지 않습니다. 에러: {e}")
    st.info("💡 깃허브에 'pages' 폴더가 소문자로 존재하고, 그 안에 'explorer.py'와 'yield_analysis.py' 파일이 정확히 올라갔는지 조장님과 확인해주세요!")
    st.stop()

# 3. 가져온 함수들을 각각의 서브 페이지로 등록합니다.
page1 = st.Page(
    show_explorer_page,
    title="공정 탐색기",
    icon="🔍"
)

page2 = st.Page(
    show_yield_page,
    title="중요 공정과 수율",
    icon="📈"
)

# 4. 네비게이션 생성 (무조건 왼쪽 사이드바가 활성화됩니다!)
pg = st.navigation([page1, page2])
pg.run()
