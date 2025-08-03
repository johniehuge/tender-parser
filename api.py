from fastapi import FastAPI
from fastapi.responses import JSONResponse
from parser import Tender
from typing import List
import uvicorn

class TenderAPI:
    """Class to store main logic for a Tender API"""
    
    def __init__(self, tenders: List[Tender]):
        self.app = FastAPI()
        self.tenders = tenders
        self._setup_routes()

    def _setup_routes(self):

        @self.app.get("/")
        async def root():
            return {"message": "Welcome to Tender API"}


        @self.app.get("/tenders")
        async def get_tenders():
            return JSONResponse([
                {
                    'number': tender.number,
                    'url': tender.url,
                    'title': tender.title,
                    'delivery_address': tender.delivery_address,
                    'region': tender.region,
                    'price': tender.price,
                    'end_date': tender.end_date
                }
                for tender in self.tenders
            ])

def run_api(tenders: List[Tender]):
    api = TenderAPI(tenders)
    uvicorn.run(api.app, host="0.0.0.0", port=8000)