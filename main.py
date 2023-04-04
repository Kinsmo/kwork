import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
from datetime import datetime as dt
import datetime

colors = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd', '#8c564b', '#e377c2', '#7f7f7f', '#bcbd22', '#17becf']

def time_diff(start_time,end_time):
    start_time = dt.strptime(start_work, '%H:%M')
    end_time = dt.strptime(end_work, '%H:%M')
    time_diff = end_time - start_time
    time_diff_h = time_diff.total_seconds() / 3600
    return time_diff_h

st.title('张运霄写论文日志')
col1,col2 = st.columns(2)

# "01 read file"
file_path = "static/data.csv"
df = pd.read_csv(file_path)

date_today = pd.Timestamp.today().strftime('%Y-%m-%d')
time_now = dt.now().strftime('%H:%M')

last_line = pd.DataFrame(df.tail(1))
last_date = last_line.iloc[0,0]

if last_date == date_today:
    # today
    time_today = last_line.iloc[0,1]
    total_time_today = last_line.iloc[0,4]
    total_pages_today = last_line.iloc[0,5]
    total_words_today = last_line.iloc[0,6]
    
    # yesterday
    df.drop(df.tail(1).index, inplace=True)
    last_line = pd.DataFrame(df.tail(1))
    total_time_yesterday = last_line.iloc[0,4]
    total_pages_yesterday = last_line.iloc[0,5]
    total_words_yesterday = last_line.iloc[0,6]
    
    default_time_today = time_today
    default_total_words = total_time_today
    default_total_pages = total_pages_today
    default_total_time = total_words_today
    default_start_work = last_line.iloc[0,7]
    default_end_work = last_line.iloc[0,8]
    
else:
    total_time_today = last_line.iloc[0,4]
    total_pages_today = last_line.iloc[0,5]
    total_words_today = last_line.iloc[0,6]
    
    total_time_yesterday = last_line.iloc[0,4]
    total_pages_yesterday = last_line.iloc[0,5]
    total_words_yesterday = last_line.iloc[0,6]
    
    default_time_today = 0
    default_total_words = total_time_yesterday
    default_total_pages = total_pages_yesterday
    default_total_time = total_words_yesterday
    default_start_work = '9:00'
    default_end_work = '23:00'

new_df = last_line

# "03 new content"
with col2:
    time_today = st.number_input("今日时常:", value=default_time_today)
    total_words_today = st.number_input("当前字数:", value=default_total_words)
    total_pages_today = st.number_input("当前页数:", value=default_total_pages)
    start_work = st.text_input("上班打卡:", value=default_start_work)
    end_work = st.text_input("下班打卡:", value=default_end_work)

today_words = total_words_today - total_words_yesterday
today_pages = total_pages_today - total_pages_yesterday

new_df = pd.DataFrame({'date':[date_today],
                       'today_time':[time_today],
                       'today_pages':[today_pages],
                       'today_words':[today_words],
                       'total_time':[total_time_yesterday + time_today],
                       'total_pages':[total_pages_today],
                       'total_words':[total_words_today],
                       'start_work':[start_work],
                       'end_work':[end_work],
                       'work_time':[time_diff(start_work,end_work)]})

work_till_now = time_diff(start_work,time_now)

with col1:
    st.subheader(f":red[今日时间：{time_today}] -> :green[{total_time_today}] -> :blue[10]")
    st.subheader(f":red[今日字数：{today_words}] -> :green[{total_words_today}]")
    st.subheader(f":red[今日页数：{today_pages}] -> :green[{total_pages_today}] -> :blue[150]")
    st.subheader(f":red[今日上班打卡：{start_work}]")
    st.subheader(f":red[已工作时间：{work_till_now:.1f}]")

# "04 add to df"
df = pd.concat([df,new_df])
df.to_csv(file_path, index=False)
        
df2 = df.rename({'date':'日期','today_time':'当日时长','today_pages':'当日页数','today_words':'当日字数','total_time':'总时长','total_pages':'总页数','total_words':'总字数','start_work':'上班打卡','end_work':'下班打卡','work_time':'工作时长'}, axis='columns')
df2['日期'] = pd.to_datetime(df2['日期'])
df2['日期'] = df2['日期'].dt.strftime('%m-%d')

st.dataframe(df2)

data = df.to_csv(index=False)

with col2:
    col3,col4 = st.columns(3)
    with col3: rerun = st.button("刷新")
    with col4: st.download_button("下载数据",data,"data.csv","text/csv")
    if rerun: st.experimental_rerun()

# Plot
st.area_chart(df2,x='日期',y=['当日时长','当日页数','工作时长'])
st.bar_chart(df2,x='日期',y=['当日字数','总字数'])
