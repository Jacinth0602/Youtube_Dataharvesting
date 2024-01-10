import pymongo
import psycopg2
import pandas as pd
import streamlit as st
from googleapiclient.discovery import build

def app():
#Youtube Channel API key connection
    def Api_connect():
        Api_Id="AIzaSyCXBF8srBTVKX3JpcWkrBd82E2AuFd9jRA"

        api_service_name = "youtube"
        api_version = "v3"
        youtube = build(api_service_name,api_version,developerKey=Api_Id)
        return youtube

    youtube=Api_connect()

#to get Channel details from the Channel ID
    def get_channel_info(channel_id):
        
        request = youtube.channels().list(
                    part = "snippet,contentDetails,Statistics",
                    id = channel_id)
                
        response1=request.execute()

        for i in range(0,len(response1["items"])):
            data = dict(
                        Channel_Name = response1["items"][i]["snippet"]["title"],
                        Channel_Id = response1["items"][i]["id"],
                        Subscription_Count= response1["items"][i]["statistics"]["subscriberCount"],
                        Views = response1["items"][i]["statistics"]["viewCount"],
                        Total_Videos = response1["items"][i]["statistics"]["videoCount"],
                        Channel_Description = response1["items"][i]["snippet"]["description"],
                        Playlist_Id = response1["items"][i]["contentDetails"]["relatedPlaylists"]["uploads"],
                        )
            return data
        

#To get Xhannel Playlist details
    def get_playlist_info(channel_id):
        All_data = []
        next_page_token = None
        next_page = True
        while next_page:

            request = youtube.playlists().list(
                part="snippet,contentDetails",
                channelId=channel_id,
                maxResults=50,
                pageToken=next_page_token
                )
            response = request.execute()

            for item in response['items']: 
                data={'PlaylistId':item['id'],
                        'Title':item['snippet']['title'],
                        'ChannelId':item['snippet']['channelId'],
                        'ChannelName':item['snippet']['channelTitle'],
                        'PublishedAt':item['snippet']['publishedAt'],
                        'VideoCount':item['contentDetails']['itemCount']}
                All_data.append(data)
            next_page_token = response.get('nextPageToken')
            if next_page_token is None:
                next_page=False
        return All_data

#To get Video ids using Channel ID
    def get_channel_videos(channel_id):
        video_ids = []
        res = youtube.channels().list(id=channel_id, 
                                    part='contentDetails').execute()
        playlist_id = res['items'][0]['contentDetails']['relatedPlaylists']['uploads']
        next_page_token = None
        
        while True:
            res = youtube.playlistItems().list( 
                                            part = 'snippet',
                                            playlistId = playlist_id, 
                                            maxResults = 50,
                                            pageToken = next_page_token).execute()
            
            for i in range(len(res['items'])):
                video_ids.append(res['items'][i]['snippet']['resourceId']['videoId'])
            next_page_token = res.get('nextPageToken')
            
            if next_page_token is None:
                break
        return video_ids


#To get Channel Video information using VideoId from above func
    def get_video_info(video_ids):

        video_data = []

        for video_id in video_ids:
            request = youtube.videos().list(
                        part="snippet,contentDetails,statistics",
                        id= video_id)
            response = request.execute()

            for item in response["items"]:
                data = dict(Channel_Name = item['snippet']['channelTitle'],
                            Channel_Id = item['snippet']['channelId'],
                            Video_Id = item['id'],
                            Title = item['snippet']['title'],
                            Tags = item['snippet'].get('tags'),
                            Thumbnail = item['snippet']['thumbnails']['default']['url'],
                            Description = item['snippet']['description'],
                            Published_Date = item['snippet']['publishedAt'],
                            Duration = item['contentDetails']['duration'],
                            Views = item['statistics']['viewCount'],
                            Likes = item['statistics'].get('likeCount'),
                            Comments = item['statistics'].get('commentCount'),
                            Favorite_Count = item['statistics']['favoriteCount'],
                            Definition = item['contentDetails']['definition'],
                            Caption_Status = item['contentDetails']['caption']
                            )
                video_data.append(data)
        return video_data


