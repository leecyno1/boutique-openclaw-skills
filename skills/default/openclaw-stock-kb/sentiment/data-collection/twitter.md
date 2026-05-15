# Twitter/X 数据抓取指南

## 概述

Twitter/X 是金融情绪分析的重要数据源，尤其是加密货币和美股领域。

## 数据采集方法

### 方法一：官方 API (推荐)

```python
import tweepy

# 认证
client = tweepy.Client(
    bearer_token="YOUR_BEARER_TOKEN",
    consumer_key="YOUR_API_KEY",
    consumer_secret="YOUR_API_SECRET",
    access_token="YOUR_ACCESS_TOKEN",
    access_token_secret="YOUR_ACCESS_TOKEN_SECRET"
)

# 搜索推文
 tweets = client.search_recent_tweets(
    query="$AAPL OR #Apple",
    max_results=100,
    tweet_fields=['created_at', 'public_metrics', 'context_annotations']
)

for tweet in tweets.data:
    print(f"{tweet.created_at}: {tweet.text}")
    print(f"Likes: {tweet.public_metrics['like_count']}")
```

### 方法二：免费替代方案

使用 Nitter 实例（无需 API Key）：

```python
import requests
from bs4 import BeautifulSoup

def scrape_nitter(query, count=20):
    """从 Nitter 抓取推文"""
    url = f"https://nitter.net/search?f=tweets&q={query}"
    response = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'})
    soup = BeautifulSoup(response.text, 'html.parser')
    
    tweets = []
    for tweet in soup.find_all('div', class_='timeline-item')[:count]:
        content = tweet.find('div', class_='tweet-content')
        if content:
            tweets.append({
                'text': content.get_text(strip=True),
                'time': tweet.find('span', class_='tweet-date'),
                'likes': tweet.find('span', class_='icon-heart')
            })
    return tweets
```

## 数据预处理

### 清洗推文

```python
import re

def clean_tweet(text):
    """清洗推文文本"""
    # 移除 URL
    text = re.sub(r'http\S+', '', text)
    # 移除 @提及
    text = re.sub(r'@\w+', '', text)
    # 移除 #标签符号（保留词）
    text = re.sub(r'#', '', text)
    # 移除多余空格
    text = re.sub(r'\s+', ' ', text).strip()
    return text
```

### 过滤金融相关推文

```python
FINANCIAL_KEYWORDS = ['stock', 'market', 'trading', 'price', 'buy', 'sell', 
                      'long', 'short', 'bull', 'bear', 'moon', 'dump']

def is_financial_tweet(text):
    """判断是否为金融相关推文"""
    text_lower = text.lower()
    return any(keyword in text_lower for keyword in FINANCIAL_KEYWORDS)
```

## 重要账户监控

### 财经大 V 列表

```python
INFLUENCERS = {
    'Elon Musk': 'elonmusk',
    'Cathie Wood': 'CathieDWood',
    'Warren Buffett': 'WarrenBuffett',
    'Ray Dalio': 'RayDalio',
    '花街调查员': 'HuaStreet_Research',  # 中文财经
}

def get_user_tweets(username, count=50):
    """获取特定用户推文"""
    tweets = client.get_users_tweets(
        id=get_user_id(username),
        max_results=count,
        tweet_fields=['created_at', 'public_metrics']
    )
    return tweets.data
```

## 数据存储

```python
import json
from datetime import datetime

def save_tweets(tweets, symbol):
    """保存推文到文件"""
    filename = f"data/tweets_{symbol}_{datetime.now().strftime('%Y%m%d')}.json"
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump([{
            'text': t.text,
            'created_at': str(t.created_at),
            'metrics': t.public_metrics
        } for t in tweets], f, ensure_ascii=False, indent=2)
```

## 注意事项

1. **API 限制**: Twitter API 有速率限制，免费版每月 1500 条推文
2. **合规使用**: 遵守 Twitter Terms of Service
3. **数据延迟**: 免费 API 有 7 天限制，需付费获取历史数据
4. **反爬措施**: 过于频繁抓取可能导致 IP 被封

## 相关阅读

- [NLP 情感分析基础](../nlp/sentiment-basics.md)
- [情绪得分计算](../indicators/sentiment-score.md)
