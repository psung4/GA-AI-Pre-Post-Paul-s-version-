#!/usr/bin/env python3
"""
Questionnaire Configuration

This file contains predefined question sets for different types of analysis.
You can easily customize the questions, add new question types, or create
entirely new analysis categories.
"""

# Business Analysis Questions (Default)
BUSINESS_ANALYSIS_QUESTIONS = [
    {
        "id": "business_type",
        "question": "What type of business are you analyzing?",
        "type": "multiple_choice",
        "options": ["Technology", "Finance", "Healthcare", "Retail", "Manufacturing", "Other"],
        "required": True
    },
    {
        "id": "company_size",
        "question": "What is the approximate size of the company?",
        "type": "multiple_choice",
        "options": ["1-10 employees", "11-50 employees", "51-200 employees", "201-1000 employees", "1000+ employees"],
        "required": True
    },
    {
        "id": "revenue_range",
        "question": "What is the annual revenue range?",
        "type": "multiple_choice",
        "options": ["Under $100K", "$100K - $1M", "$1M - $10M", "$10M - $100M", "$100M+"],
        "required": True
    },
    {
        "id": "growth_rate",
        "question": "What is the current growth rate?",
        "type": "multiple_choice",
        "options": ["Declining", "Stable", "Growing slowly (1-10%)", "Growing moderately (10-25%)", "Growing rapidly (25%+)"],
        "required": True
    },
    {
        "id": "market_position",
        "question": "How would you describe the company's market position?",
        "type": "multiple_choice",
        "options": ["Market leader", "Strong competitor", "Established player", "Emerging player", "Niche player"],
        "required": True
    },
    {
        "id": "challenges",
        "question": "What are the main challenges the company faces? (Select all that apply)",
        "type": "multi_select",
        "options": ["Market competition", "Regulatory compliance", "Technology disruption", "Talent acquisition", "Financial constraints", "Supply chain issues", "Customer retention"],
        "required": True
    },
    {
        "id": "opportunities",
        "question": "What opportunities do you see for the company?",
        "type": "text",
        "required": False
    },
    {
        "id": "risk_factors",
        "question": "What are the main risk factors?",
        "type": "text",
        "required": False
    },
    {
        "id": "recommendations",
        "question": "What recommendations would you make?",
        "type": "text",
        "required": False
    }
]

# Investment Analysis Questions
INVESTMENT_ANALYSIS_QUESTIONS = [
    {
        "id": "investment_type",
        "question": "What type of investment are you analyzing?",
        "type": "multiple_choice",
        "options": ["Stocks", "Bonds", "Real Estate", "Startup/Private Equity", "Commodities", "Cryptocurrency", "Other"],
        "required": True
    },
    {
        "id": "investment_horizon",
        "question": "What is your investment time horizon?",
        "type": "multiple_choice",
        "options": ["Short-term (1-3 years)", "Medium-term (3-10 years)", "Long-term (10+ years)"],
        "required": True
    },
    {
        "id": "risk_tolerance",
        "question": "What is your risk tolerance level?",
        "type": "multiple_choice",
        "options": ["Conservative", "Moderate", "Aggressive"],
        "required": True
    },
    {
        "id": "expected_return",
        "question": "What is your expected annual return?",
        "type": "multiple_choice",
        "options": ["2-5%", "5-10%", "10-15%", "15-25%", "25%+"],
        "required": True
    },
    {
        "id": "market_conditions",
        "question": "How would you describe current market conditions?",
        "type": "multiple_choice",
        "options": ["Bear market", "Sideways/Volatile", "Bull market", "Uncertain"],
        "required": True
    },
    {
        "id": "diversification",
        "question": "How diversified is your current portfolio?",
        "type": "multiple_choice",
        "options": ["Not diversified", "Somewhat diversified", "Well diversified", "Highly diversified"],
        "required": True
    },
    {
        "id": "liquidity_needs",
        "question": "What are your liquidity needs?",
        "type": "multiple_choice",
        "options": ["High (need cash within 1 year)", "Medium (1-3 years)", "Low (3+ years)"],
        "required": True
    },
    {
        "id": "investment_goals",
        "question": "What are your primary investment goals?",
        "type": "multi_select",
        "options": ["Capital preservation", "Income generation", "Capital appreciation", "Tax efficiency", "Inflation protection"],
        "required": True
    },
    {
        "id": "concerns",
        "question": "What are your main investment concerns?",
        "type": "text",
        "required": False
    }
]

