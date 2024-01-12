import pandas as pd
import sqlalchemy as sql
import psycopg2 as pg2
import streamlit as st



engine = sql.create_engine("postgresql://postgres:admin@localhost:5432/channel_demo")
conn = pg2.connect(database = "channel_details",user ="postgres",password = "admin", host = "localhost",port = 5432)
cursor = conn.cursor()

def insert(df):    
    df[["channel","video"]] = df["channel_details"].apply(lambda i : pd.Series([i["channel"],i["video"]]))
    df.drop("channel_details",axis=1,inplace=True)
    channel = []
    [channel.append(i) for i in df["channel"]]
    #st.write()
    df_channel = pd.DataFrame(channel)
    st.caption(":red[Channels stored in MongoDB]")
    st.write(df_channel)
    df_channel.to_sql(name="ch",con=engine,if_exists="replace")

    comment = []
    cmnt_dic =[]
    for i in df["video"]:
        for j in i:
            res = {key: j[key] for key in j.keys()
            & {'video_comments'}}
            
            comment.append(res)

    df_comment = pd.DataFrame(comment)
    
    for i in df_comment["video_comments"]:
        if i != 0 :
            for j in i:
                #df_cmnt = pd.json_normalize(j)
                cmnt_dic.append(j)

    df_cmnt = pd.DataFrame(cmnt_dic)
    
    df_cmnt.to_sql(name="comments",con=engine,if_exists="replace")
    video1 = []
    
    for i in df["video"]:
        for j in i:
            res = {key: j[key] for key in j.keys()
            & {'channel_id','video_id','video_name','video_description',
                'video_start','video_categoryid','video_duration_in_seconds','video_dimention',
                'video_likecount','video_thumbnail','video_commentcount','video_viewcount'}}
            video1.append(res)
            
        
        
    
    df_video = pd.DataFrame(video1)
    df_video.to_sql(name="videos",con=engine,if_exists="replace")
    return("inserted into sql")