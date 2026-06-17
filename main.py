import streamlit as st

# 1. 페이지 전체 설정 (main.py에서 단 한 번만 선언)
st.set_page_config(
    page_title="반도체 공정 및 수율 탐구",
    page_icon="🔬",
    layout="wide"
)

# 2. 최상위 폴더에 있는 파이썬 파일들로부터 페이지 함수들을 가져옵니다.
try:
    from explorer import show_explorer_page
    from yield_analysis import show_yield_page
except ModuleNotFoundError as e:
    st.error(f"❌ 파일을 찾을 수 없습니다. 에러: {e}")
    st.info("💡 깃허브 최상위 폴더에 'explorer.py'와 'yield_analysis.py' 파일이 정상적으로 올라갔는지 확인해 주세요!")
    st.stop()

# 3. 가져온 함수들을 st.Page 형태로 사이드바 메뉴에 등록합니다.
page_explorer = st.Page(
    show_explorer_page,
    title="반도체 세부 공정 탐색기",  # 1번째 페이지 제목 설정
    icon="🔍",
    default=True                   # 첫 화면(기본값)으로 지정
)

page_yield = st.Page(
    show_yield_page,
    title="중요 공정과 수율",         # 2번째 페이지 제목 설정
    icon="📈"
)

# 4. 네비게이션 적용 (이 코드가 왼쪽 사이드바를 무조건 생성해 줍니다!)
pg = st.navigation([page_explorer, page_yield])
pg.run()
