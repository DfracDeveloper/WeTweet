from datetime import datetime
import pandas as pd
import numpy as np
import json
import seaborn as sns
import matplotlib as plt
import plotly.offline as pyo
import plotly.graph_objects as go
import plotly.figure_factory as ff
import plotly.express as px
from os import listdir
from os.path import isfile, join
import ast
import matplotlib.pyplot as plt
import re
from PIL import Image
import glob

# Timeline of the tweets
def timeline(data_df):
    dated_df = data_df['Date'].value_counts()
    dated_df = pd.DataFrame(dated_df)
    dated_df.reset_index(inplace=True)
    dated_df = dated_df.rename(columns= {'index' : 'date', 'Date' : 'count'})
    dated_df = dated_df.sort_values(by='date')

    title = 'Tweets Timeline'
    labels = ['Tweets']
    colors = ['crimson', 'rgb(49,130,189)', 'rgb(49,130,189)', 'rgb(189,189,189)']

    mode_size = [8, 8, 12, 8]
    line_size = [2, 2, 4, 2]

    if dated_df.shape[0] > 1:

        x_data = np.array([dated_df['date']
                        ])

        y_data = np.array([
            dated_df['count']
        ])

        fig = go.Figure()

        for i in range(0, 1):
            fig.add_trace(go.Scatter(x=x_data[i], y=y_data[i], mode='lines',
                name=labels[i],
                line=dict(color=colors[i], width=line_size[i]),
                connectgaps=True,
            ))

            # endpoints
        #     fig.add_trace(go.Scatter(
        #         x=[x_data[i][0], x_data[i][-1]],
        #         y=[y_data[i][0], y_data[i][-1]],
        #         mode='markers',
        #         marker=dict(color=colors[i], size=mode_size[i])
        #     ))

        fig.update_layout(
            xaxis=dict(
                showline=True,
                showgrid=False,
                showticklabels=True,
                linecolor='rgb(204, 204, 204)',
                linewidth=2,
                ticks='outside',
                tickfont=dict(
                    family='Arial',
                    size=12,
                    color='rgb(82, 82, 82)',
                ),
            ),
            yaxis=dict(
                showgrid=True,
                zeroline=True,
                showline=True,
                showticklabels=True,
            ),
            autosize=True,
            margin=dict(
                autoexpand=True,
                l=100,
                r=20,
                t=110,
            ),
            showlegend=True,
            plot_bgcolor='white'
        )

        annotations = []

        # Adding labels
        for y_trace, label, color in zip(y_data, labels, colors):
            # labeling the left_side of the plot
            annotations.append(dict(xref='paper', x=-0.01, y=y_trace[0],
                                        xanchor='right', yanchor='middle',
                                        text= ' ',
                                        font=dict(family='Arial',
                                                    size=16),
                                        showarrow=False))
            # labeling the right_side of the plot
            annotations.append(dict(xref='paper', x=0.85, y=y_trace[1],
                                        xanchor='left', yanchor='middle',
                                        text=' ',
                                        font=dict(family='Arial',
                                                    size=16),
                                        showarrow=False))
        # Title
        annotations.append(dict(xref='paper', yref='paper', x=0.0, y=1.15,
                                    xanchor='left', yanchor='bottom',
                                    text='Tweets Timeline',
                                    font=dict(family='Arial',
                                                size=30,
                                                color='rgb(37,37,37)'),
                                    showarrow=False))
        # Source
        annotations.append(dict(xref='paper', yref='paper', x=0.5, y=1.0,
                                    xanchor='center', yanchor='top',
                                    text='The graph indicates the timeline of the tweets' +
                                        '<br>  ',
                                    font=dict(family='Arial',
                                                size=12,
                                                color='rgb(150,150,150)'),
                                    showarrow=False))

        # Source
        annotations.append(dict(xref='paper', yref='paper', x=0.5, y=-0.5,
                                    xanchor='center', yanchor='top',
                                    text='Time Series with Range Slider ' +
                                        '',
                                    font=dict(family='Arial',
                                                size=12,
                                                color='rgb(150,150,150)'),
                                    showarrow=False))

        fig.update_layout(annotations=annotations)
        fig.update_xaxes(rangeslider_visible=True, rangeselector=dict(
                buttons=list([
                    dict(count=1, label="1 day", step="day", stepmode="backward"),
                    dict(count=6, label="7 days", step="day", stepmode="backward"),
                    dict(count=1, label="1 month", step="month", stepmode="backward"),
                    dict(count=2, label="2 months", step="month", stepmode="backward"),
                    dict(step="all")
                ])
            ))

        # pyo.plot(fig, filename='save_mathura_masjid_tweets_replies_timeline.html')
        # py.plot(fig, filename='save_mathura_masjid_tweets_replies_timeline')

        return fig
    else:
        return ""
   
# Tweets per year
def tweets_per_year(data_df):
    # user_location_df['location'].value_counts()
    tweets_year_df = data_df['Tweet Year'].value_counts()
    tweets_year_df = pd.DataFrame(tweets_year_df)
    tweets_year_df.reset_index(inplace=True)
    tweets_year_df = tweets_year_df.rename(columns= {'index' : 'Year', 'Tweet Year' : 'Tweets'})

    label_colors = ['crimson', 'rgb(79, 129, 102)', 'rgb(129, 180, 179)', 'rgb(124, 103, 37)', 'rgb(146, 123, 21)', 'rgb(177, 180, 34)']

    fig = go.Figure(data=[go.Pie(labels=tweets_year_df['Year'], values=tweets_year_df['Tweets'], textinfo='label+percent',
                                insidetextorientation='radial', marker_colors=label_colors
                                )])
    fig.update_traces(hoverinfo='label+percent+name', hole=.25)
    fig.update(layout_title_text='Tweets done per year',
            layout_showlegend=True)
    return fig

