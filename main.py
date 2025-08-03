import argparse
from parser import TenderParser
from storage import save_to_csv, save_to_sqlite

def main():
    parser = argparse.ArgumentParser(description='Парсер тендеров с rostender.info')
    parser.add_argument('--max', type=int, default=100, help='Максимальное количество тендеров')
    parser.add_argument('--output', type=str, help='Файл для сохранения (CSV или SQLite)')
    parser.add_argument('--api', action='store_true', help='Запустить FastAPI сервер')
    
    args = parser.parse_args()
    
    tender_parser = TenderParser()
    tenders = tender_parser.parse(max_tenders=args.max)
    
    if args.output:
        if args.output.endswith('.csv'):
            save_to_csv(tenders, args.output)
        elif args.output.endswith('.db') or args.output.endswith('.sqlite'):
            save_to_sqlite(tenders, args.output)
        else:
            print("Неподдерживаемый формат файла. Используйте .csv или .db/.sqlite")
    
    if args.api:
        from api import run_api
        run_api(tenders)

if __name__ == "__main__":
    main()