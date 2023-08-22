import requests
import os
from twilio.rest import Client
from my_numbers import num1, num2


STOCK = "TSLA"
COMPANY_NAME = "Tesla Inc"

STOCK_ENDPOINT = "https://www.alphavantage.co/query"
NEWS_ENDPOINT = "https://newsapi.org/v2/everything"


stock_api_key = os.environ.get("STOCK_API_KEY")
news_api_key = os.environ.get("NEWS_API_KEY")

stock_params = {
    "function": "TIME_SERIES_DAILY",
    "symbol": STOCK,
    "apikey": stock_api_key
}

news_params = {
    "q": COMPANY_NAME,
    "apiKey": news_api_key
}

# stock data
stock_response = requests.get(STOCK_ENDPOINT, params=stock_params)
stock_response.raise_for_status()
stock_data = stock_response.json()

dates = stock_data["Time Series (Daily)"]
dates_list = [value for (key, value) in dates.items()]

yesterday_data = dates_list[0]
yesterday_close = float(yesterday_data["4. close"])

before_yesterday = dates_list[1]
before_yesterday_close = float(before_yesterday['4. close'])

difference = yesterday_close - before_yesterday_close

up_down = None
if difference > 0:
    up_down = "🔺"
else:
    up_down = "🔻"

difference_percentage = round(difference / yesterday_close * 100)

# news data

news_response = requests.get(NEWS_ENDPOINT, params=news_params)
news_response.raise_for_status()
news_data = news_response.json()

if difference_percentage > 4:
    articles = news_data["articles"][:3]
    article_format = [(f"{STOCK}: {up_down} {difference_percentage}%\n"
                       f"Headline: {article['title']}\nBrief: {article['description']}") for article in articles]

    for article in article_format:
        account_sid = os.environ['TWILIO_ACCOUNT_SID']
        auth_token = os.environ['TWILIO_AUTH_TOKEN']
        client = Client(account_sid, auth_token)
        message = client.messages \
            .create(
                body=article,
                from_=num1,
                to=num2
            )
        print(message.status)
