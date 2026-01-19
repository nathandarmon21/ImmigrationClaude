"""
Service for fetching live immigration law updates and policy changes.
"""

from typing import List, Dict, Optional
from datetime import datetime, timedelta
import aiohttp
from bs4 import BeautifulSoup
import asyncio


class ImmigrationUpdatesService:
    """Fetches and caches immigration law updates from official sources."""

    def __init__(self):
        self.cache = {}
        self.cache_duration = timedelta(hours=6)  # Cache for 6 hours

    async def get_latest_updates(self, limit: int = 10) -> List[Dict]:
        """
        Get latest immigration updates from multiple sources.

        Returns:
            List of update dictionaries with title, date, source, summary, and full_text
        """
        cache_key = "latest_updates"

        # Check cache
        if cache_key in self.cache:
            cached_time, cached_data = self.cache[cache_key]
            if datetime.now() - cached_time < self.cache_duration:
                return cached_data[:limit]

        # Fetch fresh data
        updates = []

        try:
            # Fetch from multiple sources in parallel
            tasks = [
                self._fetch_uscis_news(),
                self._fetch_state_dept_updates(),
                self._fetch_executive_orders(),
            ]

            results = await asyncio.gather(*tasks, return_exceptions=True)

            # Combine results
            for result in results:
                if isinstance(result, list):
                    updates.extend(result)

            # Sort by date (newest first)
            updates.sort(key=lambda x: x.get('date', datetime.min), reverse=True)

            # Cache results
            self.cache[cache_key] = (datetime.now(), updates)

        except Exception as e:
            print(f"Error fetching updates: {e}")
            # Return cached data if available, even if expired
            if cache_key in self.cache:
                return self.cache[cache_key][1][:limit]

        return updates[:limit]

    async def _fetch_uscis_news(self) -> List[Dict]:
        """Fetch latest news from USCIS."""
        updates = []

        try:
            async with aiohttp.ClientSession() as session:
                url = "https://www.uscis.gov/news"
                async with session.get(url, timeout=10) as response:
                    if response.status == 200:
                        html = await response.text()
                        soup = BeautifulSoup(html, 'html.parser')

                        # This is a simplified parser - actual USCIS structure may vary
                        # In production, you'd need to inspect the actual HTML structure
                        news_items = soup.find_all('article', limit=5) or soup.find_all('div', class_='news-item', limit=5)

                        for item in news_items:
                            try:
                                title_elem = item.find('h2') or item.find('h3') or item.find('a')
                                title = title_elem.get_text(strip=True) if title_elem else "Untitled"

                                link_elem = item.find('a')
                                link = link_elem.get('href', '') if link_elem else ''
                                if link and not link.startswith('http'):
                                    link = f"https://www.uscis.gov{link}"

                                summary_elem = item.find('p')
                                summary = summary_elem.get_text(strip=True) if summary_elem else ""

                                updates.append({
                                    'title': title,
                                    'date': datetime.now(),  # Would parse actual date from page
                                    'source': 'USCIS',
                                    'source_url': link or 'https://www.uscis.gov/news',
                                    'summary': summary[:300] if summary else "No summary available",
                                    'full_text': None,  # Would fetch full article if needed
                                    'category': 'policy_update'
                                })
                            except Exception as e:
                                print(f"Error parsing USCIS news item: {e}")
                                continue

        except Exception as e:
            print(f"Error fetching USCIS news: {e}")

        return updates

    async def _fetch_state_dept_updates(self) -> List[Dict]:
        """Fetch visa bulletin and travel updates from State Department."""
        updates = []

        try:
            # Visa Bulletin is published monthly
            updates.append({
                'title': 'Current Visa Bulletin',
                'date': datetime.now(),
                'source': 'U.S. Department of State',
                'source_url': 'https://travel.state.gov/content/travel/en/legal/visa-law0/visa-bulletin.html',
                'summary': 'Monthly bulletin showing immigrant visa availability and priority dates for family and employment-based categories.',
                'full_text': None,
                'category': 'visa_bulletin'
            })
        except Exception as e:
            print(f"Error fetching State Dept updates: {e}")

        return updates

    async def _fetch_executive_orders(self) -> List[Dict]:
        """Fetch recent executive orders related to immigration."""
        updates = []

        try:
            # Federal Register for executive orders
            async with aiohttp.ClientSession() as session:
                url = "https://www.federalregister.gov/api/v1/documents.json"
                params = {
                    'conditions[term]': 'immigration',
                    'conditions[type][]': 'PRESDOCU',
                    'per_page': 5,
                    'order': 'newest'
                }

                async with session.get(url, params=params, timeout=10) as response:
                    if response.status == 200:
                        data = await response.json()

                        for doc in data.get('results', []):
                            updates.append({
                                'title': doc.get('title', 'Untitled'),
                                'date': datetime.fromisoformat(doc['publication_date']) if 'publication_date' in doc else datetime.now(),
                                'source': 'Federal Register',
                                'source_url': doc.get('html_url', ''),
                                'summary': doc.get('abstract', 'No summary available')[:300],
                                'full_text': doc.get('full_text_xml_url'),
                                'category': 'executive_order'
                            })
        except Exception as e:
            print(f"Error fetching executive orders: {e}")

        return updates

    async def get_update_details(self, source_url: str) -> Optional[Dict]:
        """
        Fetch full details and legal text for a specific update.

        Args:
            source_url: URL of the update

        Returns:
            Dictionary with full text and parsed legal details
        """
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(source_url, timeout=15) as response:
                    if response.status == 200:
                        html = await response.text()
                        soup = BeautifulSoup(html, 'html.parser')

                        # Extract main content
                        main_content = soup.find('main') or soup.find('article') or soup.find('div', class_='content')
                        full_text = main_content.get_text(strip=True) if main_content else "Content not available"

                        return {
                            'full_text': full_text,
                            'html_content': str(main_content) if main_content else None,
                            'fetched_at': datetime.now().isoformat()
                        }
        except Exception as e:
            print(f"Error fetching update details: {e}")
            return None

    async def search_updates(self, query: str, category: Optional[str] = None) -> List[Dict]:
        """
        Search for specific immigration updates.

        Args:
            query: Search query (e.g., "H-1B", "green card backlog")
            category: Optional category filter

        Returns:
            List of matching updates
        """
        all_updates = await self.get_latest_updates(limit=50)

        # Simple keyword search
        query_lower = query.lower()
        results = []

        for update in all_updates:
            if category and update.get('category') != category:
                continue

            if (query_lower in update.get('title', '').lower() or
                query_lower in update.get('summary', '').lower()):
                results.append(update)

        return results
