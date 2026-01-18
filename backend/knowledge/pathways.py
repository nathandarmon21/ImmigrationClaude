"""
Immigration pathway definitions and knowledge base.
Contains comprehensive information about US immigration options.
"""

from typing import List, Dict, Optional
from pydantic import BaseModel


class Requirement(BaseModel):
    """A single requirement for an immigration pathway."""
    name: str
    description: str
    is_mandatory: bool = True
    alternatives: Optional[List[str]] = None


class PathwayInfo(BaseModel):
    """Comprehensive information about an immigration pathway."""
    id: str
    name: str
    category: str  # work, green_card, study, family, other
    short_description: str
    detailed_description: str
    requirements: List[Requirement]
    advantages: List[str]
    disadvantages: List[str]
    typical_timeline: str
    cost_range: str
    success_factors: List[str]
    common_denials: List[str]
    next_steps: List[str]
    official_links: List[Dict[str, str]]
    prerequisites: Optional[List[str]] = None
    leads_to: Optional[List[str]] = None  # What pathways this can lead to


# Define all major US immigration pathways
IMMIGRATION_PATHWAYS: Dict[str, PathwayInfo] = {
    "h1b": PathwayInfo(
        id="h1b",
        name="H-1B Specialty Occupation Visa",
        category="work",
        short_description="Temporary work visa for specialty occupations requiring theoretical or technical expertise",
        detailed_description="""The H-1B visa is one of the most common work visas for skilled professionals.
        It allows US employers to temporarily employ foreign workers in specialty occupations. The visa is
        initially granted for up to 3 years and can be extended to 6 years total. It's commonly used in
        technology, engineering, mathematics, medicine, and other specialized fields.""",
        requirements=[
            Requirement(
                name="Job Offer",
                description="Valid job offer from a US employer willing to sponsor",
                is_mandatory=True
            ),
            Requirement(
                name="Bachelor's Degree",
                description="Bachelor's degree or higher in a specific specialty, or equivalent experience (3 years work experience = 1 year education)",
                is_mandatory=True,
                alternatives=["12 years of specialized work experience in lieu of bachelor's degree"]
            ),
            Requirement(
                name="Specialty Occupation",
                description="Position must require theoretical or technical expertise in a specialized field",
                is_mandatory=True
            ),
            Requirement(
                name="Labor Condition Application (LCA)",
                description="Employer must file LCA with Department of Labor",
                is_mandatory=True
            ),
            Requirement(
                name="Prevailing Wage",
                description="Employer must pay at least the prevailing wage for the occupation in the geographic area",
                is_mandatory=True
            ),
        ],
        advantages=[
            "Dual intent - can pursue green card while on H-1B",
            "Can work for up to 6 years (3+3)",
            "Spouse (H-4) can apply for work authorization if you have approved I-140",
            "Can change employers through H-1B transfer",
            "Can travel in and out of US",
            "Extensions possible beyond 6 years if green card is pending",
        ],
        disadvantages=[
            "Annual cap of 85,000 visas (65,000 regular + 20,000 Master's cap)",
            "Lottery system - not guaranteed even if qualified",
            "Tied to sponsoring employer (though can transfer)",
            "Can only work for sponsoring employer unless you have EAD",
            "Registration period only once per year (typically March)",
            "Processing times can be lengthy (premium processing available for fee)",
        ],
        typical_timeline="Registration in March, lottery results in April, petition filing April-June, start date October 1st of the same year. Total process: 6-8 months from registration to start",
        cost_range="$5,000-$10,000 (employer typically pays). Includes registration fee ($10), base filing fee ($460), fraud fee ($500), ACWIA fee ($750-$1,500), attorney fees ($2,000-$5,000), premium processing optional ($2,500)",
        success_factors=[
            "Strong educational credentials matching job requirements",
            "Employer with good track record of sponsorship",
            "Job clearly qualifies as specialty occupation",
            "Competitive salary meeting prevailing wage",
            "Well-documented job duties and requirements",
        ],
        common_denials=[
            "Insufficient proof of specialty occupation",
            "Degree not directly related to job position",
            "Employer cannot demonstrate ability to pay salary",
            "Past immigration violations",
            "Inadequate employer-employee relationship",
        ],
        next_steps=[
            "Find employer willing to sponsor",
            "Employer registers during registration period (March)",
            "If selected in lottery, prepare detailed petition package",
            "Employer files Form I-129 with USCIS",
            "Attend visa interview at consulate (if abroad)",
            "Enter US and begin work on October 1st or approval date",
        ],
        official_links=[
            {"title": "USCIS H-1B Page", "url": "https://www.uscis.gov/working-in-the-united-states/temporary-workers/h-1b-specialty-occupations"},
            {"title": "H-1B Registration", "url": "https://www.uscis.gov/h-1b-electronic-registration"},
            {"title": "DOL Foreign Labor Certification", "url": "https://www.dol.gov/agencies/eta/foreign-labor"},
        ],
        leads_to=["h1b_to_green_card", "eb2", "eb3"]
    ),

    "o1": PathwayInfo(
        id="o1",
        name="O-1 Visa for Individuals with Extraordinary Ability",
        category="work",
        short_description="For individuals with extraordinary ability in sciences, arts, education, business, or athletics",
        detailed_description="""The O-1 visa is for individuals who possess extraordinary ability in the sciences,
        arts, education, business, or athletics, or who have a demonstrated record of extraordinary achievement in
        the motion picture or television industry. This visa has no annual cap and can be a strong alternative to H-1B.""",
        requirements=[
            Requirement(
                name="Extraordinary Ability",
                description="Must demonstrate sustained national or international acclaim",
                is_mandatory=True
            ),
            Requirement(
                name="Evidence of Achievement",
                description="Must meet at least 3 of 8 criteria (awards, membership, published material, judging, original contributions, scholarly articles, critical employment, high salary)",
                is_mandatory=True
            ),
            Requirement(
                name="Job Offer",
                description="Valid job offer or contracts showing work in area of extraordinary ability",
                is_mandatory=True
            ),
            Requirement(
                name="Consultation",
                description="Written advisory opinion from relevant peer group or labor organization",
                is_mandatory=True
            ),
        ],
        advantages=[
            "No annual cap or lottery",
            "Can be filed any time of year",
            "Initial period up to 3 years, unlimited 1-year extensions",
            "Faster processing possible",
            "Strong option for entrepreneurs and founders",
            "Demonstrates exceptional qualifications (helpful for future green card)",
            "Can hold multiple O-1 visas with different employers",
        ],
        disadvantages=[
            "High bar to prove 'extraordinary ability'",
            "Requires extensive documentation",
            "Need consultation letter from peer group",
            "Not dual intent (though in practice can pursue green card)",
            "More expensive legal fees due to complexity",
            "Subjective evaluation by USCIS",
        ],
        typical_timeline="2-3 months standard processing, 15 days with premium processing",
        cost_range="$8,000-$15,000+ (includes filing fee $460, fraud fee $500, premium processing $2,500 optional, attorney fees $5,000-$12,000)",
        success_factors=[
            "Well-documented record of achievement",
            "Strong letters of recommendation from experts",
            "Media coverage or publications",
            "Awards and recognition",
            "Evidence of critical role in distinguished organizations",
            "High salary compared to peers",
        ],
        common_denials=[
            "Insufficient evidence of extraordinary ability",
            "Weak recommendation letters",
            "Credentials not rising above 'merely talented'",
            "Lack of sustained acclaim",
            "Poor consultation letter",
        ],
        next_steps=[
            "Assess if you meet 3+ of the 8 criteria",
            "Gather extensive documentation (awards, media, letters)",
            "Obtain consultation from peer group/union",
            "Employer files Form I-129 with all evidence",
            "Attend visa interview if applying from abroad",
        ],
        official_links=[
            {"title": "USCIS O-1 Visa Page", "url": "https://www.uscis.gov/working-in-the-united-states/temporary-workers/o-1-visa-individuals-with-extraordinary-ability-or-achievement"},
        ],
        leads_to=["eb1a", "eb1b", "eb2_niw"]
    ),

    "l1": PathwayInfo(
        id="l1",
        name="L-1 Intracompany Transfer Visa",
        category="work",
        short_description="For intracompany transferees in managerial, executive, or specialized knowledge roles",
        detailed_description="""The L-1 visa allows companies to transfer employees from foreign offices to
        US offices. L-1A is for managers/executives (up to 7 years), L-1B is for specialized knowledge workers
        (up to 5 years). Good option for those already working for multinational companies.""",
        requirements=[
            Requirement(
                name="Qualifying Relationship",
                description="Employer must have qualifying relationship with foreign company (parent, subsidiary, affiliate, branch)",
                is_mandatory=True
            ),
            Requirement(
                name="Prior Employment",
                description="Must have worked for foreign entity for at least 1 continuous year in past 3 years",
                is_mandatory=True
            ),
            Requirement(
                name="Qualifying Position",
                description="Position must be managerial, executive, or require specialized knowledge",
                is_mandatory=True
            ),
            Requirement(
                name="US Office",
                description="US company must be doing business",
                is_mandatory=True
            ),
        ],
        advantages=[
            "No annual cap",
            "Dual intent - can pursue green card",
            "L-1A can lead directly to EB-1C green card",
            "Blanket L petitions available for large companies (faster)",
            "Spouse (L-2) automatically gets work authorization",
            "Can be initial validity up to 3 years",
        ],
        disadvantages=[
            "Requires existing employment with foreign entity",
            "Limited to 5 years (L-1B) or 7 years (L-1A)",
            "New offices only get 1 year initially",
            "Specialized knowledge for L-1B can be subjective",
            "Cannot change employers (must stay with transferring company)",
            "More scrutiny in recent years",
        ],
        typical_timeline="2-4 months standard, 15 days with premium processing. Blanket L can be faster.",
        cost_range="$5,000-$12,000 (filing fee $460, fraud fee $500, blanket fee $500 if applicable, premium processing $2,500, attorney fees $3,000-$8,000)",
        success_factors=[
            "Clear documentation of foreign employment",
            "Well-defined qualifying relationship between entities",
            "Detailed description of specialized knowledge or managerial duties",
            "Proof of business operations in US",
            "Strong organizational charts",
        ],
        common_denials=[
            "Insufficient proof of qualifying relationship",
            "Specialized knowledge not adequately demonstrated",
            "Lack of managerial/executive duties",
            "New office concerns about viability",
            "Gap in employment with foreign entity",
        ],
        next_steps=[
            "Verify qualifying corporate relationship",
            "Ensure 1 year foreign employment requirement met",
            "Prepare organizational charts and job descriptions",
            "Company files Form I-129",
            "Attend visa interview if outside US",
        ],
        official_links=[
            {"title": "USCIS L-1 Visa Page", "url": "https://www.uscis.gov/working-in-the-united-states/temporary-workers/l-1a-intracompany-transferee-executive-or-manager"},
        ],
        leads_to=["eb1c"]
    ),

    "eb1a": PathwayInfo(
        id="eb1a",
        name="EB-1A Green Card (Extraordinary Ability)",
        category="green_card",
        short_description="Permanent residence for individuals with extraordinary ability in sciences, arts, education, business, or athletics",
        detailed_description="""EB-1A is a first-preference employment-based green card for individuals with
        extraordinary ability. Unlike other employment green cards, it does not require a job offer or labor
        certification, making it attractive for researchers, artists, entrepreneurs, and top professionals.""",
        requirements=[
            Requirement(
                name="Extraordinary Ability",
                description="Sustained national or international acclaim in your field",
                is_mandatory=True
            ),
            Requirement(
                name="Evidence",
                description="Either a one-time major award (Nobel, Oscar, Olympic medal) OR at least 3 of 10 criteria",
                is_mandatory=True
            ),
            Requirement(
                name="Continued Work",
                description="Plan to continue working in area of extraordinary ability in US",
                is_mandatory=True
            ),
        ],
        advantages=[
            "No job offer required (self-petition)",
            "No labor certification needed",
            "First preference - typically current or short wait times",
            "Can include spouse and unmarried children under 21",
            "Permanent residence - not tied to employer",
            "Can work for anyone or be self-employed",
            "Premium processing available",
        ],
        disadvantages=[
            "Very high bar to meet extraordinary ability standard",
            "Requires extensive documentation",
            "Expensive legal fees",
            "Subjective evaluation",
            "Can take 12-18 months even if approved quickly",
            "Risk of denial even with strong credentials",
        ],
        typical_timeline="12-24 months total (6-8 months for I-140 with premium processing, then 6-12+ months for adjustment/consular processing)",
        cost_range="$10,000-$25,000+ (I-140 fee $700, premium processing $2,500, I-485 fee $1,140-$1,440 per person, medical exam $200-$500, attorney fees $7,000-$20,000)",
        success_factors=[
            "Major awards or recognition",
            "Extensive media coverage",
            "Published work widely cited",
            "Original contributions of major significance",
            "High salary relative to field",
            "Membership in exclusive associations",
            "Evidence of judging others' work",
        ],
        common_denials=[
            "Achievements not rising to 'extraordinary' level",
            "Weak evidence for claimed criteria",
            "Lack of sustained acclaim",
            "Regional rather than national/international recognition",
            "Insufficient comparative evidence",
        ],
        next_steps=[
            "Evaluate if you meet 3+ of 10 criteria",
            "Gather comprehensive evidence portfolio",
            "Obtain strong expert letters",
            "File Form I-140 (can self-petition)",
            "If approved, file I-485 (if in US) or consular processing",
        ],
        official_links=[
            {"title": "USCIS EB-1 Page", "url": "https://www.uscis.gov/working-in-the-united-states/permanent-workers/employment-based-immigration-first-preference-eb-1"},
        ],
        prerequisites=["o1"],
    ),

    "eb2_niw": PathwayInfo(
        id="eb2_niw",
        name="EB-2 NIW (National Interest Waiver)",
        category="green_card",
        short_description="Green card for advanced degree professionals whose work is in the national interest",
        detailed_description="""EB-2 NIW allows qualified individuals to obtain permanent residence by
        demonstrating that their work is in the US national interest. It waives the job offer and labor
        certification requirements, making it popular among researchers, entrepreneurs, and STEM professionals.""",
        requirements=[
            Requirement(
                name="Advanced Degree or Exceptional Ability",
                description="Master's degree or higher, OR bachelor's + 5 years progressive experience, OR exceptional ability in sciences/arts/business",
                is_mandatory=True
            ),
            Requirement(
                name="National Interest",
                description="Must meet 3-prong Matter of Dhanasar test: substantial merit and national importance, well-positioned to advance endeavor, beneficial to waive job offer requirement",
                is_mandatory=True
            ),
        ],
        advantages=[
            "No job offer required (self-petition)",
            "No labor certification (PERM) needed",
            "Can change jobs freely after filing",
            "Second preference - often current for most countries",
            "Can include spouse and children",
            "Faster and less expensive than regular EB-2",
            "Good option for entrepreneurs and researchers",
        ],
        disadvantages=[
            "Still requires advanced degree or exceptional ability",
            "Must build strong national interest case",
            "Longer wait times than EB-1 (especially for India/China)",
            "Subjective evaluation of national interest",
            "No premium processing for I-140 currently",
            "Country-specific backlogs can delay green card receipt",
        ],
        typical_timeline="18-36 months total (12-18 months for I-140, then 6-18 months for adjustment depending on priority date)",
        cost_range="$8,000-$18,000 (I-140 fee $700, I-485 fees $1,140-$1,440 per person, medical exams, attorney fees $6,000-$15,000)",
        success_factors=[
            "Advanced degree in STEM or critical field",
            "Work with national/economic impact",
            "Publications and citations",
            "Strong expert recommendation letters",
            "Evidence of being well-positioned to advance work",
            "Documentation of impact on US interests",
        ],
        common_denials=[
            "Insufficient proof of national interest",
            "Weak evidence of being well-positioned",
            "Work seen as benefiting only a small region/company",
            "Failure to meet advanced degree requirement",
            "Poor documentation of endeavor's importance",
        ],
        next_steps=[
            "Assess qualification (advanced degree + impactful work)",
            "Develop national interest argument using Dhanasar framework",
            "Gather evidence (publications, citations, letters)",
            "File Form I-140 with comprehensive documentation",
            "If approved and priority date current, file I-485",
        ],
        official_links=[
            {"title": "USCIS EB-2 Page", "url": "https://www.uscis.gov/working-in-the-united-states/permanent-workers/employment-based-immigration-second-preference-eb-2"},
        ],
    ),

    "perm_eb2": PathwayInfo(
        id="perm_eb2",
        name="EB-2 with PERM Labor Certification",
        category="green_card",
        short_description="Green card through employer sponsorship with labor certification",
        detailed_description="""Traditional EB-2 requires employer sponsorship and PERM labor certification
        process. Employer must prove no qualified US workers available. Common path for professionals with
        advanced degrees sponsored by established employers.""",
        requirements=[
            Requirement(
                name="Job Offer",
                description="Permanent, full-time job offer from US employer",
                is_mandatory=True
            ),
            Requirement(
                name="Advanced Degree",
                description="Master's or higher, OR bachelor's + 5 years progressive experience",
                is_mandatory=True
            ),
            Requirement(
                name="PERM Labor Certification",
                description="Employer must complete PERM process proving no qualified US workers",
                is_mandatory=True
            ),
            Requirement(
                name="Prevailing Wage",
                description="Job must offer at least prevailing wage",
                is_mandatory=True
            ),
        ],
        advantages=[
            "Employer supports entire process",
            "Well-established procedure",
            "Second preference priority date",
            "Can include spouse and children",
        ],
        disadvantages=[
            "Requires employer sponsorship",
            "Lengthy PERM process (6-12 months)",
            "Tied to sponsoring employer until I-485 pending 180 days",
            "Employer bears recruitment and legal costs",
            "Must prove no qualified US workers (can be challenging)",
            "Backlogs for India and China nationals",
        ],
        typical_timeline="24-48 months total (6-12 months PERM, 6-12 months I-140, 12-24+ months for adjustment depending on country)",
        cost_range="$10,000-$20,000 (typically employer-paid: PERM filing fee $100, recruitment costs $3,000-$8,000, I-140 fee $700, I-485 fees employee-paid $1,140+ per person, attorney fees $6,000-$12,000)",
        success_factors=[
            "Employer committed to sponsorship",
            "Position truly requires advanced degree",
            "Proper recruitment process",
            "No qualified US applicants",
            "Good documentation of job requirements",
        ],
        common_denials=[
            "Qualified US workers found during recruitment",
            "Job requirements not matching employee qualifications",
            "PERM audit issues",
            "Recruitment process errors",
            "Employer cannot demonstrate financial ability",
        ],
        next_steps=[
            "Employer determines position requirements",
            "Prevailing wage determination",
            "Recruitment process (ads, job postings)",
            "File PERM application",
            "After approval, file I-140",
            "When priority date current, file I-485",
        ],
        official_links=[
            {"title": "DOL PERM", "url": "https://www.dol.gov/agencies/eta/foreign-labor/programs/permanent"},
            {"title": "USCIS EB-2", "url": "https://www.uscis.gov/working-in-the-united-states/permanent-workers/employment-based-immigration-second-preference-eb-2"},
        ],
    ),
}


