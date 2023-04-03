import pandas as pd
import streamlit as st
import datetime
import matplotlib.pyplot as plt

st.title('张运霄写论文日志')
col1,col2 = st.columns(2)

# "01 read file"
file_path = "static/data.csv"
df = pd.read_csv(file_path)
st.dataframe(df)

last_line = pd.DataFrame(df.tail(1))
last_date = last_line.iloc[0,0]
last_time = last_line.iloc[0,4]
last_pages = last_line.iloc[0,5]
last_words = last_line.iloc[0,6]

date = pd.Timestamp.today().strftime('%Y-%m-%d')

# "02 new line"
new_df = None
if last_date == date:
    new_df = last_line
    df.drop(df.tail(1).index, inplace=True)
else:
    new_df = pd.DataFrame({'date':[date],'today_time':[0],'today_pages':[0],'today_words':[0],'total_time':[last_time],'total_pages':[last_pages],'total_words':[last_words]})
    
# "03 new content"
with col2:
    is_submit = st.checkbox("提交数据？",value=False)
    is_rerun = st.button("刷新")
    if is_rerun:
        st.experimental_rerun()
    time = st.number_input("增加时长:", value=0)
    words = st.number_input("增加字数:", value=0)
    pages = st.number_input("增加页数:", value=0)

new_df['today_time'] += time
new_df['today_pages'] += pages
new_df['today_words'] += words
new_df['total_time'] += time
new_df['total_pages'] += pages
new_df['total_words'] += words

today_time = new_df.iloc[0,1]
today_pages = new_df.iloc[0,2]
today_words = new_df.iloc[0,3]


with col1:
    st.subheader(f":red[今日时间：{today_time}] / :green[{last_time}] / :blue[10]")
    st.subheader(f":red[今日字数：{today_words}] / :green[{last_words}]")
    st.subheader(f":red[今日页数：{today_pages}] / :green[{last_pages}] /:blue[150]")

# "04 add to df"
df = pd.concat([df,new_df])

if is_submit:
    df.to_csv(file_path, index=False)
    st.dataframe(df)

st.line_chart(df,x='date',y=['today_time','today_pages'])
st.bar_chart(df,x='date',y=['total_words','today_words'])
