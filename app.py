import streamlit as st
import json

# [디자인] 웹페이지 기본 설정 및 좌우 넓게 보기
st.set_page_config(page_title="인스타 맞팔 확인 확장기", layout="wide")

# [디자인] 메인 타이틀
st.title("인스타 맞팔 확인 확장기")

# [디자인] 회원님이 요청하신 텍스트 반영
st.markdown("""
인스타그램에서 다운로드한 following.json과 followers.json파일을 올려주세요.  
**내 데이터는 물론, 다른 사람의 파일도 확실하게 분석합니다.** *(데이터는 서버에 저장되지않고 즉시 작동 합니다.)*
""")

st.markdown("---") # 구분선

# [디자인] 회원님이 직접 검증하신 완벽한 인스타그램 데이터 다운로드 가이드라인 상자
with st.expander("ℹ️ 인스타그램에서 데이터 파일(JSON) 다운로드하는 방법 보기", expanded=False):
    st.markdown("""
    프로그램을 이용하려면 인스타그램에서 회원님의 데이터를 먼저 다운로드하셔야 합니다. 아래 순서대로 천천히 따라 해보세요!
    
    1. **인스타그램에 접속**합니다.
    2. 설정 메뉴에서 **[계정 센터]** ➡️ **[내 정보 및 권한]**으로 이동합니다.
    3. **[내 정보 내보내기]** ➡️ **[내보내기 만들기]**를 차례로 누릅니다.
    4. 정보를 추출할 **[계정 선택]**을 진행합니다.
    5. 내보낼 위치에서 **[기기로 내보내기]**를 선택합니다.
    6. **[정보 맞춤 설정]**을 누른 후, 다른 건 다 제외하고 **[팔로워 및 팔로잉]만 선택**한 뒤 저장합니다.
    7. 옵션 설정에서 기간은 **[전체 기간]**, 파일 형식은 **[JSON]** 선택, 미디어 품질은 **[저화질]**을 선택합니다.
    8. **[내보내기 시작]**을 누릅니다.
    9. 잠시 후 인스타그램 연동 **이메일로 파일이 오면 다운로드**합니다.
    10. ⚠️ **[가장 중요!]** 다운로드한 파일 중에서 만약 **`followers1.json`**처럼 이름 뒤에 숫자 1이 붙어있다면, **이름 변경을 눌러 글자에서 '1'만 싹 지우고 `followers.json`으로 만들어 줍니다.**
    11. 파일 이름이 정확해졌다면, 아래 웹사이트 안내에 따라 파일 2개를 각각 올려주시면 됩니다!
    """)

st.markdown("<br>", unsafe_allow_html=True) # 여백

# [디자인] 파일 업로드 구역 좌우 2단 레이아웃 배치
col1, col2 = st.columns(2)

with col1:
    following_file = st.file_uploader("following.json 파일을 올려주세요.", type=["json"])

with col2:
    followers_file = st.file_uploader("followers.json 파일을 올려주세요.", type=["json"])


# ⭐ [어제 버전과 100% 일치] 272명 성공했던 오리지널 분석 로직 원본 그대로 유지
if following_file and followers_file:
    try:
        following_data = json.load(following_file)
        followers_data = json.load(followers_file)
        
        following_list = []
        if 'relationships_following' in following_data:
            for item in following_data['relationships_following']:
                following_list.append(item['string_list_data'][0]['value'])
                
        followers_list = []
        # 어제 성공했던 리스트 순회 파싱 공식 그대로 유지 (절대 변경 없음)
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
