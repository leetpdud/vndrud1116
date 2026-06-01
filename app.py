import streamlit as st
import json

# 1. 메인 타이틀 및 안내 문구
st.title("인스타 맞팔 확인 확장기")

st.markdown("""
인스타그램에서 다운로드한 following.json과 followers.json파일을 올려주세요.  
**내 데이터는 물론, 다른 사람의 파일도 확실하게 분석합니다.** *(데이터는 서버에 저장되지않고 즉시 작동 합니다.)*
""")

st.markdown("---")

# 2. 파일 업로드 구역
following_file = st.file_uploader("following.json 파일을 올려주세요.", type=["json"])
followers_file = st.file_uploader("followers.json 파일을 올려주세요.", type=["json"])

# 3. 회원님 파일 구조 맞춤형 분석 로직
if following_file and followers_file:
    try:
        following_data = json.load(following_file)
        followers_data = json.load(followers_file)
        
        following_list = []
        # [회원님 파일 맞춤] following.json은 각 항목의 'title'에 아이디가 들어있습니다.
        if isinstance(following_data, dict) and 'relationships_following' in following_data:
            for item in following_data['relationships_following']:
                if 'title' in item and item['title']:
                    following_list.append(item['title'])
                    
        followers_list = []
        # [회원님 파일 맞춤] followers.json은 기존처럼 string_list_data 내부의 value를 읽습니다.
        if isinstance(followers_data, list):
            for item in followers_data:
                try:
                    if 'string_list_data' in item and item['string_list_data']:
                        followers_list.append(item['string_list_data'][0]['value'])
                except:
                    pass
        
        # 맞팔 안 한 사람 계산
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
            # 알파벳 순으로 정렬하여 보기 편하게 제공
            unfollowers.sort()
            st.dataframe(unfollowers, column_config={"value": "사용자 아이디(Username)"}, use_container_width=True)
        else:
            st.success("🎉 축하합니다! 내가 팔로우한 모든 사람이 회원님을 맞팔하고 있습니다.")
            
    except Exception as e:
        st.error(f"파일을 분석하는 중에 오류가 발생했습니다. (오류 내용: {e})")
