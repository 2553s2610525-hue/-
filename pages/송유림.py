import streamlit as st
import pandas as pd
import plotly.express as px

# --- 페이지 타이틀 ---
st.subheader("📊 나의 소비 패턴 정밀 분석")
st.write("당신이 어디에 돈을 가장 쏟아부었는지 시각적으로 증명해 드립니다.")
st.write("---")

# --- 데이터 존재 여부 확인 ---
if 'expenses' not in st.session_state or st.session_state.expenses.empty:
    st.info("📊 분석할 소비 데이터가 아직 없습니다. 소비기록 페이지에서 먼저 데이터를 입력해 주세요!")
else:
    df = st.session_state.expenses
    
    # 1. 카테고리별 지출 합계 계산
    category_df = df.groupby("카테고리")["금액"].sum().reset_index()
    
    # 지출이 많은 순서대로 정렬
    category_df = category_df.sort_values(by="금액", ascending=False).reset_index(drop=True)

    # 2. 통계 지표 레이아웃
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### 📂 카테고리별 지출 금액")
        # 천 단위 콤마 포맷팅하여 표 출력
        display_df = category_df.copy()
        display_df["금액"] = display_df["금액"].map(lambda x: f"{x:,} 원")
        st.dataframe(display_df, use_container_width=True)
        
    with col2:
        st.markdown("#### 🍰 지출 비율")
        # Plotly를 이용한 깔끔한 도넛 차트 시각화
        fig = px.pie(
            category_df, 
            values="금액", 
            names="카테고리", 
            hole=0.4,
            color_discrete_sequence=px.colors.sequential.RdBu
        )
        fig.update_traces(textposition='inside', textinfo='percent+label')
        fig.update_layout(showlegend=False, margin=dict(t=10, b=10, l=10, r=10), height=250)
        st.plotly_chart(fig, use_container_width=True)

    st.write("---")

    # 3. 🤖 분석 기반 뼈 때리는 경고 시스템
    st.markdown("### 🔍 소비 가디언의 정밀 진단")
    
    # 가장 돈을 많이 쓴 카테고리 추출
    max_row = category_df.iloc[0]
    max_category = max_row["카테고리"]
    max_amount = max_row["금액"]
    
    # 총 지출 대비 가장 많이 쓴 카테고리의 비율 계산
    total_spent = df["금액"].sum()
    cat_ratio = (max_amount / total_spent) * 100

    # 맞춤형 잔소리 멘트 세팅
    if max_category == "식비":
        nagging_analysis = "말이 좋아 식비지, 사실상 배달 앱에 전재산 상납 중이시네요. 위장은 채워지고 통장은 비어가는 기적의 연금술사입니다."
    elif max_category == "쇼핑":
        nagging_analysis = "방 구석을 보세요. 저번에 사놓고 쓰지도 않은 택배 상자가 수두룩한데 또 샀죠? 낭비벽 초기 증세입니다."
    elif max_category == "교통비":
        nagging_analysis = "5분 더 자려다가 5년 더 일하게 생겼습니다. 택시 회사 주주도 아니면서 왜 기부하고 다니시죠? 내일부터 알람 3개 더 켜세요."
    elif max_category == "문화생활":
        nagging_analysis = "인생은 즐겁지만 통장은 슬픕니다. 문화생활도 잔고가 있을 때나 교양인 거지, 지금은 그냥 과소비입니다."
    else:
        nagging_analysis = "기타 지출이 이렇게 많다는 건 어디에 돈 새는지 본인도 모른다는 뜻입니다. 지출 구멍을 당장 막으세요!"

    # 경고 박스 출력
    st.error(
        f"🚨 현재 지출 1위 카테고리는 **[{max_category}]** 이며, 총 지출의 **{cat_ratio:.1f}%** 나 차지하고 있습니다!\n\n"
        f"👉 **한마디:** {nagging_analysis}"
    )

    # 4. 가장 비싸게 산 단일 항목 추적
    st.write("")
    max_single_item = df.loc[df["금액"].idxmax()]
    st.warning(
        f"💸 **이번 달 단일 최고 지출 항목:**\n"
        f"👉 `{max_single_item['날짜']}`에 지른 **'{max_single_item['내역']}' ({max_single_item['금액']:,}원)** 입니다. 이거 살 때 행복하셨나요? 다음 달 카드 명세서 볼 때도 행복할지 지켜보겠습니다."
    )