# Project Management Analysis Questions
PROJECT_MANAGEMENT_QUESTIONS = [
    {
        "id": "project_type",
        "question": "What type of project is this?",
        "type": "multiple_choice",
        "options": ["Software Development", "Construction", "Marketing Campaign", "Research", "Process Improvement", "Other"],
        "required": True
    },
    {
        "id": "project_size",
        "question": "What is the project size/complexity?",
        "type": "multiple_choice",
        "options": ["Small (1-3 months)", "Medium (3-12 months)", "Large (1-3 years)", "Enterprise (3+ years)"],
        "required": True
    },
    {
        "id": "team_size",
        "question": "What is the team size?",
        "type": "multiple_choice",
        "options": ["1-3 people", "4-8 people", "9-20 people", "20+ people"],
        "required": True
    },
    {
        "id": "budget_range",
        "question": "What is the budget range?",
        "type": "multiple_choice",
        "options": ["Under $10K", "$10K - $100K", "$100K - $1M", "$1M+"],
        "required": True
    },
    {
        "id": "timeline_pressure",
        "question": "How much timeline pressure is there?",
        "type": "multiple_choice",
        "options": ["No pressure", "Some pressure", "High pressure", "Critical deadline"],
        "required": True
    },
    {
        "id": "stakeholder_complexity",
        "question": "How complex are the stakeholder relationships?",
        "type": "multiple_choice",
        "options": ["Simple", "Moderate", "Complex", "Very complex"],
        "required": True
    },
    {
        "id": "technical_risks",
        "question": "What technical risks exist?",
        "type": "multi_select",
        "options": ["New technology", "Integration challenges", "Performance requirements", "Security concerns", "Scalability issues", "None"],
        "required": True
    },
    {
        "id": "resource_availability",
        "question": "How would you rate resource availability?",
        "type": "multiple_choice",
        "options": ["Excellent", "Good", "Fair", "Poor"],
        "required": True
    },
    {
        "id": "success_criteria",
        "question": "What are the key success criteria?",
        "type": "text",
        "required": False
    },
    {
        "id": "potential_issues",
        "question": "What potential issues do you foresee?",
        "type": "text",
        "required": False
    }
]

# Customer Satisfaction Analysis Questions
CUSTOMER_SATISFACTION_QUESTIONS = [
    {
        "id": "customer_segment",
        "question": "What customer segment are you analyzing?",
        "type": "multiple_choice",
        "options": ["B2B Enterprise", "B2B SMB", "B2C Premium", "B2C Mass Market", "Government", "Non-profit"],
        "required": True
    },
    {
        "id": "interaction_channel",
        "question": "What is the primary interaction channel?",
        "type": "multiple_choice",
        "options": ["In-person", "Phone", "Email", "Website", "Mobile App", "Social Media", "Multiple channels"],
        "required": True
    },
    {
        "id": "satisfaction_level",
        "question": "What is the current satisfaction level?",
        "type": "multiple_choice",
        "options": ["Very dissatisfied", "Dissatisfied", "Neutral", "Satisfied", "Very satisfied"],
        "required": True
    },
    {
        "id": "loyalty_level",
        "question": "How loyal are customers?",
        "type": "multiple_choice",
        "options": ["Not loyal", "Somewhat loyal", "Loyal", "Very loyal", "Extremely loyal"],
        "required": True
    },
    {
        "id": "pain_points",
        "question": "What are the main customer pain points?",
        "type": "multi_select",
        "options": ["Product quality", "Customer service", "Pricing", "Ease of use", "Support response time", "Documentation", "None"],
        "required": True
    },
    {
        "id": "improvement_areas",
        "question": "What areas need improvement?",
        "type": "text",
        "required": False
    },
    {
        "id": "positive_feedback",
        "question": "What positive feedback do you receive?",
        "type": "text",
        "required": False
    },
    {
        "id": "recommendation_likelihood",
        "question": "How likely are customers to recommend you?",
        "type": "multiple_choice",
        "options": ["Very unlikely", "Unlikely", "Neutral", "Likely", "Very likely"],
        "required": True
    }
]

