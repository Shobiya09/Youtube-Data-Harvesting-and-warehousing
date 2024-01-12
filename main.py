from pymongodb import *
import streamlit as st
from sqlconnection import *
import pymongo
from query import *
from PIL import Image
from streamlit_option_menu import option_menu
icon = Image.open("youtube.jpg")
st.set_page_config(page_title= "Youtube Data Harvesting and Warehousing | By Akash Jha",
                   page_icon= icon,
                   layout= "wide",
                   initial_sidebar_state= "expanded",
                   menu_items={'About': """# This app is created by Akash Jha!"""})

# CREATING OPTION MENU
with st.sidebar:
    selected = option_menu(None, ["Home","View"], 
                           icons=["house-door-fill","tools","card-text"],
                           default_index=0,
                           orientation="vertical",
                           styles={"nav-link": {"font-size": "30px", "text-align": "centre", "margin": "0px", 
                                                "--hover-color": "#C80101"},
                                   "icon": {"font-size": "30px"},
                                   "container" : {"max-width": "6000px"},
                                   "nav-link-selected": {"background-color": "#C80101"}})

client = pymongo.MongoClient("mongodb+srv://shobiya:Administration@cluster0.fr0sfzw.mongodb.net/?retryWrites=true&w=majority")
db = client.youtubeVideoHarvesting
collection = db.Channel_Details
lst = []
if selected == "Home":
    st.image("youtube.jpg",width=150)
    st.title(":red[Youtube Data Harvesting]")
    st.caption("This project helps to scrap data from youtube and store in mongodb and sql")

    ch_name = st.text_input("Enter the channel name")

    a = youtube_search(collection,ch_name)

    if a == "inserted":
        for i in collection.find({},{"_id":0}):
            lst.append(i)
        df = pd.DataFrame(lst)
        sqldata=insert(df)

if selected == "View":
    options = ["Videos and their channels", "most no of videos in a channel", "top 10 most viewed videos",
               "VideoComment Counts and their video name","highest liked video and their channel name",
               "Channels and their total no of views","Channels published in 2022",
               "Average duration of videos and their channels","Highest video comments count and thei channel"]

    # dropdown box
    selected_option = st.selectbox("Select an option:", options,index=None)

    # Display the selected option
    if selected_option:
        VideosAndChannel(selected_option)
    else:
        st.warning("please select a query to fetch data from sql")

        