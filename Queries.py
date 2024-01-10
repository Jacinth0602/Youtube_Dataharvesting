import pymongo
import psycopg2
import pandas as pd
import streamlit as st

#App() function is used to call from the main.py for multi page website

def app():

    mydb = psycopg2.connect(host="localhost",
                    user="postgres",
                    password="1234",
                    database= "youtube_data",
                    port = "5432"
                    )
    cursor = mydb.cursor()
#Required queries are posted in a dropbox below        
    question = st.selectbox(
        'Please Select Your Question',
        ('1. All the videos and the Channel Name',
        '2. Channels with most number of videos',
        '3. 10 most viewed videos',
        '4. Comments in each video',
        '5. Videos with highest likes',
        '6. likes of all videos',
        '7. views of each channel',
        '8. videos published in the year 2022',
        '9. average duration of all videos in each channel',
        '10. videos with highest number of comments'))

       
    if question == '1. All the videos and the Channel Name':
        query1 = "select Title as videos, Channel_Name as ChannelName from videos;"
        cursor.execute(query1)
        mydb.commit()
        t1=cursor.fetchall()
        st.write(pd.DataFrame(t1, columns=["Video Title","Channel Name"]))

    elif question == '2. Channels with most number of videos':
        query2 = "select Channel_Name as ChannelName,Total_Videos as NO_Videos from channels order by Total_Videos desc;"
        cursor.execute(query2)
        mydb.commit()
        t2=cursor.fetchall()
        st.write(pd.DataFrame(t2, columns=["Channel Name","No Of Videos"]))

    elif question == '3. 10 most viewed videos':
        query3 = '''select Views as views , Channel_Name as ChannelName,Title as VideoTitle from videos 
                            where Views is not null order by Views desc limit 10;'''
        cursor.execute(query3)
        mydb.commit()
        t3 = cursor.fetchall()
        st.write(pd.DataFrame(t3, columns = ["views","channel Name","video title"]))

    elif question == '4. Comments in each video':
        query4 = "select Comments as No_comments ,Title as VideoTitle from videos where Comments is not null;"
        cursor.execute(query4)
        mydb.commit()
        t4=cursor.fetchall()
        st.write(pd.DataFrame(t4, columns=["No Of Comments", "Video Title"]))

    elif question == '5. Videos with highest likes':
        query5 = '''select Title as VideoTitle, Channel_Name as ChannelName, Likes as LikesCount from videos 
                        where Likes is not null order by Likes desc;'''
        cursor.execute(query5)
        mydb.commit()
        t5 = cursor.fetchall()
        st.write(pd.DataFrame(t5, columns=["video Title","channel Name","like count"]))

    elif question == '6. likes of all videos':
        query6 = '''select Likes as likeCount,Title as VideoTitle from videos;'''
        cursor.execute(query6)
        mydb.commit()
        t6 = cursor.fetchall()
        st.write(pd.DataFrame(t6, columns=["like count","video title"]))

    elif question == '7. views of each channel':
        query7 = "select Channel_Name as ChannelName, Views as Channelviews from channels;"
        cursor.execute(query7)
        mydb.commit()
        t7=cursor.fetchall()
        st.write(pd.DataFrame(t7, columns=["channel name","total views"]))

    elif question == '8. videos published in the year 2022':
        query8 = '''select Title as Video_Title, Published_Date as VideoRelease, Channel_Name as ChannelName from videos 
                    where extract(year from Published_Date) = 2022;'''
        cursor.execute(query8)
        mydb.commit()
        t8=cursor.fetchall()
        st.write(pd.DataFrame(t8,columns=["Name", "Video Publised On", "ChannelName"]))

    elif question == '9. average duration of all videos in each channel':
        query9 =  "SELECT Channel_Name as ChannelName, AVG(Duration) AS average_duration FROM videos GROUP BY Channel_Name;"
        cursor.execute(query9)
        mydb.commit()
        t9=cursor.fetchall()
        t9 = pd.DataFrame(t9, columns=['ChannelTitle', 'Average Duration'])
        T9=[]
        for index, row in t9.iterrows():
            channel_title = row['ChannelTitle']
            average_duration = row['Average Duration']
            average_duration_str = str(average_duration)
            T9.append({"Channel Title": channel_title ,  "Average Duration": average_duration_str})
        st.write(pd.DataFrame(T9))

    elif question == '10. videos with highest number of comments':
        query10 = '''select Title as VideoTitle, Channel_Name as ChannelName, Comments as Comments from videos 
                        where Comments is not null order by Comments desc;'''
        cursor.execute(query10)
        mydb.commit()
        t10=cursor.fetchall()
        st.write(pd.DataFrame(t10, columns=['Video Title', 'Channel Name', 'NO Of Comments']))