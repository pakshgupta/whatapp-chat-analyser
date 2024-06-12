import streamlit as st
import preprocessing,helper
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

st.sidebar.title('Whatsapp Chat Analyzer')

uploaded_file = st.sidebar.file_uploader("Choose a file")
if uploaded_file is not None:
    bytes_data = uploaded_file.getvalue()
    data=bytes_data.decode('utf-8')

    df=preprocessing.preprocess(data)

    st.dataframe(df)

    #Fetching Unique users
    user_list = df['user'].unique().tolist()
    user_list.remove('Group Notification')
    user_list.sort()
    user_list.insert(0,'Overall')

    selected_user = st.sidebar.selectbox("Show Analysis wrt", user_list)

    if st.sidebar.button('Show Analysis'):

        #Stats
        no_of_messages,words,media,link=helper.fetch_stats(selected_user,df)

        col1,col2,col3,col4=st.columns(4)

        with col1:
            st.header('Total Messages')
            st.title(no_of_messages)
        with col2:
            st.header('Total Words')
            st.title(words)
        with col3:
            st.header('Media Files Shared')
            st.title(media)
        with col4:
            st.header('Links Shared')
            st.title(link)


        # Finding the Busiest Users in the Group
        if selected_user=='Overall':
            st.title('Most Busy Users')
        
        x,new_df=helper.most_busy_users(df)
        
        st.title('Top Statisics')
        col1,col2=st.columns(2)

        with col1:
            fig,ax=plt.subplots()
            ax.bar(x.index,x.values,color='red')
            plt.xticks(rotation=90)
            st.pyplot(fig)
        with col2:
            st.dataframe(new_df)


        # WordCloud
        st.title('WordCloud')
        df_wc=helper.create_wordcloud(selected_user,df)
        fig,ax=plt.subplots()
        ax.axis("off")
        ax.imshow(df_wc)
        st.pyplot(fig)


        # Most Common Words
        st.title('Most Common Words')
        df_common_words=helper.most_common_words(selected_user,df)
        fig,ax=plt.subplots()
        ax.barh(df_common_words[0],df_common_words[1])
        st.pyplot(fig)
        

        # Emoji Analysis
        st.title("Emojis Analysis")
        df_emoji=helper.emoji_ana(selected_user,df)
        st.dataframe(df_emoji)


        # Timeline
        st.title('Monthly Timeline')
        df_timeline=helper.monthly_timeline(selected_user,df)
        fig,ax=plt.subplots()
        plt.plot(df_timeline['time'],df_timeline['message'],color='green')
        plt.xticks(rotation=90)
        st.pyplot(fig)


        # Activity Map
        st.title("Activity Map")
        col1,col2=st.columns(2)
        # Most active Days
        with col1:
            st.title("Active Days")
            busy_day=helper.week_activity(selected_user,df)
            fig,ax=plt.subplots()
            ax.bar(busy_day.index,busy_day.values)
            plt.xticks(rotation=45)
            st.pyplot(fig)

        # Most active Months
        with col2:
            st.title("Active Months")
            busy_month=helper.month_activity(selected_user,df)
            fig,ax=plt.subplots()
            ax.bar(busy_month.index,busy_month.values,color='orange')
            plt.xticks(rotation=45)
            st.pyplot(fig)

        # Heatmap
        st.title("Activity Map")
        user_heatmap=helper.helper_actvity(selected_user,df)
        fig,ax=plt.subplots()
        ax=sns.heatmap(user_heatmap)
        st.pyplot(fig)