# Question Type Definitions
QUESTION_TYPES = {
    "multiple_choice": {
        "description": "Single selection from predefined options",
        "input_method": "numeric_choice",
        "validation": "range_check"
    },
    "multi_select": {
        "description": "Multiple selections from predefined options",
        "input_method": "comma_separated_numbers",
        "validation": "range_check"
    },
    "text": {
        "description": "Free-form text input",
        "input_method": "text_input",
        "validation": "length_check"
    },
    "numeric": {
        "description": "Numeric input with optional range",
        "input_method": "numeric_input",
        "validation": "range_check"
    },
    "date": {
        "description": "Date input",
        "input_method": "date_input",
        "validation": "date_format"
    },
    "rating": {
        "description": "Rating scale (e.g., 1-5, 1-10)",
        "input_method": "rating_input",
        "validation": "range_check"
    }
}

# Available Question Sets
QUESTION_SETS = {
    "business_analysis": {
        "name": "Business Analysis",
        "description": "Comprehensive business analysis covering type, size, revenue, growth, and challenges",
        "questions": BUSINESS_ANALYSIS_QUESTIONS,
        "category": "business"
    },
    "investment_analysis": {
        "name": "Investment Analysis",
        "description": "Investment evaluation covering type, risk tolerance, market conditions, and goals",
        "questions": INVESTMENT_ANALYSIS_QUESTIONS,
        "category": "finance"
    },
    "project_management": {
        "name": "Project Management",
        "description": "Project assessment covering scope, resources, risks, and success criteria",
        "questions": PROJECT_MANAGEMENT_QUESTIONS,
        "category": "management"
    },
    "customer_satisfaction": {
        "name": "Customer Satisfaction",
        "description": "Customer experience analysis covering satisfaction, loyalty, and pain points",
        "questions": CUSTOMER_SATISFACTION_QUESTIONS,
        "category": "customer"
    }
}

# Analysis Categories
ANALYSIS_CATEGORIES = {
    "business": {
        "name": "Business Analysis",
        "description": "General business and organizational analysis",
        "question_sets": ["business_analysis", "project_management"]
    },
    "finance": {
        "name": "Financial Analysis",
        "description": "Investment and financial decision analysis",
        "question_sets": ["investment_analysis"]
    },
    "management": {
        "name": "Management Analysis",
        "description": "Project and operational management analysis",
        "question_sets": ["project_management"]
    },
    "customer": {
        "name": "Customer Analysis",
        "description": "Customer experience and satisfaction analysis",
        "question_sets": ["customer_satisfaction"]
    }
}

def get_question_set(set_name: str):
    """Get a specific question set by name."""
    return QUESTION_SETS.get(set_name, {}).get("questions", [])

def get_available_question_sets():
    """Get list of available question sets."""
    return list(QUESTION_SETS.keys())

def get_question_set_info(set_name: str):
    """Get information about a specific question set."""
    return QUESTION_SETS.get(set_name, {})

def get_analysis_categories():
    """Get available analysis categories."""
    return ANALYSIS_CATEGORIES

def create_custom_question_set(name: str, description: str, questions: list, category: str = "custom"):
    """Create a custom question set."""
    custom_set = {
        "name": name,
        "description": description,
        "questions": questions,
        "category": category
    }
    return custom_set

def validate_question_format(question: dict) -> bool:
    """Validate that a question has the required format."""
    required_fields = ["id", "question", "type"]
    question_types = list(QUESTION_TYPES.keys())
    
    # Check required fields
    for field in required_fields:
        if field not in question:
            return False
    
    # Check question type
    if question["type"] not in question_types:
        return False
    
    # Check options for choice-based questions
    if question["type"] in ["multiple_choice", "multi_select"]:
        if "options" not in question or not question["options"]:
            return False
    
    return True
