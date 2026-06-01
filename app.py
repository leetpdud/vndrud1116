import streamlit as st
import json

# 1. 웹페이지 기본 설정
st.set_page_config(page_title="인스타 맞팔 확인 확장기", layout="wide")

# 2. 메인 타이틀 및 상단 안내 문구
st.title("인스타 맞팔 확인 확장기")

st.markdown("""
인스타그램에서 다운로드한 following.json과 followers.json파일을 올려주세요.  
**내 데이터는 물론, 다른 사람의 파일도 확실하게 분석합니다.** *(데이터는 서버에 저장되지 않고 즉시 작동합니다.)*
""")

# 💡 [안전 추가] 아까 성공한 코드 위에 이 접이식 설명서만 딱 얹었습니다!
with st.expander("💡 인스타 파일 다운로드 및 이용 방법 보기 (클릭)", expanded=False):
    st.markdown("""
    1. **인스타그램 접속** 후 **[계정 센터]**로 이동합니다.
    2. **[내 정보 및 권한]** ➡️ **[내 정보 내보내기]**를 선택합니다.
    3. **[내보내기 만들기]**를 누른 후 분석할 **[계정 선택]**을 합니다.
    4. 내보낼 위치에서 **[기기로 내보내기]**를 선택합니다.
    5. **[정보 맞춤 설정]**을 누른 뒤, 다른 건 다 체크 해제하고 **[팔로워 및 팔로잉]**만 선택합니다.
    6. **[기간]**은 **[전체 기간]**으로 설정합니다.
    7. **[파일 형식]**은 반드시 **[JSON]**을 선택해 주세요.
    8. **[미디어 품질]**은 빠른 다운로드를 위해 **[저화질]**을 선택한 뒤 **[내보내기 시작]**을 누릅니다.
    9. 잠시 후 이메일로 파일이 도착하면 컴퓨터에 **다운로드**합니다.
    10. **⚠️ 중요:** 다운로드한 파일 중 `followers_1.json` 또는 `followers1.json` 문서의 이름에서 **숫자 '1'을 지워 'followers.json'으로 변경**해 줍니다.
    11. 아래 파일 선택 창에 안내에 따라 두 파일을 각각 올리면 1초 만에 분석 완료!
    """)

st.markdown("---")

# 3. 파일 업로드 구역
following_file = st.file_uploader("following.json 파일을 올려주세요.", type=["json"])
followers_file = st.file_uploader("followers.json 파일을 올려주세요.", type=["json"])

# 4. ⭐ 아까 273명 완벽하게 성공한 오리지널 분석 로직 (절대 수정 안 함)
if following_file and followers_file:
    try:
        following_data = json.load(following_file)
        followers_data = json.load(followers_file)
        
        following_list = []
        if isinstance(following_data, dict) and 'relationships_following' in following_data:
            for item in following_data['relationships_following']:
                if 'title' in item and item['title']:
                    following_list.append(item['title'])
                    
        followers_list = []
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
            unfollowers.sort()  # 보기 좋게 알파벳 순 정렬
            st.dataframe(unfollowers, column_config={"value": "사용자 아이디(Username)"}, use_container_width=True)
        else:
            st.success("🎉 축하합니다! 내가 팔로우한 모든 사람이 회원님을 맞팔하고 있습니다.")
            
    except Exception as e:
        st.error(f"파일을 분석하는 중에 오류가 발생했습니다. (오류 내용: {e})")
