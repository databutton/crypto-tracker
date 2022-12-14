import databutton as db
import pandas as pd
import tracker.indicators as indicators
from tracker.slack import post_message_to_slack
from discord_webhook import DiscordWebhook


@db.jobs.repeat_every(seconds=3600)
def eval():
    monitors = db.storage.dataframes.get('monitored_signals')
    for ix, row in monitors.iterrows():
        strategy_name = row['Indicator']
        strategy_F    = indicators.list_of_strategies[strategy_name]
        current_advice = monitors.loc[ix, 'Signal']
        advice = strategy_F(row['Ticker'])
        
        monitors.loc[ix, 'Signal'] = advice
        monitors.loc[ix, 'Checked'] = pd.Timestamp.today()

        db.storage.dataframes.put(monitors,'monitored_signals' )
        # Run notifications
        if(current_advice != advice):
            msg = monitors.loc[ix, 'Name'] + ' Signal is now advising you to '+advice + '. Previous advice was ' + current_advice

            df_slack   = db.storage.dataframes.get('slack-config')
            if(len(df_slack)>0 and bool(df_slack.iloc[0].enabled)):
                row = df_slack.iloc[0]
                post_message_to_slack(msg, row['channel'], row['icon_emoji'], row['user name'])

            df_discord = db.storage.dataframes.get('discord-config')
            if(len(df_discord)>0 and bool(df_discord.iloc[0].enabled)):
                row = df_discord.iloc[0]
                webhook = DiscordWebhook(url=row['url'], content=msg)
                webhook.execute()



