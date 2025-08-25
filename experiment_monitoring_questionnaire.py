#!/usr/bin/env python3
"""
Experiment Monitoring Questionnaire

This script creates a custom questionnaire for monitoring experiments with
specific questions about experiment description, merchant ARIs, test timing,
control periods, and metrics.
"""

from enhanced_questionnaire import EnhancedAnalysisQuestionnaire
from questionnaire_config import create_custom_question_set, validate_question_format
from typing import List, Dict, Any, Optional
from datetime import datetime
import json
import os

def create_experiment_monitoring_questions():
    """Create the experiment monitoring questions."""
    
    experiment_questions = [
        {
            "id": "experiment_description",
            "question": "1. Briefly describe the experiment.",
            "type": "text",
            "required": True
        },
        {
            "id": "merchant_aris",
            "question": "2. Please provide a list of merchant ARIs or merchant partner ARIs.",
            "type": "text",
            "required": True
        },
        {
            "id": "ari_type",
            "question": "3. Are you providing merchant ARIs or merchant partner ARIs?",
            "type": "multiple_choice",
            "options": ["Merchant ARIs", "Merchant Partner ARIs"],
            "required": True
        },
        {
            "id": "test_start_date",
            "question": "4. What is the start date of the test period? (YYYY-MM-DD format)",
            "type": "text",
            "required": True
        },
        {
            "id": "test_end_date",
            "question": "What is the end date of the test period? (YYYY-MM-DD format)",
            "type": "text",
            "required": True
        },
        {
            "id": "control_start_date",
            "question": "5. What is the start date of the control period? (YYYY-MM-DD format)",
            "type": "text",
            "required": True
        },
        {
            "id": "control_end_date",
            "question": "What is the end date of the control period? (YYYY-MM-DD format)",
            "type": "text",
            "required": True
        },
        {
            "id": "metrics_to_monitor",
            "question": "6. What metrics would you like to monitor?",
            "type": "multi_select",
            "options": [
                "Authed GMV",
                "Checkouts",
                "E2E Conversion",
                "AOV",
                "Application Rate",
                "Authentication Rate",
                "Approval Rate",
                "Take-up Rate",
                "Auth Rate",
                "Median FICO",
                "% Prime+ Population",
                "Median ITACS",
                "Terms distribution",
                "% Z-term",
                "All metrics from above"
            ],
            "required": True
        },
        {
            "id": "monitoring_segmentation",
            "question": "7. What segmentation should we use for monitoring?",
            "type": "multi_select",
            "options": [
                "Overall",
                "NTA vs. Repeat",
                "FICO Bands",
                "AOV Bands",
                "ITACS Bands",
                "Loan Type (IB vs. 0%)"
            ],
            "required": True
        },
        {
            "id": "additional_context",
            "question": "8. Please provide any additional context that may be useful for the interpretation of results.",
            "type": "text",
            "required": False,
            "help_text": "This could include experiment goals, success criteria, business context, expected outcomes, or any other information that would help interpret the results."
        }
    ]
    
    # Validate questions
    print("Validating experiment monitoring questions...")
    for i, question in enumerate(experiment_questions):
        if validate_question_format(question):
            print(f"✓ Question {i+1} is valid")
        else:
            print(f"✗ Question {i+1} has format issues")
            return None
    
    # Create custom question set
    custom_set = create_custom_question_set(
        name="Experiment Monitoring Questionnaire",
        description="Comprehensive experiment monitoring setup and configuration",
        questions=experiment_questions,
        category="experiment"
    )
    
    return custom_set

