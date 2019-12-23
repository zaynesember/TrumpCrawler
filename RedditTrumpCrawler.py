
import praw
from datetime import datetime
import time
import gspread
from oauth2client.service_account import ServiceAccountCredentials

# tracks what row in the sheet we're writing data to
cursor = 3

# will be used to store # of instances of keyword
count_new, count_hot, count_top, count_rising = 0, 0, 0, 0
count_new2, count_hot2, count_top2, count_rising2 = 0, 0, 0, 0
count_new3, count_hot3, count_top3, count_rising3 = 0, 0, 0, 0


# Puts all the words from politics posts into a single list
def list_builder(keyword0, keyword1):

    # this is bad practice but the best down and dirty way to implement a cursor
    global cursor

    # will be used to store # of instances of keyword
    global count_new, count_hot, count_top, count_rising
    global count_new2, count_hot2, count_top2, count_rising2
    global count_new3, count_hot3, count_top3, count_rising3

    # use creds to create a client to interact with the Google Drive API
    # obviously would need to get your own credentials to make this work
    scope = ['https://www.googleapis.com/auth/drive']
    creds = ServiceAccountCredentials.from_json_keyfile_name('credentials.json', scope)
    client = gspread.authorize(creds)

    # Find a workbook by name and open the first sheet
    sheet = client.open("Reddit Data").sheet1

    # getting our client data (my client data removed, obviously)
    reddit = praw.Reddit(client_id='',client_secret='',
                         user_agent='',username='', password='')

    # creating subreddit objects to pull from
    politics = reddit.subreddit('Politics')
    news = reddit.subreddit('News')
    world_news = reddit.subreddit('Worldnews')

    # pulling /r/politics from client
    politics_new = politics.new(limit=100,)
    politics_hot = politics.hot(limit=100,)
    politics_top = politics.top(limit=100, time_filter='day')
    politics_rising = politics.rising(limit=100)

    # pulling /r/news from client
    news_new = news.new(limit=100)
    news_hot = news.hot(limit=100)
    news_top = news.top(limit=100, time_filter='day')
    news_rising = news.rising(limit=100)

    # pulling /r/worldnews from client
    world_news_new = world_news.new(limit=100)
    world_news_hot = world_news.hot(limit=100)
    world_news_top = world_news.top(limit=100, time_filter='day')
    world_news_rising = world_news.rising(limit=100)

    # updating all of the counts
    count_new = list_processor(politics_new, count_new, keyword0, keyword1)
    count_hot = list_processor(politics_hot, count_hot, keyword0, keyword1)
    count_top = list_processor(politics_top, count_top, keyword0, keyword1)
    count_rising = list_processor(politics_rising, count_rising, keyword0, keyword1)

    # updating timestamp
    sheet.update_cell(cursor, 1, str(datetime.now()))

    # updating new
    sheet.update_cell(cursor, 2, count_new)

    # updating hot
    sheet.update_cell(cursor, 3, count_hot)

    # updating top
    sheet.update_cell(cursor, 4, count_top)

    # updating rising
    sheet.update_cell(cursor, 5, count_rising)

    # updating all of the counts
    count_new2 = list_processor(news_new, count_new2, keyword0, keyword1)
    count_hot2 = list_processor(news_hot, count_hot2, keyword0, keyword1)
    count_top2 = list_processor(news_top, count_top2, keyword0, keyword1)
    count_rising2 = list_processor(news_rising, count_rising2, keyword0, keyword1)

    # updating timestamp
    sheet.update_cell(cursor, 7, str(datetime.now()))

    # updating new
    sheet.update_cell(cursor, 8, count_new2)

    # updating hot
    sheet.update_cell(cursor, 9, count_hot2)

    # updating top
    sheet.update_cell(cursor, 10, count_top2)

    # updating rising
    sheet.update_cell(cursor, 11, count_rising2)

    # updating all of the counts for /r/politics
    count_new3 = list_processor(world_news_new, count_new3, keyword0, keyword1)
    count_hot3 = list_processor(world_news_hot, count_hot3, keyword0, keyword1)
    count_top3 = list_processor(world_news_top, count_top3, keyword0, keyword1)
    count_rising3 = list_processor(world_news_rising, count_rising3, keyword0, keyword1)

    # updating timestamp
    sheet.update_cell(cursor, 13, str(datetime.now()))

    # updating /r/politics new
    sheet.update_cell(cursor, 14, count_new3)

    # updating /r/politics hot
    sheet.update_cell(cursor, 15, count_hot3)

    # updating /r/politics top
    sheet.update_cell(cursor, 16, count_top3)

    # updating /r/politics rising
    sheet.update_cell(cursor, 17, count_rising3)

    cursor += 1
    count_new, count_hot, count_top, count_rising = 0, 0, 0, 0
    count_new2, count_hot2, count_top2, count_rising2 = 0, 0, 0, 0
    count_new3, count_hot3, count_top3, count_rising3 = 0, 0, 0, 0

# searches through each submission title looking for keywords
def list_processor(subreddit_category, count_category, keyword0, keyword1):

    for submission in subreddit_category:

        current_title = submission.title.split()

        count_category += current_title.count(keyword0) + current_title.count(keyword1)

    return count_category


start_time = time.time()

while True:
    list_builder("Trump", "Trump's")
    time.sleep(10.0 - ((time.time() - start_time) % 10.0))