#To get Channel comment information using VideoID
    def get_comment_info(video_ids):
            Comment_Information = []
            try:
                    for video_id in video_ids:

                            request = youtube.commentThreads().list(
                                    part = "snippet",
                                    videoId = video_id,
                                    maxResults = 50
                                    )
                            response5 = request.execute()
                            
                            for item in response5["items"]:
                                    comment_information = dict(
                                            Comment_Id = item["snippet"]["topLevelComment"]["id"],
                                            Video_Id = item["snippet"]["videoId"],
                                            Comment_Text = item["snippet"]["topLevelComment"]["snippet"]["textOriginal"],
                                            Comment_Author = item["snippet"]["topLevelComment"]["snippet"]["authorDisplayName"],
                                            Comment_Published = item["snippet"]["topLevelComment"]["snippet"]["publishedAt"])

                                    Comment_Information.append(comment_information)
            except:
                    pass
                    
            return Comment_Information

#establish MongoDB Connection with new Database name and Collection name
    client= pymongo.MongoClient('mongodb://localhost:27017')
    db= client["youtube_data"]

#To Upload into MongoDB Database

    def channel_details(channel_id):
        ch_details = get_channel_info(channel_id)
        pl_details = get_playlist_info(channel_id)
        vi_ids = get_channel_videos(channel_id)
        vi_details = get_video_info(vi_ids)
        com_details = get_comment_info(vi_ids)

        coll1 = db["channel_details"]
        coll1.insert_one({"channel_information":ch_details,"playlist_information":pl_details,"video_information":vi_details,
                        "comment_information":com_details})
        
        return "upload completed successfully"

#Table creation for channels, playlists, videos, comments by connecting to POSTGRE SQL
    def channels_table():
        mydb = psycopg2.connect(host="localhost",
                user="postgres",
                password="1234",
                database= "youtube_data",
                port = "5432"
                )
        cursor = mydb.cursor()

        drop_query = "drop table if exists channels"
        cursor.execute(drop_query)
        mydb.commit()
#Returns if the Channel table is already created
        try:
            create_query = '''create table if not exists channels(Channel_Name varchar(100),
                            Channel_Id varchar(80) primary key, 
                            Subscription_Count bigint, 
                            Views bigint,
                            Total_Videos int,
                            Channel_Description text,
                            Playlist_Id varchar(50))'''
            cursor.execute(create_query)
            mydb.commit()
        except:
            st.write("Channels Table alredy created")    


        ch_list = []
        db = client["youtube_data"]
        coll1 = db["channel_details"]
        for ch_data in coll1.find({},{"_id":0,"channel_information":1}):
            ch_list.append(ch_data["channel_information"])
        df = pd.DataFrame(ch_list)
#Inserting Values from Mongo to POSTGRE SQL         
        for index,row in df.iterrows():
            insert_query = '''INSERT into channels(Channel_Name,
                                                        Channel_Id,
                                                        Subscription_Count,
                                                        Views,
                                                        Total_Videos,
                                                        Channel_Description,
                                                        Playlist_Id)
                                            VALUES(%s,%s,%s,%s,%s,%s,%s)'''
                

            values =(
                    row['Channel_Name'],
                    row['Channel_Id'],
                    row['Subscription_Count'],
                    row['Views'],
                    row['Total_Videos'],
                    row['Channel_Description'],
                    row['Playlist_Id'])
