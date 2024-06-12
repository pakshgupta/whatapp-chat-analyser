from urlextract import URLExtract
from wordcloud import WordCloud
extractor=URLExtract()
from collections import Counter
import pandas as pd
import emoji
import numpy as np

def fetch_stats(selected_user,df):
    if selected_user!='Overall':
        df=df[df['user']==selected_user]

    # 1. Fetching number of messages
    num_messages=df.shape[0]

    # 2. Fetching number of words
    words=[]
    for i in df['message']:
        words.extend(i.split())

    # 3. Fetching number of media files
    num_media=df[df['message']=='<Media omitted>'].shape[0]

    # 4. # Fetching no of URL
    links=[]
    for i in df['message']:
        links.extend(extractor.find_urls(i))
    

    return num_messages,len(words),num_media,len(links)


def most_busy_users(df):
    busy_user=df['user'].value_counts().head(5)
    df=round((df['user'].value_counts()/df.shape[0])*100,2).reset_index().rename(columns={'user':'name','count':'percentage'})
    
    return busy_user,df

def create_wordcloud(selected_user,df):
    if selected_user!='Overall':
        df=df[df['user']==selected_user]

    # Remove group messages(notifications)
    temp=df[df['user'] !='Group Notification']

    # Remove Media Omitted messages
    temp=temp[temp['message']!='<Media omitted>']
    
    wc = WordCloud(width=500, height=500, min_font_size=10, background_color='white')
    dc_wc=wc.generate(temp['message'].str.cat(sep=' '))
    return dc_wc

def most_common_words(selected_user,df):
    f = open('stop_hinglish.txt','r')
    stop_words=f.read()

    if selected_user!='Overall':
        df=df[df['user']==selected_user]

    # Remove group messages(notifications)
    temp=df[df['user'] !='Group Notification']

    # Remove Media Omitted messages
    temp=temp[temp['message']!='<Media omitted>']

    # Remove stop words
    words=[]
    for x in temp['message']:
        for word in x.lower().split():
            if word not in stop_words:
                words.append(word)

    df_common_words=pd.DataFrame(Counter(words).most_common(20))
    
    return df_common_words

def emoji_ana(selected_user,df):
    if selected_user!='Overall':
        df=df[df['user']==selected_user]
    emojis = []
    for x in df['message']:
        emojis.extend([c for c in x if c in emoji.EMOJI_DATA])
    df_emoji=pd.DataFrame(Counter(emojis).most_common(len(Counter(emojis))))
    return df_emoji

def monthly_timeline(selected_user,df):
    if selected_user!='Overall':
        df=df[df['user']==selected_user]

    timeline=df.groupby(['year','month_num','month']).count()['message'].reset_index()
    time=[]
    for i in range(timeline.shape[0]):
        time.append(timeline['month'][i] + "-" + str(timeline['year'][i]))

    timeline['time']=time
    return timeline

def week_activity(selected_user,df):
    if selected_user!='Overall':
        df=df[df['user']==selected_user]

    return df['day_name'].value_counts()


def month_activity(selected_user,df):
    if selected_user!='Overall':
        df=df[df['user']==selected_user]

    return df['month'].value_counts()

def helper_actvity(selected_user,df):
    if selected_user!='Overall':
        df=df[df['user']==selected_user]

    activity_heatmap_df=df.pivot_table(index='day_name',columns='period',values='message',aggfunc='count').fillna(0)
    return activity_heatmap_df