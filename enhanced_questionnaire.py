#!/usr/bin/env python3
"""
Enhanced Analysis Questionnaire Tool

This script allows users to choose from different question sets and conducts
analysis based on their responses. It's more flexible than the basic version.
"""

import json
import datetime
from typing import Dict, List, Any, Optional
import os
from questionnaire_config import (
    QUESTION_SETS, 
    get_question_set, 
    get_available_question_sets,
    get_question_set_info,
    get_analysis_categories
)

class EnhancedAnalysisQuestionnaire:
    def __init__(self):
        self.responses = {}
        self.analysis_results = {}
        self.selected_question_set = None
        self.questions = []
    
    def display_welcome(self):
        """Display welcome message and instructions."""
        print("=" * 70)
        print("              ENHANCED ANALYSIS QUESTIONNAIRE")
        print("=" * 70)
        print("\nThis tool provides multiple analysis categories to choose from.")
        print("Select the type of analysis that best fits your needs.")
        print("\n" + "=" * 70 + "\n")
    
    def select_question_set(self):
        """Allow user to select a question set."""
        print("Available Analysis Categories:")
        print("-" * 40)
        
        categories = get_analysis_categories()
        for cat_id, cat_info in categories.items():
            print(f"\n{cat_info['name']}:")
            print(f"  {cat_info['description']}")
            print("  Available question sets:")
            for qset in cat_info['question_sets']:
                qset_info = get_question_set_info(qset)
                print(f"    • {qset_info['name']}: {qset_info['description']}")
        
        print("\n" + "-" * 40)
        print("Available Question Sets:")
        print("-" * 40)
        
        available_sets = get_available_question_sets()
        for i, set_name in enumerate(available_sets, 1):
            set_info = get_question_set_info(set_name)
            print(f"{i}. {set_info['name']} - {set_info['description']}")
        
        while True:
            try:
                choice = input(f"\nSelect a question set (1-{len(available_sets)}): ")
                choice_num = int(choice)
                if 1 <= choice_num <= len(available_sets):
                    selected_set = available_sets[choice_num - 1]
                    self.selected_question_set = selected_set
                    self.questions = get_question_set(selected_set)
                    set_info = get_question_set_info(selected_set)
                    print(f"\nSelected: {set_info['name']}")
                    print(f"Description: {set_info['description']}")
                    print(f"Number of questions: {len(self.questions)}")
                    return
                else:
                    print("Invalid choice. Please try again.")
            except ValueError:
                print("Please enter a valid number.")
    
    def get_user_input(self, question_data: Dict[str, Any]) -> Any:
        """Get user input based on question type."""
        question_id = question_data["id"]
        question_text = question_data["question"]
        question_type = question_data["type"]
        required = question_data.get("required", False)
        
        while True:
            print(f"\n{question_text}")
            if required:
                print("(Required)")
            
            if question_type == "multiple_choice":
                options = question_data["options"]
                for i, option in enumerate(options, 1):
                    print(f"  {i}. {option}")
                
                try:
                    choice = int(input(f"\nEnter your choice (1-{len(options)}): "))
                    if 1 <= choice <= len(options):
                        return options[choice - 1]
                    else:
                        print("Invalid choice. Please try again.")
                except ValueError:
                    print("Please enter a valid number.")
                    
            elif question_type == "multi_select":
                options = question_data["options"]
                for i, option in enumerate(options, 1):
                    print(f"  {i}. {option}")
                
                print("\nEnter the numbers of your choices separated by commas (e.g., 1,3,5):")
                try:
                    choices_input = input("Your choices: ").strip()
                    if not choices_input and not required:
                        return []
                    
                    choice_numbers = [int(x.strip()) for x in choices_input.split(",")]
                    selected_options = []
                    
                    for num in choice_numbers:
                        if 1 <= num <= len(options):
                            selected_options.append(options[num - 1])
                        else:
                            print(f"Invalid choice {num}. Please try again.")
                            break
                    else:
                        if selected_options or not required:
                            return selected_options
                        else:
                            print("Please select at least one option.")
                            
                except ValueError:
                    print("Please enter valid numbers separated by commas.")
                    
            elif question_type == "text":
                if not required:
                    print("(Optional - press Enter to skip)")
                
                response = input("Your response: ").strip()
                if response or not required:
                    return response
                else:
                    print("This field is required. Please provide a response.")
            
            elif question_type == "numeric":
                if not required:
                    print("(Optional - press Enter to skip)")
                
                response = input("Enter numeric value: ").strip()
                if not response and not required:
                    return None
                
                try:
                    return float(response)
                except ValueError:
                    print("Please enter a valid number.")
            
            elif question_type == "rating":
                scale = question_data.get("scale", 5)
                print(f"Rate on a scale of 1-{scale}:")
                try:
                    rating = int(input(f"Your rating (1-{scale}): "))
                    if 1 <= rating <= scale:
                        return rating
                    else:
                        print(f"Please enter a rating between 1 and {scale}.")
                except ValueError:
                    print("Please enter a valid number.")
            
            else:
                print(f"Unsupported question type: {question_type}")
                return None
    
    def conduct_questionnaire(self):
        """Conduct the full questionnaire."""
        if not self.questions:
            print("No questions loaded. Please select a question set first.")
            return
        
        print(f"\nStarting {get_question_set_info(self.selected_question_set)['name']} questionnaire...")
        print("=" * 60)
        
        for i, question in enumerate(self.questions, 1):
            print(f"\nQuestion {i} of {len(self.questions)}")
            response = self.get_user_input(question)
            self.responses[question["id"]] = response
            
            # Show progress
            completed = len(self.responses)
            total = len(self.questions)
            progress = (completed / total) * 100
            print(f"\nProgress: {completed}/{total} questions completed ({progress:.1f}%)")
        
        print("\n" + "=" * 60)
        print("           QUESTIONNAIRE COMPLETED!")
        print("=" * 60)
    
    def analyze_responses(self):
        """Analyze the collected responses based on the selected question set."""
        print("\nAnalyzing your responses...\n")
        
        if self.selected_question_set == "business_analysis":
            self._analyze_business_responses()
        elif self.selected_question_set == "investment_analysis":
            self._analyze_investment_responses()
        elif self.selected_question_set == "project_management":
            self._analyze_project_responses()
        elif self.selected_question_set == "customer_satisfaction":
            self._analyze_customer_responses()
        else:
            self._analyze_generic_responses()
        
        # Generate overall assessment
        self.analysis_results["overall_assessment"] = self._generate_overall_assessment()
    
    def _analyze_business_responses(self):
        """Analyze business analysis responses."""
        # Business Type Analysis
        business_type = self.responses.get("business_type")
        if business_type:
            self.analysis_results["business_insights"] = {
                "type": business_type,
                "characteristics": self._get_business_characteristics(business_type)
            }
        
        # Company Size Analysis
        company_size = self.responses.get("company_size")
        if company_size:
            self.analysis_results["size_analysis"] = {
                "size": company_size,
                "implications": self._get_size_implications(company_size)
            }
        
        # Revenue Analysis
        revenue = self.responses.get("revenue_range")
        if revenue:
            self.analysis_results["revenue_analysis"] = {
                "revenue_range": revenue,
                "financial_health": self._assess_financial_health(revenue)
            }
        
        # Growth Analysis
        growth = self.responses.get("growth_rate")
        if growth:
            self.analysis_results["growth_analysis"] = {
                "growth_rate": growth,
                "stage": self._assess_growth_stage(growth)
            }
        
        # Market Position Analysis
        market_pos = self.responses.get("market_position")
        if market_pos:
            self.analysis_results["market_analysis"] = {
                "position": market_pos,
                "strategic_implications": self._get_market_implications(market_pos)
            }
        
        # Challenges Analysis
        challenges = self.responses.get("challenges", [])
        if challenges:
            self.analysis_results["challenges_analysis"] = {
                "challenges": challenges,
                "priority_levels": self._prioritize_challenges(challenges),
                "mitigation_strategies": self._suggest_mitigation_strategies(challenges)
            }
    
    def _analyze_investment_responses(self):
        """Analyze investment analysis responses."""
        # Investment Type Analysis
        inv_type = self.responses.get("investment_type")
        if inv_type:
            self.analysis_results["investment_type_analysis"] = {
                "type": inv_type,
                "characteristics": self._get_investment_characteristics(inv_type)
            }
        
        # Risk Profile Analysis
        risk_tolerance = self.responses.get("risk_tolerance")
        if risk_tolerance:
            self.analysis_results["risk_profile"] = {
                "tolerance": risk_tolerance,
                "recommendations": self._get_risk_recommendations(risk_tolerance)
            }
        
        # Market Conditions Analysis
        market_conditions = self.responses.get("market_conditions")
        if market_conditions:
            self.analysis_results["market_analysis"] = {
                "conditions": market_conditions,
                "strategies": self._get_market_strategies(market_conditions)
            }
        
        # Portfolio Analysis
        diversification = self.responses.get("diversification")
        if diversification:
            self.analysis_results["portfolio_analysis"] = {
                "diversification": diversification,
                "improvement_suggestions": self._get_diversification_suggestions(diversification)
            }
    
    def _analyze_project_responses(self):
        """Analyze project management responses."""
        # Project Complexity Analysis
        project_size = self.responses.get("project_size")
        if project_size:
            self.analysis_results["complexity_analysis"] = {
                "size": project_size,
                "management_implications": self._get_project_implications(project_size)
            }
        
        # Risk Assessment
        technical_risks = self.responses.get("technical_risks", [])
        if technical_risks:
            self.analysis_results["risk_assessment"] = {
                "technical_risks": technical_risks,
                "mitigation_strategies": self._get_project_risk_strategies(technical_risks)
            }
        
        # Resource Analysis
        resource_availability = self.responses.get("resource_availability")
        if resource_availability:
            self.analysis_results["resource_analysis"] = {
                "availability": resource_availability,
                "recommendations": self._get_resource_recommendations(resource_availability)
            }
    
    def _analyze_customer_responses(self):
        """Analyze customer satisfaction responses."""
        # Satisfaction Analysis
        satisfaction = self.responses.get("satisfaction_level")
        if satisfaction:
            self.analysis_results["satisfaction_analysis"] = {
                "level": satisfaction,
                "interpretation": self._interpret_satisfaction_level(satisfaction)
            }
        
        # Pain Points Analysis
        pain_points = self.responses.get("pain_points", [])
        if pain_points:
            self.analysis_results["pain_points_analysis"] = {
                "points": pain_points,
                "priority": self._prioritize_pain_points(pain_points),
                "solutions": self._suggest_pain_point_solutions(pain_points)
            }
        
        # Loyalty Analysis
        loyalty = self.responses.get("loyalty_level")
        if loyalty:
            self.analysis_results["loyalty_analysis"] = {
                "level": loyalty,
                "improvement_areas": self._identify_loyalty_improvements(loyalty)
            }
    
    def _analyze_generic_responses(self):
        """Generic analysis for custom question sets."""
        self.analysis_results["generic_analysis"] = {
            "total_questions": len(self.questions),
            "completed_questions": len(self.responses),
            "response_summary": self._summarize_responses()
        }
    
    def _summarize_responses(self):
        """Create a summary of all responses."""
        summary = {}
        for question_id, response in self.responses.items():
            question = next((q for q in self.questions if q["id"] == question_id), None)
            if question:
                summary[question["question"]] = {
                    "response": response,
                    "type": question["type"]
                }
        return summary
    
    # Helper methods for business analysis
    def _get_business_characteristics(self, business_type: str) -> List[str]:
        """Get characteristics based on business type."""
        characteristics = {
            "Technology": ["Innovation-driven", "Fast-paced", "High R&D investment", "Talent-dependent"],
            "Finance": ["Regulated", "Risk-averse", "Compliance-focused", "Customer trust critical"],
            "Healthcare": ["Highly regulated", "Quality-focused", "Long sales cycles", "Ethical considerations"],
            "Retail": ["Customer-centric", "Seasonal", "Inventory management", "Location-dependent"],
            "Manufacturing": ["Capital-intensive", "Supply chain dependent", "Quality control", "Efficiency-focused"],
            "Other": ["Industry-specific factors", "Market dynamics", "Regulatory environment"]
        }
        return characteristics.get(business_type, ["Industry-specific characteristics"])
    
    def _get_size_implications(self, company_size: str) -> List[str]:
        """Get implications based on company size."""
        implications = {
            "1-10 employees": ["Agile decision-making", "Limited resources", "Owner-dependent", "Personal relationships"],
            "11-50 employees": ["Growing structure", "Process development", "Team building", "Scaling challenges"],
            "51-200 employees": ["Established processes", "Department structure", "Management layers", "Growth opportunities"],
            "201-1000 employees": ["Corporate structure", "Standardized processes", "Multiple locations", "Professional management"],
            "1000+ employees": ["Enterprise scale", "Complex bureaucracy", "Global presence", "Institutional processes"]
        }
        return implications.get(company_size, ["Size-specific implications"])
    
    def _assess_financial_health(self, revenue: str) -> str:
        """Assess financial health based on revenue."""
        if "Under $100K" in revenue:
            return "Early stage/Startup - Focus on growth and funding"
        elif "$100K - $1M" in revenue:
            return "Growth stage - Focus on scaling operations"
        elif "$1M - $10M" in revenue:
            return "Established - Focus on market expansion"
        elif "$10M - $100M" in revenue:
            return "Mature - Focus on efficiency and diversification"
        else:
            return "Enterprise - Focus on optimization and innovation"
    
    def _assess_growth_stage(self, growth: str) -> str:
        """Assess growth stage based on growth rate."""
        if "Declining" in growth:
            return "Decline phase - Focus on turnaround strategies"
        elif "Stable" in growth:
            return "Maturity phase - Focus on efficiency and innovation"
        elif "Growing slowly" in growth:
            return "Growth phase - Focus on market penetration"
        elif "Growing moderately" in growth:
            return "Expansion phase - Focus on market development"
        else:
            return "Hypergrowth phase - Focus on scaling and infrastructure"
    
    def _get_market_implications(self, market_pos: str) -> List[str]:
        """Get strategic implications based on market position."""
        implications = {
            "Market leader": ["Defend position", "Innovate continuously", "Expand markets", "Acquire competitors"],
            "Strong competitor": ["Challenge leader", "Differentiate offerings", "Improve efficiency", "Expand capabilities"],
            "Established player": ["Maintain position", "Improve operations", "Explore new markets", "Innovate products"],
            "Emerging player": ["Gain market share", "Build brand", "Develop capabilities", "Secure funding"],
            "Niche player": ["Deepen expertise", "Expand niche", "Build relationships", "Consider diversification"]
        }
        return implications.get(market_pos, ["Position-specific strategies"])
    
    def _prioritize_challenges(self, challenges: List[str]) -> Dict[str, str]:
        """Prioritize challenges by importance."""
        priority_mapping = {
            "Market competition": "High",
            "Regulatory compliance": "Medium",
            "Technology disruption": "High",
            "Talent acquisition": "Medium",
            "Financial constraints": "High",
            "Supply chain issues": "Medium",
            "Customer retention": "High"
        }
        
        priorities = {}
        for challenge in challenges:
            priorities[challenge] = priority_mapping.get(challenge, "Medium")
        
        return priorities
    
    def _suggest_mitigation_strategies(self, challenges: List[str]) -> Dict[str, List[str]]:
        """Suggest mitigation strategies for challenges."""
        strategies = {
            "Market competition": ["Differentiate offerings", "Improve customer service", "Innovate products"],
            "Regulatory compliance": ["Hire compliance experts", "Implement compliance systems", "Regular audits"],
            "Technology disruption": ["Invest in R&D", "Partner with tech companies", "Hire tech talent"],
            "Talent acquisition": ["Improve employer brand", "Offer competitive compensation", "Develop internal talent"],
            "Financial constraints": ["Optimize operations", "Seek funding", "Improve cash flow"],
            "Supply chain issues": ["Diversify suppliers", "Build relationships", "Implement monitoring"],
            "Customer retention": ["Improve customer experience", "Loyalty programs", "Regular feedback"]
        }
        
        mitigation = {}
        for challenge in challenges:
            mitigation[challenge] = strategies.get(challenge, ["Develop specific strategies"])
        
        return mitigation
    
    # Helper methods for investment analysis
    def _get_investment_characteristics(self, inv_type: str) -> List[str]:
        """Get characteristics based on investment type."""
        characteristics = {
            "Stocks": ["Equity ownership", "Market volatility", "Dividend potential", "Growth potential"],
            "Bonds": ["Fixed income", "Lower risk", "Interest payments", "Maturity dates"],
            "Real Estate": ["Tangible asset", "Rental income", "Appreciation potential", "Illiquid"],
            "Startup/Private Equity": ["High risk", "High return potential", "Illiquid", "Long-term horizon"],
            "Commodities": ["Inflation hedge", "Volatile", "No income", "Global factors"],
            "Cryptocurrency": ["Digital asset", "Extremely volatile", "24/7 trading", "Regulatory uncertainty"]
        }
        return characteristics.get(inv_type, ["Type-specific characteristics"])
    
    def _get_risk_recommendations(self, risk_tolerance: str) -> List[str]:
        """Get recommendations based on risk tolerance."""
        recommendations = {
            "Conservative": ["Focus on bonds and stable dividend stocks", "Maintain high cash reserves", "Consider annuities"],
            "Moderate": ["Balanced portfolio of stocks and bonds", "Diversify across sectors", "Regular rebalancing"],
            "Aggressive": ["Higher allocation to stocks", "Consider alternative investments", "Active management"]
        }
        return recommendations.get(risk_tolerance, ["Consult with financial advisor"])
    
    def _get_market_strategies(self, market_conditions: str) -> List[str]:
        """Get strategies based on market conditions."""
        strategies = {
            "Bear market": ["Dollar-cost averaging", "Defensive stocks", "Bond allocation", "Cash reserves"],
            "Sideways/Volatile": ["Diversification", "Regular rebalancing", "Quality companies", "Patience"],
            "Bull market": ["Growth stocks", "Sector rotation", "Take profits", "Monitor valuations"],
            "Uncertain": ["Conservative approach", "Quality over quantity", "Regular monitoring", "Professional advice"]
        }
        return strategies.get(market_conditions, ["Adapt strategy to conditions"])
    
    def _get_diversification_suggestions(self, diversification: str) -> List[str]:
        """Get suggestions for improving diversification."""
        suggestions = {
            "Not diversified": ["Start with index funds", "Add different asset classes", "Consider ETFs", "Professional guidance"],
            "Somewhat diversified": ["Add international exposure", "Include bonds", "Sector diversification", "Regular review"],
            "Well diversified": ["Maintain current strategy", "Rebalance regularly", "Monitor correlations", "Tax optimization"],
            "Highly diversified": ["Consider consolidation", "Focus on quality", "Reduce complexity", "Cost optimization"]
        }
        return suggestions.get(diversification, ["Assess current allocation"])
    
    # Helper methods for project management analysis
    def _get_project_implications(self, project_size: str) -> List[str]:
        """Get management implications based on project size."""
        implications = {
            "Small (1-3 months)": ["Simple planning", "Minimal documentation", "Direct communication", "Quick execution"],
            "Medium (3-12 months)": ["Detailed planning", "Regular reviews", "Team coordination", "Risk management"],
            "Large (1-3 years)": ["Complex planning", "Multiple phases", "Stakeholder management", "Change control"],
            "Enterprise (3+ years)": ["Strategic planning", "Portfolio management", "Governance structure", "Continuous monitoring"]
        }
        return implications.get(project_size, ["Size-specific management approach"])
    
    def _get_project_risk_strategies(self, risks: List[str]) -> Dict[str, List[str]]:
        """Get risk mitigation strategies for project risks."""
        strategies = {
            "New technology": ["Proof of concept", "Expert consultation", "Training programs", "Fallback plans"],
            "Integration challenges": ["API documentation", "Testing protocols", "Vendor support", "Gradual rollout"],
            "Performance requirements": ["Load testing", "Performance monitoring", "Optimization", "Scalability planning"],
            "Security concerns": ["Security audits", "Penetration testing", "Compliance review", "Incident response"],
            "Scalability issues": ["Architecture review", "Performance testing", "Capacity planning", "Monitoring tools"]
        }
        
        mitigation = {}
        for risk in risks:
            mitigation[risk] = strategies.get(risk, ["Develop specific mitigation plan"])
        
        return mitigation
    
    def _get_resource_recommendations(self, availability: str) -> List[str]:
        """Get recommendations based on resource availability."""
        recommendations = {
            "Excellent": ["Optimize utilization", "Consider expansion", "Skill development", "Innovation focus"],
            "Good": ["Maintain efficiency", "Plan for growth", "Cross-training", "Process improvement"],
            "Fair": ["Prioritize critical needs", "Resource optimization", "External support", "Efficiency focus"],
            "Poor": ["Critical path focus", "External resources", "Scope reduction", "Timeline adjustment"]
        }
        return recommendations.get(availability, ["Assess resource needs"])
    
    # Helper methods for customer satisfaction analysis
    def _interpret_satisfaction_level(self, satisfaction: str) -> str:
        """Interpret satisfaction level and provide context."""
        interpretations = {
            "Very dissatisfied": "Critical issues requiring immediate attention",
            "Dissatisfied": "Significant problems need urgent resolution",
            "Neutral": "Room for improvement to increase satisfaction",
            "Satisfied": "Good performance with opportunities for enhancement",
            "Very satisfied": "Excellent performance, focus on maintaining standards"
        }
        return interpretations.get(satisfaction, "Level-specific interpretation")
    
    def _prioritize_pain_points(self, pain_points: List[str]) -> Dict[str, str]:
        """Prioritize pain points by impact."""
        priority_mapping = {
            "Product quality": "High",
            "Customer service": "High",
            "Pricing": "Medium",
            "Ease of use": "Medium",
            "Support response time": "High",
            "Documentation": "Low"
        }
        
        priorities = {}
        for point in pain_points:
            priorities[point] = priority_mapping.get(point, "Medium")
        
        return priorities
    
    def _suggest_pain_point_solutions(self, pain_points: List[str]) -> Dict[str, List[str]]:
        """Suggest solutions for pain points."""
        solutions = {
            "Product quality": ["Quality assurance processes", "Customer feedback loops", "Regular testing", "Continuous improvement"],
            "Customer service": ["Staff training", "Service standards", "Response time targets", "Customer feedback"],
            "Pricing": ["Competitive analysis", "Value proposition", "Pricing strategy", "Customer segmentation"],
            "Ease of use": ["User experience design", "User testing", "Interface improvements", "Documentation"],
            "Support response time": ["Support team expansion", "Automation tools", "Response time targets", "Escalation procedures"],
            "Documentation": ["Content review", "User testing", "Regular updates", "Multiple formats"]
        }
        
        pain_solutions = {}
        for point in pain_points:
            pain_solutions[point] = solutions.get(point, ["Develop specific solution"])
        
        return pain_solutions
    
    def _identify_loyalty_improvements(self, loyalty: str) -> List[str]:
        """Identify areas for improving customer loyalty."""
        improvements = {
            "Not loyal": ["Build trust", "Improve product quality", "Enhance customer service", "Loyalty programs"],
            "Somewhat loyal": ["Strengthen relationships", "Personalized experiences", "Regular communication", "Value demonstration"],
            "Loyal": ["Maintain standards", "Innovation", "Exclusive benefits", "Community building"],
            "Very loyal": ["Advocacy programs", "Referral incentives", "Exclusive access", "Partnership opportunities"],
            "Extremely loyal": ["Brand ambassadors", "Co-creation opportunities", "Exclusive experiences", "Strategic partnerships"]
        }
        return improvements.get(loyalty, ["Assess loyalty drivers"])
    
    def _generate_overall_assessment(self) -> Dict[str, Any]:
        """Generate overall assessment and recommendations."""
        # Calculate risk score based on question set
        risk_score = 0
        
        if self.selected_question_set == "business_analysis":
            if self.responses.get("growth_rate") == "Declining":
                risk_score += 3
            if self.responses.get("market_position") in ["Niche player", "Emerging player"]:
                risk_score += 2
            if len(self.responses.get("challenges", [])) > 3:
                risk_score += 2
        elif self.selected_question_set == "investment_analysis":
            if self.responses.get("risk_tolerance") == "Aggressive":
                risk_score += 2
            if self.responses.get("market_conditions") in ["Bear market", "Uncertain"]:
                risk_score += 2
            if self.responses.get("diversification") == "Not diversified":
                risk_score += 3
        elif self.selected_question_set == "project_management":
            if self.responses.get("timeline_pressure") in ["High pressure", "Critical deadline"]:
                risk_score += 2
            if self.responses.get("resource_availability") in ["Fair", "Poor"]:
                risk_score += 2
            if len(self.responses.get("technical_risks", [])) > 2:
                risk_score += 2
        elif self.selected_question_set == "customer_satisfaction":
            if self.responses.get("satisfaction_level") in ["Very dissatisfied", "Dissatisfied"]:
                risk_score += 3
            if self.responses.get("loyalty_level") in ["Not loyal", "Somewhat loyal"]:
                risk_score += 2
            if len(self.responses.get("pain_points", [])) > 3:
                risk_score += 2
        
        # Determine risk level
        if risk_score >= 5:
            risk_level = "High"
        elif risk_score >= 3:
            risk_level = "Medium"
        else:
            risk_level = "Low"
        
        # Generate recommendations based on question set
        recommendations = self._generate_set_specific_recommendations(risk_level)
        
        return {
            "risk_level": risk_level,
            "risk_score": risk_score,
            "overall_health": "Good" if risk_level == "Low" else "Fair" if risk_level == "Medium" else "Concerning",
            "key_recommendations": recommendations
        }
    
    def _generate_set_specific_recommendations(self, risk_level: str) -> List[str]:
        """Generate recommendations specific to the question set."""
        if self.selected_question_set == "business_analysis":
            if risk_level == "High":
                return [
                    "Immediate action required on key challenges",
                    "Consider strategic partnerships or acquisitions",
                    "Review and strengthen risk management processes"
                ]
            elif risk_level == "Medium":
                return [
                    "Address priority challenges systematically",
                    "Monitor market conditions closely",
                    "Strengthen competitive positioning"
                ]
            else:
                return [
                    "Maintain current strategies",
                    "Focus on growth opportunities",
                    "Continue monitoring for emerging risks"
                ]
        elif self.selected_question_set == "investment_analysis":
            if risk_level == "High":
                return [
                    "Review risk tolerance and portfolio allocation",
                    "Consider professional financial advice",
                    "Implement risk management strategies"
                ]
            elif risk_level == "Medium":
                return [
                    "Monitor portfolio performance regularly",
                    "Consider rebalancing",
                    "Stay informed about market conditions"
                ]
            else:
                return [
                    "Maintain current investment strategy",
                    "Continue regular monitoring",
                    "Consider new opportunities within risk parameters"
                ]
        elif self.selected_question_set == "project_management":
            if risk_level == "High":
                return [
                    "Immediate risk mitigation planning",
                    "Consider project scope reduction",
                    "Increase stakeholder communication"
                ]
            elif risk_level == "Medium":
                return [
                    "Implement risk monitoring processes",
                    "Regular status reviews",
                    "Prepare contingency plans"
                ]
            else:
                return [
                    "Continue current project management approach",
                    "Regular risk assessment",
                    "Focus on optimization and efficiency"
                ]
        elif self.selected_question_set == "customer_satisfaction":
            if risk_level == "High":
                return [
                    "Immediate customer experience improvements",
                    "Address critical pain points",
                    "Implement customer feedback systems"
                ]
            elif risk_level == "Medium":
                return [
                    "Systematic improvement planning",
                    "Regular customer satisfaction monitoring",
                    "Focus on high-impact improvements"
                ]
            else:
                return [
                    "Maintain current service standards",
                    "Continue monitoring customer feedback",
                    "Look for enhancement opportunities"
                ]
        else:
            # Generic recommendations
            if risk_level == "High":
                return ["Immediate action required", "Professional consultation recommended", "Risk mitigation planning"]
            elif risk_level == "Medium":
                return ["Monitor situation closely", "Implement improvement plans", "Regular assessment needed"]
            else:
                return ["Maintain current approach", "Continue monitoring", "Look for enhancement opportunities"]
    
    def display_analysis(self):
        """Display the analysis results."""
        set_info = get_question_set_info(self.selected_question_set)
        print(f"\n{'='*70}")
        print(f"           {set_info['name'].upper()} - ANALYSIS RESULTS")
        print(f"{'='*70}")
        
        # Display each analysis section
        for section, data in self.analysis_results.items():
            if section == "overall_assessment":
                continue  # Handle this separately
            
            print(f"\n{section.replace('_', ' ').title()}:")
            print("-" * 50)
            
            if isinstance(data, dict):
                for key, value in data.items():
                    if isinstance(value, list):
                        print(f"  {key.replace('_', ' ').title()}:")
                        for item in value:
                            print(f"    • {item}")
                    else:
                        print(f"  {key.replace('_', ' ').title()}: {value}")
            else:
                print(f"  {data}")
        
        # Display overall assessment
        overall = self.analysis_results.get("overall_assessment", {})
        if overall:
            print(f"\n{'Overall Assessment':-^70}")
            print(f"Risk Level: {overall.get('risk_level', 'Unknown')}")
            print(f"Overall Health: {overall.get('overall_health', 'Unknown')}")
            print(f"Risk Score: {overall.get('risk_score', 'Unknown')}")
            
            print(f"\nKey Recommendations:")
            for rec in overall.get('key_recommendations', []):
                print(f"  • {rec}")
    
    def save_results(self, filename: Optional[str] = None):
        """Save results to a JSON file."""
        if not filename:
            timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
            set_name = self.selected_question_set.replace("_", "")
            filename = f"{set_name}_analysis_{timestamp}.json"
        
        results = {
            "timestamp": datetime.datetime.now().isoformat(),
            "question_set": self.selected_question_set,
            "set_info": get_question_set_info(self.selected_question_set),
            "responses": self.responses,
            "analysis": self.analysis_results
        }
        
        try:
            with open(filename, 'w') as f:
                json.dump(results, f, indent=2)
            print(f"\nResults saved to: {filename}")
        except Exception as e:
            print(f"Error saving results: {e}")
    
    def run_full_analysis(self):
        """Run the complete analysis workflow."""
        try:
            # Display welcome and select question set
            self.display_welcome()
            self.select_question_set()
            
            # Conduct questionnaire
            self.conduct_questionnaire()
            
            # Analyze responses
            self.analyze_responses()
            
            # Display results
            self.display_analysis()
            
            # Save results
            save_choice = input("\nWould you like to save the results? (y/n): ").lower()
            if save_choice in ['y', 'yes']:
                filename = input("Enter filename (or press Enter for default): ").strip()
                if not filename:
                    filename = None
                self.save_results(filename)
            
            print("\nAnalysis complete! Thank you for using the enhanced questionnaire tool.")
            
        except KeyboardInterrupt:
            print("\n\nQuestionnaire interrupted by user.")
        except Exception as e:
            print(f"\nAn error occurred: {e}")

def main():
    """Main function to run the enhanced questionnaire."""
    questionnaire = EnhancedAnalysisQuestionnaire()
    questionnaire.run_full_analysis()

if __name__ == "__main__":
    main()
