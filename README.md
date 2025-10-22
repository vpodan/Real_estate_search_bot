# Real Estate Search System

AI-powered real estate search system with MongoDB and vector database integration.

## Features

- **Web Scraping**: Collects real estate listings from Otodom.pl using Scrapy
- **MongoDB Storage**: Stores scraped data in MongoDB database
- **Vector Database**: Chroma vector database for semantic search
- **Hybrid Search**: Combines MongoDB filtering with semantic search
- **OpenAI Integration**: Uses OpenAI embeddings for semantic search
- **Multi-language Support**: Polish interface with natural language queries

## Architecture

```
Otodom.pl → Scrapy → MongoDB → Vector DB (Chroma) → Semantic Search
```

## Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/real-estate-search-bot.git
cd real-estate-search-bot
```

2. Create virtual environment:
```bash
python -m venv venv
venv\Scripts\activate  # Windows
# or
source venv/bin/activate  # Linux/Mac
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Set up environment variables:
```bash
# Create .env file with your API keys
OPENAI_API_KEY=your_openai_api_key_here
```

## Usage

### 1. Scrape Data
```bash
python scarpy.py
```

### 2. Populate Vector Database
```bash
python real_estate_vector_db.py --populate --stats
```

### 3. Run Hybrid Search
```bash
python hybrid_search.py
```

### 4. Test Semantic Search
```bash
python demo_system.py
```

## Files Description

- `scarpy.py` - Web scraping spiders for Otodom.pl
- `main.py` - MongoDB search and natural language processing
- `hybrid_search.py` - Hybrid search implementation
- `real_estate_vector_db.py` - Vector database management
- `real_estate_embedding_function.py` - Embedding functions and text processing
- `app.py` - Flask web application for WhatsApp integration

## Requirements

- Python 3.8+
- MongoDB
- OpenAI API key
- Required Python packages (see requirements.txt)


