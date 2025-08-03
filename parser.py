import requests
from bs4 import BeautifulSoup
from dataclasses import dataclass
from typing import List
import re


@dataclass
class Tender:
    """
    Class to store main fields for a tender object
    """
    number: str
    url: str
    title: str
    delivery_address: str
    region: str
    price: str
    end_date: str

class TenderParser:
    """
    Class to control the main parsing logic for fetching tenders.
    """
    BASE_URL = "https://rostender.info/extsearch"
    
    def parse(self, max_tenders=100) -> List[Tender]:
        tenders = []
        page = 1
        
        while len(tenders) < max_tenders:
            url = f"{self.BASE_URL}?page={page}"
            response = requests.get(url, headers={
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
            })
            response.raise_for_status()
                
            soup = BeautifulSoup(response.text, 'lxml')
            tender_articles = soup.select('article.tender-row')
            
            if not tender_articles:
                break
                
            for article in tender_articles[:max_tenders - len(tenders)]:
                try:
                    tender = self._parse_tender_article(article)
                    if tender:
                        tenders.append(tender)
                except Exception as e:
                    print(f"Ошибка при парсинге тендера: {e}")
                    continue
                        
            page += 1
            
        return tenders[:max_tenders]
    
    def _parse_tender_article(self, article) -> Tender:
        # Номер тендера
        number_tag = article.select_one('.tender__number')
        number = re.search(r'№(\d+)', number_tag.text).group(1) if number_tag else "Без номера"
        
            
        # Ссылка
        link_tag = article.select_one('a.description[href^="/"]')
        url = f"https://rostender.info{link_tag['href']}" if link_tag else "Нет ссылки"
        
        # Название
        title = link_tag.text.strip() if link_tag else "Без названия"
        
        # Место поставки (используем данные из региона, так как отдельного поля нет)
        address_tag = article.select_one('.tender-address .line-clamp')
        delivery_address = address_tag.text.strip() if address_tag else "Не указан"
        
        # Регион (извлекаем из ссылки или текста)
        region_tag = article.select_one('.tender__region-link')
        region = region_tag.text.strip() if region_tag else delivery_address
        
        # Цена
        price_tag = article.select_one('.starting-price--price')
        cleaned_price = price_tag.text.strip()
        if not cleaned_price or cleaned_price in ["—", "–", "-", "N/A", ""]:
            price = "Не указана"
        else:
            price = cleaned_price
        
        # Дата окончания
        end_date_tag = article.select_one('.tender__countdown-text')
        if end_date_tag:
            end_date_text = ' '.join(end_date_tag.stripped_strings)
            end_date = re.search(r'(\d{2}\.\d{2}\.\d{4})\s*(\d{2}:\d{2})?', end_date_text)
            end_date = f"{end_date.group(1)} {end_date.group(2) or ''}".strip() if end_date else "Не указана"
        else:
            end_date = "Не указана"
        
        return Tender(
            number=number,
            url=url,
            title=title,
            delivery_address=delivery_address,
            region=region,
            price=price,
            end_date=end_date
        )