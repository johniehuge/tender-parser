import csv
import sqlite3
from typing import List
from parser import Tender

def save_to_csv(tenders: List[Tender], filename: str):
    with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
        fieldnames = ['number', 'url', 'title', 'delivery_address', 'region', 'price', 'end_date']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        
        writer.writeheader()
        for tender in tenders:
            writer.writerow({
                'number': tender.number,
                'url': tender.url,
                'title': tender.title,
                'delivery_address': tender.delivery_address,
                'region': tender.region,
                'price': tender.price,
                'end_date': tender.end_date
            })

def save_to_sqlite(tenders: List[Tender], filename: str):
    conn = sqlite3.connect(filename)
    cursor = conn.cursor()
    
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS tenders (
        number TEXT PRIMARY KEY,
        url TEXT,
        title TEXT,
        delivery_address TEXT,
        region TEXT,
        price TEXT,
        end_date TEXT
    )
    ''')
    
    for tender in tenders:
        cursor.execute('''
        INSERT OR REPLACE INTO tenders 
        VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (
            tender.number,
            tender.url,
            tender.title,
            tender.delivery_address,
            tender.region,
            tender.price,
            tender.end_date
        ))
    
    conn.commit()
    conn.close()