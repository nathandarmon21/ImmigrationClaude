"""
Immigration pathway analyzer - scores and recommends pathways based on user profile.
"""

from typing import List, Dict, Tuple
from models.schemas import UserProfile, PathwayRecommendation
from knowledge.pathways import IMMIGRATION_PATHWAYS, PathwayInfo


class PathwayAnalyzer:
    """Analyzes user profile and recommends immigration pathways."""

    def __init__(self):
        self.pathways = IMMIGRATION_PATHWAYS

    def analyze_profile(self, profile: UserProfile) -> List[PathwayRecommendation]:
        """
        Analyze user profile and return ranked pathway recommendations.

        Args:
            profile: User's immigration profile

        Returns:
            List of pathway recommendations sorted by fit score
        """
        recommendations = []

        for pathway_id, pathway_info in self.pathways.items():
            score, feasibility, reasoning = self._score_pathway(profile, pathway_info)

            if score > 0:  # Only include pathways with some relevance
                requirements_met, requirements_missing = self._check_requirements(profile, pathway_info)

                recommendation = PathwayRecommendation(
                    pathway_id=pathway_id,
                    pathway_name=pathway_info.name,
                    fit_score=score,
                    feasibility=feasibility,
                    reasoning=reasoning,
                    pros=pathway_info.advantages,
                    cons=pathway_info.disadvantages,
                    estimated_timeline=pathway_info.typical_timeline,
                    estimated_cost=pathway_info.cost_range,
                    next_steps=pathway_info.next_steps,
                    requirements_met=requirements_met,
                    requirements_missing=requirements_missing,
                )
                recommendations.append(recommendation)

        # Sort by fit score descending
        recommendations.sort(key=lambda x: x.fit_score, reverse=True)

        return recommendations

    def _score_pathway(self, profile: UserProfile, pathway: PathwayInfo) -> Tuple[float, str, str]:
        """
        Score a pathway's fit for the user profile.

        Returns:
            (score, feasibility, reasoning)
        """
        score = 0.0
        reasons = []

        # Purpose alignment
        if profile.purpose == "work" and pathway.category == "work":
            score += 30
            reasons.append("Aligns with work visa purpose")
        elif profile.purpose == "permanent" and pathway.category == "green_card":
            score += 30
            reasons.append("Permanent residence pathway")
        elif profile.purpose == "work" and pathway.category == "green_card":
            score += 25
            reasons.append("Work visas can lead to green cards")

        # Education level alignment
        if pathway.id in ["h1b", "o1", "eb2_niw", "perm_eb2"]:
            if profile.education_level in ["masters", "phd"]:
                score += 20
                reasons.append("Advanced degree matches pathway requirements")
            elif profile.education_level == "bachelors":
                score += 15
                reasons.append("Bachelor's degree meets minimum requirements")

        # Achievement-based pathways
        if pathway.id in ["o1", "eb1a"]:
            achievement_count = len([a for a in profile.achievements if a != "none"])
            if achievement_count >= 3:
                score += 25
                reasons.append(f"Strong achievements ({achievement_count} categories)")
            elif achievement_count > 0:
                score += 10
                reasons.append("Some achievements demonstrated")
            else:
                score -= 20
                reasons.append("Extraordinary ability pathways require significant achievements")

        # Employer sponsorship
        if pathway.id in ["h1b", "l1", "perm_eb2"]:
            if profile.has_job_offer and profile.employer_will_sponsor:
                score += 25
                reasons.append("Employer willing to sponsor")
            elif profile.has_job_offer:
                score += 10
                reasons.append("Job offer exists, sponsorship possible")
            else:
                score -= 15
                reasons.append("Requires employer sponsorship")

        # Self-petition advantage
        if pathway.id in ["o1", "eb1a", "eb2_niw"]:
            if not profile.has_job_offer:
                score += 15
                reasons.append("Can self-petition without job offer")

        # Experience level
        if profile.years_experience and profile.years_experience >= 5:
            if pathway.id in ["eb2_niw", "perm_eb2", "o1"]:
                score += 10
                reasons.append("Significant experience beneficial")

        # Field alignment
        if profile.field_of_expertise in ["technology", "engineering", "science"]:
            if pathway.id in ["h1b", "eb2_niw"]:
                score += 10
                reasons.append("STEM field aligns well with pathway")

        # Determine feasibility
        if score >= 70:
            feasibility = "high"
        elif score >= 40:
            feasibility = "medium"
        else:
            feasibility = "low"

        reasoning = "; ".join(reasons) if reasons else "Limited alignment with profile"

        return min(score, 100), feasibility, reasoning

    def _check_requirements(self, profile: UserProfile, pathway: PathwayInfo) -> Tuple[List[str], List[str]]:
        """
        Check which requirements are met vs missing.

        Returns:
            (requirements_met, requirements_missing)
        """
        met = []
        missing = []

        for req in pathway.requirements:
            is_met = self._is_requirement_met(profile, pathway.id, req.name)
            if is_met:
                met.append(req.name)
            else:
                missing.append(req.name)

        return met, missing

    def _is_requirement_met(self, profile: UserProfile, pathway_id: str, requirement_name: str) -> bool:
        """Check if a specific requirement is met."""

        # Job offer requirements
        if "Job Offer" in requirement_name:
            return profile.has_job_offer

        # Education requirements
        if "Bachelor" in requirement_name or "Advanced Degree" in requirement_name:
            return profile.education_level in ["bachelors", "masters", "phd"]

        if "Master" in requirement_name:
            return profile.education_level in ["masters", "phd"]

        # Extraordinary ability
        if "Extraordinary Ability" in requirement_name:
            achievement_count = len([a for a in profile.achievements if a != "none"])
            return achievement_count >= 3

        # Default: can't determine without more info
        return False

    def compare_pathways(self, pathway_ids: List[str], profile: UserProfile) -> Dict:
        """
        Create detailed comparison of selected pathways.

        Args:
            pathway_ids: List of pathway IDs to compare
            profile: User profile for contextualization

        Returns:
            Comparison data structure
        """
        pathways = [self.pathways[pid] for pid in pathway_ids if pid in self.pathways]

        comparison = {
            "timeline": {},
            "cost": {},
            "employer_sponsorship": {},
            "difficulty": {},
            "can_self_petition": {},
            "leads_to_green_card": {},
        }

        for pathway in pathways:
            comparison["timeline"][pathway.name] = pathway.typical_timeline
            comparison["cost"][pathway.name] = pathway.cost_range
            comparison["employer_sponsorship"][pathway.name] = "Required" if pathway.id in ["h1b", "l1", "perm_eb2"] else "Not required"
            comparison["can_self_petition"][pathway.name] = "Yes" if pathway.id in ["o1", "eb1a", "eb2_niw"] else "No"
            comparison["leads_to_green_card"][pathway.name] = "Yes" if pathway.category == "green_card" or pathway.id in ["h1b", "l1", "o1"] else "No"

            # Difficulty assessment
            if pathway.id in ["eb1a", "o1"]:
                comparison["difficulty"][pathway.name] = "High (requires extraordinary ability)"
            elif pathway.id in ["h1b"]:
                comparison["difficulty"][pathway.name] = "Medium (lottery, requires sponsorship)"
            else:
                comparison["difficulty"][pathway.name] = "Medium"

        return comparison
