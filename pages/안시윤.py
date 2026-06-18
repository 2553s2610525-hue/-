import streamlit as st
import pandas as pd
from datetime import datetime

# --- 페이지 타이틀 (메인에서 호출되므로 subheader 형태로 깔끔하게 구성) ---
st.subheader("📝 소비 내역 기록소")
st.write("방금 지출한 내역을 숨김없이 솔직하게 기록하세요. AI가 지켜보고 있습니다.")
st.write("---")

# --- 입력 폼 (Form) 구성 ---
with st.form("expense_input_form", clear_on_submit=True):
    # 1. 날짜 입력 (기본값 오늘)
    date = st.date_input("지출 날짜", datetime.now())
    
    # 2. 지출 내역 명세
    item = st.text_input("지출 내역", placeholder="예: 엽기떡볶이, 충동구매 셔츠, 지각 택시비")
    
    # 3. 카테고리 선택
    category = st.selectbox(
        "카테고리", 
        ["식비", "교통비", "쇼핑", "문화생활", "기타"]
    )
    
    # 4. 금액 입력 (원 단위)
    amount = st.number_input(
        "지출 금액 (원)", 
        min_value=0, 
        step=1000, 
        format="%d"
    )
    
    # 제출 버튼
    submitted = st.form_submit_button("가계부에 기록하기 💸")

    # --- 데이터 저장 로직 ---
    if submitted:
        if not item:
            st.error("지출 내역을 입력해 주세요!")
        elif amount <= 0:
            st.error("금액은 0원보다 커야 합니다!")
        else:
            # 새로운 지출 데이터를 딕셔너리로 생성
            new_data = {
                "날짜": str(date),
                "내역": item,
                "카테고리": category,
                "금액": amount
            }
            
            # 메인 데이터프레임(expenses)에 추가 연동
            if 'expenses' in st.session_state:
                st.session_state.expenses = pd.concat([
                    st.session_state.expenses, 
                    pd.DataFrame([new_data])
                ], ignore_index=True)
                
                st.success(f"✅ '{item}' ({amount:,}원) 기록 완료! 메인 홈에서 업데이트된 잔소리를 확인하세요.")
            else:
                st.error("메인 시스템과의 연결에 문제가 발생했습니다.")

st.write("---")

# --- 현재까지 기록된 내역 실시간 확인창 ---
st.markdown("### 📋 현재까지 기록된 내역")
if 'expenses' in st.session_state and not st.session_state.expenses.empty:
    # 보기 좋게 역순(최신순)으로 정렬하여 테이블 출력
    st.dataframe(st.session_state.expenses.iloc[::-1], use_container_width=True)
else:
    st.info("아직 기록된 지출 내역이 없습니다.")
