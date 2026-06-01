import streamlit as st
import json

# 1. 메인 타이틀 및 수정 요청하신 안내 문구
st.title("인스타 맞팔 확인 확장기")

st.markdown("""
인스타그램에서 다운로드한 following.json과 followers.json파일을 올려주세요.  
**내 데이터는 물론, 다른 사람의 파일도 확실하게 분석합니다.** *(데이터는 서버에 저장되지않고 즉시 작동 합니다.)*
""")

st.markdown("---")

# 2. 파일 업로드 구역
following_file = st.file_uploader("following.json 파일을 올려주세요.", type=["json"])
followers_file = st.file_uploader("followers.json 파일을 올려주세요.", type=["json"])

# 💡 어떤 형식의 인스타 파일이 들어와도 안전하게 데이터를 추출하는 공식
def get_instagram_list(data, key_name):
    # 형식 A: 대괄호 [ ] 로 바로 시작하는 리스트 형태인 경우
    if isinstance(data, list):
        return data
    # 형식 B: 중괄호 { } 로 시작하고 내부에 키가 존재하는 경우
    elif isinstance(data, dict):
        if key_name in data:
            return data[key_name]
        elif 'relationships_' + key_name in data:
            return data['relationships_' + key_name]
        # 그 외에 다른 키 안에 리스트가 들어있는 경우 탐색
        for val in data.values():
            if isinstance(val, list):
                return val
    return []

# 3. 데이터 분석 및 결과 출력 로직
if following_file and followers_file:
    try:
        following_raw = json.load(following_file)
        followers_raw = json.load(followers_file)
        
        # 파일 구조에 맞게 데이터를 안전하게 변환
        following_data = get_instagram_list(following_raw, 'following')
        followers_data = get_instagram_list(followers_raw, 'followers')
        
        following_list = []
        for item in following_data:
            try:
                following_list.append(item['string_list_data'][0]['value'])
            except (KeyError, IndexError, TypeError):
                continue
                
        followers_list = []
        for item in followers_data:
            try:
                followers_list.append(item['string_list_data'][0]['value'])
            except (KeyError, IndexError, TypeError):
                continue
        
        # 맞팔 안 한 사람 계산 (어제 성공했던 핵심 로직)
        unfollowers = list(set(following_list) - set(followers_list))
        
        st.markdown("---")
        st.subheader("📊 분석 결과")
        
        res_col1, res_col2, res_col3 = st.columns(3)
        res_col1.metric("내가 팔로잉하는 사람", f"{len(following_list)}명")
        res_col2.metric("나를 팔로우하는 사람", f"{len(followers_list)}명")
        res_col3.metric("나를 맞팔하지 않는 사람", f"{len(unfollowers)}명")
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        if unfollowers:
            st.error("🚫 나를 맞팔하지 않고 있는 계정 목록입니다:")
            st.dataframe(unfollowers, column_config={"value": "사용자 아이디(Username)"}, use_container_width=True)
        else:
            st.success("🎉 축하합니다! 내가 팔로우한 모든 사람이 회원님을 맞팔하고 있습니다.")
            
    except Exception as e:
        st.error(f"파일을 분석하는 중에 오류가 발생했습니다. 인스타그램 원본 JSON 파일이 맞는지 확인해 주세요. (에러 내용: {e})")
