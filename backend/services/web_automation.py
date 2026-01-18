"""
Agentic web automation for immigration processes.
Uses Playwright to interact with USCIS and other immigration websites.
"""

from typing import Dict, List, Optional
import asyncio
from playwright.async_api import async_playwright, Page, Browser
import os


class ImmigrationWebAutomation:
    """Automates web interactions for immigration processes."""

    def __init__(self):
        self.browser: Optional[Browser] = None
        self.playwright = None

    async def initialize(self):
        """Initialize Playwright browser."""
        if not self.playwright:
            self.playwright = await async_playwright().start()
            self.browser = await self.playwright.chromium.launch(headless=True)

    async def close(self):
        """Close browser and playwright."""
        if self.browser:
            await self.browser.close()
        if self.playwright:
            await self.playwright.stop()

    async def check_case_status(self, receipt_number: str) -> Dict:
        """
        Check USCIS case status for a receipt number.

        Args:
            receipt_number: USCIS receipt number (e.g., "WAC2190012345")

        Returns:
            Case status information
        """
        await self.initialize()

        try:
            page = await self.browser.new_page()
            await page.goto("https://egov.uscis.gov/casestatus/landing.do")

            # Fill in receipt number
            await page.fill('input[name="appReceiptNum"]', receipt_number)
            await page.click('input[type="submit"]')

            # Wait for results
            await page.wait_for_selector('.rows', timeout=10000)

            # Extract status
            status_text = await page.text_content('.rows')

            await page.close()

            return {
                "receipt_number": receipt_number,
                "status": status_text,
                "checked_at": asyncio.get_event_loop().time(),
                "source": "USCIS Case Status Online"
            }

        except Exception as e:
            return {
                "error": f"Failed to check case status: {str(e)}",
                "receipt_number": receipt_number,
                "fallback": "Check manually at https://egov.uscis.gov/casestatus/"
            }

    async def find_immigration_forms(self, pathway_id: str) -> List[Dict]:
        """
        Find and list required forms for an immigration pathway.

        Args:
            pathway_id: Immigration pathway identifier

        Returns:
            List of required forms with download links
        """
        await self.initialize()

        # Mapping of pathways to forms
        form_mappings = {
            "h1b": [
                {"form": "I-129", "name": "Petition for Nonimmigrant Worker", "url": "https://www.uscis.gov/i-129"},
                {"form": "LCA", "name": "Labor Condition Application", "url": "https://www.dol.gov/agencies/eta/foreign-labor/programs/h-1b"},
            ],
            "o1": [
                {"form": "I-129", "name": "Petition for Nonimmigrant Worker", "url": "https://www.uscis.gov/i-129"},
            ],
            "l1": [
                {"form": "I-129", "name": "Petition for Nonimmigrant Worker", "url": "https://www.uscis.gov/i-129"},
            ],
            "eb1a": [
                {"form": "I-140", "name": "Immigrant Petition for Alien Worker", "url": "https://www.uscis.gov/i-140"},
                {"form": "I-485", "name": "Application to Register Permanent Residence", "url": "https://www.uscis.gov/i-485"},
            ],
            "eb2_niw": [
                {"form": "I-140", "name": "Immigrant Petition for Alien Worker", "url": "https://www.uscis.gov/i-140"},
                {"form": "I-485", "name": "Application to Register Permanent Residence", "url": "https://www.uscis.gov/i-485"},
            ],
            "perm_eb2": [
                {"form": "ETA-9089", "name": "PERM Labor Certification", "url": "https://www.dol.gov/agencies/eta/foreign-labor/programs/permanent"},
                {"form": "I-140", "name": "Immigrant Petition for Alien Worker", "url": "https://www.uscis.gov/i-140"},
                {"form": "I-485", "name": "Application to Register Permanent Residence", "url": "https://www.uscis.gov/i-485"},
            ],
        }

        forms = form_mappings.get(pathway_id, [])

        return {
            "pathway_id": pathway_id,
            "forms": forms,
            "note": "Download forms from official USCIS website. Consider consulting an attorney for filing."
        }

    async def get_attorney_search_results(self, location: str, specialty: str = "immigration") -> List[Dict]:
        """
        Help find immigration attorneys in a location.

        Args:
            location: City/state for attorney search
            specialty: Type of immigration case

        Returns:
            Information about finding attorneys
        """
        return {
            "location": location,
            "specialty": specialty,
            "resources": [
                {
                    "name": "American Immigration Lawyers Association (AILA)",
                    "url": "https://www.ailalawyer.com",
                    "description": "Official directory of immigration attorneys"
                },
                {
                    "name": "State Bar Association",
                    "description": f"Check your state bar association for licensed attorneys in {location}"
                },
                {
                    "name": "USCIS Pro Bono Services",
                    "url": "https://www.uscis.gov/avoid-scams/find-legal-services",
                    "description": "Free or low-cost legal services"
                }
            ],
            "tips": [
                "Verify attorney is licensed and in good standing",
                "Ask about experience with your specific visa type",
                "Get fee agreement in writing",
                "Beware of notarios (not attorneys in the US)",
            ]
        }

    async def prepare_document_checklist(self, pathway_id: str, user_profile: Dict) -> Dict:
        """
        Generate personalized document checklist for a pathway.

        Args:
            pathway_id: Immigration pathway
            user_profile: User's profile information

        Returns:
            Customized document checklist
        """
        # Base documents for most pathways
        base_documents = [
            "Valid passport (valid for at least 6 months beyond intended stay)",
            "Passport-style photographs (meeting USCIS specifications)",
            "Birth certificate with certified English translation",
            "Educational credentials (diplomas, transcripts)",
            "Resume/CV",
        ]

        # Pathway-specific documents
        pathway_documents = {
            "h1b": [
                "Job offer letter from US employer",
                "Labor Condition Application (filed by employer)",
                "Proof of specialty occupation qualifications",
                "Employer support letter",
                "Educational credential evaluation (if degree from outside US)",
            ],
            "o1": [
                "Evidence of extraordinary ability (awards, publications, media coverage)",
                "Letters of recommendation from experts in field",
                "Consultation letter from peer group or labor organization",
                "Contract or itinerary showing work in US",
                "Documentation of sustained acclaim",
            ],
            "eb1a": [
                "Evidence meeting at least 3 of 10 criteria for extraordinary ability",
                "Expert recommendation letters",
                "Documentation of original contributions of major significance",
                "Published material about you in major media",
                "Proof of high salary or remuneration",
            ],
            "eb2_niw": [
                "Advanced degree (Master's or higher) or equivalent",
                "Evidence of work in national interest",
                "Documentation of substantial merit and national importance",
                "Proof of being well-positioned to advance the endeavor",
                "Letters from experts in the field",
            ],
        }

        documents = base_documents + pathway_documents.get(pathway_id, [])

        return {
            "pathway_id": pathway_id,
            "documents_required": documents,
            "next_steps": [
                "Gather all documents",
                "Get certified translations for non-English documents",
                "Organize in logical order",
                "Make copies for your records",
                "Consult with attorney before filing"
            ],
            "important_notes": [
                "All foreign language documents must have certified English translations",
                "Keep original documents safe - submit copies unless originals required",
                "Ensure all documents are current and valid",
            ]
        }
