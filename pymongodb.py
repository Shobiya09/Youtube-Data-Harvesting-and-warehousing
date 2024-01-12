import streamlit as st
import pandas as pd
import googleapiclient.discovery 
import googleapiclient.errors
import pymongo
from isodate import parse_duration
from datetime import datetime, timedelta,time,datetime

api_service_name = "youtube" #service name
api_version = "v3" #service version
api_key = "AIzaSyB3thY3-icD9Am4_RqdrVVz00XrIZ7SSLQ"
youtube = googleapiclient.discovery.build(
    api_service_name, api_version, developerKey=api_key)


""""client = pymongo.MongoClient("mongodb+srv://shobiya:Administration@cluster0.fr0sfzw.mongodb.net/?retryWrites=true&w=majority")
db = client.youtubeVideoHarvesting
collection = db.Channel_Details"""

def channel_detail(ch_id):
    request_channel = youtube.channels().list(
        part="snippet,contentDetails,statistics",
        id=ch_id
    )
    response_channel = request_channel.execute()
    ch_dic = dict(channel_id = response_channel["items"][0]["id"],
                    channel_name = response_channel["items"][0]["snippet"]["title"],
                    channel_description = response_channel["items"][0]["snippet"]["description"],
                    channel_start = response_channel["items"][0]["snippet"]["publishedAt"],
                    channel_country = response_channel["items"][0]["snippet"]["country"],
                    channel_videocount = int(response_channel["items"][0]["statistics"]["videoCount"]),
                    channel_subscribercount = int(response_channel["items"][0]["statistics"]["subscriberCount"]),
                    channel_thumbnail = response_channel["items"][0]["snippet"]["thumbnails"]["high"]["url"],
                    channel_viewcount = int(response_channel["items"][0]["statistics"]["viewCount"]) )
   # st.write(ch_dic)
    return ch_dic

def comment_detail(vd_id):
    comment = []
    request_comment = youtube.commentThreads().list( #comments for each videoid
        part="snippet,replies",
        maxResults=1,                    
        videoId=vd_id

    )
    response_comment = request_comment.execute()
    for i in response_comment["items"]:
        cmnt_dic = dict(comment_channelid = i["snippet"]["channelId"],
                        comment_videoid = i["snippet"]["videoId"],
                        comment_id = i["id"],
                        comment_text = i["snippet"]["topLevelComment"]["snippet"]["textDisplay"],
                        comment_author = i["snippet"]["topLevelComment"]["snippet"]["authorDisplayName"],
                        comment_authorpic = i["snippet"]["topLevelComment"]["snippet"]["authorProfileImageUrl"],
                        comment_authorchannelurl = i["snippet"]["topLevelComment"]["snippet"]["authorChannelUrl"],
                        comment_likecount = i["snippet"]["topLevelComment"]["snippet"]["likeCount"],
                        comment_postedat = i["snippet"]["topLevelComment"]["snippet"]["publishedAt"],
                        comment_totalreplycount = i["snippet"]["totalReplyCount"]
                    )
        comment.append(cmnt_dic)
    return(comment)

def video_detail(vd_id):

    request_video = youtube.videos().list( #video details by video id for each playlist
            part="snippet,contentDetails,statistics",
            id=vd_id
        )
    response_video = request_video.execute()
    duration = parse_duration(response_video["items"][0]["contentDetails"]["duration"])
    vd_dic = dict(
        channel_id = response_video["items"][0]["snippet"]["channelId"],
        video_id = response_video["items"][0]["id"],
                video_name = response_video["items"][0]["snippet"]["title"],
                video_description = response_video["items"][0]["snippet"]["description"],
                video_start = response_video["items"][0]["snippet"]["publishedAt"],
                video_categoryid = response_video["items"][0]["snippet"]["categoryId"],
                video_duration_in_seconds = duration.total_seconds(),
                video_dimention = response_video["items"][0]["contentDetails"]["dimension"],
                video_likecount = int(response_video["items"][0]["statistics"]["likeCount"]) if "likeCount" in response_video["items"][0]["statistics"] else 0,                 
                video_thumbnail = response_video["items"][0]["snippet"]["thumbnails"]["high"]["url"],
                video_commentcount = int(response_video["items"][0]["statistics"]["commentCount"]) if "commentCount" in response_video["items"][0]["statistics"] else 0,
                video_viewcount = int(response_video["items"][0]["statistics"]["viewCount"]) if "viewCount" in response_video["items"][0]["statistics"] else 0,
                video_comments = comment_detail(vd_id) if "commentCount" in response_video["items"][0]["statistics"] and response_video["items"][0]["statistics"]["commentCount"] != '0' else 0)
    #t.write(response_video["items"][0]["contentDetails"]["duration"])
    #st.write(vd_dic)
    
    return(vd_dic)
  
def youtube_search(collection,ch_name):
    channels = [{"channel_details":{"channel":{},"video":[]}}]
    if ch_name:
        st.write("Thank you!! Your data is pushing into mongo db")
        request = youtube.search().list(
            part="snippet",
            maxResults=50,
            q=ch_name #Channels name
        )
        next_page_token = None
        response = request.execute()
        
        #channel details
        
        
        ch_id = response["items"][0]["snippet"]["channelId"]
        ch_dic = channel_detail(ch_id)
        channels[0]["channel_details"]["channel"] = ch_dic
        
        
        #video Details
        for i in range(1,len(response["items"])): 
            if "videoId" in response["items"][i]["id"]:
                vd_id = response["items"][i]["id"]["videoId"]
                vd_dic = video_detail(vd_id)
                channels[0]["channel_details"]["video"].append(vd_dic)

        #next_page_token = response.get('nextPageToken')
        while True:
            next_page_token = response.get('nextPageToken')
            if next_page_token:
                request = youtube.search().list(
                q='Your Search Query',
                part='snippet',
                maxResults=50,
                pageToken=next_page_token
            )
                response = request.execute()
                for i in range(1,len(response["items"])): 
                    if "videoId" in response["items"][i]["id"]:
                        vd_id = response["items"][i]["id"]["videoId"]
                        vd_dic = video_detail(vd_id)
                        channels[0]["channel_details"]["video"].append(vd_dic)
            if next_page_token is None:
                break

        #response = request.execute()
        st.write("please give correct channel name")

        collection.insert_many(channels)
        st.write("Data stored into mongodb")
        return("inserted")
    

        