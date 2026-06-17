import streamlit as st

# 1. 페이지 전체 설정 (app.py에서 단 한 번만 선언)
st.set_page_config(
    page_title="반도체 공정 및 수율 탐구",
    page_icon="🔬",
    layout="wide"
)

# 2. 깃허브 pages 폴더 안의 한글 파일명을 강제로 매칭합니다.
try:
    page1 = st.Page(
        "pages/반도체 세부 공정 탐색기.py",  # 실제 깃허브 한글 파일명과 100% 일치
        title="반도체 세부 공정 탐색기",      # 사이드바 메뉴에 표시될 한글 이름
        icon="🔍",
        default=True                       # 첫 화면으로 설정
    )

    page2 = st.Page(
        "pages/중요 공정과 수율.py",         # 실제 깃허브 한글 파일명과 100% 일치
        title="중요 공정과 수율",             # 사이드바 메뉴에 표시될 한글 이름
        icon="📈"
    )
    
    # 3. 네비게이션 적용 (왼쪽 사이드바 자동 생성)
    pg = st.navigation([page1, page2])
    pg.run()
    
except Exception as e:
    st.error("❌ 페이지 파일들을 불러오는 과정에서 오류가 발생했습니다.")
    st.info("💡 깃허브의 'pages' 폴더 내부에 '반도체 세부 공정 탐색기.py'와 '중요 공정과 수율.py' 파일이 정확하게 업로드되어 있는지 확인해 주세요!")
    st.write(f"상세 에러 내용: {e}")
