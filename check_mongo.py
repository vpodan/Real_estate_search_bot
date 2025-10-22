#!/usr/bin/env python3
"""
Sprawdzanie danych w MongoDB
"""

from pymongo import MongoClient

def check_mongo_data():
    """Sprawdza obecność danych w MongoDB"""
    try:
        client = MongoClient("mongodb://localhost:27017/")
        db = client["real_estate"]
        
        rent_count = db["rent_listings"].count_documents({})
        sale_count = db["sale_listings"].count_documents({})
        
        print(f"Dane w MongoDB:")
        print(f"   Ogłoszeń wynajmu: {rent_count}")
        print(f"   Ogłoszeń sprzedaży: {sale_count}")
        print(f"   Wszystkich ogłoszeń: {rent_count + sale_count}")
        
        # Pokazujemy przykładowe dane
        if rent_count > 0:
            print(f"\nPrzykład ogłoszenia wynajmu:")
            sample_rent = db["rent_listings"].find_one()
            if sample_rent:
                print(f"   ID: {sample_rent.get('_id')}")
                print(f"   Tytuł: {sample_rent.get('title', 'N/A')}")
                print(f"   Miasto: {sample_rent.get('city', 'N/A')}")
                print(f"   Cena: {sample_rent.get('price', 'N/A')} zł")
        
        if sale_count > 0:
            print(f"\nPrzykład ogłoszenia sprzedaży:")
            sample_sale = db["sale_listings"].find_one()
            if sample_sale:
                print(f"   ID: {sample_sale.get('_id')}")
                print(f"   Tytuł: {sample_sale.get('title', 'N/A')}")
                print(f"   Miasto: {sample_sale.get('city', 'N/A')}")
                print(f"   Cena: {sample_sale.get('price', 'N/A')} zł")
        
        return rent_count + sale_count > 0
        
    except Exception as e:
        print(f"Błąd połączenia z MongoDB: {e}")
        return False

if __name__ == "__main__":
    check_mongo_data()