#Returns if the values already present in the table            
            try:                     
                cursor.execute(insert_query,values)
                mydb.commit()    
            except:
                st.write("Channels values are already inserted")

                
    def playlists_table():
        mydb = psycopg2.connect(host="localhost",
                user="postgres",
                password="1234",
                database= "youtube_data",
                port = "5432"
                )
        cursor = mydb.cursor()

        drop_query = "drop table if exists playlists"
        cursor.execute(drop_query)
        mydb.commit()

        try:
            create_query = '''create table if not exists playlists(PlaylistId varchar(100) primary key,
                            Title varchar(80), 
                            ChannelId varchar(100), 
                            ChannelName varchar(100),
                            PublishedAt timestamp,
                            VideoCount int
                            )'''
            cursor.execute(create_query)
            mydb.commit()
        except:
            st.write("Playlists Table alredy created")    


        db = client["youtube_data"]
        coll1 =db["channel_details"]
        pl_list = []
        for pl_data in coll1.find({},{"_id":0,"playlist_information":1}):
            for i in range(len(pl_data["playlist_information"])):
                    pl_list.append(pl_data["playlist_information"][i])
        df = pd.DataFrame(pl_list)
        
        for index,row in df.iterrows():
            insert_query = '''INSERT into playlists(PlaylistId,
                                                        Title,
                                                        ChannelId,
                                                        ChannelName,
                                                        PublishedAt,
                                                        VideoCount)
                                            VALUES(%s,%s,%s,%s,%s,%s)'''            
            values =(
                    row['PlaylistId'],
                    row['Title'],
                    row['ChannelId'],
                    row['ChannelName'],
                    row['PublishedAt'],
                    row['VideoCount'])
                    
            try:                     
                cursor.execute(insert_query,values)
                mydb.commit()    
            except:
                st.write("Playlists values are already inserted")

    def videos_table():

        mydb = psycopg2.connect(host="localhost",
                    user="postgres",
                    password="1234",
                    database= "youtube_data",
                    port = "5432"
                    )
        cursor = mydb.cursor()

        drop_query = "drop table if exists videos"
        cursor.execute(drop_query)
        mydb.commit()

        try:
            create_query = '''create table if not exists videos(
                            Channel_Name varchar(150),
                            Channel_Id varchar(100),
                            Video_Id varchar(50) primary key, 
                            Title varchar(150), 
                            Tags text,
                            Thumbnail varchar(225),
                            Description text, 
                            Published_Date timestamp,
                            Duration interval, 
                            Views bigint, 
                            Likes bigint,
                            Comments int,
                            Favorite_Count int, 
                            Definition varchar(10), 
                            Caption_Status varchar(50) 
                            )''' 
                            
            cursor.execute(create_query)             
            mydb.commit()
        except:
            st.write("Videos Table alrady created")

        vi_list = []
        db = client["youtube_data"]
        coll1 = db["channel_details"]
        for vi_data in coll1.find({},{"_id":0,"video_information":1}):
            for i in range(len(vi_data["video_information"])):
                vi_list.append(vi_data["video_information"][i])
        df2 = pd.DataFrame(vi_list)
            
        
        for index, row in df2.iterrows():
            insert_query = '''
                        INSERT INTO videos (Channel_Name,
                            Channel_Id,
                            Video_Id, 
                            Title, 
                            Tags,
                            Thumbnail,
                            Description, 
                            Published_Date,
                            Duration, 
                            Views, 
                            Likes,
                            Comments,
                            Favorite_Count, 
                            Definition, 
                            Caption_Status 
                            )
                        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)

                    '''
            values = (
                        row['Channel_Name'],
                        row['Channel_Id'],
                        row['Video_Id'],
                        row['Title'],
                        row['Tags'],
                        row['Thumbnail'],
                        row['Description'],
                        row['Published_Date'],
                        row['Duration'],
                        row['Views'],
                        row['Likes'],
                        row['Comments'],
                        row['Favorite_Count'],
                        row['Definition'],
                        row['Caption_Status'])
                                    
            try:    
                cursor.execute(insert_query,values)
                mydb.commit()
            except:
                st.write("videos values already inserted in the table")
            

    def comments_table():
        
        mydb = psycopg2.connect(host="localhost",
                    user="postgres",
                    password="1234",
                    database= "youtube_data",
                    port = "5432"
                    )
        cursor = mydb.cursor()

        drop_query = "drop table if exists comments"
        cursor.execute(drop_query)
        mydb.commit()

        try:
            create_query = '''CREATE TABLE if not exists comments(Comment_Id varchar(100) primary key,
                        Video_Id varchar(80),
                        Comment_Text text, 
                        Comment_Author varchar(150),
                        Comment_Published timestamp)'''
            cursor.execute(create_query)
            mydb.commit()
            
        except:
            st.write("Comments Table already created")

        com_list = []
        db = client["youtube_data"]
        coll1 = db["channel_details"]
        for com_data in coll1.find({},{"_id":0,"comment_information":1}):
            for i in range(len(com_data["comment_information"])):
                com_list.append(com_data["comment_information"][i])
        df3 = pd.DataFrame(com_list)


        for index, row in df3.iterrows():
                insert_query = '''
                    INSERT INTO comments (Comment_Id,
                                        Video_Id ,
                                        Comment_Text,
                                        Comment_Author,
                                        Comment_Published)
                    VALUES (%s, %s, %s, %s, %s)

                '''
                values = (
                    row['Comment_Id'],
                    row['Video_Id'],
                    row['Comment_Text'],
                    row['Comment_Author'],
                    row['Comment_Published']
                )
                try:
                    cursor.execute(insert_query,values)
                    mydb.commit()
                except:
                    st.write("This comments are already exist in comments table")
