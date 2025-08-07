import datetime

news = []
# Function to add news item to the list
# It creates a new item with a unique ID, title, content, and timestamp.
def add_news(title, content):
    item = {
        "id": len(news) + 1,
        "title": title,
        "content": content,
        "timestamp": datetime.datetime.utcnow().isoformat()
    }

    # latest first
    news.insert(0, item)  
    return item
