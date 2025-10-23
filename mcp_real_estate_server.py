"""
MCP Server do wyszukiwania nieruchomości z wykorzystaniem FastMCP
Integruje się z systemem hybrid_search.py
"""

from mcp.server.fastmcp import FastMCP
from dotenv import load_dotenv
from typing import Dict, List
import os
import logging

load_dotenv()


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


from hybrid_search import hybrid_search
from real_estate_vector_db import RealEstateVectorDB

# Ustawienia serwera
PORT = os.environ.get("PORT", 10000)

# Tworzymy serwer MCP
mcp = FastMCP("real-estate-search", host="0.0.0.0", port=PORT)

# Inicjalizujemy bazę danych wektorową
vector_db = RealEstateVectorDB()

@mcp.tool()
def search_real_estate(query: str, max_results: int = 10) -> List[Dict]:
    """
    Wyszukiwanie nieruchomości w języku naturalnym.
    
    Obsługuje wyszukiwanie mieszkań, domów, pokoi do wynajęcia i sprzedaży w Polsce.
    Używa wyszukiwania hybrydowego (MongoDB + wyszukiwanie semantyczne).
    
    Args:
        query: Zapytanie w języku naturalnym, np.: 
               'chcę kupić 2-pokojowe mieszkanie w Warszawie do 500000 zł' 
               lub 'szukam mieszkania do wynajęcia na Mokotowie'
        
    Returns:
        Lista znalezionych ogłoszeń ze szczegółowymi informacjami
    """
    try:
        logger.info(f"Wykonywanie wyszukiwania: {query}")
        
        # Wykonujemy wyszukiwanie hybrydowe
        search_results = hybrid_search(query)
        
        if not search_results or search_results is None:
            return [{
                "error": "Nie znaleziono wyników dla Twojego zapytania",
                "message": "Spróbuj zmienić kryteria wyszukiwania"
            }]
        
        # Pobieramy końcowe wyniki z hybrid_search
        results = search_results.get("final_results", [])
        
        if not results:
            return [{
                "error": "Nie znaleziono wyników dla Twojego zapytania",
                "message": "Spróbuj zmienić kryteria wyszukiwania"
            }]
        
        # Ograniczamy liczbę wyników
        
        
        # Formatujemy wyniki dla MCP
        formatted_results = []
        for result in results:
            formatted_result = {
                "title": result.get('title', 'Bez tytułu'),
                "price": result.get('price', 'Nie podana'),
                "room_count": result.get('room_count', 'Nie podane'),
                "space_sm": result.get('space_sm', 'Nie podana'),
                "city": result.get('city', 'Nie podane'),
                "district": result.get('district', 'Nie podane'),
                "link": result.get('link', ''),
                "score": result.get('score', 0),
                "description": result.get('description', '')[:200] + "..." if result.get('description') else ""
            }
            formatted_results.append(formatted_result)
        
        return formatted_results
        
    except Exception as e:
        logger.error(f"Błąd podczas wyszukiwania: {e}")
        return [{
            "error": "Wystąpił błąd podczas wyszukiwania",
            "message": str(e)
        }]

@mcp.tool()
def get_database_stats() -> Dict:
    """
    Pobierz statystyki bazy danych nieruchomości.
    
    Returns:
        Słownik ze statystykami bazy danych
    """
    try:
        stats = vector_db.get_stats()
        
        return {
            "total_listings": stats.get('total', 0),
            "rent_listings": stats.get('rent', 0),
            "sale_listings": stats.get('sale', 0),
            "status": "success"
        }
        
    except Exception as e:
        logger.error(f"Błąd podczas pobierania statystyk: {e}")
        return {
            "error": "Wystąpił błąd podczas pobierania statystyk",
            "message": str(e),
            "status": "error"
        }

# Uruchamiamy serwer
if __name__ == "__main__":
    logger.info(f"Uruchamianie serwera MCP do wyszukiwania nieruchomości na porcie {PORT}")
    mcp.run(transport="streamable-http")
