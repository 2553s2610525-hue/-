import streamlit as st
import pandas as pd
import random

# --- 1. 페이지 초기 설정 ---
st.set_page_config(
    page_title="AI 잔소리 가계부 - 홈",
    page_icon="💸",
    layout="centered"
)

# --- 2. 임시 데이터 (대시보드 출력용) ---
if 'expenses' not in st.session_state:
    st.session_state.expenses = pd.DataFrame([
        {"날짜": "2026-06-01", "내역": "스타벅스", "금액": 6000},
        {"날짜": "2026-06-05", "내역": "택시비", "금액": 15000},
        {"날짜": "2026-06-12", "내역": "치킨 배달", "금액": 28000},
    ])

if 'budget' not in st.session_state:
    st.session_state.budget = 500000 


# --- 3. 소비 요약 계산 및 AI 잔소리 ---
total_spent = st.session_state.expenses["금액"].sum()
remaining = st.session_state.budget - total_spent
ratio = total_spent / st.session_state.budget

def get_nagging_message(ratio):
    if ratio < 0.5:
        return "🙄 통장이 아직 숨은 쉬네요. 언제 지를지 내가 지켜보고 있습니다."
    elif ratio < 0.9:
        return "⚠️ 슬슬 시동 걸리죠? 지금 긁으려는 그 카드 당장 내려놓으세요."
    else:
        return "🚨 파산 직전! 통장이 아니라 텅장입니다. 당장 숨만 쉬고 사세요!!"


# --- 4. 메인 화면 UI 구현 ---
st.title("💸 AI 잔소리 가계부")
st.markdown("### 이번 달 소비 현황 요약")
st.write("---")

# 대시보드 상단 카드 지표
col1, col2, col3 = st.columns(3)
col1.metric("총 지출액", f"{total_spent:,} 원")
col2.metric("설정 예산", f"{st.session_state.budget:,} 원")
col3.metric("남은 금액", f"{remaining:,} 원", delta=f"-{total_spent:,}원")

# 소비 진행 바
st.progress(min(1.0, float(ratio)))
st.caption(f"현재 예산 대비 **{ratio*100:.1f}%** 사용 중입니다.")

st.write("---")

# 🔥 AI 잔소리 한마디 제공
st.subheader("🤖 AI 가디언의 잔소리 한마디")
nagging_msg = get_nagging_message(ratio)

if ratio >= 0.9:
    st.error(nagging_msg)
elif ratio >= 0.5:
    st.warning(nagging_msg)
else:
    st.success(nagging_msg)

st.write("---")


# --- 5. 🔀 팀원 이름 메뉴 (파일 없어도 에러 안 나는 안전 버튼 방식) ---
st.subheader("🛠️ 팀원별 기능 페이지로 이동")
st.write("담당 팀원의 이름을 클릭하면 해당 페이지로 이동합니다. (팀원 파일 업로드 대기 중)")

# Grid 레이아웃으로 2x2 버튼 배치
menu_col1, menu_col2 = st.columns(2)

with menu_col1:
    st.info("📊 소비 패턴을 분석하고 싶나요?")
    if st.button("🙋‍♀️ 송유림: 소비분석 페이지", use_container_width=True):
        st.toast("송유림 님의 파일('pages/송유림.py')이 GitHub에 추가되면 연결됩니다!", icon="ℹ️")

    st.write("") # 간격 조절용
    
    st.info("🔥 건별 잔소리 폭격을 맞고 싶나요?")
    if st.button("🙋‍♀️ 김유민: AI 잔소리 페이지", use_container_width=True):
        st.toast("김유민 님의 파일('pages/김유민.py')이 GitHub에 추가되면 연결됩니다!", icon="ℹ️")

with menu_col2:
    st.info("📝 새로운 소비를 기록하고 싶나요?")
    if st.button("🙋‍♂️ 안시윤: 소비기록 페이지", use_container_width=True):
        st.toast("안시윤 님의 파일('pages/안시윤.py')이 GitHub에 추가되면 연결됩니다!", icon="ℹ️")

    st.write("") # 간격 조절용

    st.info("🌱 절약 활동 미션을 확인해볼까요?")
    if st.button("🙋‍♀️ 정선아: 절약활동 페이지", use_container_width=True):
        st.toast("정선아 님의 파일('pages/정선아.py')이 GitHub에 추가되면 연결됩니다!", icon="ℹ️")


# --- 6. 사이드바 안내 ---
st.sidebar.title("📌 대시보드 안내")
st.sidebar.info("현재 페이지는 메인 홈 화면입니다. 팀원들이 각자 코드를 'pages/' 폴더에 업로드하면 실시간 내비게이션 링크로 전환해 드릴게요!")
