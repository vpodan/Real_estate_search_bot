import os
from real_estate_vector_db import RealEstateVectorDB
from pymongo import MongoClient

def demo_system():
    print("DEMONSTRACJA SYSTEMU WYSZUKIWANIA SEMANTYCZNEGO NIERUCHOMOŚCI")
    print("=" * 70)
    
    client = MongoClient("mongodb://localhost:27017/")
    db = client["real_estate"]
    
    print("\nSTATYSTYKI BAZY DANYCH:")
    rent_count = db["rent_listings"].count_documents({})
    sale_count = db["sale_listings"].count_documents({})
    print(f"   Ogłoszeń wynajmu: {rent_count}")
    print(f"   Ogłoszeń sprzedaży: {sale_count}")
    print(f"   Wszystkich ogłoszeń: {rent_count + sale_count}")
    
    print("\nINICJALIZACJA WEKTOROWEJ BAZY DANYCH...")
    vector_db = RealEstateVectorDB()
    stats = vector_db.get_stats()
    print(f"   Wpisów wektorowych: {stats.get('total', 0)}")
    
    demo_queries = [
        {
            "query": "Chce kupić dwupokojowe  mieszkanie w warszawie z balkonem i garażem do 850000 zlotych z fajynym widokiem z okna na wysokim piętrze, w dzielnicach mokotów, wola",
            "description": "Wyszukiwanie dwupokojowych mieszkań w Warszawie w budynku nie starszym niż 2005 roku"
        }
       
    ]
    
    print("\nDEMONSTRACJA WYSZUKIWANIA SEMANTYCZNEGO:")
    print("=" * 70)
    
    for i, demo in enumerate(demo_queries, 1):
        print(f"\n{i}. {demo['description']}")
        print(f"   Zapytanie: '{demo['query']}'")
        print("-" * 50)
        
        results = vector_db.semantic_search(demo['query'], top_k=5)
        
        if results:
            for j, result in enumerate(results, 1):
                # Pobieramy pełne dane z MongoDB
                collection = db["rent_listings"] if result['metadata'].get('collection_type') == 'rent' else db["sale_listings"]
                full_data = collection.find_one({"_id": result['id']})
                
                if full_data:
                    print(f"   {j}. {full_data.get('title', 'Bez tytułu')[:160]}...")
                    print(f"      Cena: {full_data.get('price', 'N/A')} zł")
                    print(f"      Pokoje: {full_data.get('room_count', 'N/A')}, Powierzchnia: {full_data.get('space_sm', 'N/A')} m2")
                    print(f"      Dzielnica: {full_data.get('district', 'N/A')}, Miasto: {full_data.get('city', 'N/A')}")
                    print(f"      Wynik semantyczny: {result['score']:.3f}")
                    
                    # Pokazujemy udogodnienia jeśli są
                    amenities = []
                    if full_data.get('has_balcony'): amenities.append('balkon')
                    if full_data.get('has_garage'): amenities.append('garaż')
                    if full_data.get('has_elevator'): amenities.append('winda')
                    if full_data.get('furnished'): amenities.append('umeblowane')
                    
                    if amenities:
                        print(f"      Udogodnienia: {', '.join(amenities)}")
                    
                    link = full_data.get('link', 'N/A')
                    
                    print(f"      Link: {link}")
        else:
            print("   Nie znaleziono wyników")

if __name__ == "__main__":
    demo_system()
