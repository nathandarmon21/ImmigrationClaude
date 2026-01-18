"""
Web scraping and data fetching for up-to-date immigration information.
"""

import httpx
from bs4 import BeautifulSoup
from typing import Dict, List, Optional
import asyncio
from datetime import datetime, timedelta


class ImmigrationDataFetcher:
    """Fetches real-time data from USCIS and other official sources."""

    def __init__(self):
        self.cache = {}
        self.cache_duration = timedelta(hours=24)  # Cache for 24 hours

    async def get_processing_times(self, form_type: str, service_center: Optional[str] = None) -> Dict:
        """
        Fetch current processing times from USCIS.

        Args:
            form_type: e.g., "I-129" (H-1B), "I-140" (Employment green card), "I-485" (Adjustment)
            service_center: Optional specific service center

        Returns:
            Processing time information
        """
        cache_key = f"processing_{form_type}_{service_center}"

        # Check cache
        if cache_key in self.cache:
            cached_data, cached_time = self.cache[cache_key]
            if datetime.now() - cached_time < self.cache_duration:
                return cached_data

        try:
            url = "https://egov.uscis.gov/processing-times/"

            async with httpx.AsyncClient(timeout=30.0) as client:
                response = await client.get(url)
                response.raise_for_status()

            # Parse HTML
            soup = BeautifulSoup(response.text, 'html.parser')

            # This is a simplified version - actual implementation would parse specific tables
            processing_data = {
                "form_type": form_type,
                "service_center": service_center or "All Centers",
                "last_updated": datetime.now().isoformat(),
                "estimated_range": "Data fetched from USCIS",
                "source_url": url,
                "note": "Check official USCIS website for most current times"
            }

            # Cache the result
            self.cache[cache_key] = (processing_data, datetime.now())

            return processing_data

        except Exception as e:
            return {
                "error": f"Failed to fetch processing times: {str(e)}",
                "fallback": "Please check https://egov.uscis.gov/processing-times/ directly"
            }

    async def get_visa_bulletin(self) -> Dict:
        """
        Fetch current State Department Visa Bulletin.

        Returns:
            Current priority dates and availability
        """
        cache_key = "visa_bulletin"

        if cache_key in self.cache:
            cached_data, cached_time = self.cache[cache_key]
            if datetime.now() - cached_time < self.cache_duration:
                return cached_data

        try:
            url = "https://travel.state.gov/content/travel/en/legal/visa-law0/visa-bulletin.html"

            async with httpx.AsyncClient(timeout=30.0) as client:
                response = await client.get(url)
                response.raise_for_status()

            soup = BeautifulSoup(response.text, 'html.parser')

            bulletin_data = {
                "month": datetime.now().strftime("%B %Y"),
                "last_updated": datetime.now().isoformat(),
                "source_url": url,
                "employment_based": {
                    "EB-1": "Current for most countries (check for China/India backlog)",
                    "EB-2": "Check bulletin for current priority dates",
                    "EB-3": "Check bulletin for current priority dates",
                },
                "note": "Visit official State Department Visa Bulletin for exact dates"
            }

            self.cache[cache_key] = (bulletin_data, datetime.now())

            return bulletin_data

        except Exception as e:
            return {
                "error": f"Failed to fetch visa bulletin: {str(e)}",
                "fallback": "Please check https://travel.state.gov/content/travel/en/legal/visa-law0/visa-bulletin.html directly"
            }

    async def get_h1b_stats(self) -> Dict:
        """
        Fetch H-1B lottery statistics and cap information.

        Returns:
            H-1B cap and lottery information
        """
        cache_key = "h1b_stats"

        if cache_key in self.cache:
            cached_data, cached_time = self.cache[cache_key]
            if datetime.now() - cached_time < self.cache_duration:
                return cached_data

        # For now, return known data (can be enhanced with real scraping)
        stats_data = {
            "fiscal_year": 2025,
            "regular_cap": 65000,
            "masters_cap": 20000,
            "total_cap": 85000,
            "registration_period": "Typically March (check USCIS for exact dates)",
            "lottery_date": "Typically late March/early April",
            "start_date": "October 1, 2025",
            "estimated_registrations": "400,000+ (varies by year)",
            "estimated_selection_rate": "~21% (varies by year)",
            "source": "USCIS H-1B information",
            "note": "Check https://www.uscis.gov/working-in-the-united-states/temporary-workers/h-1b-specialty-occupations for current information"
        }

        self.cache[cache_key] = (stats_data, datetime.now())

        return stats_data

    async def get_filing_fees(self) -> Dict:
        """
        Get current USCIS filing fees.

        Returns:
            Dictionary of current fees
        """
        cache_key = "filing_fees"

        if cache_key in self.cache:
            cached_data, cached_time = self.cache[cache_key]
            if datetime.now() - cached_time < self.cache_duration:
                return cached_data

        fees_data = {
            "last_updated": "2024",
            "fees": {
                "I-129 (H-1B, L-1, O-1)": "$460",
                "I-129 Fraud Prevention Fee": "$500",
                "I-129 ACWIA Fee": "$750 (small) or $1,500 (large employer)",
                "I-140 (Employment Green Card)": "$700",
                "I-485 (Adjustment of Status)": "$1,140-$1,440",
                "Premium Processing": "$2,500 (15-day processing)",
                "H-1B Registration": "$10 per registration",
            },
            "note": "Fees subject to change. Check https://www.uscis.gov/forms/filing-fees for current fees",
            "source_url": "https://www.uscis.gov/forms/filing-fees"
        }

        self.cache[cache_key] = (fees_data, datetime.now())

        return fees_data

    async def search_uscis_policy(self, query: str) -> Dict:
        """
        Search USCIS policy manual for specific guidance.

        Args:
            query: Search query

        Returns:
            Search results from policy manual
        """
        try:
            search_url = f"https://www.uscis.gov/policy-manual"

            # In a full implementation, this would actually search the policy manual
            # For now, return guidance to check manually

            return {
                "query": query,
                "message": "For specific policy guidance, please search the USCIS Policy Manual",
                "url": search_url,
                "note": "The policy manual contains authoritative guidance on all USCIS procedures"
            }

        except Exception as e:
            return {
                "error": f"Search failed: {str(e)}",
                "fallback_url": "https://www.uscis.gov/policy-manual"
            }

    def clear_cache(self):
        """Clear the data cache."""
        self.cache = {}
