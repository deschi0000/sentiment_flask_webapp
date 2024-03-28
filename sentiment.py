from flask import Flask, render_template, request
import urllib.request as req
import re
from bs4 import BeautifulSoup
import nltk
from nltk.sentiment import SentimentIntensityAnalyzer

import plotly.graph_objs as go

app = Flask(__name__)

@app.route('/', methods=['GET','POST'])
def home():

    if request.method == 'POST':
        url = request.form['url']
        # Here you can process the URL and return something different
        # For demonstration, let's just add a prefix to the URL
        stripped_url = url.strip()
         # Set a custom User-Agent header
        headers = {'User-Agent': 'Mozilla/5.0'}
        req_obj = req.Request(stripped_url, headers=headers)
        
        try:
            resp = req.urlopen(req_obj)
            text = resp.read()

            # ========================================================

            # Parse the HTML content using BeautifulSoup
            soup = BeautifulSoup(text, 'html.parser')

            # Find the <bsp-story-page> div
            story_page_div = soup.find('bsp-story-page')

            # url_text = story_page_div
            text = story_page_div.get_text()

            # tokenize by using python string's split and regex:
            tokens_by_re=re.split(r'\W+', text)

            # ========================================================

            # Initialize sentiment analyzer
            sid = SentimentIntensityAnalyzer()

            # Perform sentiment analysis on character's dialogueS
            # sentiment_score = sid.polarity_scores(tokens_by_re)
            sentiment_score = sid.polarity_scores(text)

            # sentiment_score = []
            # for t in tokens_by_re:
            #     sentiment_score = sid.polarity_scores(t)
            #     sentiment_score.append(sentiment_score)

            # ========================================================

            # Graph it
                        # Extract negative, neutral, and positive scores
            negative = sentiment_score['neg']
            neutral = sentiment_score['neu']
            positive = sentiment_score['pos']

            # radar
            radar_data = go.Figure(data=go.Scatterpolar(
                r=[negative, neutral, positive],
                theta=['Negative', 'Neutral', 'Positive'],
                fill='toself'
            ))
            radar_data.update_layout(
                title='Sentiment Analysis Radar Chart',
                polar=dict(
                    radialaxis=dict(
                        visible=True,
                        range=[0, 1]
                    )
                )
            )

            # bar chart
            # Create bar chart data
            bar_data = go.Figure(data=go.Bar(
                x=['Negative', 'Neutral', 'Positive'],
                y=[negative, neutral, positive],
                marker_color=['red', 'gray', 'green']
            ))
            bar_data.update_layout(
                title='Sentiment Analysis Bar Chart',
                xaxis_title='Sentiment',
                yaxis_title='Score',
                yaxis=dict(range=[0, 1])  # Adjust the y-axis range if needed
            )


            # ========================================================

            return render_template('index.html', 
                                   url_text=tokens_by_re, 
                                   sentiment_score=sentiment_score,
                                   radar_data=radar_data.to_html(full_html=False, include_plotlyjs='cdn'),
                                   bar_data=bar_data.to_html(full_html=False, include_plotlyjs='cdn'))
        except Exception as e:
            return "Error occurred: " + str(e)

        # return render_template('index.html', url_text=url_text)
    else:
    
        return render_template('index.html')


@app.route('/dave')
def dave():
    return 'Hello Dave!'




if __name__ == '__main__':
    app.run()