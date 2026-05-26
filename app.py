import streamlit as st
from datetime import datetime, timedelta
import random

# --- 핵심 데이터 변수 ---
my_location = "위치 미인증"
is_authenticated = False
total_carbon_saved = 0.0
my_manner_temp = 36.5
my_wishlist = []
my_coords = (0, 0)

# 사용자별 매너 온도 데이터
user_temperatures = {
    "나": 36.5,
    "신촌불주먹": 37.2,
    "노원지킴이": 36.0,
    "상계동주민": 40.5,
    "꿀팁요정": 38.0,
    "자취고수": 39.1
}

# 공유 냉장고 위치 정보
fridge_locations = {
    "상계 1호점": (200, 150),
    "상계 2호점": (500, 200),
    "상계 3호점": (350, 350)
}

chats = {}
community_posts = [
    {"id": 1, "user": "꿀팁요정", "content": "1호 공유냉장고에 오늘 신선한 채소가 많이 들어왔네요!", "time": "10분 전"},
    {"id": 2, "user": "자취고수", "content": "역 앞 마트 오늘 타임세일 한대요. 참고하세요~", "time": "30분 전"}
]

foods = [
    {
        "id": 1, "name": "감자 3알", "type": "무료나눔",
        "exp_date": (datetime.now() + timedelta(days=1)).strftime("%Y-%m-%d"),
        "user": "신촌불주먹", "carbon": 0.3, "status": "실온",
        "fridge": "상계 1호점",
        "desc": "요리하고 남았어요.", "cook_date": "2026-05-13", "storage": "서늘한 곳 보관"
    },
    {
        "id": 2, "name": "우유 500ml (미개봉)", "type": "무료나눔",
        "exp_date": (datetime.now() + timedelta(days=3)).strftime("%Y-%m-%d"),
        "user": "노원지킴이", "carbon": 0.5, "status": "냉장",
        "fridge": "상계 2호점",
        "desc": "유통기한 임박해서 나눔합니다.", "cook_date": "안 했어요.", "storage": "냉장 보관"
    },
    {
        "id": 3, "name": "방울토마토 한 팩", "type": "물물교환",
        "exp_date": (datetime.now() + timedelta(days=5)).strftime("%Y-%m-%d"),
        "user": "상계동주민", "carbon": 0.4, "status": "냉장",
        "fridge": "상계 3호점",
        "desc": "사과나 다른 과일이랑 바꾸고 싶어요!", "cook_date": "2026-05-14", "storage": "냉장 보관"
    }
]

# --- Streamlit UI 시작 ---
st.set_page_config(page_title="공유냉장고 : 우리 동네 소통 플랫폼", layout="wide")

st.title("공유냉장고 : 우리 동네 소통 플랫폼")

# 헤더 영역
col1, col2, col3, col4 = st.columns([2,2,2,2])
with col1:
    st.markdown(f"📍 {my_location}")
with col2:
    if st.button("동네 인증하기"):
        detected = "서울시 노원구 상계동"
        my_location = detected
        is_authenticated = True
        my_coords = (random.randint(250, 650), random.randint(250, 550))
        st.success(f"{detected} 커뮤니티에 입장하셨습니다!")
with col3:
    st.markdown(f"🌱 탄소 절감: {total_carbon_saved:.2f}kg")
with col4:
    st.markdown(f"🌡️ 매너 온도: {my_manner_temp:.1f}℃")

# 탭 메뉴
tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
    "🍲 음식 공유", "💬 채팅목록", "🏡 동네생활", "📍 지도", "✍️ 나눔하기", "⚙️ 설정"
])
# 🍲 음식 공유 탭
with tab1:
    st.subheader("음식 공유 목록")
    for food in foods:
        st.markdown(f"### {food['name']} ({food['status']})")
        st.write(f"- 방식: {food['type']}")
        st.write(f"- 기한: {food['exp_date']}")
        st.write(f"- 보관: {food['storage']}")
        st.write(f"- 조리: {food['cook_date']}")
        st.write(f"- 위치: {food['fridge']}")
        st.write(f"- 작성자: {food['user']}")
        if st.button(f"채팅하기 - {food['name']}"):
            st.info(f"{food['user']}님과의 채팅방이 열렸습니다 (데모).")

# 💬 채팅목록 탭
with tab2:
    st.subheader("진행 중인 채팅")
    if not chats:
        st.write("진행 중인 채팅이 없습니다.")
    else:
        for fid, chat in chats.items():
            st.write(f"👤 {chat['food']['user']} ({chat['food']['name']})")
            st.write(f"마지막 메시지: {chat['messages'][-1]['text']}")

# 🏡 동네생활 탭
with tab3:
    st.subheader("우리 동네 실시간 정보통")
    if not is_authenticated:
        st.warning("동네 인증을 완료해야 글을 열람하고 작성할 수 있습니다.")
    else:
        new_post = st.text_input("글 작성하기")
        if st.button("올리기"):
            if new_post:
                community_posts.insert(0, {
                    "id": len(community_posts)+1,
                    "user": "나",
                    "content": new_post,
                    "time": "방금 전"
                })
                st.success("글이 등록되었습니다!")
        for post in community_posts:
            st.markdown(f"**👤 {post['user']}**")
            st.write(post['content'])
            st.caption(post['time'])
            st.divider()

# 📍 지도 탭
with tab4:
    st.subheader("상계동 공유 냉장고 현황")
    st.write("지도 이미지는 서버 환경에서 표시되지 않을 수 있습니다.")
    for name, pos in fridge_locations.items():
        count = len([f for f in foods if f['fridge'] == name])
        st.write(f"- {name}: 음식 {count}개")

    if is_authenticated:
        st.success(f"🙋 내 위치: {my_coords}")
    else:
        st.info("상단 [동네 인증하기] 완료 시 내 위치가 표시됩니다.")

# ✍️ 나눔하기 탭
with tab5:
    st.subheader("음식 등록하기")
    name = st.text_input("음식명")
    fridge = st.selectbox("보관 냉장고", list(fridge_locations.keys()))
    trade_type = st.selectbox("거래 방식", ["무료나눔", "물물교환", "소액판매"])
    status = st.selectbox("보관 상태", ["냉장", "냉동", "실온"])
    exp_date = st.date_input("유통기한", datetime.now())
    cook_date = st.date_input("조리 날짜", datetime.now())
    storage = st.text_input("상세 보관방법")

    if st.button("등록하기"):
        if not name:
            st.warning("음식명을 입력해주세요.")
        else:
            new_item = {
                "id": len(foods)+1, "name": name,
                "type": trade_type,
                "exp_date": exp_date.strftime("%Y-%m-%d"),
                "status": status,
                "user": "나", "fridge": fridge,
                "carbon": 0.45, "storage": storage,
                "cook_date": cook_date.strftime("%Y-%m-%d")
            }
            foods.append(new_item)
            total_carbon_saved += 0.45
            st.success(f"'{name}'이(가) {fridge}에 등록되었습니다!")

# ⚙️ 설정 탭
with tab6:
    st.subheader("알람 설정")
    wish = st.text_input("관심 키워드 추가")
    if st.button("추가"):
        if wish:
            my_wishlist.append(wish)
            st.success(f"'{wish}' 키워드가 추가되었습니다.")
    st.write(f"관심 키워드: {', '.join(my_wishlist)}")
