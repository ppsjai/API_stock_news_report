# Stock News Monitoring Project

# 1st fetch current stock price
# get an news about stock market what name of the stock we are currently using 
# to send alerts sending by sending SMS in your mobile by twilio 

# now we are going to pull stock market data today's closing date share price was for example $1000
# we are going to compare to yesterdays closing price $900
# and we going to calculate it's percentage how much it increase

# NOTE 🚫 Free Plan Limitations:
# Maximum of 25 API requests per day
# Maximum of 5 API requests per minute
import requests
import json
from twilio.rest import Client

VIRTUAL_TWILIO_NUMBER = "your virtual twilio number"
VERIFIED_NUMBER = "your own phone number verified with Twilio"

# we can use any stock names
STOCK_NAME = "TSLA"
COMPANY_NAME = "Tesla Inc"
# STEP 1: Use https://www.alphavantage.co/documentation/#daily --> read the documentation
STOCK_ENDPOINT = "https://www.alphavantage.co/query"
NEWS_ENDPOINT = "https://newsapi.org/v2/everything"

# from alphavantage.co to create an free API key by providing the given credentials have to fill inorder to get Free API key
STOCK_API_KEY = "YOUR OWN API KEY FROM ALPHAVANTAGE"
# For NEWSAPI documentation https://newsapi.org/docs/endpoints/top-headlines 1st create an account
NEWS_API_KEY = "YOUR OWN API KEY FROM NEWSAPI"

# THIS is twilio SID_number and auth_token from your account
TWILIO_SID = "YOUR TWILIO ACCOUNT SID"
TWILIO_AUTH_TOKEN = "YOUR TWILIO AUTH TOKEN"

# When stock price increase/decreases by 5% between yesterday and the day before yesterday then print("Get News").

#TODO-1: Get yesterday's closing stock price
stock_report = {
    "function": "TIME_SERIES_DAILY",
    "symbol": STOCK_NAME,
    "apikey": STOCK_API_KEY,
    "outputsize": "compact",
    "datatype": json,
}

response = requests.get(STOCK_ENDPOINT, params=stock_report)
print(response.status_code)
daily_report = response.json()["Time Series (Daily)"]
converting_list = [value for (key, value) in daily_report.items()]
today_data = converting_list[0]
today_closing_price = today_data["4. close"]
print(today_closing_price)
print(converting_list)
print(response.json())

#Get the day before yesterday's closing stock price
yesterday_data = converting_list[1]
yesterday_closing_price = yesterday_data["4. close"]
print(f"24/07/2025 closing stock price report: {today_closing_price}") #
print(f"23/07/2025 closing stock price report: {yesterday_closing_price}")

#TODO-2: Find the positive difference between 1 and 2. e.g. 40 - 20 = -20, but the positive difference is 20.
# Hint: https://www.w3schools.com/python/ref_func_abs.asp
difference = float(today_closing_price) - float(yesterday_closing_price)
print(difference) # 27.25999999999999

up_down = None
if difference > 0:
    up_down = "🔺"
else:
    up_down = "🔻"

#TODO-3: to find out the percentage in between the closing stock price  today and yesterday.
percentage = round((difference / float(today_closing_price)) * 100)
print(percentage) # 8.928922371437926

# STEP 2: Instead of printing ("Get News"), actually get the first 3 news pieces for the COMPANY_NAME.
# TODO-4: go to news-API create an account for free API key
# for documentation how we use our dict https://newsapi.org/docs/endpoints/everything
# for Title link: https://newsdata.io/blog/how-do-q-qintitle-qinmeta-works/
# The “qInTitle” parameter is short for “query in title.”

#TODO-5: If difference percentage is greater than 5 then print("Get News").
if abs(percentage) > 1:
    news_params = {
        "apiKey": NEWS_API_KEY,
        "qInTitle": COMPANY_NAME,
    }

    news_response = requests.get(NEWS_ENDPOINT, params=news_params)
    articles = news_response.json()["articles"]
    print(articles)

#Todo-6: using python slice operator to slice that we get an particular part of info Hint: https://stackoverflow.com/questions/509211/understanding-slice-notation
    three_articles = articles[:3] # to get only 3 set of articles
    print(three_articles)

#TODO-7: Use Twilio to send a separate message with each article's title and description to your phone number.

#Create a new list of the first 3 article's headline and description using list comprehension.
    articles_in_format = [f"{STOCK_NAME}: {up_down}{percentage}%\nHeadline: {article['title']}. \nBrief: {article['description']}" 
                          for article in three_articles]
    print(articles_in_format)
#Send each article as a separate message via Twilio.
    client = Client(TWILIO_SID, TWILIO_AUTH_TOKEN)

#TODO-8. - Send each article as a separate message via Twilio.
    for article in articles_in_format:
        message = client.messages.create(
            body=article,
            from_=VIRTUAL_TWILIO_NUMBER,
            to=VERIFIED_NUMBER
        )
