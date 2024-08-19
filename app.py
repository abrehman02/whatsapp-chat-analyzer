import preprocessor
import streamlit as st
import helper
import matplotlib.pyplot as plt
import seaborn as sns



st.sidebar.title('Whatsapp Chat')
uploaded_file = st.sidebar.file_uploader("Upload the File")
if uploaded_file is not None:
    # To read file as bytes:
    bytes_data = uploaded_file.getvalue()
    data = bytes_data.decode("utf-8")
    df = preprocessor.preprocess(data)
    st.dataframe(df,use_container_width=True)
    #fetch unique users
    user_list = df['user'].unique().tolist()
    user_list.remove('group_notification')
    user_list.sort()
    user_list.insert(0,'Overall')

    selected_user = st.sidebar.selectbox("Show Analysis WRT:",user_list)
    if st.sidebar.button('Show Analysis'):
        col1, col2 ,col3, col4 = st.columns(4)
        num_messages, words, num_media , links = helper.fetch_stats(selected_user, df)
        with col1:
            st.header('Total Messages')
            st.title(num_messages)
        with col2 :
            st.header('Total Words')
            st.title(words)
        with col3 :
            st.header('Media Shared')

            st.title(num_media)
        with col4 :
            st.header('Links Shared')
            st.title(links)
        if selected_user == 'Overall' :
            st.title('Most active Users')
            x , new_df = helper.most_active_users(df)
            fig , ax = plt.subplots()

            col1 ,col2 = st.columns(2)
            with col1:
                ax.bar(x.index,x.values,color ='red')
                plt.xticks(rotation = 'vertical')
                st.pyplot(fig)

            with col2:
                st.dataframe(new_df,use_container_width=True)

        # creating WorldCloud
        st.title('WorldCloud')
        df_wc = helper.create_wordclooud(selected_user,df)
        fig ,ax = plt.subplots()
        ax.imshow(df_wc)
        st.pyplot(fig)

# configure how to remove the group notification user from the dataframe
# '''

    # most commn words
        st.title('Most Common Words')
        most_common_df = helper.most_common_words(selected_user,df)
        # st.dataframe(most_common_df,use_container_width=True)
        fig,ax = plt.subplots()
        ax.barh(most_common_df[0],most_common_df[1])
        st.pyplot(fig)


    # most_common_emojis
        st.title('Most Common Emojis')
        most_common_emojis = helper.emoji_helper(selected_user,df)
        col1 , col2  = st.columns(2)
        with col1:
            fig,ax = plt.subplots()
            ax.barh(most_common_emojis[0],most_common_emojis[1])
            st.pyplot(fig)

        with col2:
            st.dataframe(most_common_emojis,use_container_width=True)


    # week activity map
        col1 , col2 = st.columns(2)


        with col1:
            st.title('Weekly Activity')
            busy_day = helper.week_activity_map(selected_user,df)
            fig , ax = plt.subplots()
            ax.bar(busy_day.index , busy_day.values)
            plt.xticks(rotation = 'vertical')
            st.pyplot(fig)

        with col2:
            st.title('Monthly Activity')
            busy_month = helper.monthly_activity_map(selected_user, df)
            fig, ax = plt.subplots()
            ax.bar(busy_month.index, busy_month.values, color = 'orange')
            plt.xticks(rotation = 'vertical')
            st.pyplot(fig)



        st.title('Activity Heatmap')
        user_heatmap  = helper.activity_heatmap(selected_user,df)
        fig, ax = plt.subplots()
        ax = sns.heatmap(user_heatmap)
        st.pyplot(fig)

  # monthly_timeline
        st.title('Monthly Timeline')
        timeline = helper.monthly_timeline(selected_user,df)
        fig,ax = plt.subplots()
        ax.plot(timeline['time'], timeline['message'])
        plt.xticks(rotation='vertical')
        st.pyplot(fig)

    # daily timeline
        st.title('Daily Timeline')
        daily_timeline = helper.daily_timeline(selected_user, df)
        fig, ax = plt.subplots()
        ax.plot(daily_timeline['only_time'], daily_timeline['message'])
        plt.xticks(rotation='vertical')
        st.pyplot(fig)
