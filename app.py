import streamlit as st
import pandas as pd
import random
import importlib.util
import os

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
    if ratio < 0.5: return "🙄 통장이 아직 숨은 쉬네요. 언제 지를지 내가 지켜보고 있습니다."
    elif ratio < 0.9: return "⚠️ 슬슬 시동 걸리죠? 지금 긁으려는 그 카드 당장 내려놓으세요."
    else: return "🚨 파산 직전! 통장이 아니라 텅장입니다. 당장 숨만 쉬고 사세요!!"

# --- 4. 메뉴 선택 기능 (사이드바) ---
st.sidebar.title("📌 메뉴 내비게이션")
menu = st.sidebar.radio(
    "이동할 기능을 선택하세요:",
    ["🏠 메인 홈 / 소비 요약", "📊 소비분석", "📝 소비기록", "🤖 AI 잔소리", "🌱 절약활동"]
)

# --- 5. 안전하게 다른 팀원 코드를 불러오는 함수 ---
def run_team_page(file_name, page_title):
    file_path = f"pages/{file_name}"
    if os.path.exists(file_path):
        try:
            # 팀원 파일의 코드를 동적으로 안전하게 실행
            spec = importlib.util.spec_from_file_location("mod", file_path)
            mod = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(mod)
        except Exception as e:
            # 팀원 코드 내부에서 에러가 나면 메인을 죽이지 않고 에러 메시지만 표시
            st.error(f"🚨 {page_title} 페이지 코드 내부에 오류가 있습니다!")
            st.exception(e)
    else:
        st.warning(f"⚠️ `pages/{file_name}` 파일이 아직 깃허브에 없습니다. 팀원이 업로드하면 활성화됩니다!")

# --- 6. 메뉴별 화면 조건문 처리 ---
if menu == "🏠 메인 홈 / 소비 요약":
    st.title("💸 AI 잔소리 가계부")
    st.markdown("### 이번 달 소비 현황 요약")
    st.write("---")

    col1, col2, col3 = st.columns(3)
    col1.metric("총 지출액", f"{total_spent:,} 원")
    col2.metric("설정 예산", f"{st.session_state.budget:,} 원")
    col3.metric("남은 금액", f"{remaining:,} 원", delta=f"-{total_spent:,}원")

    st.progress(min(1.0, float(ratio)))
    st.caption(f"현재 예산 대비 **{ratio*100:.1f}%** 사용 중입니다.")

    st.write("---")
    st.subheader("🤖 AI 가디언의 잔소리 한마디")
    nagging_msg = get_nagging_message(ratio)
    if ratio >= 0.9: st.error(nagging_msg)
    elif ratio >= 0.5: st.warning(nagging_msg)
    else: st.success(nagging_msg)

elif menu == "📊 소비분석":
    st.title("📊 소비분석")
    run_team_page("송유림.py", "소비분석")

elif menu == "📝 소비기록":
    st.title("📝 소비기록")
    run_team_page("안시윤.py", "소비기록")

elif menu == "🤖 AI 잔소리":
    st.title("🤖 AI 잔소리")
    run_team_page("김유민.py", "AI 잔소리")

elif menu == "🌱 절약활동":
    st.title("🌱 절약활동")
    run_team_page("정선아.py", "절약활동")
