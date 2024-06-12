import pandas as pd
import re



def preprocess(data):
    pattern = r'\d{1,2}/\d{1,2}/\d{1,2},\s\d{1,2}:\d{2}\s-\s'
    dates = re.findall(pattern, data)
    messages=re.split(pattern,data)[1:]

    df=pd.DataFrame({'user_message':messages,'date':dates})
    df['date'] = df['date'].str.strip()
    df['date'] = pd.to_datetime(df['date'],format='%d/%m/%y, %H:%M -')

    users = []
    messages = []
    for i in df['user_message']:
        parts = i.split(':')
        if len(parts) > 1:
            users.append(parts[0].strip())
            messages.append(' '.join(parts[1:]).strip())
        else:
            users.append('Group Notification')
            messages.append(i.strip())

    df['user']=users
    df['message']=messages
    
    df.drop(columns=['user_message'],inplace=True)

    df['year']=df['date'].dt.year
    df['month_num']=df['date'].dt.month
    df['day_name']=df['date'].dt.day_name()
    df['month']=df['date'].dt.month_name()
    df['day']=df['date'].dt.day
    df['hour']=df['date'].dt.hour
    df['minute']=df['date'].dt.minute

    period=[]
    for hour in df[['day_name','hour']]['hour']:
        if hour==23:
            period.append(str(hour)+ "-" + str('00'))
        elif hour==0:
            period.append(str('00')+ "-" + str(hour+1))
        else:
            period.append(str(hour)+ "-" + str(hour+1))

    df['period']=period

    return df

    