#Calling all the above functions to create and values into tables in Postgre SQL
    def tables():
        channels_table()
        playlists_table()
        videos_table()
        comments_table()
        return "Tables Created successfully"
        
    def show_channels_table():
        ch_list = []
        db = client["youtube_data"]
        coll1 = db["channel_details"] 
        for ch_data in coll1.find({},{"_id":0,"channel_information":1}):
            ch_list.append(ch_data["channel_information"])
        channels_table = st.dataframe(ch_list)
        return channels_table

    def show_playlists_table():
        db = client["youtube_data"]
        coll1 =db["channel_details"]
        pl_list = []
        for pl_data in coll1.find({},{"_id":0,"playlist_information":1}):
            for i in range(len(pl_data["playlist_information"])):
                    pl_list.append(pl_data["playlist_information"][i])
        playlists_table = st.dataframe(pl_list)
        return playlists_table

    def show_videos_table():
        vi_list = []
        db = client["youtube_data"]
        coll2 = db["channel_details"]
        for vi_data in coll2.find({},{"_id":0,"video_information":1}):
            for i in range(len(vi_data["video_information"])):
                vi_list.append(vi_data["video_information"][i])
        videos_table = st.dataframe(vi_list)
        return videos_table

    def show_comments_table():
        com_list = []
        db = client["youtube_data"]
        coll3 = db["channel_details"]
        for com_data in coll3.find({},{"_id":0,"comment_information":1}):
            for i in range(len(com_data["comment_information"])):
                com_list.append(com_data["comment_information"][i])
        comments_table = st.dataframe(com_list)
        return comments_table
    
 
    channel_id = st.text_input("Enter Channel id")
    channels = channel_id.split(',')
    channels = [ch.strip() for ch in channels if ch]

    if st.button("Scrap & Store data"):
        for channel in channels:
            ch_ids = []
            db = client["youtube_data"]
            coll1 = db["channel_details"]
            for ch_data in coll1.find({},{"_id":0,"channel_information":1}):
                ch_ids.append(ch_data["channel_information"]["Channel_Id"])
            if channel in ch_ids:
                st.success("Channel details of the given channel id: " + channel + " already exists")
            else:
                output = channel_details(channel)
                st.success(output)
                
    if st.button("Migrate to SQL"):
        display = tables()
        st.success(display)
    tab1 , tab2, tab3 , tab4 = st.tabs(["Channels","Playlists","Videos","Comments"])
    with tab1:
        show_channels_table()
    with tab2:
        show_playlists_table()
    with tab3:
        show_videos_table()
    with tab4:
        show_comments_table()
