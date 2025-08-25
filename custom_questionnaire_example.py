#!/usr/bin/env python3
"""
Custom Questionnaire Example

This script demonstrates how to create custom questionnaires with
user-defined questions and analysis logic.
"""

from enhanced_questionnaire import EnhancedAnalysisQuestionnaire
from questionnaire_config import create_custom_question_set, validate_question_format
from typing import List, Dict, Any

def create_custom_questionnaire():
    """Create a custom questionnaire for employee satisfaction analysis."""
    
    # Define custom questions
    custom_questions = [
        {
            "id": "department",
            "question": "What department do you work in?",
            "type": "multiple_choice",
            "options": ["Engineering", "Sales", "Marketing", "HR", "Finance", "Operations", "Other"],
            "required": True
        },
        {
            "id": "tenure",
            "question": "How long have you been with the company?",
            "type": "multiple_choice",
            "options": ["Less than 1 year", "1-3 years", "3-5 years", "5-10 years", "10+ years"],
            "required": True
        },
        {
            "id": "job_satisfaction",
            "question": "How satisfied are you with your current job?",
            "type": "rating",
            "scale": 10,
            "required": True
        },
        {
            "id": "work_life_balance",
            "question": "How would you rate your work-life balance?",
            "type": "rating",
            "scale": 5,
            "required": True
        },
        {
            "id": "career_growth",
            "question": "How satisfied are you with career growth opportunities?",
            "type": "rating",
            "scale": 5,
            "required": True
        },
        {
            "id": "compensation",
            "question": "How satisfied are you with your compensation?",
            "type": "rating",
            "scale": 5,
            "required": True
        },
        {
            "id": "management_support",
            "question": "How would you rate the support from your manager?",
            "type": "rating",
            "scale": 5,
            "required": True
        },
        {
            "id": "team_collaboration",
            "question": "How would you rate team collaboration?",
            "type": "rating",
            "scale": 5,
            "required": True
        },
        {
            "id": "company_culture",
            "question": "How would you rate the company culture?",
            "type": "rating",
            "scale": 5,
            "required": True
        },
        {
            "id": "concerns",
            "question": "What are your main concerns about working here?",
            "type": "multi_select",
            "options": ["Compensation", "Career growth", "Work-life balance", "Management", "Company direction", "Job security", "None"],
            "required": False
        },
        {
            "id": "suggestions",
            "question": "What suggestions do you have for improving the workplace?",
            "type": "text",
            "required": False
        },
        {
            "id": "recommendation_likelihood",
            "question": "How likely are you to recommend this company as a place to work?",
            "type": "rating",
            "scale": 10,
            "required": True
        }
    ]
    
    # Validate questions
    print("Validating custom questions...")
    for i, question in enumerate(custom_questions):
        if validate_question_format(question):
            print(f"✓ Question {i+1} is valid")
        else:
            print(f"✗ Question {i+1} has format issues")
            return None
    
    # Create custom question set
    custom_set = create_custom_question_set(
        name="Employee Satisfaction Survey",
        description="Comprehensive employee satisfaction and engagement analysis",
        questions=custom_questions,
        category="hr"
    )
    
    return custom_set

