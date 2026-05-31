import streamlit as st
import json

# 1. 웹 페이지 스타일 및 레이아웃 설정
st.set_page_config(page_title="인스타 맞팔 확인기", page_icon="✨", layout="centered")

st.title("✨ 인스타 언팔 판독기 (범용 완성판)")
st.markdown("인스타그램에서 다운로드한 `following.json`과 `followers.json` 파일을 올려주세요.")
st.markdown("내 데이터는 물론, 다른 사람의 파일도 완벽하게 분석합니다. (데이터는 서버에 저장되지 않고 즉시 휘발됩니다.)")
st.markdown("---")

# 2. 강력한 범용 ID 추출 알고리즘 (어떤 형태의 인스타 JSON이 와도 ID만 쏙쏙 뽑아냄)
def extract_insta_ids(data):
    results = []
    if isinstance(data, dict):
        # 인스타 JSON의 다양한 핵심 키(Key) 패턴 분석
        if 'value' in data and isinstance(data['value'], str) and not data['value'].startswith('http'):
            results.append(data['value'])
        if 'title' in data and data['title'] and isinstance(data['title'], str):
            # 대여/공식 계정 등 특수문자나 안내문 제외하고 ID만 추출
            clean_title = data['title'].split('님')[0].strip()
            results.append(clean_title)
        if 'string_list_data' in data and isinstance(data['string_list_data'], list):
            for item in data['string_list_data']:
                if 'value' in item:
                    results.append(item['value'])
                    
        # 하위 구조가 더 있다면 재귀적으로 파고들기
        for k, v in data.items():
            if k not in ['title', 'value', 'href', 'timestamp']: # 불필요한 키 패스
                results.extend(extract_insta_ids(v))
                
    elif isinstance(data, list):
        for item in data:
            results.extend(extract_insta_ids(item))
            
    return results

# 3. 파일 업로드 UI 화면 구성
col1, col2 = st.columns(2)

with col1:
    following_file = st.file_uploader("📂 following.json (내가 팔로잉)", type=["json"])

with col2:
    followers_file = st.file_uploader("📂 followers.json (나를 팔로우)", type=["json"])

# 4. 핵심 로직 가동
if following_file and followers_file:
    try:
        # 파일 읽기
        following_data = json.load(following_file)
        followers_data = json.load(followers_file)
        
        # ID 추출 및 텍스트 정제
        raw_following = extract_insta_ids(following_data)
        raw_followers = extract_insta_ids(followers_data)
        
        # 순수 아이디만 필터링 (숫자로만 된 ID나 무의미한 텍스트 제외)
        following_set = set([user.strip() for user in raw_following if user and not user.replace('_', '').replace('.', '').isdigit() and ' ' not in user])
        followers_set = set([user.strip() for user in raw_followers if user and not user.replace('_', '').replace('.', '').isdigit() and ' ' not in user])
        
        # 나를 맞팔하지 않은 사람 계산 (차집합)
        not_following_me = sorted(list(following_set - followers_set))
        
        # 결과 화면 출력
        st.success("🎉 성공적으로 분석을 마쳤습니다!")
        
        # 대시보드 스코어 보드
        m_col1, m_col2, m_col3 = st.columns(3)
        m_col1.metric("내가 팔로잉", f"{len(following_set)}명")
        m_col2.metric("나를 팔로우", f"{len(followers_set)}명")
        m_col3.metric("맞팔 안 한 사람", f"{len(not_following_me)}명", delta=f"-{len(not_following_me)}" if not_following_me else None, delta_color="inverse")
        
        st.markdown("---")
        st.subheader(f"❌ 나를 맞팔하지 않은 사람 목록 ({len(not_following_me)}명)")
        
        if not_following_me:
            # 실시간 아이디 검색창 기능
            search_term = st.text_input("🔍 리스트에서 아이디 검색", "", placeholder="궁금한 아이디를 입력하세요...")
            filtered_list = [user for user in not_following_me if search_term.lower() in user.lower()]
            
            # 보기 좋은 텍스트 박스 형태로 리스트 출력
            for i, user in enumerate(filtered_list, 1):
                st.text(f"{i:3d}. {user}")
        else:
            if len(followers_set) == 0:
                st.warning("⚠️ 파일은 업로드되었으나 팔로워 정보를 읽지 못했습니다. 파일이 깨지지 않았는지 확인해 주세요.")
            else:
                st.balloons()
                st.info("🥳 대단해요! 팔로잉하는 모든 사람과 맞팔로우 상태입니다!")
                
    except Exception as e:
        st.error(f"⚠️ 파일을 처리하는 중 오류가 발생했습니다: {e}")
else:
    st.info("💡 왼쪽에 팔로잉 파일, 오른쪽에 팔로워 파일을 모두 올려주시면 판독이 시작됩니다.")