# Question flow for assessment
ASSESSMENT_QUESTIONS = [
    {
        "id": "purpose",
        "question": "What is your primary purpose for coming to or staying in the United States?",
        "type": "single_choice",
        "options": [
            {"value": "work", "label": "Work/Employment"},
            {"value": "study", "label": "Education/Study"},
            {"value": "family", "label": "Family reunification"},
            {"value": "business", "label": "Start/run a business"},
            {"value": "permanent", "label": "Permanent residence (green card)"},
            {"value": "other", "label": "Other"},
        ],
        "next_question_map": {
            "work": "work_current_status",
            "study": "study_level",
            "family": "family_relationship",
            "business": "business_type",
            "permanent": "green_card_category",
        }
    },
    {
        "id": "work_current_status",
        "question": "What is your current immigration status?",
        "type": "single_choice",
        "options": [
            {"value": "outside_us", "label": "Outside the US"},
            {"value": "f1", "label": "F-1 Student"},
            {"value": "h1b", "label": "H-1B"},
            {"value": "l1", "label": "L-1"},
            {"value": "o1", "label": "O-1"},
            {"value": "other_status", "label": "Other status"},
        ],
        "next_question_map": {
            "outside_us": "education_level",
            "f1": "opt_status",
        }
    },
    {
        "id": "education_level",
        "question": "What is your highest level of education?",
        "type": "single_choice",
        "options": [
            {"value": "phd", "label": "PhD/Doctorate"},
            {"value": "masters", "label": "Master's degree"},
            {"value": "bachelors", "label": "Bachelor's degree"},
            {"value": "some_college", "label": "Some college"},
            {"value": "high_school", "label": "High school"},
        ],
        "next_question_map": {}
    },
    {
        "id": "field_of_expertise",
        "question": "What is your field of work/expertise?",
        "type": "single_choice",
        "options": [
            {"value": "technology", "label": "Technology/Software"},
            {"value": "engineering", "label": "Engineering"},
            {"value": "science", "label": "Sciences/Research"},
            {"value": "business", "label": "Business/Finance"},
            {"value": "arts", "label": "Arts/Entertainment"},
            {"value": "healthcare", "label": "Healthcare/Medicine"},
            {"value": "education", "label": "Education"},
            {"value": "other", "label": "Other"},
        ],
    },
    {
        "id": "achievements",
        "question": "Do you have any of the following achievements? (Select all that apply)",
        "type": "multiple_choice",
        "options": [
            {"value": "awards", "label": "Major awards or prizes"},
            {"value": "publications", "label": "Published research or articles"},
            {"value": "media", "label": "Media coverage about your work"},
            {"value": "high_salary", "label": "High salary (top 10% in field)"},
            {"value": "leadership", "label": "Leadership in distinguished organizations"},
            {"value": "none", "label": "None of the above"},
        ],
    },
]
