import streamlit as st
import json
import pandas as pd

# 1. 웹페이지 기본 설정 (다크 모드 대시보드)
st.set_page_config(page_title="Insta-Extractor Pro Analytics", layout="wide", initial_sidebar_state="collapsed")

# 2. 메인 타이틀 (전문가용 대시보드 스타일)
st.markdown("<h1 style='text-align: center; color: white;'>✨ Insta-Extractor Pro Analytics</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #a1a1a1;'>인스타그램 팔로워/팔로잉 JSON 파일을 비교 분석하여 한눈에 보여드립니다.</p>", unsafe_allow_html=True)

st.markdown("---") # 구분선

# 3. 💡 인스타그램 데이터 다운로드 가이드라인 (접혀있는 상자)
with st.expander("ℹ️ 인스타그램에서 데이터 파일(JSON) 다운로드 및 파일 준비 방법", expanded=False):
    st.markdown("""
    프로그램을 이용하려면 인스타그램에서 회원님의 데이터를 먼저 다운로드하셔야 합니다. 아래 순서대로 천천히 따라 해보세요!
    
    1. **인스타그램 앱 또는 웹사이트**에서 내 프로필로 이동한 뒤 **[설정(톱니바퀴)]** 메뉴를 누릅니다.
    2. **[메타 계정 센터]** -> **[내 정보 및 권한]** 메뉴로 이동합니다.
    3. **[내 정보 다운로드]** ➡️ **[다운로드 또는 전송 요청]**을 클릭합니다.
    4. 정보를 추출할 **계정을 선택**합니다.
    5. 내보낼 위치에서 **[기기로 내보내기]**를 선택합니다.
    6. **[정보 맞춤 설정]**을 누른 후, 다른 건 다 제외하고 **[팔로워 및 팔로잉]만 선택**한 뒤 저장합니다.
    7. 옵션 설정에서 기간은 **[전체 기간]**, 파일 형식은 **[JSON]** 선택, 미디어 품질은 **[저화질]**을 선택합니다.
    8. **[내보내기 시작]http://googleusercontent.com/image_generation_content/1