def create_custom_questionnaire_class():
    """Create a custom questionnaire class with specialized analysis."""
    
    class EmployeeSatisfactionQuestionnaire(EnhancedAnalysisQuestionnaire):
        def __init__(self):
            super().__init__()
            # Override with custom questions
            custom_set = create_custom_questionnaire()
            if custom_set:
                self.questions = custom_set["questions"]
                self.selected_question_set = "employee_satisfaction"
            else:
                print("Failed to create custom questionnaire")
                return
        
        def analyze_responses(self):
            """Custom analysis for employee satisfaction."""
            print("\nAnalyzing employee satisfaction responses...\n")
            
            # Job Satisfaction Analysis
            job_satisfaction = self.responses.get("job_satisfaction")
            if job_satisfaction:
                self.analysis_results["job_satisfaction_analysis"] = {
                    "score": job_satisfaction,
                    "interpretation": self._interpret_satisfaction_score(job_satisfaction, 10),
                    "recommendations": self._get_satisfaction_recommendations(job_satisfaction, 10)
                }
            
            # Work-Life Balance Analysis
            work_life_balance = self.responses.get("work_life_balance")
            if work_life_balance:
                self.analysis_results["work_life_balance_analysis"] = {
                    "score": work_life_balance,
                    "interpretation": self._interpret_satisfaction_score(work_life_balance, 5),
                    "recommendations": self._get_work_life_recommendations(work_life_balance)
                }
            
            # Career Growth Analysis
            career_growth = self.responses.get("career_growth")
            if career_growth:
                self.analysis_results["career_growth_analysis"] = {
                    "score": career_growth,
                    "interpretation": self._interpret_satisfaction_score(career_growth, 5),
                    "recommendations": self._get_career_growth_recommendations(career_growth)
                }
            
            # Compensation Analysis
            compensation = self.responses.get("compensation")
            if compensation:
                self.analysis_results["compensation_analysis"] = {
                    "score": compensation,
                    "interpretation": self._interpret_satisfaction_score(compensation, 5),
                    "recommendations": self._get_compensation_recommendations(compensation)
                }
            
            # Management Support Analysis
            management_support = self.responses.get("management_support")
            if management_support:
                self.analysis_results["management_analysis"] = {
                    "score": management_support,
                    "interpretation": self._interpret_satisfaction_score(management_support, 5),
                    "recommendations": self._get_management_recommendations(management_support)
                }
            
            # Team Collaboration Analysis
            team_collaboration = self.responses.get("team_collaboration")
            if team_collaboration:
                self.analysis_results["team_collaboration_analysis"] = {
                    "score": team_collaboration,
                    "interpretation": self._interpret_satisfaction_score(team_collaboration, 5),
                    "recommendations": self._get_team_recommendations(team_collaboration)
                }
            
            # Company Culture Analysis
            company_culture = self.responses.get("company_culture")
            if company_culture:
                self.analysis_results["company_culture_analysis"] = {
                    "score": company_culture,
                    "interpretation": self._interpret_satisfaction_score(company_culture, 5),
                    "recommendations": self._get_culture_recommendations(company_culture)
                }
            
            # Concerns Analysis
            concerns = self.responses.get("concerns", [])
            if concerns:
                self.analysis_results["concerns_analysis"] = {
                    "concerns": concerns,
                    "priority_levels": self._prioritize_concerns(concerns),
                    "action_items": self._suggest_actions_for_concerns(concerns)
                }
            
            # Recommendation Likelihood Analysis
            recommendation_likelihood = self.responses.get("recommendation_likelihood")
            if recommendation_likelihood:
                self.analysis_results["recommendation_analysis"] = {
                    "score": recommendation_likelihood,
                    "interpretation": self._interpret_satisfaction_score(recommendation_likelihood, 10),
                    "nps_category": self._categorize_nps_score(recommendation_likelihood)
                }
            
            # Generate overall assessment
            self.analysis_results["overall_assessment"] = self._generate_employee_assessment()
        
        def _interpret_satisfaction_score(self, score: int, max_score: int) -> str:
            """Interpret satisfaction scores."""
            percentage = (score / max_score) * 100
            
            if percentage >= 80:
                return "Excellent - High satisfaction level"
            elif percentage >= 60:
                return "Good - Satisfactory level with room for improvement"
            elif percentage >= 40:
                return "Fair - Some concerns that need attention"
            elif percentage >= 20:
                return "Poor - Significant issues requiring immediate attention"
            else:
                return "Very Poor - Critical issues requiring urgent action"
        
        def _get_satisfaction_recommendations(self, score: int, max_score: int) -> List[str]:
            """Get recommendations based on satisfaction score."""
            percentage = (score / max_score) * 100
            
            if percentage >= 80:
                return ["Maintain current practices", "Recognize and reward success", "Share best practices"]
            elif percentage >= 60:
                return ["Identify improvement areas", "Gather specific feedback", "Implement targeted improvements"]
            elif percentage >= 40:
                return ["Conduct detailed surveys", "Address major concerns", "Develop improvement plans"]
            else:
                return ["Immediate intervention required", "Conduct exit interviews", "Develop retention strategies"]
        
        def _get_work_life_recommendations(self, score: int) -> List[str]:
            """Get work-life balance recommendations."""
            if score >= 4:
                return ["Maintain current policies", "Share best practices", "Monitor workload"]
            elif score >= 3:
                return ["Review workload distribution", "Implement flexible policies", "Promote time management"]
            else:
                return ["Immediate workload review", "Implement flexible work arrangements", "Consider additional resources"]
        
        def _get_career_growth_recommendations(self, score: int) -> List[str]:
            """Get career growth recommendations."""
            if score >= 4:
                return ["Maintain development programs", "Expand opportunities", "Succession planning"]
            elif score >= 3:
                return ["Enhance development programs", "Create growth paths", "Mentorship programs"]
            else:
                return ["Develop career framework", "Create growth opportunities", "Regular career discussions"]
        
        def _get_compensation_recommendations(self, score: int) -> List[str]:
            """Get compensation recommendations."""
            if score >= 4:
                return ["Maintain competitive compensation", "Regular market reviews", "Performance-based rewards"]
            elif score >= 3:
                return ["Review compensation structure", "Market benchmarking", "Performance incentives"]
            else:
                return ["Comprehensive compensation review", "Market analysis", "Consider adjustments"]
        
        def _get_management_recommendations(self, score: int) -> List[str]:
            """Get management support recommendations."""
            if score >= 4:
                return ["Maintain management standards", "Share best practices", "Leadership development"]
            elif score >= 3:
                return ["Management training", "Feedback mechanisms", "Support systems"]
            else:
                return ["Immediate management review", "Training programs", "Support structures"]
        
        def _get_team_recommendations(self, score: int) -> List[str]:
            """Get team collaboration recommendations."""
            if score >= 4:
                return ["Maintain team dynamics", "Cross-team collaboration", "Team building activities"]
            elif score >= 3:
                return ["Enhance communication", "Team building", "Collaboration tools"]
            else:
                return ["Team dynamics review", "Communication training", "Collaboration processes"]
        
        def _get_culture_recommendations(self, score: int) -> List[str]:
            """Get company culture recommendations."""
            if score >= 4:
                return ["Maintain culture", "Reinforce values", "Culture ambassadors"]
            elif score >= 3:
                return ["Culture assessment", "Values clarification", "Culture initiatives"]
            else:
                return ["Culture transformation", "Values definition", "Cultural change management"]
        
        def _prioritize_concerns(self, concerns: List[str]) -> Dict[str, str]:
            """Prioritize employee concerns."""
            priority_mapping = {
                "Compensation": "High",
                "Career growth": "High",
                "Work-life balance": "High",
                "Management": "High",
                "Company direction": "Medium",
                "Job security": "Medium"
            }
            
            priorities = {}
            for concern in concerns:
                priorities[concern] = priority_mapping.get(concern, "Medium")
            
            return priorities
        
        def _suggest_actions_for_concerns(self, concerns: List[str]) -> Dict[str, List[str]]:
            """Suggest actions for addressing concerns."""
            actions = {
                "Compensation": ["Market benchmarking", "Compensation review", "Performance-based rewards"],
                "Career growth": ["Career framework", "Development programs", "Growth opportunities"],
                "Work-life balance": ["Flexible policies", "Workload review", "Wellness programs"],
                "Management": ["Management training", "Feedback systems", "Support structures"],
                "Company direction": ["Communication strategy", "Vision clarity", "Employee involvement"],
                "Job security": ["Business transparency", "Growth plans", "Employee development"]
            }
            
            concern_actions = {}
            for concern in concerns:
                concern_actions[concern] = actions.get(concern, ["Develop specific action plan"])
            
            return concern_actions
        
        def _categorize_nps_score(self, score: int) -> str:
            """Categorize Net Promoter Score."""
            if score >= 9:
                return "Promoter"
            elif score >= 7:
                return "Passive"
            else:
                return "Detractor"
        
        def _generate_employee_assessment(self) -> Dict[str, Any]:
            """Generate overall employee satisfaction assessment."""
            # Calculate average scores
            scores = [
                self.responses.get("job_satisfaction", 0),
                self.responses.get("work_life_balance", 0),
                self.responses.get("career_growth", 0),
                self.responses.get("compensation", 0),
                self.responses.get("management_support", 0),
                self.responses.get("team_collaboration", 0),
                self.responses.get("company_culture", 0)
            ]
            
            # Filter out 0 scores (not answered)
            valid_scores = [s for s in scores if s > 0]
            if valid_scores:
                average_score = sum(valid_scores) / len(valid_scores)
            else:
                average_score = 0
            
            # Determine overall health
            if average_score >= 4:
                overall_health = "Excellent"
            elif average_score >= 3:
                overall_health = "Good"
            elif average_score >= 2:
                overall_health = "Fair"
            else:
                overall_health = "Poor"
            
            # Generate recommendations
            if overall_health == "Excellent":
                recommendations = [
                    "Maintain current practices and policies",
                    "Continue monitoring employee satisfaction",
                    "Share best practices across the organization"
                ]
            elif overall_health == "Good":
                recommendations = [
                    "Address areas with lower scores",
                    "Implement targeted improvements",
                    "Regular feedback collection and review"
                ]
            elif overall_health == "Fair":
                recommendations = [
                    "Immediate attention to low-scoring areas",
                    "Develop comprehensive improvement plans",
                    "Consider external consultation"
                ]
            else:
                recommendations = [
                    "Critical intervention required",
                    "Comprehensive organizational review",
                    "Immediate action on all fronts"
                ]
            
            return {
                "average_score": round(average_score, 2),
                "overall_health": overall_health,
                "key_recommendations": recommendations,
                "response_count": len(self.responses)
            }
    
    return EmployeeSatisfactionQuestionnaire

def run_custom_questionnaire():
    """Run the custom employee satisfaction questionnaire."""
    print("Creating custom employee satisfaction questionnaire...")
    
    # Create custom questionnaire class
    CustomQuestionnaire = create_custom_questionnaire_class()
    
    if CustomQuestionnaire:
        # Create and run questionnaire
        questionnaire = CustomQuestionnaire()
        questionnaire.run_full_analysis()
    else:
        print("Failed to create custom questionnaire")

if __name__ == "__main__":
    run_custom_questionnaire()
