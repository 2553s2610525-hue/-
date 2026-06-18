st.page_link("pages/송유림.py", label="🙋‍♀️ 송유림: 소비분석 페이지")
import streamlit as st
import pandas as pd

st.set_page_config(page_title="소비 기록", page_icon="📝")
st.title("📝 새로운 소비 기록")

st.write("돈을 또 쓰셨군요? 숨기지 말고 정직하게 적으세요.")

with st.form("expense_form", clear_on_submit=True):
    date = st.date_input("지출 날짜")
    item = st.text_input("지출 내역 (예: 마라탕, 지각 택시비)")
    category = st.selectbox("카테고리", ["식비", "교통비", "쇼핑", "문화생활", "기타"])
    amount = st.number_input("지출 금액 (원)", min_value=0, step=1000)
    
    submitted = st.form_submit_button("가계부에 지출 추가")
    
    if submitted:
        if not item or amount == 0:
            st.error("내역과 금액을 올바르게 입력하세요!")
        else:
            new_row = {"날짜": str(date), "내역": item, "카테고리": category, "금액": amount}
            st.session_state.expenses = pd.concat([st.session_state.expenses, pd.DataFrame([new_row])], ignore_index=True)
            st.success(f"'{item}' ({amount:,}원) 기록 완료! 메인 페이지로 가서 AI의 잔소리를 들으세요.")

st.write("---")
st.subheader("📋 전체 내역 목록")
st.dataframe(st.session_state.expenses, use_container_width=True)
