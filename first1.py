import streamlit as st
import pandas as pd

# 파일 업로드
st.title("2025년 5월 기준 연령별 인구 현황 분석")
#uploaded_file = st.file_uploader("CSV 파일을 업로드하세요 (EUC-KR 인코딩)", type="csv")

if uploaded_file is not None:
    # CSV 파일 읽기 (EUC-KR 인코딩)
    df = pd.read_csv("202505_202505_연령별인구현황_월간.csv", encoding='euc-kr')

    # 열 이름 전처리
    df.columns = df.columns.str.strip()  # 공백 제거
    age_columns = [col for col in df.columns if col.startswith("2025년05월_계_")]
    new_age_columns = [col.replace("2025년05월_계_", "") for col in age_columns]
    
    # 총인구수와 행정구역 컬럼 확인 (이름이 다를 수 있으므로 자동 추출)
    region_col = df.columns[0]  # 첫 번째 열이 보통 행정구역
    total_pop_col = [col for col in df.columns if '총인구수' in col][0]
    
    # 연령별 데이터 추출
    age_df = df[[region_col, total_pop_col] + age_columns].copy()
    age_df.columns = [region_col, '총인구수'] + new_age_columns
    
    # 총인구수 기준 상위 5개 행정구역 선택
    top5_df = age_df.sort_values(by='총인구수', ascending=False).head(5)

    # 시각화
    st.subheader("연령별 인구 분포 (상위 5개 행정구역)")
    for _, row in top5_df.iterrows():
        region = row[region_col]
        population_by_age = row[new_age_columns]
        population_by_age.index = new_age_columns  # 연령
        st.write(f"📍 {region}")
        st.line_chart(population_by_age.astype(int))  # 숫자형 변환

    # 원본 데이터 표시
    st.subheader("📄 원본 데이터 (일부 열 생략 가능)")
    st.dataframe(age_df)
