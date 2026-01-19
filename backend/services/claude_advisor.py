"""
Claude AI integration for intelligent immigration advisory.
"""

import os
from typing import List, Optional
from anthropic import Anthropic
from models.schemas import UserProfile, ConversationMessage, PathwayRecommendation
from knowledge.pathways import IMMIGRATION_PATHWAYS


class ClaudeAdvisor:
    """Provides intelligent immigration advice using Claude AI."""

    def __init__(self, api_key: Optional[str] = None):
        """Initialize Claude advisor."""
        self.api_key = api_key or os.getenv("ANTHROPIC_API_KEY")
        if not self.api_key:
            raise ValueError("ANTHROPIC_API_KEY not found in environment")

        self.client = Anthropic(api_key=self.api_key)
        self.model = "claude-sonnet-4-5-20250929"

    def get_advice(
        self,
        user_profile: UserProfile,
        user_message: str,
        conversation_history: List[ConversationMessage] = None,
        recommended_pathways: List[PathwayRecommendation] = None,
    ) -> str:
        """
        Get immigration advice from Claude.

        Args:
            user_profile: User's immigration profile
            user_message: Current question/message from user
            conversation_history: Previous conversation messages
            recommended_pathways: Recommended pathways from analyzer

        Returns:
            Claude's response
        """
        # Build system prompt with immigration expertise
        system_prompt = self._build_system_prompt(user_profile, recommended_pathways)

        # Build conversation messages
        messages = []

        # Add conversation history if exists
        if conversation_history:
            for msg in conversation_history:
                messages.append({
                    "role": msg.role,
                    "content": msg.content
                })

        # Add current user message
        messages.append({
            "role": "user",
            "content": user_message
        })

        # Call Claude API
        response = self.client.messages.create(
            model=self.model,
            max_tokens=4096,
            system=system_prompt,
            messages=messages,
            temperature=0.7,
        )

        return response.content[0].text

    def _build_system_prompt(
        self,
        user_profile: UserProfile,
        recommended_pathways: Optional[List[PathwayRecommendation]] = None
    ) -> str:
        """Build system prompt with context about user and immigration pathways."""

        prompt = """You are an expert US immigration attorney with deep knowledge of all immigration pathways,
visa categories, and procedures. You provide clear, accurate, and actionable advice to help people navigate
the complex US immigration system.

Your role:
- Provide clear, step-by-step guidance on immigration options
- Ask relevant follow-up questions to understand the user's situation fully
- Compare different immigration pathways objectively
- Explain complex immigration concepts in simple terms
- Always cite specific visa categories and requirements
- Warn about common pitfalls and risks
- Provide realistic timelines and cost estimates
- Emphasize that you provide informational guidance, not legal representation

Communication style:
- Professional yet approachable
- Clear and concise
- Use bullet points and structure for readability
- Ask clarifying questions when needed
- Provide specific examples

Current User Profile:
"""

        # Add user profile information
        prompt += f"- Purpose: {user_profile.purpose}\n"
        if user_profile.current_status:
            prompt += f"- Current Status: {user_profile.current_status}\n"
        if user_profile.education_level:
            prompt += f"- Education: {user_profile.education_level}\n"
        if user_profile.field_of_expertise:
            prompt += f"- Field: {user_profile.field_of_expertise}\n"
        if user_profile.achievements:
            prompt += f"- Achievements: {', '.join(user_profile.achievements)}\n"
        if user_profile.years_experience:
            prompt += f"- Years of Experience: {user_profile.years_experience}\n"
        if user_profile.has_job_offer:
            prompt += f"- Has Job Offer: Yes\n"
        if user_profile.employer_will_sponsor:
            prompt += f"- Employer Will Sponsor: Yes\n"

        # Add recommended pathways context
        if recommended_pathways:
            prompt += "\n\nRecommended Immigration Pathways (based on initial analysis):\n"
            for pathway in recommended_pathways[:3]:  # Top 3
                pathway_info = IMMIGRATION_PATHWAYS.get(pathway.pathway_id)
                if pathway_info:
                    prompt += f"\n{pathway.pathway_name} (Fit Score: {pathway.fit_score:.0f}%):\n"
                    prompt += f"- Feasibility: {pathway.feasibility}\n"
                    prompt += f"- Timeline: {pathway_info.typical_timeline}\n"
                    prompt += f"- Cost: {pathway_info.cost_range}\n"
                    prompt += f"- Key Requirements: {', '.join([r.name for r in pathway_info.requirements[:3]])}\n"
                    prompt += f"- Reasoning: {pathway.reasoning}\n"

        prompt += """

Available Immigration Pathways Knowledge:
You have access to detailed information about these pathways:
- H-1B: Specialty occupation work visa (lottery, employer sponsorship)
- O-1: Extraordinary ability visa (no cap, high bar)
- L-1: Intracompany transfer (requires foreign employment)
- EB-1A: Extraordinary ability green card (self-petition, no job offer needed)
- EB-2 NIW: National Interest Waiver (self-petition, advanced degree)
- EB-2 PERM: Traditional employment green card (requires labor certification)

When discussing pathways:
1. Explain eligibility requirements clearly
2. Discuss pros and cons specific to user's situation
3. Provide realistic assessment of chances
4. Explain next concrete steps
5. Mention important deadlines or timing considerations

Important reminders:
- H-1B registration is typically in March each year
- Many pathways have country-specific backlogs (especially India, China)
- Processing times vary significantly
- Premium processing is available for some visa types ($2,500 for 15-day processing)
- Always recommend consulting with a licensed attorney for specific legal advice

Current date context: January 2025"""

        return prompt

    def generate_comparison(
        self,
        pathway_ids: List[str],
        user_profile: UserProfile,
    ) -> str:
        """
        Generate detailed comparison of immigration pathways.

        Args:
            pathway_ids: List of pathway IDs to compare
            user_profile: User's profile for contextualization

        Returns:
            Detailed comparison text
        """
        pathways_info = []
        for pid in pathway_ids:
            if pid in IMMIGRATION_PATHWAYS:
                pathways_info.append(IMMIGRATION_PATHWAYS[pid])

        system_prompt = f"""You are an expert immigration attorney comparing different immigration pathways
for a client. Provide a clear, structured comparison that helps them make an informed decision.

User Profile:
- Purpose: {user_profile.purpose}
- Education: {user_profile.education_level}
- Field: {user_profile.field_of_expertise}
- Has Job Offer: {user_profile.has_job_offer}

Create a comprehensive comparison covering:
1. Overview of each pathway
2. Eligibility requirements for this specific user
3. Pros and cons in their situation
4. Timeline and costs
5. Success likelihood given their profile
6. Recommended pathway with clear reasoning"""

        pathways_text = "\n\n".join([
            f"**{p.name}**\n{p.detailed_description}\n"
            f"Timeline: {p.typical_timeline}\n"
            f"Cost: {p.cost_range}\n"
            f"Requirements: {', '.join([r.name for r in p.requirements])}"
            for p in pathways_info
        ])

        message = f"Please provide a detailed comparison of these immigration pathways:\n\n{pathways_text}"

        response = self.client.messages.create(
            model=self.model,
            max_tokens=4096,
            system=system_prompt,
            messages=[{"role": "user", "content": message}],
            temperature=0.7,
        )

        return response.content[0].text

    def get_next_steps(
        self,
        pathway_id: str,
        user_profile: UserProfile,
    ) -> str:
        """
        Get detailed next steps for a specific pathway.

        Args:
            pathway_id: Selected immigration pathway
            user_profile: User's profile

        Returns:
            Detailed next steps
        """
        if pathway_id not in IMMIGRATION_PATHWAYS:
            return "Invalid pathway selected."

        pathway = IMMIGRATION_PATHWAYS[pathway_id]

        system_prompt = f"""You are an expert immigration attorney providing a detailed action plan
for a client pursuing the {pathway.name}.

Provide:
1. Immediate next steps (this week)
2. Short-term actions (this month)
3. Medium-term preparation (next 3 months)
4. Long-term timeline
5. Documents to gather
6. Common mistakes to avoid
7. Tips for success

Be specific and actionable. Include deadlines and time-sensitive considerations."""

        profile_text = f"""
User Profile:
- Education: {user_profile.education_level}
- Field: {user_profile.field_of_expertise}
- Experience: {user_profile.years_experience} years
- Has Job Offer: {user_profile.has_job_offer}
- Achievements: {', '.join(user_profile.achievements)}

Pathway: {pathway.name}
Official Next Steps: {'; '.join(pathway.next_steps)}
"""

        response = self.client.messages.create(
            model=self.model,
            max_tokens=4096,
            system=system_prompt,
            messages=[{"role": "user", "content": f"Create a detailed action plan for:\n{profile_text}"}],
            temperature=0.7,
        )

        return response.content[0].text
