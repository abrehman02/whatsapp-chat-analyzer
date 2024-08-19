import pandas as pd
from urlextract import URLExtract
extract = URLExtract()
from wordcloud import WordCloud
from collections import Counter
import emoji

def fetch_stats(selected_user,df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]
    # fetch the number of messages
    num_messages = df.shape[0]
    # fetch the  total number of words
    words = []
    for message in df['message']:
        words.extend(message.split())

    # fetch number of media messages
    media_numbers = df[df['message'] == '<Media omitted>\n'].shape[0]

    # fetch the number of links shared
    links = []
    for message in df['message']:
        links.extend(extract.find_urls(message))

    return num_messages, len(words) , media_numbers , len(links)

def most_active_users(df):
    x = df['user'].value_counts().head()
    df = round((df['user'].value_counts()/df.shape[0])*100,2).reset_index().rename(columns={'index':'name','user':'percentage'})
    return x , df


def create_wordclooud(selected_user ,df):
    if selected_user != "Overall" :
        df = df[df['user']==selected_user]

    wc = WordCloud(width=350,height=350,min_font_size = 10,background_color='white')
    df_wc = wc.generate(df['message'].str.cat(sep=" "))
    return df_wc


def most_common_words(selected_user,df):
    f = open('stop_hinglish.txt', 'r')
    stop_words = f.read()

    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    temp = df[df['user'] != 'group_notification']
    temp = temp[temp['message'] != '<Media omitted>\n']

    words = []
    for message in temp['message']:
        for word in message.lower().split():
            if word not in stop_words:
                words.append(word)

    most_common_df = pd.DataFrame(Counter(words).most_common(20))
    return most_common_df



def emoji_helper(selected_user,df):
    if selected_user != 'Overall' :
        df = df[df['user'] == selected_user]

    emojis = []
    for message in df['message']:
        for c in message:
            if c in emoji.EMOJI_DATA:
                emojis.extend(c)

    commom_emojis = pd.DataFrame(Counter(emojis).most_common(len(Counter(emojis))))
    return commom_emojis.head()



def monthly_timeline(selected_user,df):
    if selected_user != "Overall":
        df = df[df['user'] == selected_user]

    timeline = df.groupby(['year', 'month_num', 'month']).count()['message'].reset_index()

    time = []

    for i in range(timeline.shape[0]):
        time.append(timeline['month'][i] + '-' + str(timeline['year'][i]))

    timeline['time'] = time

    return timeline

def daily_timeline(selected_user, df):

    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    daily_timeline = df.groupby(['only_time']).count()['message'].reset_index()
    return daily_timeline


def week_activity_map(selected_user, df):

    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    return df['day_name'].value_counts()


def monthly_activity_map(selected_user , df):

    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]


    return df['month'].value_counts()


def activity_heatmap(selected_user,df):

    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    user_heatmap = df.pivot_table(index='day_name', columns = 'period' ,values = 'message', aggfunc = 'count').fillna(0)

    return user_heatmap