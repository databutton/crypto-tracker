from cgitb import enable
import inspect
from turtle import width
import ccxt
import databutton as db
import streamlit as st
import pandas as pd
from streamlit_option_menu import option_menu
from tracker.slack import post_message_to_slack
from discord_webhook import DiscordWebhook
from tracker.strategies import list_of_strategies
from streamlit import components
import plotly.graph_objects as go



@db.apps.streamlit(route='/app')
def app():
    ftx = ccxt.ftx()
    markets = ftx.load_markets()
    monitors = db.storage.dataframes.get('monitored_signals')

    with st.sidebar:
         selected = option_menu("Crypto Tracker", ["Status", "Add Tracker", 'Strategies', 'Notifications'], 
         icons=['house', 'gear','send','pen'], menu_icon="cast", default_index=0)
         selected

         

    if(selected=='Status'):
        st.title('Tracker Status')
        st.markdown("""---""")
        show = st.container()

        t1, t2, t3, t4, t5, t6 = st.columns(6)
        t1.write('**NAME**')
        t2.write('**TICKER**')
        t3.write('**ADVICE**')
        t4.write('**STRATEGY**')
        t5.write('**CHECKED**')
        t6.write('  ')
        
        view_buttons={}
        for ix, row in monitors.iterrows():
            t1, t2, t3, t4, t5, t6 = st.columns(6)
            t1.write(row['Name'])
            t2.write(row['Ticker'])
            t3.write(row['Advice'])
            t4.write(row['Strategy'])
            t5.write(row['Checked'])
            view_buttons[row['Ticker']] = t6.button('View', key=row['Ticker'])

        for key in view_buttons.keys():
            ix = monitors[monitors['Ticker'] == key].index[0]
            btn = view_buttons[key]
            dune_emb = (monitors.loc[ix, 'Dune embed']!='')
            if(btn and not dune_emb):
                show.write('**'+key + ' tracker**', anchor='inspect')
                candle = ftx.fetchOHLCV(key, '1d')
                df = pd.DataFrame(data=candle, columns=['Date', 'Open', 'High', 'Low', 'Close', 'Volume'])
                df['Date'] = pd.to_datetime(df.Date, unit='ms')
                fig = go.Figure(data=[go.Candlestick(x=df['Date'],
                                open=df['Open'],
                                high=df['High'],
                                 low=df['Low'],
                            close=df['Close'])])
                show.plotly_chart(fig)
                show.markdown("""---""")
            elif(btn and dune_emb):
                show.write('**'+key + ' tracker**', anchor='inspect')
                with show:
                    st.markdown("""<style>iframe {background-color: white;}</style>""", unsafe_allow_html=True)
                    components.v1.iframe(monitors.loc[ix,'Dune embed'], width=600, height=400)
                #components.v1.iframe('https://dune.xyz/embeds/208941/391702/2cbe40da-a0e4-43ac-896b-fef6d4d9fda7')



        st.markdown("""---""")
        st.write('**What is Crypto Tracker?**')
        st.write('''
                    Crypto tracker continuously monitors Crypto assets on FTX of your choice, 
                    evaluates them against your chosen strategy, 
                    and sends you notifications on e-mail, Slack, or Discord.
                    
                    ''')

        

    elif(selected=='Add Tracker'):
        st.title('Add a new Tracker')
        st.write('''Here you can add a new tracker. Note that all trackers act on the FTX exchange. 
                    If you have a Dune dashboard you normally use, you can embed that with the tracker. ''')


        
       

        with st.expander("Add a new tracker", expanded=True): 
            name     = st.text_input('Name')
            ticker   = st.selectbox('Market',   options=markets.keys())
            strategy = st.selectbox('Strategy', options=list_of_strategies.keys())
            descript = st.text_area('Description')
            dune     = st.text_input('Dune embed url')
            add      = st.button('Add')
    

            if(add):
                dd = pd.DataFrame(data=[[name, ticker, strategy, descript, dune,'None' , 0]], columns=['Name', 'Ticker', 'Strategy', 'Description','Dune embed',  'Advice', 'Checked'])
                if(len(monitors)==0):
                    monitors = dd
                else:
                    monitors.loc[len(monitors)] = dd.loc[0]

                db.storage.dataframes.put(monitors, 'monitored_signals')


    elif(selected=='Notifications'):
        st.title('Notification settings')
        st.write('''When a tracker changes its recommendation, 
        you will be notified in all the ways you configure below.
        ''')
        with st.expander("Setup Slack notifications"):
            st.write('''You need to duplicate this project into your own account to setup notifications.
                        To setup Slack notifications, first create an app using https://api.slack.com/apps.
                        Next, add your app's Slack Token as a Databutton secret called 'slack-token'
                        (see https://docs.databutton.com/#/?id=secrets). Then, fill inn the below information as desired:  ''')
            df_slack = db.storage.dataframes.get('slack-config')
            if(len(df_slack) == 0):
                slack_channel = st.text_input(label='Channel')
                slack_icon_emoji = st.text_input(label='icon', value= ':see_no_evil:')
                slack_user_name = st.text_input(label='User name')
                slack_enabled = st.checkbox(label='Enabled')
            else:
                row = df_slack.iloc[0]
                slack_channel = st.text_input(label='Channel', value=row['channel'])
                slack_icon_emoji = st.text_input(label='icon', value=row['icon_emoji'])
                slack_user_name = st.text_input(label='User name', value=row['user name'])
                slack_enabled = st.checkbox(label='Enabled', value=row['enabled'])
            
            test = st.button('Test')
            if(test and bool(slack_enabled)):
                post_message_to_slack('I am the Crypto bot', slack_channel, slack_icon_emoji, slack_user_name)
            
            save = st.button('Save')
            if(save):
                df_slack = pd.DataFrame(columns=['channel', 'user name', 'icon_emoji', 'enabled'])
                df_slack['channel']   = [slack_channel]
                df_slack['user name'] = [slack_user_name]
                df_slack['icon_emoji']= [slack_icon_emoji]
                df_slack['enabled']   = [slack_enabled]
                db.storage.dataframes.put(df_slack.reset_index(drop=True), 'slack-config')



        with st.expander("Setup Discord notifications"):
            st.write('''To setup Discord notifications, first create a Webhook in the **Intergrations** section of
                        the **Server Settings**. Then, paste that here:''')

            df_discord = db.storage.dataframes.get('discord-config')
            if(len(df_discord) == 0):
                webhook = st.text_input(label='Webhook url')
                wh_enabled = st.checkbox(label='Enabled', key='when')
            else:
                row = df_discord.iloc[0]
                webhook = st.text_input(label='Webhook url', value=row['url'])
                wh_enabled = st.checkbox(label='Enabled', value=row['enabled'], key='when')

            ds_test = st.button('Test', key='ds_test')
            if(ds_test and bool(wh_enabled)):
                webhook = DiscordWebhook(url=webhook, content='I am the crypto bot')
                webhook.execute()

            ds_save = st.button('Save', key='ds_save')
            if(ds_save):
                df_discord = pd.DataFrame(data=[[webhook, wh_enabled]],columns=['url', 'enabled'])
                db.storage.dataframes.put(df_discord.reset_index(drop=True), 'discord-config')
                



    elif(selected=='Strategies'):
        st.title('Strategies')
        st.write('''Here you can can find all the strategies available to use with a tracker.
                    To add your own strategy, first you need to duplicate the project. Then, you need 
                    to open **strategies.py** and add your own function like the ones below -- that is it.
        ''')
        slct = st.selectbox('View Strategy', options=list_of_strategies.keys())
        lines = inspect.getsource(list_of_strategies[slct])
        st.code(body=lines,language='python')


      