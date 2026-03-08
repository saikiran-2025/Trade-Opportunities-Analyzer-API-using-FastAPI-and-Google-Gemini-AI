import requests
from bs4 import BeautifulSoup
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def get_market_news(sector: str, max_headlines: int = 10):
    """
    Scrape market news headlines for a given sector from Google News India
    """
    url = f"https://news.google.com/search?q={sector.replace(' ', '+')}+india+market+when:7d"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }
    
    try:
        logger.info(f"Fetching news for sector: {sector}")
        response = requests.get(url, headers=headers, timeout=15)
        response.raise_for_status()  # Raises exception for bad status
        
        soup = BeautifulSoup(response.text, "html.parser")
        headlines = []
        
        # Better selector for Google News articles
        articles = soup.find_all("a", href=True)[:max_headlines * 2]
        
        for a in articles:
            text = a.get_text().strip()
            if len(text) > 20 and len(headlines) < max_headlines:
                # Filter out navigation links and short text
                if any(word in text.lower() for word in ['google', 'news', 'home', 'more']):
                    continue
                headlines.append(text)
        
        if not headlines:
            headlines = [f"No recent news found for {sector} sector."]
            
        logger.info(f"Found {len(headlines)} headlines for {sector}")
        return headlines
        
    except requests.exceptions.RequestException as e:
        logger.error(f"Error fetching news for {sector}: {str(e)}")
        return [f"Error fetching news for {sector}: {str(e)}"]
    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}")
        return ["Error processing news data"]
