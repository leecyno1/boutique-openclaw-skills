# 微博/雪球中文数据采集

## 概述

中文社交媒体（微博、雪球、东方财富股吧）是A股情绪分析的重要数据源。

## 微博数据采集

### 使用微博API

```python
import requests
import json

def fetch_weibo_topics(keyword, count=50):
    """抓取微博话题"""
    # 注意：需要使用微博开放平台API
    # 申请地址：https://open.weibo.com/
    
    url = "https://api.weibo.com/2/search/topics.json"
    params = {
        'q': keyword,
        'count': count,
        'access_token': 'YOUR_ACCESS_TOKEN'
    }
    
    response = requests.get(url, params=params)
    data = response.json()
    
    return data['statuses']
```

### 雪球网数据采集

```python
import requests
from bs4 import BeautifulSoup

def fetch_xueqiu_discussion(symbol, count=20):
    """抓取雪球讨论"""
    
    headers = {
        'User-Agent': 'Mozilla/5.0',
        'Cookie': 'xq_a_token=YOUR_TOKEN'  # 需要登录获取
    }
    
    url = f"https://xueqiu.com/query/v1/symbol/search.json"
    params = {
        'symbol': symbol,
        'count': count,
        'source': 'all'
    }
    
    response = requests.get(url, headers=headers, params=params)
    return response.json()

# 提取情绪关键词
def extract_sentiment_keywords(text):
    """提取中文情感关键词"""
    positive = ['涨', '买入', '看好', '牛市', '涨停', '推荐']
    negative = ['跌', '卖出', '看空', '熊市', '跌停', '垃圾']
    
    pos_count = sum(1 for word in positive if word in text)
    neg_count = sum(1 for word in negative if word in text)
    
    return pos_count, neg_count
```

## 情绪分析

### 中文情感分析

```python
from snownlp import SnowNLP

def analyze_chinese_sentiment(text):
    """使用SnowNLP进行中文情感分析"""
    s = SnowNLP(text)
    return s.sentiments  # 0-1，越接近1越正面

# 或使用BERT模型
from transformers import pipeline

# 加载中文情感分析模型
sentiment_pipeline = pipeline("sentiment-analysis", 
                              model="uer/roberta-base-finetuned-jd-binary-chinese")

def bert_sentiment(text):
    result = sentiment_pipeline(text)[0]
    return result['label'], result['score']
```

## 监控标的

### A股热门板块

```python
HOT_SECTORS = {
    '新能源': ['宁德时代', '比亚迪', '隆基绿能'],
    '人工智能': ['科大讯飞', '寒武纪', '海康威视'],
    '中特估': ['中国移动', '中国石油', '工商银行'],
    '芯片': ['中芯国际', '韦尔股份', '兆易创新']
}

def monitor_sector_sentiment(sector):
    """监控板块情绪"""
    keywords = HOT_SECTORS[sector]
    sentiments = []
    
    for keyword in keywords:
        posts = fetch_weibo_topics(keyword)
        for post in posts:
            sentiment = analyze_chinese_sentiment(post['text'])
            sentiments.append(sentiment)
    
    avg_sentiment = sum(sentiments) / len(sentiments)
    return avg_sentiment
```

## 数据存储

```python
import sqlite3
from datetime import datetime

def save_sentiment_data(symbol, sentiment_score, source):
    """保存情绪数据到数据库"""
    conn = sqlite3.connect('sentiment.db')
    cursor = conn.cursor()
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS sentiment (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            symbol TEXT,
            sentiment REAL,
            source TEXT,
            timestamp DATETIME
        )
    ''')
    
    cursor.execute('''
        INSERT INTO sentiment (symbol, sentiment, source, timestamp)
        VALUES (?, ?, ?, ?)
    ''', (symbol, sentiment_score, source, datetime.now()))
    
    conn.commit()
    conn.close()
```

## 注意事项

1. **合规性**：遵守平台爬虫协议，控制请求频率
2. **反爬**：使用代理池，模拟正常用户行为
3. **数据清洗**：过滤广告、水军内容
4. **时效性**：中文社交媒体信息传播快，需要实时监控

## 相关工具

- **微博API**：https://open.weibo.com/
- **SnowNLP**：中文文本处理库
- **jieba**：中文分词工具
