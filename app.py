import streamlit as st
from google import genai
from google.genai import types
from google.genai.errors import APIError

# 1. 웹페이지 설정
st.set_page_config(page_title="연애코치 밍글", page_icon="💖", layout="centered")
st.title("💖 연애코치 밍글의 비밀 상담소")
st.caption("연애 고민, 썸, 이별... 말 못 할 고민을 솔직하게 털어놓으세요.")

# 2. Streamlit Secrets에서 API 키 안전하게 불러오기
try:
    api_key = st.secrets["GEMINI_API_KEY"]
    client = genai.Client(api_key=api_key)
except KeyError:
    st.error("🚨 Streamlit Secrets에 'GEMINI_API_KEY'가 설정되지 않았습니다. 배포 설정을 확인해주세요.")
    st.stop()

# 3. 세션 상태(Session State)로 채팅 기록 및 대화 객체 유지
if "messages" not in st.session_state:
    st.session_state.messages = []

if "chat_session" not in st.session_state:
    # 챗봇의 페르소나 설정 (이 부분을 바꾸면 다른 주제의 챗봇이 됩니다)
    system_instruction = (
        "당신은 공감 능력이 뛰어나고 위트 있는 전문 연애 상담사 '밍글'입니다. "
        "사용자의 연애 고민(썸, 이별, 짝사랑 등)을 듣고, 친구처럼 친근하면서도 "
        "때로는 객관적이고 뼈 때리는 조언을 해주세요. 답변은 너무 길지 않게 다정한 말투로 작성해주세요."
    )
    
    # gemini-2.5-flash-lite 모델과 system_instruction을 결합하여 채팅 세션 시작
    st.session_state.chat_session = client.chats.create(
        model="gemini-2.5-flash-lite",
        config=types.GenerateContentConfig(
            system_instruction=system_instruction,
            temperature=0.7,
        )
    )

# 4. 기존 대화 기록 화면에 출력
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 5. 사용자 입력 처리
if user_input := st.chat_input("오늘 어떤 고민이 있으신가요?"):
    # 사용자 메시지 화면에 표시 및 저장
    with st.chat_message("user"):
        st.markdown(user_input)
    st.session_state.messages.append({"role": "user", "content": user_input})

    # 챗봇 답변 생성 및 오류 처리
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        message_placeholder.markdown("Thinking... 💬")
        
        try:
            # API 호출
            response = st.session_state.chat_session.send_message(user_input)
            bot_reply = response.text
            
            # 답변 화면 출력 및 저장
            message_placeholder.markdown(bot_reply)
            st.session_state.messages.append({"role": "assistant", "content": bot_reply})
            
        except APIError as e:
            # 구글 API 관련 에러 처리
            message_placeholder.markdown("⚠️ 구글 API 통신 중 오류가 발생했습니다. 잠시 후 다시 시도해주세요.")
            st.sidebar.error(f"API Error: {e}")
        except Exception as e:
            # 기타 예외 처리
            message_placeholder.markdown("⚠️ 죄송합니다. 메시지를 처리하는 중에 문제가 발생했습니다.")
            st.sidebar.error(f"Unknown Error: {e}")
