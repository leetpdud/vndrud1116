import streamlit as st
import json

# 1. 스트림릿 내부 버그 및 캐시를 강제로 비우기 위한 설정
st.cache_data.clear()  # 기존에 브라우저가 잘못 기억하고 있는 파일 데이터 강제 삭제

# 2. 웹페이지 레이아웃 설정
st.set_page_config(page_title="인스타 맞팔 확인 확장기", layout="wide")

# 3. 메인 타이틀 및 수정 요청하신 안내 문구
st.title("인스타 맞팔 확인 확장기")

st.markdown("""
인스타그램에서 다운로드한 following.json과 followers.json파일을 올려주세요.  
**내 데이터는 물론, 다른 사람의 파일도 확실하게 분석합니다.** *(데이터는 서버에 저장되지않고 즉시 작동 합니다.)*
""")

st.markdown("---") # 구분선

# 4. 파일 업로드 구역 (좌우 2단 배치 레이아웃)
col1, col2 = st.columns(2)

with col1:
    following_file = st.file_uploader("following.json 파일을 올려주세요.", type=["json"], key="original_following_key")

with col2:
    followers_file = st.file_uploader("followers.json 파일을 올려주세요.", type=["json"], key="original_followers_key")


# ⭐ 어제 272명 정확하게 나오던 오리지널 분석 로직 100% 원본 그대로 유지
if following_file and followers_file:
    try:
        following_data = json.load(following_file)
        followers_data = json.load(followers_file)
        
        following_list = []
        if 'relationships_following' in following_data:
            for item in following_data['relationships_following']:
                following_list.append(item['string_list_data'][0]['value'])
                
        followers_list = []
        # 어제 성공했던 껍데기 없는 순수 리스트 파싱 공식
        for item in followers_data:
            followers_list.append(item['string_list_data'][0]['value'])
        
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
            st.dataframe(unfollowers, column_config={"value": "사용자 아이디(Username)"}, use_container_width=True)
        else:
            st.success("🎉 축하합니다! 내가 팔로우한 모든 사람이 회원님을 맞팔하고 있습니다.")
            
    except Exception as e:
        st.error("파일을 분석하는 중에 오류가 발생했습니다. 인스타그램에서 다운로드한 원본 JSON 파일이 맞는지 확인해 주세요.")
