import psycopg2
import streamlit as st
import pandas as pd


def VideosAndChannel(selected_option):
    connection = psycopg2.connect(host="localhost",user="postgres",password="admin",database="channel_demo")
#connection1 = psycopg2.connect(host="localhost",user="postgres",password="admin",database="test_db")

    shobiya = connection.cursor() #access to read/write db
    if selected_option == "Videos and their channels":
        shobiya.execute("select ch.channel_name,videos.video_name from ch full join videos on ch.channel_id = videos.channel_id;")
        res_shobiya = shobiya.fetchall()
        df1 = pd.DataFrame(res_shobiya)
        df1 = df1.rename(columns={0: 'Channel Name',1: 'Video Name'})
        st.write(df1)
    if selected_option == "most no of videos in a channel":
        shobiya.execute("select channel_name,channel_videocount from ch order by channel_videocount desc limit 1;")
        res_shobiya = shobiya.fetchall()
        df1 = pd.DataFrame(res_shobiya)
        df1 = df1.rename(columns={0: 'Channel Name',1: 'Video count'})
        st.write(df1)
    if selected_option == "top 10 most viewed videos":
        shobiya.execute("select ch.channel_name,videos.video_name,videos.video_viewcount from videos full join ch on ch.channel_id = videos.channel_id order by videos.video_viewcount desc limit 10;")
        res_shobiya = shobiya.fetchall()
        df1 = pd.DataFrame(res_shobiya)
        df1 = df1.rename(columns={0: 'Channel Name',1: 'Video Name',2:"View count"})
        st.write(df1)
        #st.write(res_shobiya)
    if selected_option == "VideoComment Counts and their video name":
        shobiya.execute("select video_commentcount,video_name from videos;")
        res_shobiya = shobiya.fetchall()
        df1 = pd.DataFrame(res_shobiya)
        df1 = df1.rename(columns={0: 'video comment count',1: 'Video Name'})
        st.write(df1)
    if selected_option == "highest liked video and their channel name":
        shobiya.execute("select ch.channel_name,videos.video_name,videos.video_likecount from videos full join ch on ch.channel_id = videos.channel_id order by videos.video_likecount desc limit 1")
        res_shobiya = shobiya.fetchall()
        df1 = pd.DataFrame(res_shobiya)
        df1 = df1.rename(columns={0: 'channel Name',1: 'Video Name',2:"video like count"})
        st.write(df1)
    if selected_option == "Channels and their total no of views":
        shobiya.execute("select channel_name,channel_viewcount from ch;")
        res_shobiya = shobiya.fetchall()
        df1 = pd.DataFrame(res_shobiya)
        df1 = df1.rename(columns={0: 'channel Name',1: 'channel view count'})
        st.write(df1)
    if selected_option == "Channels published in 2022":
        shobiya.execute("select ch.channel_name,SUBSTRING(videos.video_start, 1, 4) as published_year from videos full join ch on ch.channel_id = videos.channel_id where SUBSTRING(videos.video_start, 1, 4) = '2022';")
        res_shobiya = shobiya.fetchall()
        df1 = pd.DataFrame(res_shobiya)
        df1 = df1.rename(columns={0: 'channel Name',1: 'Published year'})
        st.write(df1)
    if selected_option == "Average duration of videos in secs and their channels":
        shobiya.execute("select ch.channel_name,avg(videos.video_duration_in_seconds) as average_duration from videos full join ch on ch.channel_id = videos.channel_id group by ch.channel_name;")
        res_shobiya = shobiya.fetchall()
        df1 = pd.DataFrame(res_shobiya)
        df1 = df1.rename(columns={0: 'channel Name',1: 'Avg duration of videos'})
        st.write(df1)
    if selected_option == "Highest video comments count and thei channel":
        shobiya.execute("select ch.channel_name,videos.video_name,videos.video_commentcount from videos full join ch on ch.channel_id = videos.channel_id order by videos.video_commentcount desc limit 1;")
        res_shobiya = shobiya.fetchall()
        df1 = pd.DataFrame(res_shobiya)
        df1 = df1.rename(columns={0: 'channel Name',1: 'video name',2: "video comment count"})
        st.write(df1)
    shobiya.close()
    connection.close()
    