def create_experiment_questionnaire_class():
    """Create a custom questionnaire class for experiment monitoring."""
    
    class ExperimentMonitoringQuestionnaire(EnhancedAnalysisQuestionnaire):
        def __init__(self):
            super().__init__()
            # Override with custom questions
            custom_set = create_experiment_monitoring_questions()
            if custom_set:
                self.questions = custom_set["questions"]
                self.selected_question_set = "experiment_monitoring"
            else:
                print("Failed to create experiment monitoring questionnaire")
                return
        
        def display_experiment_welcome(self):
            """Display experiment-specific welcome message and instructions."""
            print("=" * 80)
            print("                    EXPERIMENT MONITORING QUESTIONNAIRE")
            print("=" * 80)
            print("\nThis tool helps you set up comprehensive experiment monitoring.")
            print("Please provide detailed information about your experiment setup.")
            print("\n📅 DATE FORMAT INSTRUCTIONS:")
            print("   • Use YYYY-MM-DD format for all dates (e.g., 2024-01-15)")
            print("   • Test period: The actual duration when your experiment was running")
            print("   • Control period: The baseline period to compare against")
            print("   • Ensure control period ends before test period begins")
            print("\n📊 METRICS & ARIs:")
            print("   • Select relevant metrics that align with your experiment goals")
            print("   • Choose merchant ARIs that were part of your experiment")
            print("   • Add custom metrics or ARIs if needed")
            print("\n" + "=" * 80 + "\n")
        
        def analyze_responses(self):
            """Custom analysis for experiment monitoring."""
            print("\nAnalyzing experiment monitoring responses...\n")
            
            # Experiment Description Analysis
            experiment_desc = self.responses.get("experiment_description")
            if experiment_desc:
                self.analysis_results["experiment_analysis"] = {
                    "description": experiment_desc,
                    "description_length": len(experiment_desc),
                    "clarity_assessment": self._assess_description_clarity(experiment_desc)
                }
            
            # Merchant ARIs Analysis
            merchant_aris = self.responses.get("merchant_aris", "")
            ari_type = self.responses.get("ari_type", "")
            if merchant_aris and ari_type:
                all_aris = self._compile_all_aris(merchant_aris)
                self.analysis_results["merchant_ari_analysis"] = {
                    "ari_list": merchant_aris,
                    "ari_type": ari_type,
                    "total_aris": len(all_aris),
                    "monitoring_scope": self._assess_monitoring_scope(len(all_aris))
                }
            
            # Test Run Date Analysis
            test_start_date = self.responses.get("test_start_date", "")
            test_end_date = self.responses.get("test_end_date", "")
            if test_start_date and test_end_date:
                # Validate test period dates
                test_validation = self._validate_date_range(test_start_date, test_end_date)
                
                self.analysis_results["test_timing_analysis"] = {
                    "test_start_date": test_start_date,
                    "test_end_date": test_end_date,
                    "test_duration": self._calculate_date_duration(test_start_date, test_end_date),
                    "timing_implications": self._analyze_test_timing(test_start_date, test_end_date),
                    "date_validation": test_validation
                }
            
            # Control Period Analysis
            control_start_date = self.responses.get("control_start_date", "")
            control_end_date = self.responses.get("control_end_date", "")
            if control_start_date and control_end_date:
                # Validate control period timing relative to test period
                test_start_date = self.responses.get("test_start_date", "")
                test_end_date = self.responses.get("test_end_date", "")
                timing_validation = self._validate_experiment_timing(
                    control_start_date, control_end_date, test_start_date, test_end_date
                )
                
                self.analysis_results["control_period_analysis"] = {
                    "control_start_date": control_start_date,
                    "control_end_date": control_end_date,
                    "control_duration": self._calculate_date_duration(control_start_date, control_end_date),
                    "statistical_implications": self._analyze_control_period(control_start_date, control_end_date),
                    "timing_validation": timing_validation
                }
            
            # Metrics Analysis
            metrics = self.responses.get("metrics_to_monitor", [])
            if metrics:
                all_metrics = self._compile_all_metrics(metrics, "")
                # Check if "All metrics from above" was selected
                all_selected = "All metrics from above" in metrics
                
                self.analysis_results["metrics_analysis"] = {
                    "selected_metrics": metrics,
                    "all_metrics_selected": all_selected,
                    "compiled_metrics": all_metrics,
                    "total_metrics": len(all_metrics),
                    "metric_categories": self._categorize_metrics(all_metrics),
                    "monitoring_complexity": self._assess_monitoring_complexity(len(all_metrics)),
                    "metric_descriptions": {metric: self._get_metric_description(metric) for metric in all_metrics}
                }
            
            # Monitoring Segmentation Analysis
            segmentation = self.responses.get("monitoring_segmentation", [])
            if segmentation:
                self.analysis_results["segmentation_analysis"] = {
                    "selected_segmentation": segmentation,
                    "total_segments": len(segmentation),
                    "segmentation_complexity": self._assess_segmentation_complexity(segmentation),
                    "segmentation_implications": self._analyze_segmentation_implications(segmentation)
                }
            
            # Additional Context Analysis
            additional_context = self.responses.get("additional_context", "")
            if additional_context:
                self.analysis_results["additional_context_analysis"] = {
                    "context": additional_context,
                    "context_length": len(additional_context),
                    "context_clarity": self._assess_description_clarity(additional_context)
                }
            
            # Generate overall assessment
            self.analysis_results["overall_assessment"] = self._generate_experiment_assessment()
        
        def _assess_description_clarity(self, description: str) -> str:
            """Assess the clarity of the experiment description."""
            word_count = len(description.split())
            
            if word_count < 10:
                return "Too brief - may need more detail for clear understanding"
            elif word_count < 25:
                return "Brief but clear - provides good overview"
            elif word_count < 50:
                return "Detailed - comprehensive description"
            else:
                return "Very detailed - may be overly verbose"
        
        def _compile_all_aris(self, ari_text: str) -> List[str]:
            """Compile all merchant ARIs from text input for analysis."""
            if not ari_text:
                return []
            
            # Parse ARIs from text input (assuming comma-separated, newline-separated, or space-separated)
            # Handle various separators: commas, newlines, semicolons, or spaces
            ari_list = []
            
            # First try comma separation
            if ',' in ari_text:
                ari_list = [ari.strip() for ari in ari_text.split(',') if ari.strip()]
            # Then try newline separation
            elif '\n' in ari_text:
                ari_list = [ari.strip() for ari in ari_text.split('\n') if ari.strip()]
            # Then try semicolon separation
            elif ';' in ari_text:
                ari_list = [ari.strip() for ari in ari_text.split(';') if ari.strip()]
            # Finally, try space separation for single-line inputs
            else:
                ari_list = [ari.strip() for ari in ari_text.split() if ari.strip()]
            
            # Filter out empty strings and normalize
            return [ari for ari in ari_list if ari]
        
        def _assess_monitoring_scope(self, ari_count: int) -> str:
            """Assess the scope of monitoring based on ARI count."""
            if ari_count == 0:
                return "No ARIs selected - monitoring not possible"
            elif ari_count == 1:
                return "Single ARI - focused monitoring"
            elif ari_count <= 5:
                return "Small scope - manageable monitoring"
            elif ari_count <= 15:
                return "Medium scope - moderate complexity"
            elif ari_count <= 30:
                return "Large scope - high complexity"
            else:
                return "Very large scope - may need monitoring strategy"
        
        def _analyze_test_timing(self, test_start_date: str, test_end_date: str) -> str:
            """Analyze the implications of test timing."""
            try:
                start_date = datetime.strptime(test_start_date, "%Y-%m-%d")
                end_date = datetime.strptime(test_end_date, "%Y-%m-%d")
                today = datetime.now()
                
                # Calculate days since test ended
                days_since_end = (today - end_date).days
                
                if days_since_end <= 1:
                    return "Very recent test - excellent data freshness and relevance"
                elif days_since_end <= 7:
                    return "Recent test - good data freshness and relevance"
                elif days_since_end <= 30:
                    return "Recent test - reasonable data age, verify availability"
                elif days_since_end <= 90:
                    return "Older test - data may need validation, check availability"
                else:
                    return "Old test - significant data age, verify availability and relevance"
                    
            except ValueError:
                return "Date format error - please use YYYY-MM-DD format"
        
        def _analyze_control_period(self, control_start_date: str, control_end_date: str) -> str:
            """Analyze the statistical implications of control period."""
            try:
                start_date = datetime.strptime(control_start_date, "%Y-%m-%d")
                end_date = datetime.strptime(control_end_date, "%Y-%m-%d")
                
                # Calculate control period duration in days
                control_duration = (end_date - start_date).days
                
                if control_duration < 7:
                    return "Very short control period - may have seasonal bias, consider longer period for statistical significance"
                elif control_duration < 14:
                    return "Short control period - adequate for some metrics, consider longer period for stability"
                elif control_duration < 30:
                    return "Good control period - balances stability and relevance"
                elif control_duration < 90:
                    return "Excellent control period - good statistical stability and seasonal coverage"
                elif control_duration < 180:
                    return "Long control period - excellent stability, good seasonal coverage"
                else:
                    return "Very long control period - excellent stability, comprehensive seasonal coverage"
                    
            except ValueError:
                return "Date format error - please use YYYY-MM-DD format"
        
        def _calculate_date_duration(self, start_date: str, end_date: str) -> str:
            """Calculate the duration between two dates."""
            try:
                start = datetime.strptime(start_date, "%Y-%m-%d")
                end = datetime.strptime(end_date, "%Y-%m-%d")
                duration_days = (end - start).days
                
                if duration_days < 0:
                    return "Invalid date range (end date before start date)"
                elif duration_days == 0:
                    return "Same day"
                elif duration_days == 1:
                    return "1 day"
                elif duration_days < 7:
                    return f"{duration_days} days"
                elif duration_days < 30:
                    weeks = duration_days // 7
                    remaining_days = duration_days % 7
                    if remaining_days == 0:
                        return f"{weeks} week{'s' if weeks > 1 else ''}"
                    else:
                        return f"{weeks} week{'s' if weeks > 1 else ''} and {remaining_days} day{'s' if remaining_days > 1 else ''}"
                elif duration_days < 365:
                    months = duration_days // 30
                    remaining_days = duration_days % 30
                    if remaining_days == 0:
                        return f"{months} month{'s' if months > 1 else ''}"
                    else:
                        return f"{months} month{'s' if months > 1 else ''} and {remaining_days} day{'s' if remaining_days > 1 else ''}"
                else:
                    years = duration_days // 365
                    remaining_days = duration_days % 365
                    if remaining_days == 0:
                        return f"{years} year{'s' if years > 1 else ''}"
                    else:
                        months = remaining_days // 30
                        return f"{years} year{'s' if years > 1 else ''} and {months} month{'s' if months > 1 else ''}"
                        
            except ValueError:
                return "Date format error - please use YYYY-MM-DD format"
        
        def _validate_date_format(self, date_string: str) -> bool:
            """Validate if a string is in YYYY-MM-DD format."""
            try:
                datetime.strptime(date_string, "%Y-%m-%d")
                return True
            except ValueError:
                return False
        
        def _validate_date_range(self, start_date: str, end_date: str) -> Dict[str, Any]:
            """Validate date range (start before end, not in future, not too old)."""
            try:
                start = datetime.strptime(start_date, "%Y-%m-%d")
                end = datetime.strptime(end_date, "%Y-%m-%d")
                today = datetime.now()
                
                validation_result = {
                    "is_valid": True,
                    "warnings": [],
                    "errors": []
                }
                
                # Check if start is before end
                if start >= end:
                    validation_result["is_valid"] = False
                    validation_result["errors"].append("Start date must be before end date")
                
                # Check if dates are in the future
                if start > today:
                    validation_result["warnings"].append("Start date is in the future")
                
                if end > today:
                    validation_result["warnings"].append("End date is in the future")
                
                # Check if dates are too old (more than 5 years ago)
                five_years_ago = today.replace(year=today.year - 5)
                if start < five_years_ago:
                    validation_result["warnings"].append("Start date is more than 5 years ago")
                
                if end < five_years_ago:
                    validation_result["warnings"].append("End date is more than 5 years ago")
                
                return validation_result
                
            except ValueError:
                return {
                    "is_valid": False,
                    "warnings": [],
                    "errors": ["Invalid date format"]
                }
        

        
        def display_analysis(self):
            """Display the analysis results for experiment monitoring."""
            print(f"\n{'='*80}")
            print(f"                    EXPERIMENT MONITORING - ANALYSIS RESULTS")
            print(f"{'='*80}")
            
            # Display each analysis section
            for section, data in self.analysis_results.items():
                if section == "overall_assessment":
                    continue  # Handle this separately
                
                print(f"\n{section.replace('_', ' ').title()}:")
                print("-" * 60)
                
                if isinstance(data, dict):
                    for key, value in data.items():
                        if isinstance(value, list):
                            print(f"  {key.replace('_', ' ').title()}:")
                            for item in value:
                                print(f"    • {item}")
                        elif isinstance(value, dict):
                            print(f"  {key.replace('_', ' ').title()}:")
                            for sub_key, sub_value in value.items():
                                if isinstance(sub_value, list):
                                    print(f"    {sub_key.replace('_', ' ').title()}:")
                                    for item in sub_value:
                                        print(f"      • {item}")
                                elif isinstance(sub_value, dict) and sub_key in ["date_validation", "timing_validation"]:
                                    print(f"    {sub_key.replace('_', ' ').title()}:")
                                    validation = sub_value
                                    if validation.get("is_valid"):
                                        if sub_key == "date_validation":
                                            print(f"      ✓ Valid date range")
                                        else:
                                            print(f"      ✓ Valid timing relationship")
                                    else:
                                        if sub_key == "date_validation":
                                            print(f"      ✗ Invalid date range")
                                        else:
                                            print(f"      ✗ Invalid timing relationship")
                                    
                                    if validation.get("warnings"):
                                        print(f"      Warnings:")
                                        for warning in validation["warnings"]:
                                            print(f"        • {warning}")
                                    
                                    if validation.get("errors"):
                                        print(f"      Errors:")
                                        for error in validation["errors"]:
                                            print(f"        • {error}")
                                else:
                                    print(f"    {sub_key.replace('_', ' ').title()}: {sub_value}")
                        else:
                            print(f"  {key.replace('_', ' ').title()}: {value}")
                else:
                    print(f"  {data}")
            
            # Display overall assessment
            overall = self.analysis_results.get("overall_assessment", {})
            if overall:
                print(f"\n{'Overall Assessment':-^80}")
                print(f"Complexity Level: {overall.get('complexity_level', 'Unknown')}")
                print(f"Complexity Score: {overall.get('complexity_score', 'Unknown')}")
                print(f"Monitoring Scope: {overall.get('monitoring_scope', 'Unknown')}")
                print(f"Experiment Readiness: {overall.get('experiment_readiness', 'Unknown')}")
                
                print(f"\nKey Recommendations:")
                for rec in overall.get('key_recommendations', []):
                    print(f"  • {rec}")
        

        
        def save_results(self, filename: Optional[str] = None):
            """Save results to a JSON file (simplified version)."""
            if not filename:
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                filename = f"experiment_monitoring_{timestamp}.json"
            
            try:
                results = {
                    "timestamp": datetime.now().isoformat(),
                    "question_set": "experiment_monitoring",
                    "set_info": {
                        "name": "Experiment Monitoring Questionnaire",
                        "description": "Comprehensive experiment monitoring setup and configuration",
                        "category": "experiment"
                    },
                    "responses": self.responses,
                    "analysis": self.analysis_results
                }
                
                with open(filename, 'w') as f:
                    json.dump(results, f, indent=2)
                
                print(f"\nResults saved to: {filename}")
            except Exception as e:
                print(f"Error saving results: {e}")
        
        def conduct_questionnaire(self):
            """Conduct the experiment monitoring questionnaire with validation."""
            if not self.questions:
                print("No questions loaded. Please check questionnaire setup.")
                return
            
            print(f"\nStarting Experiment Monitoring Questionnaire...")
            print("=" * 60)
            
            for i, question in enumerate(self.questions, 1):
                print(f"\nQuestion {i} of {len(self.questions)}")
                print()
                print(question["question"])
                
                if question["required"]:
                    print("(Required)")
                else:
                    print("(Optional)")
                
                # Get validated response
                response = self._get_validated_response(question, i)
                self.responses[question["id"]] = response
                
                # Show progress
                completed = len(self.responses)
                total = len(self.questions)
                progress = (completed / total) * 100
                print(f"\nProgress: {completed}/{total} questions completed ({progress:.1f}%)")
                print()
            
            print("\n" + "=" * 60)
            print("           QUESTIONNAIRE COMPLETED!")
            print("=" * 60)
        
        def _get_validated_response(self, question: Dict[str, Any], question_number: int) -> Any:
            """Get user response with validation for date questions."""
            while True:
                # Get user input using the parent class method
                response = self.get_user_input(question)
                
                # Validate date questions
                if self._is_date_question(question):
                    validation_result = self._validate_date_input(response, question, question_number)
                    if validation_result["is_valid"]:
                        # Show warnings if any
                        if validation_result["warnings"]:
                            print("\n⚠️  Warnings:")
                            for warning in validation_result["warnings"]:
                                print(f"   • {warning}")
                        
                        # Check for timing validation if we have enough dates
                        timing_validation = self._validate_timing_relationship(question_number)
                        if timing_validation and not timing_validation["is_valid"]:
                            print("\n❌ CRITICAL TIMING ERROR:")
                            for error in timing_validation["errors"]:
                                print(f"   • {error}")
                            print("\n🚫 You cannot proceed until this timing issue is fixed.")
                            print("   The control period must end before the test period begins.")
                            print("   Please correct the dates to fix this overlap.")
                            continue
                        
                        return response
                    else:
                        print("\n❌ Validation Failed:")
                        for error in validation_result["errors"]:
                            print(f"   • {error}")
                        print("\nPlease enter a valid date in YYYY-MM-DD format.")
                        continue
                
                # For non-date questions, return immediately
                return response
        
        def _is_date_question(self, question: Dict[str, Any]) -> bool:
            """Check if a question is asking for a date."""
            date_questions = ["test_start_date", "test_end_date", "control_start_date", "control_end_date"]
            return question["id"] in date_questions
        
        def _validate_date_input(self, date_input: str, question: Dict[str, Any], question_number: int) -> Dict[str, Any]:
            """Validate a single date input."""
            # Basic format validation
            if not self._validate_date_format(date_input):
                return {
                    "is_valid": False,
                    "warnings": [],
                    "errors": ["Invalid date format. Please use YYYY-MM-DD format (e.g., 2024-01-15)"]
                }
            
            # Range validation for start/end date pairs
            if question["id"] in ["test_start_date", "control_start_date"]:
                # This is a start date, we'll validate the range when we get the end date
                return {"is_valid": True, "warnings": [], "errors": []}
            
            elif question["id"] in ["test_end_date", "control_end_date"]:
                # This is an end date, validate the range with the start date
                if question["id"] == "test_end_date":
                    start_date = self.responses.get("test_start_date", "")
                else:  # control_end_date
                    start_date = self.responses.get("control_start_date", "")
                
                if start_date:
                    range_validation = self._validate_date_range(start_date, date_input)
                    
                    # Additional validation for control_end_date to prevent overlap with test period
                    if question["id"] == "control_end_date":
                        test_start = self.responses.get("test_start_date", "")
                        if test_start:
                            try:
                                control_end_dt = datetime.strptime(date_input, "%Y-%m-%d")
                                test_start_dt = datetime.strptime(test_start, "%Y-%m-%d")
                                if control_end_dt >= test_start_dt:
                                    range_validation["is_valid"] = False
                                    range_validation["errors"].append(
                                        "Control period end date cannot be on or after test period start date"
                                    )
                            except ValueError:
                                pass
                    
                    return range_validation
                else:
                    return {"is_valid": True, "warnings": [], "errors": []}
            
            return {"is_valid": True, "warnings": [], "errors": []}
        
        def _validate_timing_relationship(self, current_question_number: int) -> Optional[Dict[str, Any]]:
            """Validate timing relationship between control and test periods."""
            # Validate as soon as we have enough information to detect overlaps
            test_start = self.responses.get("test_start_date", "")
            test_end = self.responses.get("test_end_date", "")
            control_start = self.responses.get("control_start_date", "")
            control_end = self.responses.get("control_end_date", "")
            
            # Check for overlaps as soon as we have the necessary date pairs
            if current_question_number >= 5 and test_start and test_end:
                # We have test period, check if control period overlaps
                if control_start and control_end:
                    return self._validate_experiment_timing(control_start, control_end, test_start, test_end)
                elif control_start:
                    # We have control start and test period, check if control start is after test start
                    try:
                        control_start_dt = datetime.strptime(control_start, "%Y-%m-%d")
                        test_start_dt = datetime.strptime(test_start, "%Y-%m-%d")
                        if control_start_dt >= test_start_dt:
                            return {
                                "is_valid": False,
                                "warnings": [],
                                "errors": ["Control period start date cannot be on or after test period start date"]
                            }
                    except ValueError:
                        pass
            
            return None
        
        def _validate_experiment_timing(self, control_start: str, control_end: str, test_start: str, test_end: str) -> Dict[str, Any]:
            """Validate the timing relationship between control and test periods."""
            try:
                control_start_dt = datetime.strptime(control_start, "%Y-%m-%d")
                control_end_dt = datetime.strptime(control_end, "%Y-%m-%d")
                test_start_dt = datetime.strptime(test_start, "%Y-%m-%d")
                test_end_dt = datetime.strptime(test_end, "%Y-%m-%d")
                
                validation_result = {
                    "is_valid": True,
                    "warnings": [],
                    "errors": []
                }
                
                # Check if control period ends before test period begins
                if control_end_dt >= test_start_dt:
                    validation_result["is_valid"] = False
                    validation_result["errors"].append(
                        "Control period should end before test period begins for proper baseline comparison"
                    )
                
                # Check for gaps between control and test periods
                gap_days = (test_start_dt - control_end_dt).days
                if gap_days > 30:
                    validation_result["warnings"].append(
                        f"Large gap ({gap_days} days) between control and test periods may affect comparison validity"
                    )
                elif gap_days < 0:
                    validation_result["warnings"].append(
                        "Control and test periods overlap - this may invalidate your baseline comparison"
                    )
                
                # Check if control period is too close to test period
                if 0 <= gap_days <= 7:
                    validation_result["warnings"].append(
                        "Very small gap between control and test periods - ensure no carryover effects"
                    )
                
                return validation_result
                
            except ValueError:
                return {
                    "is_valid": False,
                    "warnings": [],
                    "errors": ["Date format error - cannot validate timing relationship"]
                }
        

        
        def _compile_all_metrics(self, selected_metrics: List[str], custom_metrics: str) -> List[str]:
            """Compile all metrics for analysis."""
            all_metrics = selected_metrics.copy()
            
            # Handle "All metrics from above" selection
            if "All metrics from above" in all_metrics:
                # Remove the "All metrics from above" option
                all_metrics.remove("All metrics from above")
                # Add all individual metrics
                individual_metrics = [
                    "Authed GMV",
                    "Checkouts",
                    "E2E Conversion",
                    "AOV",
                    "Application Rate",
                    "Authentication Rate",
                    "Approval Rate",
                    "Take-up Rate",
                    "Auth Rate",
                    "Median FICO",
                    "% Prime+ Population",
                    "Median ITACS",
                    "Terms distribution",
                    "% Z-term"
                ]
                # Add individual metrics (avoiding duplicates)
                for metric in individual_metrics:
                    if metric not in all_metrics:
                        all_metrics.append(metric)
            
            # Remove any "Other" options if they exist
            
            return all_metrics
        
        def _categorize_metrics(self, metrics: List[str]) -> Dict[str, List[str]]:
            """Categorize metrics by type."""
            categories = {
                "Financial Metrics": ["Authed GMV", "AOV"],
                "Conversion Metrics": ["Checkouts", "E2E Conversion", "Application Rate", "Authentication Rate", "Approval Rate", "Take-up Rate", "Auth Rate"],
                "Credit Quality Metrics": ["Median FICO", "% Prime+ Population", "Median ITACS"],
                "Product Metrics": ["Terms distribution", "% Z-term"]
            }
            
            categorized = {}
            for category, category_metrics in categories.items():
                found_metrics = [metric for metric in metrics if metric in category_metrics]
                if found_metrics:
                    categorized[category] = found_metrics
            
            # Add uncategorized metrics
            all_categorized = [metric for metrics_list in categorized.values() for metric in metrics_list]
            uncategorized = [metric for metric in metrics if metric not in all_categorized]
            if uncategorized:
                categorized["Other/Uncategorized"] = uncategorized
            
            return categorized
        
        def _get_metric_description(self, metric: str) -> str:
            """Get description and calculation guidance for a metric."""
            descriptions = {
                "Authed GMV": "Gross Merchandise Value from authenticated users - Total transaction value after user authentication",
                "Checkouts": "Number of completed checkout processes - Count of users who reached checkout completion",
                "E2E Conversion": "End-to-end conversion rate - Users who complete the full journey from start to finish",
                "AOV": "Average Order Value - Total revenue divided by number of orders",
                "Application Rate": "Rate of users who submit applications - Applications submitted / total users",
                "Authentication Rate": "Rate of successful user authentications - Successful auths / total attempts",
                "Approval Rate": "Rate of approved applications - Approved applications / total applications",
                "Take-up Rate": "Rate of users who accept offers - Accepted offers / total offers presented",
                "Auth Rate": "Overall authentication success rate - Successful authentications / total attempts",
                "Median FICO": "Median FICO score of users - Middle value of all user FICO scores",
                "% Prime+ Population": "Percentage of users with Prime+ status - Prime+ users / total users",
                "Median ITACS": "Median ITACS score of users - Middle value of all user ITACS scores",
                "Terms distribution": "Distribution of loan terms selected - Breakdown of term lengths chosen",
                "% Z-term": "Percentage of zero-term or immediate transactions - Zero-term transactions / total transactions"
            }
            return descriptions.get(metric, "Metric description not available")
        
        def _assess_monitoring_complexity(self, metric_count: int) -> str:
            """Assess the complexity of monitoring based on metric count."""
            if metric_count == 0:
                return "No metrics selected - monitoring not possible"
            elif metric_count <= 3:
                return "Low complexity - easy to monitor and analyze"
            elif metric_count <= 7:
                return "Medium complexity - manageable monitoring"
            elif metric_count <= 12:
                return "High complexity - requires organized monitoring approach"
            else:
                return "Very high complexity - consider monitoring dashboard or tools"
        
        def _compile_all_goals(self, selected_goals: List[str], custom_goals: str) -> List[str]:
            """Compile all experiment goals for analysis."""
            all_goals = selected_goals.copy()
            
            if custom_goals and "Other" in selected_goals:
                # Parse custom goals (assuming comma-separated or newline-separated)
                custom_list = [goal.strip() for goal in custom_goals.replace('\n', ',').split(',') if goal.strip()]
                all_goals.extend(custom_list)
                # Remove the placeholder "Other" option
            
            return all_goals
        
        def _assess_goal_alignment(self, goals: List[str], metrics: List[str]) -> str:
            """Assess alignment between goals and selected metrics."""
            if not goals or not metrics:
                return "Cannot assess alignment - missing goals or metrics"
            
            # Define goal-metric mappings
            goal_metric_mapping = {
                "Increase conversion rates": ["E2E Conversion", "Application Rate", "Approval Rate", "Take-up Rate"],
                "Improve user engagement": ["Checkouts", "Authentication Rate", "Auth Rate"],
                "Reduce customer acquisition costs": ["Application Rate", "Authentication Rate"],
                "Increase average order value": ["AOV", "Authed GMV"],
                "Improve customer satisfaction": ["E2E Conversion", "Take-up Rate"],
                "Test new features or designs": ["Checkouts", "E2E Conversion", "Application Rate"],
                "Optimize pricing strategy": ["AOV", "Authed GMV", "Terms distribution", "% Z-term"],
                "Improve checkout process": ["Checkouts", "E2E Conversion", "Application Rate"],
                "Test APR/pricing changes": ["AOV", "Authed GMV", "Terms distribution", "% Z-term", "Take-up Rate"],
                "Improve credit approval rates": ["Approval Rate", "Median FICO", "% Prime+ Population", "Median ITACS"],
                "Increase loan take-up": ["Take-up Rate", "E2E Conversion", "Application Rate"],
                "Optimize risk assessment": ["Median FICO", "% Prime+ Population", "Median ITACS", "Approval Rate"]
            }
            
            # Count aligned goals
            aligned_count = 0
            for goal in goals:
                if goal in goal_metric_mapping:
                    goal_metrics = goal_metric_mapping[goal]
                    if any(metric in metrics for metric in goal_metrics):
                        aligned_count += 1
            
            alignment_percentage = (aligned_count / len(goals)) * 100
            
            if alignment_percentage >= 80:
                return f"Excellent alignment ({alignment_percentage:.0f}%) - metrics well-aligned with goals"
            elif alignment_percentage >= 60:
                return f"Good alignment ({alignment_percentage:.0f}%) - most goals have relevant metrics"
            elif alignment_percentage >= 40:
                return f"Moderate alignment ({alignment_percentage:.0f}%) - some goals lack relevant metrics"
            else:
                return f"Poor alignment ({alignment_percentage:.0f}%) - consider adding relevant metrics"
        
        def _assess_measurability(self, success_criteria: str) -> str:
            """Assess how measurable the success criteria are."""
            measurable_keywords = ["increase", "decrease", "improve", "reduce", "achieve", "reach", "maintain", "exceed"]
            percentage_keywords = ["%", "percent", "percentage"]
            number_keywords = ["number", "count", "amount", "value", "rate"]
            
            criteria_lower = success_criteria.lower()
            
            has_measurable_terms = any(keyword in criteria_lower for keyword in measurable_keywords)
            has_percentages = any(keyword in criteria_lower for keyword in percentage_keywords)
            has_numbers = any(keyword in criteria_lower for keyword in number_keywords)
            
            if has_percentages and has_measurable_terms:
                return "Highly measurable - specific percentage targets with clear direction"
            elif has_numbers and has_measurable_terms:
                return "Well measurable - specific numeric targets with clear direction"
            elif has_measurable_terms:
                return "Moderately measurable - clear direction but may need specific targets"
            else:
                return "Low measurability - consider adding specific, measurable targets"
        
        def _assess_criteria_metric_alignment(self, success_criteria: str, metrics: List[str]) -> str:
            """Assess alignment between success criteria and selected metrics."""
            if not success_criteria or not metrics:
                return "Cannot assess alignment - missing criteria or metrics"
            
            # Simple keyword matching
            criteria_lower = success_criteria.lower()
            metrics_lower = [metric.lower() for metric in metrics]
            
            # Check if criteria mention any of the selected metrics
            mentioned_metrics = [metric for metric in metrics_lower if metric in criteria_lower]
            
            if mentioned_metrics:
                return f"Good alignment - criteria mention {len(mentioned_metrics)} selected metrics"
            else:
                return "Limited alignment - consider ensuring success criteria reference selected metrics"
        
        def run_full_analysis(self):
            """Run the complete experiment monitoring analysis workflow."""
            try:
                # Display experiment-specific welcome
                self.display_experiment_welcome()
                
                # Conduct questionnaire
                self.conduct_questionnaire()
                
                # Analyze responses
                self.analyze_responses()
                
                # Display results
                self.display_analysis()
                
                # Generate and save SQL query automatically
                print("\n" + "=" * 80)
                print("                    GENERATING SQL QUERY")
                print("=" * 80)
                try:
                    sql_query = self.generate_populated_sql()
                    print("✅ SQL Query generated successfully!")
                    
                    # Auto-save SQL query with experiment description as filename
                    experiment_desc = self.responses.get("experiment_description", "experiment")
                    # Clean filename by removing special characters
                    clean_filename = "".join(c for c in experiment_desc if c.isalnum() or c in (' ', '-', '_')).rstrip()
                    sql_filename = f"{clean_filename}.sql" if clean_filename else "experiment_query.sql"
                    
                    saved_sql_file = self.save_sql_query(sql_filename)
                    print(f"✅ SQL query auto-saved to: {saved_sql_file}")
                    
                    # Automatically open in Cursor
                    print("🚀 Opening SQL file in Cursor...")
                    self.open_in_cursor(saved_sql_file)
                    
                    # Automatically execute the query
                    print("\n🔄 Executing SQL query against Snowflake...")
                    try:
                        # First, prepare the optimized SQL query
                        base_sql = self.generate_populated_sql()
                        optimized_sql = self.add_performance_optimizations(base_sql)
                        
                        # Save the optimized SQL to a file for MCP execution
                        with open("mcp_ready_query.sql", "w") as f:
                            f.write(optimized_sql)
                        
                        print("✅ SQL query prepared and optimized!")
                        print("🚀 Triggering automatic MCP execution...")
                        
                        # Use the MCP executor
                        import subprocess
                        result = subprocess.run([
                            'python3', 'mcp_executor.py', optimized_sql
                        ], capture_output=True, text=True)
                        
                        if result.returncode == 0:
                            import json
                            mcp_response = json.loads(result.stdout)
                            print(f"✅ {mcp_response.get('message', 'MCP preparation complete')}")
                            
                            # Now we'll trigger the actual execution by outputting a clear instruction
                            print("\\n" + "="*80)
                            print("                    🎯 AUTO-EXECUTION READY")
                            print("="*80)
                            print("🤖 The optimized SQL query is ready for automatic execution.")
                            print(f"📁 SQL file saved as: mcp_ready_query.sql")
                            print("\\n🔥 ASSISTANT: Please execute the SQL from mcp_ready_query.sql and provide automatic analysis!")
                            print("="*80)
                            
                        else:
                            print(f"⚠️ MCP preparation issue: {result.stderr}")
                            print("💡 Falling back to manual execution request...")
                            
                    except Exception as e:
                        print(f"❌ Error in SQL execution process: {e}")
                        print("🔍 You can still view and manually run the SQL file in Cursor.")
                    
                except Exception as e:
                    print(f"❌ Error generating SQL query: {e}")
                
                print("\nExperiment monitoring setup complete! Thank you for using the questionnaire tool.")
                
            except KeyboardInterrupt:
                print("\n\nQuestionnaire interrupted by user.")
            except Exception as e:
                print(f"\nAn error occurred: {e}")
        
        def _generate_experiment_assessment(self) -> Dict[str, Any]:
            """Generate overall experiment assessment."""
            # Calculate complexity score
            complexity_score = 0
            
            # ARI complexity
            ari_count = len(self._compile_all_aris(
                self.responses.get("merchant_aris", "")
            ))
            if ari_count > 10:
                complexity_score += 2
            elif ari_count > 5:
                complexity_score += 1
            
            # Metrics complexity
            metrics_count = len(self._compile_all_metrics(
                self.responses.get("metrics_to_monitor", []),
                ""
            ))
            if metrics_count > 10:
                complexity_score += 2
            elif metrics_count > 5:
                complexity_score += 1
            
            # Control period complexity
            control_start_date = self.responses.get("control_start_date", "")
            control_end_date = self.responses.get("control_end_date", "")
            if control_start_date and control_end_date:
                try:
                    start = datetime.strptime(control_start_date, "%Y-%m-%d")
                    end = datetime.strptime(control_end_date, "%Y-%m-%d")
                    control_duration = (end - start).days
                    if control_duration < 14:  # Short control periods add complexity
                        complexity_score += 1
                except ValueError:
                    complexity_score += 1  # Invalid dates add complexity
            
            # Determine complexity level
            if complexity_score >= 4:
                complexity_level = "High"
            elif complexity_score >= 2:
                complexity_level = "Medium"
            else:
                complexity_level = "Low"
            
            # Generate recommendations
            recommendations = []
            if complexity_level == "High":
                recommendations.extend([
                    "Consider using monitoring dashboards or tools",
                    "Implement automated reporting systems",
                    "Establish clear monitoring schedules",
                    "Consider breaking into smaller experiments"
                ])
            elif complexity_level == "Medium":
                recommendations.extend([
                    "Use organized monitoring approaches",
                    "Establish regular review cycles",
                    "Consider monitoring templates"
                ])
            else:
                recommendations.extend([
                    "Standard monitoring approach should be sufficient",
                    "Focus on data quality and consistency",
                    "Establish baseline measurements"
                ])
            
            # Add specific recommendations based on responses
            if ari_count > 10:
                recommendations.append("Large number of ARIs - consider sampling or prioritization")
            
            if metrics_count > 10:
                recommendations.append("Many metrics - consider grouping or prioritization")
            
            if not self.responses.get("additional_context"):
                recommendations.append("Provide additional context for better experiment evaluation")
            
            # Add ARI type specific recommendations
            ari_type = self.responses.get("ari_type", "")
            if ari_type == "Merchant Partner ARIs":
                recommendations.append("Partner ARIs selected - ensure proper data access and permissions")
            
            return {
                "complexity_level": complexity_level,
                "complexity_score": complexity_score,
                "monitoring_scope": "Large" if ari_count > 10 or metrics_count > 10 else "Medium" if ari_count > 5 or metrics_count > 5 else "Small",
                "key_recommendations": recommendations,
                "experiment_readiness": "Ready" if complexity_level != "High" else "Needs Planning"
            }
        
        def _assess_segmentation_complexity(self, segmentation: List[str]) -> str:
            """Assess the complexity of monitoring based on segmentation choices."""
            if "Overall" in segmentation and len(segmentation) == 1:
                return "Low complexity - overall monitoring only"
            elif len(segmentation) <= 2:
                return "Medium complexity - manageable segmentation"
            elif len(segmentation) <= 4:
                return "High complexity - consider monitoring tools and dashboards"
            else:
                return "Very high complexity - requires dedicated monitoring infrastructure"
        
        def _analyze_segmentation_implications(self, segmentation: List[str]) -> str:
            """Analyze the implications of chosen segmentation."""
            implications = []
            
            if "Overall" in segmentation:
                implications.append("Overall monitoring provides baseline performance")
            
            if "NTA vs. Repeat" in segmentation:
                implications.append("Customer type segmentation - useful for understanding new vs. existing customer behavior")
            
            if "FICO Bands" in segmentation:
                implications.append("Credit quality segmentation - important for risk assessment and approval patterns")
            
            if "AOV Bands" in segmentation:
                implications.append("Transaction value segmentation - useful for understanding spending behavior")
            
            if "ITACS Bands" in segmentation:
                implications.append("Income segmentation - important for affordability and loan sizing")
            
            if "Loan Type (IB vs. 0%)" in segmentation:
                implications.append("Product segmentation - critical for understanding product preference and performance")
            
            if len(implications) == 1:
                return implications[0]
            else:
                return "Multiple segmentation approaches: " + "; ".join(implications)
        
        def generate_populated_sql(self) -> str:
            """Generate a populated SQL query based on questionnaire responses."""
            if not self.responses:
                raise ValueError("No responses available. Please complete the questionnaire first.")
            
            # Extract key parameters from responses
            merchant_aris = self.responses.get("merchant_aris", "")
            ari_type = self.responses.get("ari_type", "")
            test_start_date = self.responses.get("test_start_date", "")
            test_end_date = self.responses.get("test_end_date", "")
            control_start_date = self.responses.get("control_start_date", "")
            control_end_date = self.responses.get("control_end_date", "")
            
            # Parse merchant ARIs into list format
            if merchant_aris:
                ari_list = [ari.strip() for ari in merchant_aris.split(',')]
                ari_list_str = "', '".join(ari_list)
            else:
                ari_list_str = ""
            
            # Determine the WHERE clause based on ARI type
            if ari_type == "Merchant ARIs":
                where_clause = f"md.merchant_ari IN ('{ari_list_str}')"
            elif ari_type == "Merchant Partner ARIs":
                where_clause = f"md.merchant_partner_ari IN ('{ari_list_str}')"
            else:
                where_clause = f"md.merchant_ari IN ('{ari_list_str}') OR md.merchant_partner_ari IN ('{ari_list_str}')"
            
            # Generate the SQL query
            sql_query = f"""SELECT
-- Generated from questionnaire responses --
-- Experiment: {self.responses.get('experiment_description', 'N/A')}
-- Control Period: {control_start_date} to {control_end_date}
-- Test Period: {test_start_date} to {test_end_date}

CASE 
    WHEN to_date(cfv5.CHECKOUT_CREATED_DT) BETWEEN '{control_start_date}' AND '{control_end_date}' THEN 'Pre'
    WHEN to_date(cfv5.CHECKOUT_CREATED_DT) BETWEEN '{test_start_date}' AND '{test_end_date}' THEN 'Post'
    ELSE 'Other'
END AS analysis_period

, CASE WHEN cfv5.USER_ARI IS NULL THEN 'UNKNOWN'
    WHEN cfv5.USER_ARI IS NOT NULL THEN 'EXISTING'
    ELSE 'OTHER' END AS user_status
    
, CASE 
  WHEN cfv5.TOTAL_AMOUNT < 100 THEN '1|<$100'
  WHEN cfv5.TOTAL_AMOUNT >= 100 AND cfv5.TOTAL_AMOUNT < 250 THEN '2|$100-250'
  WHEN cfv5.TOTAL_AMOUNT >= 250 AND cfv5.TOTAL_AMOUNT < 500 THEN '3|$250-500'
  WHEN cfv5.TOTAL_AMOUNT >= 500 AND cfv5.TOTAL_AMOUNT < 1000 THEN '4|$500-1000'
  WHEN cfv5.TOTAL_AMOUNT >= 1000 THEN '5|$1000+'
  ELSE '6|Other'
END AS AOV_bucket

, CASE
        WHEN cfv5.ITACS_V1 >= 98 then '1: 98+'
        WHEN cfv5.ITACS_V1 >= 96 then '2: 96+'
        WHEN cfv5.ITACS_V1 >= 95 then '3: 95-96'
        WHEN cfv5.ITACS_V1 >= 94 then '4: 94-95'
        WHEN cfv5.ITACS_V1 IS NOT NULL AND cfv5.ITACS_V1 < 94 THEN '5: < 94'
        ELSE 'Unknown'
    END as itacs_bucket

, CASE WHEN cfv5.LOAN_TYPE = 'affirm_go_v3' THEN 'Split Pay'
  ELSE 'IB' END as loan_type_checkout
 
, count(distinct cfv5.CHECKOUT_ARI) as checkouts
, count(distinct case when cfv5.IS_LOGIN_AUTHENTICATED = 1 then cfv5.CHECKOUT_ARI end) as authenticated
, count(distinct case when cfv5.IS_IDENTITY_APPROVED = 1 then cfv5.CHECKOUT_ARI end) as identity_approved 
, count(distinct case when cfv5.IS_FRAUD_APPROVED = 1 then cfv5.CHECKOUT_ARI end) as fraud_approved 
, count(distinct case when cfv5.IS_CHECKOUT_APPLIED = 1 then cfv5.CHECKOUT_ARI end) as applied
, count(distinct case when cfv5.IS_APPROVED = 1 then cfv5.CHECKOUT_ARI end) as approved_checkouts 
, count(distinct case when cfv5.IS_CONFIRMED = 1 then cfv5.CHECKOUT_ARI end) as confirmed_checkouts
, count(distinct case when cfv5.IS_AUTHED = 1 then cfv5.CHECKOUT_ARI end) as authed_checkouts
, sum(case when cfv5.IS_AUTHED = 1 then cfv5.TOTAL_AMOUNT end) as GMV
, COALESCE(authenticated,0) / NULLIF(checkouts,0) as authentication_rate
, COALESCE(identity_approved,0) / NULLIF(authenticated,0) as identity_approval_rate
, COALESCE(fraud_approved,0) / NULLIF(authenticated,0) as fraud_approval_rate
, COALESCE(applied,0) / NULLIF(checkouts,0) as application_rate
, COALESCE(approved_checkouts,0) / NULLIF(applied,0) as credit_approval_rate
, COALESCE(confirmed_checkouts,0) / NULLIF(approved_checkouts,0) as confirmation_rate
, COALESCE(authed_checkouts,0) / NULLIF(confirmed_checkouts,0) as authorization_rate
, COALESCE(authed_checkouts,0) / NULLIF(checkouts,0) as E2E
, COALESCE(SUM(CASE WHEN cfv5.IS_AUTHED = 1 THEN cfv5.TOTAL_AMOUNT END),0)/ NULLIF(authed_checkouts,0) as AOV

from prod__us.dbt_analytics.checkout_funnel_v5 cfv5
left join prod__us.dbt_analytics.merchant_dim md on md.merchant_ari = cfv5.MERCHANT_ARI

-- Filter based on questionnaire responses --
WHERE {where_clause}

group by all
"""
            
            return sql_query
        
        def save_sql_query(self, filename: str = None) -> str:
            """Save the generated SQL query to a file."""
            if not filename:
                from datetime import datetime
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                filename = f"experiment_query_{timestamp}.sql"
            
            try:
                sql_content = self.generate_populated_sql()
                with open(filename, 'w') as f:
                    f.write(sql_content)
                return filename
            except Exception as e:
                raise Exception(f"Failed to save SQL query: {e}")
        
        def open_in_cursor(self, filename: str):
            """Open the SQL file in Cursor IDE."""
            try:
                import subprocess
                import os
                
                # Try different methods to open in Cursor
                cursor_commands = ["cursor", "code"]
                
                for cmd in cursor_commands:
                    try:
                        # Try to open with the command
                        result = subprocess.run([cmd, filename], 
                                              capture_output=True, 
                                              text=True, 
                                              timeout=5)
                        if result.returncode == 0:
                            print(f"✅ Opened {filename} in Cursor using '{cmd}' command")
                            return
                    except (subprocess.TimeoutExpired, FileNotFoundError):
                        continue
                
                # If commands don't work, try macOS open command with Cursor app
                try:
                    result = subprocess.run(["open", "-a", "Cursor", filename],
                                          capture_output=True,
                                          text=True,
                                          timeout=5)
                    if result.returncode == 0:
                        print(f"✅ Opened {filename} in Cursor using macOS open command")
                        return
                except (subprocess.TimeoutExpired, FileNotFoundError):
                    pass
                
                # Fallback: just print the location
                abs_path = os.path.abspath(filename)
                print(f"📁 SQL file saved at: {abs_path}")
                print("💡 Please manually open this file in Cursor")
                
            except Exception as e:
                print(f"⚠️ Could not auto-open in Cursor: {e}")
                print(f"📁 SQL file location: {os.path.abspath(filename) if os.path.exists(filename) else filename}")
        
        def execute_sql_query_optimized(self) -> dict:
            """Execute the generated SQL query with optimizations for better performance."""
            try:
                # First, let's try to import the Snowflake connector
                try:
                    from snowflake.connector import connect
                    print("🔗 Using Snowflake connector...")
                except ImportError:
                    # If Snowflake connector not available, try MCP Snowflake
                    print("🔗 Snowflake connector not found, trying MCP interface...")
                    return self.execute_sql_via_mcp()
                
                # Get connection parameters from environment
                account = os.environ.get('SNOWFLAKE_ACCOUNT')
                user = os.environ.get('SNOWFLAKE_USER')
                authenticator = os.environ.get('SNOWFLAKE_AUTHENTICATOR', 'externalbrowser')
                warehouse = os.environ.get('SNOWFLAKE_WAREHOUSE', 'COMPUTE_WH')
                database = os.environ.get('SNOWFLAKE_DATABASE', 'PROD__US')
                schema = os.environ.get('SNOWFLAKE_SCHEMA', 'DBT_ANALYTICS')
                
                if not all([account, user]):
                    print("⚠️ Snowflake credentials not found in environment, trying MCP interface...")
                    return self.execute_sql_via_mcp()
                
                # Connect to Snowflake
                conn = connect(
                    account=account,
                    user=user,
                    authenticator=authenticator,
                    warehouse=warehouse,
                    database=database,
                    schema=schema
                )
                
                # Generate optimized SQL query
                base_sql = self.generate_populated_sql()
                optimized_sql = self.add_performance_optimizations(base_sql)
                
                cursor = conn.cursor()
                
                # Ensure warehouse is active
                cursor.execute(f"USE WAREHOUSE {warehouse}")
                cursor.execute(f"USE DATABASE {database}")
                cursor.execute(f"USE SCHEMA {schema}")
                
                cursor.execute(optimized_sql)
                
                # Fetch results
                results = cursor.fetchall()
                column_names = [desc[0] for desc in cursor.description]
                
                # Convert to list of dictionaries
                data = []
                for row in results:
                    data.append(dict(zip(column_names, row)))
                
                cursor.close()
                conn.close()
                
                return {
                    'success': True,
                    'data': data,
                    'row_count': len(data),
                    'columns': column_names,
                    'sql_query': optimized_sql
                }
                
            except Exception as e:
                print(f"⚠️ Direct Snowflake connection failed: {e}")
                print("🔗 Trying MCP interface...")
                return self.execute_sql_via_mcp()
        
        def execute_sql_via_mcp(self) -> dict:
            """Execute SQL via MCP Snowflake interface (fallback method)."""
            try:
                import subprocess
                import json
                import tempfile
                
                base_sql = self.generate_populated_sql()
                optimized_sql = self.add_performance_optimizations(base_sql)
                
                print("🔧 Using optimized SQL query via MCP interface...")
                
                # Create a temporary Python script to execute the MCP call
                mcp_script = '''
import subprocess
import sys
import json

def execute_sql_via_mcp(sql_query):
    """Execute SQL using MCP Snowflake interface."""
    try:
        # This will be handled by the parent process that has MCP access
        # For now, we'll return a structured response that can be processed
        return {
            "success": True,
            "needs_mcp_execution": True,
            "sql_query": sql_query,
            "message": "SQL ready for MCP execution"
        }
    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }

if __name__ == "__main__":
    sql = sys.argv[1] if len(sys.argv) > 1 else ""
    result = execute_sql_via_mcp(sql)
    print(json.dumps(result))
'''
                
                # Write the script to a temporary file
                with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as f:
                    f.write(mcp_script)
                    script_path = f.name
                
                # Execute the script
                result = subprocess.run([
                    'python3', script_path, optimized_sql
                ], capture_output=True, text=True)
                
                if result.returncode == 0:
                    response = json.loads(result.stdout.strip())
                    if response.get('needs_mcp_execution'):
                        # Signal that we need MCP execution
                        print("✅ SQL query prepared for MCP execution...")
                        return {
                            'success': True,
                            'needs_mcp_execution': True,
                            'sql_query': optimized_sql,
                            'message': 'SQL query ready for execution'
                        }
                    else:
                        return response
                else:
                    return {
                        'success': False,
                        'error': f'MCP script execution failed: {result.stderr}',
                        'sql_query': optimized_sql
                    }
                
            except Exception as e:
                return {
                    'success': False,
                    'error': f'Failed to execute via MCP: {str(e)}',
                    'sql_query': None
                }
        
        def add_performance_optimizations(self, base_sql: str) -> str:
            """Add performance optimizations to the base SQL query."""
            # Extract date ranges and merchant info from responses
            control_start = self.responses.get("control_start_date", "")
            control_end = self.responses.get("control_end_date", "")
            test_start = self.responses.get("test_start_date", "")
            test_end = self.responses.get("test_end_date", "")
            merchant_aris = self.responses.get("merchant_aris", "")
            ari_type = self.responses.get("ari_type", "")
            
            # Parse merchant ARIs
            if merchant_aris:
                ari_list = [ari.strip() for ari in merchant_aris.split(',')]
                ari_list_str = "', '".join(ari_list)
            else:
                ari_list_str = ""
            
            # Create optimized WHERE clause with date filtering
            date_filter = f"""
  AND (
    to_date(cfv5.CHECKOUT_CREATED_DT) BETWEEN '{control_start}' AND '{control_end}'
    OR to_date(cfv5.CHECKOUT_CREATED_DT) BETWEEN '{test_start}' AND '{test_end}'
  )"""
            
            # Add the date filter to the WHERE clause
            if "WHERE" in base_sql:
                optimized_sql = base_sql.replace("group by all", date_filter + "\n\ngroup by 1, 2, 3, 4, 5\nORDER BY analysis_period, user_status, AOV_bucket, itacs_bucket, loan_type_checkout")
            else:
                # Add WHERE clause if it doesn't exist
                optimized_sql = base_sql.replace("group by all", f"WHERE TRUE{date_filter}\n\ngroup by 1, 2, 3, 4, 5\nORDER BY analysis_period, user_status, AOV_bucket, itacs_bucket, loan_type_checkout")
            
            return optimized_sql
        
        def test_snowflake_connection(self) -> dict:
            """Test Snowflake connection and list available tables."""
            try:
                import snowflake.connector
                from snowflake.connector import connect
                
                # Get connection parameters from environment or config
                account = os.environ.get('SNOWFLAKE_ACCOUNT')
                user = os.environ.get('SNOWFLAKE_USER')
                authenticator = os.environ.get('SNOWFLAKE_AUTHENTICATOR', 'externalbrowser')
                warehouse = os.environ.get('SNOWFLAKE_WAREHOUSE', 'COMPUTE_WH')
                database = os.environ.get('SNOWFLAKE_DATABASE', 'PROD__US')
                schema = os.environ.get('SNOWFLAKE_SCHEMA', 'DBT_ANALYTICS')
                
                if not all([account, user]):
                    raise Exception("Snowflake connection parameters not found. Please set SNOWFLAKE_ACCOUNT and SNOWFLAKE_USER environment variables.")
                
                # Connect to Snowflake
                conn = connect(
                    account=account,
                    user=user,
                    authenticator=authenticator,
                    warehouse=warehouse,
                    database=database,
                    schema=schema
                )
                
                cursor = conn.cursor()
                
                # Ensure warehouse is active
                cursor.execute(f"USE WAREHOUSE {warehouse}")
                cursor.execute(f"USE DATABASE {database}")
                cursor.execute(f"USE SCHEMA {schema}")
                
                # Test simple query to verify connection
                cursor.execute("SELECT CURRENT_DATABASE(), CURRENT_SCHEMA(), CURRENT_WAREHOUSE()")
                connection_info = cursor.fetchone()
                
                # List available tables in the schema
                cursor.execute(f"SHOW TABLES IN {database}.{schema}")
                tables = cursor.fetchall()
                
                cursor.close()
                conn.close()
                
                return {
                    'success': True,
                    'connection_info': {
                        'database': connection_info[0],
                        'schema': connection_info[1],
                        'warehouse': connection_info[2]
                    },
                    'available_tables': [table[1] for table in tables] if tables else []
                }
                
            except ImportError:
                return {
                    'success': False,
                    'error': 'Snowflake connector not installed. Please install with: pip install snowflake-connector-python'
                }
            except Exception as e:
                return {
                    'success': False,
                    'error': f'Failed to test Snowflake connection: {str(e)}'
                }
        
        def execute_sql_query(self) -> dict:
            """Execute the generated SQL query against Snowflake and return results."""
            try:
                import snowflake.connector
                from snowflake.connector import connect
                
                # Get connection parameters from environment or config
                account = os.environ.get('SNOWFLAKE_ACCOUNT')
                user = os.environ.get('SNOWFLAKE_USER')
                authenticator = os.environ.get('SNOWFLAKE_AUTHENTICATOR', 'externalbrowser')
                warehouse = os.environ.get('SNOWFLAKE_WAREHOUSE', 'COMPUTE_WH')
                database = os.environ.get('SNOWFLAKE_DATABASE', 'PROD__US')
                schema = os.environ.get('SNOWFLAKE_SCHEMA', 'DBT_ANALYTICS')
                
                if not all([account, user]):
                    raise Exception("Snowflake connection parameters not found. Please set SNOWFLAKE_ACCOUNT and SNOWFLAKE_USER environment variables.")
                
                # Connect to Snowflake
                conn = connect(
                    account=account,
                    user=user,
                    authenticator=authenticator,
                    warehouse=warehouse,
                    database=database,
                    schema=schema
                )
                
                # Execute the query
                sql_query = self.generate_populated_sql()
                cursor = conn.cursor()
                
                # Ensure warehouse is active
                cursor.execute(f"USE WAREHOUSE {warehouse}")
                cursor.execute(f"USE DATABASE {database}")
                cursor.execute(f"USE SCHEMA {schema}")
                
                cursor.execute(sql_query)
                
                # Fetch results
                results = cursor.fetchall()
                column_names = [desc[0] for desc in cursor.description]
                
                # Convert to list of dictionaries
                data = []
                for row in results:
                    data.append(dict(zip(column_names, row)))
                
                cursor.close()
                conn.close()
                
                return {
                    'success': True,
                    'data': data,
                    'row_count': len(data),
                    'columns': column_names,
                    'sql_query': sql_query
                }
                
            except ImportError:
                return {
                    'success': False,
                    'error': 'Snowflake connector not installed. Please install with: pip install snowflake-connector-python'
                }
            except Exception as e:
                return {
                    'success': False,
                    'error': f'Failed to execute SQL query: {str(e)}'
                }
        
        def analyze_experiment_results(self, results: dict) -> dict:
            """Analyze the experiment results from SQL execution."""
            if not results.get('success'):
                return {'error': results.get('error', 'Unknown error')}
            
            data = results['data']
            if not data:
                return {'warning': 'No data returned from query'}
            
            # Debug: Print the first few rows to see the data structure
            print(f"\n🔍 DEBUG: Data structure analysis")
            print(f"📊 Total rows: {len(data)}")
            if data:
                print(f"📋 Sample row keys: {list(data[0].keys())}")
                print(f"📋 Sample row values: {data[0]}")
            
            analysis = {
                'summary_stats': {},
                'control_vs_test': {},
                'key_insights': [],
                'recommendations': []
            }
            
            # Separate control and test data
            control_data = [row for row in data if row.get('ANALYSIS_PERIOD') == 'Pre']
            test_data = [row for row in data if row.get('ANALYSIS_PERIOD') == 'Post']
            
            print(f"🔍 DEBUG: Control data rows: {len(control_data)}, Test data rows: {len(test_data)}")
            if control_data:
                print(f"🔍 DEBUG: Control data sample: {control_data[0]}")
            if test_data:
                print(f"🔍 DEBUG: Test data sample: {test_data[0]}")
            
            # Calculate summary statistics
            if control_data:
                analysis['summary_stats']['control'] = {
                    'total_checkouts': sum(row.get('CHECKOUTS', 0) or 0 for row in control_data),
                    'total_gmv': sum(row.get('GMV', 0) or 0 for row in control_data),
                    'avg_e2e_rate': sum(row.get('E2E', 0) or 0 for row in control_data) / len(control_data) if control_data else 0,
                    'avg_aov': sum(row.get('AOV', 0) or 0 for row in control_data) / len(control_data) if control_data else 0
                }
            
            if test_data:
                analysis['summary_stats']['test'] = {
                    'total_checkouts': sum(row.get('CHECKOUTS', 0) or 0 for row in test_data),
                    'total_gmv': sum(row.get('GMV', 0) or 0 for row in test_data),
                    'avg_e2e_rate': sum(row.get('E2E', 0) or 0 for row in test_data) / len(test_data) if test_data else 0,
                    'avg_aov': sum(row.get('AOV', 0) or 0 for row in test_data) / len(test_data) if test_data else 0
                }
            
            # Calculate control vs test comparisons
            if control_data and test_data:
                control_stats = analysis['summary_stats']['control']
                test_stats = analysis['summary_stats']['test']
                
                # Calculate percentage changes
                checkout_change = ((test_stats['total_checkouts'] - control_stats['total_checkouts']) / control_stats['total_checkouts'] * 100) if control_stats['total_checkouts'] > 0 else 0
                gmv_change = ((test_stats['total_gmv'] - control_stats['total_gmv']) / control_stats['total_gmv'] * 100) if control_stats['total_gmv'] > 0 else 0
                e2e_change = ((test_stats['avg_e2e_rate'] - control_stats['avg_e2e_rate']) / control_stats['avg_e2e_rate'] * 100) if control_stats['avg_e2e_rate'] > 0 else 0
                aov_change = ((test_stats['avg_aov'] - control_stats['avg_aov']) / control_stats['avg_aov'] * 100) if control_stats['avg_aov'] > 0 else 0
                
                analysis['control_vs_test'] = {
                    'checkout_change_pct': round(checkout_change, 2),
                    'gmv_change_pct': round(gmv_change, 2),
                    'e2e_change_pct': round(e2e_change, 2),
                    'aov_change_pct': round(aov_change, 2)
                }
                
                # Generate insights
                if checkout_change > 5:
                    analysis['key_insights'].append(f"✅ Checkouts increased by {checkout_change:.1f}% during test period")
                elif checkout_change < -5:
                    analysis['key_insights'].append(f"⚠️ Checkouts decreased by {abs(checkout_change):.1f}% during test period")
                
                if gmv_change > 5:
                    analysis['key_insights'].append(f"✅ GMV increased by {gmv_change:.1f}% during test period")
                elif gmv_change < -5:
                    analysis['key_insights'].append(f"⚠️ GMV decreased by {abs(gmv_change):.1f}% during test period")
                
                if e2e_change > 5:
                    analysis['key_insights'].append(f"✅ E2E conversion improved by {e2e_change:.1f}% during test period")
                elif e2e_change < -5:
                    analysis['key_insights'].append(f"⚠️ E2E conversion declined by {abs(e2e_change):.1f}% during test period")
                
                # Generate recommendations
                if gmv_change > 10 and e2e_change > 5:
                    analysis['recommendations'].append("🎯 Strong positive results! Consider expanding the experiment")
                elif gmv_change < -5 or e2e_change < -5:
                    analysis['recommendations'].append("⚠️ Negative impact detected. Consider stopping the experiment")
                else:
                    analysis['recommendations'].append("📊 Mixed results. Continue monitoring and consider adjustments")
            
            return analysis
        
        def display_experiment_results(self, results: dict, analysis: dict):
            """Display the experiment results and analysis."""
            print("\n" + "=" * 80)
            print("                    EXPERIMENT RESULTS ANALYSIS")
            print("=" * 80)
            
            if 'error' in results:
                print(f"❌ Error: {results['error']}")
                return
            
            if 'warning' in analysis:
                print(f"⚠️ Warning: {analysis['warning']}")
                return
            
            print(f"📊 Data Retrieved: {results['row_count']} rows")
            print(f"📋 Columns: {', '.join(results['columns'])}")
            
            if 'summary_stats' in analysis:
                print("\n📈 SUMMARY STATISTICS:")
                print("-" * 50)
                
                if 'control' in analysis['summary_stats']:
                    control = analysis['summary_stats']['control']
                    print("Control Period (Pre):")
                    print(f"  • Total Checkouts: {control['total_checkouts']:,}")
                    print(f"  • Total GMV: ${control['total_gmv']:,.2f}")
                    print(f"  • Avg E2E Rate: {control['avg_e2e_rate']:.3f}")
                    print(f"  • Avg AOV: ${control['avg_aov']:.2f}")
                
                if 'test' in analysis['summary_stats']:
                    test = analysis['summary_stats']['test']
                    print("\nTest Period (Post):")
                    print(f"  • Total Checkouts: {test['total_checkouts']:,}")
                    print(f"  • Total GMV: ${test['total_gmv']:,.2f}")
                    print(f"  • Avg E2E Rate: {test['avg_e2e_rate']:.3f}")
                    print(f"  • Avg AOV: ${test['avg_aov']:.2f}")
            
            if 'control_vs_test' in analysis:
                print("\n🔄 CONTROL VS TEST COMPARISON:")
                print("-" * 50)
                comp = analysis['control_vs_test']
                print(f"  • Checkout Change: {comp['checkout_change_pct']:+.1f}%")
                print(f"  • GMV Change: {comp['gmv_change_pct']:+.1f}%")
                print(f"  • E2E Conversion Change: {comp['e2e_change_pct']:+.1f}%")
                print(f"  • AOV Change: {comp['aov_change_pct']:+.1f}%")
            
            if 'key_insights' in analysis:
                print("\n💡 KEY INSIGHTS:")
                print("-" * 50)
                for insight in analysis['key_insights']:
                    print(f"  {insight}")
            
            if 'recommendations' in analysis:
                print("\n🎯 RECOMMENDATIONS:")
                print("-" * 50)
                for rec in analysis['recommendations']:
                    print(f"  {rec}")
            
            print("\n" + "=" * 80)
     
    return ExperimentMonitoringQuestionnaire

def run_experiment_questionnaire():
    """Run the experiment monitoring questionnaire."""
    print("Creating experiment monitoring questionnaire...")
    
    # Create custom questionnaire class
    CustomQuestionnaire = create_experiment_questionnaire_class()
    
    if CustomQuestionnaire:
        # Create and run questionnaire
        questionnaire = CustomQuestionnaire()
        questionnaire.run_full_analysis()
    else:
        print("Failed to create experiment monitoring questionnaire")

if __name__ == "__main__":
    run_experiment_questionnaire()
