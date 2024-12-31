from confluent_kafka import Producer 
import yfinance as yf 
import time 
import requests 
import json 

# Kafka 프로듀서 구성
headers = { 
 'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3' , 
 'Content-Type' : 'application/json' , 
 'Authorization' : 'Bearer <token>'
 } 

conf = { 
 'bootstrap.servers' : 'localhost:9092' , # Kafka 브로커 주소로 변경 
 'client.id' : 'stock-price-producer'
 } 

# Kafka 프로듀서 인스턴스 생성
producer = Producer(conf)
# 비트코인 가격을 받을 topic
topic = 'bit_topic'

ticker_symbol = ['BTC-USD', 'ETH-USD', 'DOGE-USD']

def  fetch_and_send_stock_price (): 
 while True:
        for ticker in ticker_symbol:
            try:
                # Fetch data from yfinance
                data = yf.Ticker(ticker)
                price = data.history(period="1d")['Close'].iloc[-1]
                volume = data.history(period="1d")['Volume'].iloc[-1]

                # Prepare the message
                message = {
                    "ticker": ticker,
                    "price": price,
                    "volume": int(volume),
                    "timestamp": time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime())
                }

                # Send the message to Kafka
                producer.produce(topic, key=ticker, value=json.dumps(message))
                producer.flush()
                print(f"Sent to Kafka: {message}")
            except Exception as e:
                print(f"Error fetching/sending {ticker} data: {e}")
        time.sleep(30)  # Fetch data every 30 seconds


fetch_and_send_stock_price()