# Hashtags Used
def hashtags_used(data_df):
    all_hashtags = list()
    for hashtags in data_df['Hashtags']:
        if len(hashtags) > 1:
            hashtags = ast.literal_eval(str(hashtags))
            for hashtag in hashtags:
                all_hashtags.append(hashtag.lower())
                
    hashtag_df = pd.DataFrame({'Hashtags' : all_hashtags})
    hashtag_df = hashtag_df['Hashtags'].value_counts()
    hashtag_df = pd.DataFrame(hashtag_df)
    hashtag_df.reset_index(inplace=True)
    hashtag_df = hashtag_df.rename(columns= {'index' : 'hashtags', 'Hashtags' : 'count'})

    labels = ['Accounts with The Hashtag', 'Newspaper', 'Internet', 'Radio']
    colors = ['rgb(67,67,67)', 'rgb(115,115,115)', 'rgb(49,130,189)', 'rgb(189,189,189)']

    colors = ['black',] * 25
    colors[0] = 'crimson'
    colors[1] = '#004ecb'
    colors[2] = '#004ecb'
    colors[3] = 'lightslategray'
    colors[4] = 'lightslategray'
    colors[5] = 'lightslategray'
    colors[6] = 'lightslategray'

    mode_size = [8, 8, 12, 8]
    line_size = [2, 2, 4, 2]

    x_data = np.array([hashtag_df['hashtags'].head(20)])

    y_data = np.array([
        hashtag_df['count'].head(20)
    ])

    fig = go.Figure()

    # fig = go.Figure(data=[go.Bar(
    #     x=dghc_user_mention_freq_merged_df['username'].head(10),
    #     y=dghc_user_mention_freq_merged_df['occurrence'].head(10),
    #     marker_color=colors, # marker color can be a single color value or an iterable
    # )])

    for i in range(0, 1):
        fig.add_trace(go.Scatter(x=x_data[i], y=y_data[i],
            name=labels[i],
            mode='markers',
            marker_color=colors
    #         text= y_data[i]
        ))

        # endpoints
        # fig.add_trace(go.Scatter(
        #     x=[x_data[i][0], x_data[i][-1]],
        #     y=[y_data[i][0], y_data[i][-1]],
        #     mode='markers',
        #     # marker=dict(color=colors[i], size=mode_size[i]),
        #     marker_color=colors,
        # ))

        # fig.add_shape(type="line",
        #     x0=1, y0=0, x1=x_data[i], y1=y_data[i],
        #     line=dict(color="RoyalBlue",width=3)
        # )

    for i in range(0, len(hashtag_df['hashtags'].head(20))):
        fig.add_shape(type='line',
            x0 = hashtag_df['hashtags'][i], y0 = i,
            x1 = hashtag_df['hashtags'][i],
            y1 = hashtag_df['count'][i],
            line=dict(color='rgb(115,115,115)', width = 1))

    fig.update_layout(
        xaxis=dict(
            showline=True,
            showgrid=False,
            showticklabels=True,
            linecolor='rgb(204, 204, 204)',
            linewidth=2,
            ticks='outside',
            tickfont=dict(
                family='Arial',
                size=12,
                color='rgb(82, 82, 82)',
            ),
        ),
        yaxis=dict(
            showgrid=False,
            zeroline=False,
            showline=True,
            showticklabels=True,
        ),
        autosize=True,
        margin=dict(
            autoexpand=False,
            l=100,
            r=20,
            t=110,
        ),
        showlegend=False,
        plot_bgcolor='white'
    )

    annotations = []

    # Adding labels
    for y_trace, label, color in zip(y_data, labels, colors):
        # labeling the left_side of the plot
        annotations.append(dict(xref='paper', x=-0.03, y=y_trace[0],
                                    xanchor='right', yanchor='middle',
                                    text='Count ',
                                    font=dict(family='Arial',
                                                size=16),
                                    showarrow=False))
        # labeling the right_side of the plot
        annotations.append(dict(xref='paper', x=0.5, y=2.2,
                                    xanchor='left', yanchor='middle',
                                    text='',
                                    font=dict(family='Arial',
                                                size=16),
                                    showarrow=False))
    # Title
    annotations.append(dict(xref='paper', yref='paper', x=0.0, y=1.10,
                                xanchor='left', yanchor='bottom',
                                text='Hashtags Used',
                                font=dict(family='Arial',
                                            size=30,
                                            color='rgb(37,37,37)'),
                                showarrow=False))
    # Source
    annotations.append(dict(xref='paper', yref='paper', x=0.5, y=1.08,
                                xanchor='center', yanchor='top',
                                text='Hashtags that were used maximum number of times ' +
                                    '<br> <br>',
                                font=dict(family='Arial',
                                            size=12,
                                            color='rgb(150,150,150)'),
                                showarrow=False))

    fig.update_layout(annotations=annotations)

    # pyo.plot(fig, filename='save_mathura_masjid_accounts_mentioned.html')
    # py.plot(fig, filename='save_mathura_masjid_accounts_mentioned')

    return fig

