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

date = pd.Timestamp.today().strftime('%Y-%m-%d')
time_now = dt.now().strftime('%H:%M')

last_line = pd.DataFrame(df.tail(1))
last_date = last_line.iloc[0,0]

# "02 new line"
new_df = last_line
last_time = last_line.iloc[0,4]
last_pages = last_line.iloc[0,5]
last_words = last_line.iloc[0,6]

if last_date == date:
    df.drop(df.tail(1).index, inplace=True)
    last_line = pd.DataFrame(df.tail(1))
    last_time = last_line.iloc[0,4]
    last_pages = last_line.iloc[0,5]
    last_words = last_line.iloc[0,6]
 
# "03 new content"
with col2:
    today_time = st.number_input("今日时常:", value=0)
    total_words = st.number_input("当前字数:", value=last_words)
    total_pages = st.number_input("当前页数:", value=last_pages)
    start_work = st.text_input("上班打卡:", value='9:00')
    end_work = st.text_input("下班打卡:", value='23:00')
    password = st.text_input("写入密码:")

new_df = pd.DataFrame({'date':[date],
                       'today_time':[today_time],
                       'today_pages':[total_pages - last_pages],
                       'today_words':[total_words - last_words],
                       'total_time':[last_time + today_time],
                       'total_pages':[total_pages],
                       'total_words':[total_words],
                       'start_work':[start_work],
                       'end_work':[end_work],
                       'work_time':[time_diff(start_work,end_work)]})

today_pages = new_df.iloc[0,2]
today_words = new_df.iloc[0,3]
work_till_now = time_diff(start_work,time_now)

with col1:
    st.subheader(f":red[今日时间：{today_time}] -> :green[{last_time}] -> :blue[10]")
    st.subheader(f":red[今日字数：{today_words}] -> :green[{last_words}]")
    st.subheader(f":red[今日页数：{today_pages}] -> :green[{last_pages}] -> :blue[150]")
    st.subheader(f":red[今日上班打卡：{start_work}]")
    st.subheader(f":red[已工作时间：{work_till_now:.1f}]")

# "04 add to df"
df = pd.concat([df,new_df])

def submit():
    if password == '7158':
        df.to_csv(file_path, index=False)
        st.balloons()
        
df2 = df.rename({'date':'日期','today_time':'当日时长','today_pages':'当日页数','today_words':'当日字数','total_time':'总时长','total_pages':'总页数','total_words':'总字数','start_work':'上班打卡','end_work':'下班打卡','work_time':'工作时长'}, axis='columns')
df2['日期'] = pd.to_datetime(df2['日期'])
df2['日期'] = df2['日期'].dt.strftime('%m-%d')
#df2['上班打卡'] = pd.to_datetime(df2['上班打卡'])
#df2['下班打卡'] = pd.to_datetime(df2['下班打卡'])

st.dataframe(df2)

with col2:
    col3,col4 = st.columns(2)
    with col3: rerun = st.button("刷新")
    if rerun: st.experimental_rerun()
    with col4: st.button("写入数据",on_click=submit)

# Plot


st.area_chart(df2,x='日期',y=['当日时长','当日页数','工作时长'])
st.bar_chart(df2,x='日期',y=['当日字数','总字数'])
#st.line_chart(df2,x='日期',y=['上班打卡','下班打卡'])

#fig = plt.figure(figsize=(10,5))
#ax = fig.add_subplot(1, 1, 1)
#ax.plot(df2['日期'],df2['上班打卡'],'r-',lw=4,color=colors[0],label=f"上班")
#ax.plot(df2['日期'],df2['下班打卡'],'g-',lw=4,color=colors[1],label=f"下班")
#ax.axhline('9:00',color='k')
#ax.axhline('22:00',color='k')
#ax.set_ylim(ax.get_ylim()[::-1])
#ax.legend(loc="upper right")
#st.pyplot(fig)

#st.area_chart(df,x='date',y=['today_time','today_pages'])
#st.bar_chart(df,x='date',y=['today_words','total_words'])
