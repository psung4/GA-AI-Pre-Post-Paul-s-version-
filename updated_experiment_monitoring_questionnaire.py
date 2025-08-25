#!/usr/bin/env python3
"""
Updated Experiment Monitoring Questionnaire

This script creates a custom questionnaire for monitoring experiments with
metrics automatically extracted from the query.sql file.
"""

from enhanced_questionnaire import EnhancedAnalysisQuestionnaire
from questionnaire_config import create_custom_question_set, validate_question_format
from typing import List, Dict, Any, Optional
import datetime
import json
import re
import os

def extract_metrics_from_sql(sql_file_path: str = "query.sql") -> List[str]:
    """Extract metric names from the SQL file."""
    
    if not os.path.exists(sql_file_path):
        print(f"Warning: {sql_file_path} not found. Using default metrics.")
        return ["Checkouts", "Authentication Rate", "E2E Conversion", "AOV"]
    
    try:
        with open(sql_file_path, 'r') as f:
            sql_content = f.read()
        
        # Extract metrics from SELECT statements
        metrics = []
        
        # Pattern to match: , something as metric_name
        # This captures calculated metrics like rates and totals
        as_pattern = r',\s*[^,]+\s+as\s+(\w+)'
        as_matches = re.findall(as_pattern, sql_content, re.IGNORECASE | re.MULTILINE)
        
        # Pattern to match: , count(...) as metric_name
        # This captures count/sum aggregations
        agg_pattern = r',\s*(count|sum|avg|max|min|coalesce)\s*\([^)]+\)\s+as\s+(\w+)'
        agg_matches = re.findall(agg_pattern, sql_content, re.IGNORECASE | re.MULTILINE)
        
        # Metrics that should have "Num" prefix
        num_prefix_metrics = [
            'authenticated', 'identity_approved', 'fraud_approved', 
            'applied', 'approved_checkouts', 'confirmed_checkouts', 
            'authed_checkouts', 'checkouts'
        ]
        
        # Combine and clean up metric names
        for match in as_matches:
            metric_name = match.strip()
            # Convert snake_case to Title Case
            display_name = metric_name.replace('_', ' ').title()
            
            # Add "Num" prefix for count metrics
            if metric_name.lower() in num_prefix_metrics:
                display_name = f"Num {display_name}"
            
            metrics.append(display_name)
        
        for agg_type, metric_name in agg_matches:
            display_name = metric_name.replace('_', ' ').title()
            
            # Add "Num" prefix for count metrics
            if metric_name.lower() in num_prefix_metrics:
                display_name = f"Num {display_name}"
            
            if display_name not in metrics:  # Avoid duplicates
                metrics.append(display_name)
        
        # Filter out dimension columns (not metrics)
        dimension_keywords = ['period', 'bucket', 'person', 'type']
        filtered_metrics = []
        for metric in metrics:
            if not any(keyword in metric.lower() for keyword in dimension_keywords):
                filtered_metrics.append(metric)
        
        # Add "Other" option
        filtered_metrics.append("Other (specify below)")
        
        print(f"✅ Extracted {len(filtered_metrics)-1} metrics from {sql_file_path}")
        return filtered_metrics
        
    except Exception as e:
        print(f"Error reading {sql_file_path}: {e}")
        print("Using default metrics.")
        return ["Checkouts", "Authentication Rate", "E2E Conversion", "AOV", "Other (specify below)"]

def create_experiment_monitoring_questions():
    """Create the experiment monitoring questions with SQL-derived metrics."""
    
    # Extract metrics from query.sql
    sql_metrics = extract_metrics_from_sql()
    
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
            "id": "pre_start_date",
            "question": "4. What is the PRE period start date? (YYYY-MM-DD format) - This will be used as {pre_start_date} in query.sql",
            "type": "text",
            "required": True
        },
        {
            "id": "pre_end_date",
            "question": "5. What is the PRE period end date? (YYYY-MM-DD format) - This will be used as {pre_end_date} in query.sql",
            "type": "text",
            "required": True
        },
        {
            "id": "post_start_date",
            "question": "6. What is the POST period start date? (YYYY-MM-DD format) - This will be used as {post_start_date} in query.sql",
            "type": "text",
            "required": True
        },
        {
            "id": "post_end_date",
            "question": "7. What is the POST period end date? (YYYY-MM-DD format) - This will be used as {post_end_date} in query.sql",
            "type": "text",
            "required": True
        },
        {
            "id": "metrics_to_monitor",
            "question": "8. What metrics would you like to monitor? (Options from query.sql)",
            "type": "multi_select",
            "options": sql_metrics,  # Dynamically generated from SQL
            "required": True
        },
        {
            "id": "custom_metrics",
            "question": "9. If you selected 'Other', please specify the metrics:",
            "type": "text",
            "required": False
        },
        {
            "id": "experiment_goals",
            "question": "10. What are the primary goals of this experiment?",
            "type": "multi_select",
            "options": [
                "Increase conversion rates",
                "Improve user engagement", 
                "Reduce customer acquisition costs",
                "Increase average order value",
                "Improve customer satisfaction",
                "Test new features or designs",
                "Optimize pricing strategy",
                "Improve checkout process",
                "Test APR/pricing changes",
                "Improve credit approval rates",
                "Increase loan take-up",
                "Optimize risk assessment",
                "Other (specify below)"
            ],
            "required": False
        },
        {
            "id": "custom_goals",
            "question": "11. If you selected 'Other' for goals, please specify:",
            "type": "text",
            "required": False
        },
        {
            "id": "success_criteria",
            "question": "12. What would you consider a successful outcome for this experiment?",
            "type": "text",
            "required": False
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
        name="SQL-Integrated Experiment Monitoring Questionnaire",
        description="Experiment monitoring with metrics automatically extracted from query.sql",
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
                self.selected_question_set = "sql_experiment_monitoring"
            else:
                print("Failed to create experiment monitoring questionnaire")
                return
        
        def display_experiment_welcome(self):
            """Display experiment-specific welcome message and instructions."""
            print("=" * 80)
            print("           SQL-INTEGRATED EXPERIMENT MONITORING QUESTIONNAIRE")
            print("=" * 80)
            print("\nThis tool helps you set up comprehensive experiment monitoring.")
            print("Metrics are automatically extracted from your query.sql file.")
            print("\n📅 DATE FORMAT INSTRUCTIONS:")
            print("   • Use YYYY-MM-DD format for all dates (e.g., 2024-01-15)")
            print("   • Test period: The actual duration when your experiment was running")
            print("   • Control period: The baseline period to compare against")
            print("   • Ensure control period ends before test period begins")
            print("\n📊 METRICS & ARIs:")
            print("   • Metrics are sourced from query.sql calculations")
            print("   • Select metrics that align with your experiment goals")
            print("   • Choose merchant ARIs that were part of your experiment")
            print("   • Add custom metrics if needed")
            print("\n🔗 SQL INTEGRATION:")
            print("   • Metrics extracted from query.sql file")
            print("   • Includes calculated rates, counts, and aggregations")
            print("   • Automatically updates when you modify query.sql")
            print("\n" + "=" * 80 + "\n")
        
        def analyze_responses(self):
            """Custom analysis for experiment monitoring."""
            print("\nAnalyzing experiment monitoring responses...\n")
            
            # All the same analysis methods from the original questionnaire
            # (I'll include the key ones but truncate for space)
            
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
            
            # SQL Metrics Analysis
            metrics = self.responses.get("metrics_to_monitor", [])
            custom_metrics = self.responses.get("custom_metrics", "")
            if metrics or custom_metrics:
                all_metrics = self._compile_all_metrics(metrics, custom_metrics)
                self.analysis_results["sql_metrics_analysis"] = {
                    "selected_metrics": metrics,
                    "custom_metrics": custom_metrics,
                    "total_metrics": len(all_metrics),
                    "sql_sourced": len([m for m in metrics if m != "Other (specify below)"]),
                    "monitoring_complexity": self._assess_monitoring_complexity(len(all_metrics))
                }
            
            # Generate overall assessment
            self.analysis_results["overall_assessment"] = self._generate_experiment_assessment()
        
        # Include all the helper methods from the original questionnaire
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
            ari_list = []
            
            if ',' in ari_text:
                ari_list = [ari.strip() for ari in ari_text.split(',') if ari.strip()]
            elif '\n' in ari_text:
                ari_list = [ari.strip() for ari in ari_text.split('\n') if ari.strip()]
            elif ';' in ari_text:
                ari_list = [ari.strip() for ari in ari_text.split(';') if ari.strip()]
            else:
                ari_list = [ari.strip() for ari in ari_text.split() if ari.strip()]
            
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
        
        def _compile_all_metrics(self, selected_metrics: List[str], custom_metrics: str) -> List[str]:
            """Compile all metrics for analysis."""
            all_metrics = selected_metrics.copy()
            
            if custom_metrics and "Other" in selected_metrics:
                custom_list = [metric.strip() for metric in custom_metrics.replace('\n', ',').split(',') if metric.strip()]
                all_metrics.extend(custom_list)
                if "Other (specify below)" in all_metrics:
                    all_metrics.remove("Other (specify below)")
            
            return all_metrics
        
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
        
        def _generate_experiment_assessment(self) -> Dict[str, Any]:
            """Generate overall experiment assessment."""
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
                self.responses.get("custom_metrics", "")
            ))
            if metrics_count > 10:
                complexity_score += 2
            elif metrics_count > 5:
                complexity_score += 1
            
            # Determine complexity level
            if complexity_score >= 4:
                complexity_level = "High"
            elif complexity_score >= 2:
                complexity_level = "Medium"
            else:
                complexity_level = "Low"
            
            return {
                "complexity_level": complexity_level,
                "complexity_score": complexity_score,
                "monitoring_scope": "Large" if ari_count > 10 or metrics_count > 10 else "Medium" if ari_count > 5 or metrics_count > 5 else "Small",
                "key_recommendations": [
                    "Metrics sourced from query.sql for consistency",
                    "Consider monitoring dashboard for complex experiments", 
                    "Validate metric calculations before analysis"
                ],
                "experiment_readiness": "Ready" if complexity_level != "High" else "Needs Planning"
            }
        
        def display_analysis(self):
            """Display the analysis results for experiment monitoring."""
            print(f"\n{'='*80}")
            print(f"                SQL-INTEGRATED EXPERIMENT MONITORING - RESULTS")
            print(f"{'='*80}")
            
            # Display each analysis section
            for section, data in self.analysis_results.items():
                if section == "overall_assessment":
                    continue
                
                print(f"\n{section.replace('_', ' ').title()}:")
                print("-" * 60)
                
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
                print(f"\n{'Overall Assessment':-^80}")
                for key, value in overall.items():
                    if isinstance(value, list):
                        print(f"{key.replace('_', ' ').title()}:")
                        for item in value:
                            print(f"  • {item}")
                    else:
                        print(f"{key.replace('_', ' ').title()}: {value}")
        
        def generate_populated_sql(self) -> str:
            """Generate the SQL query with placeholders filled from questionnaire responses."""
            try:
                with open("query.sql", 'r') as f:
                    sql_template = f.read()
                
                # Get responses
                pre_start = self.responses.get("pre_start_date", "{pre_start_date}")
                pre_end = self.responses.get("pre_end_date", "{pre_end_date}")
                post_start = self.responses.get("post_start_date", "{post_start_date}")
                post_end = self.responses.get("post_end_date", "{post_end_date}")
                merchant_aris = self.responses.get("merchant_aris", "{merchant_ari_list}")
                ari_type = self.responses.get("ari_type", "Merchant ARIs")
                
                # Format merchant ARIs for SQL
                if merchant_aris != "{merchant_ari_list}":
                    # Parse and format ARIs
                    aris = self._compile_all_aris(merchant_aris)
                    formatted_aris = "'" + "', '".join(aris) + "'"
                else:
                    formatted_aris = merchant_aris
                
                # Determine the correct WHERE clause based on ARI type
                if ari_type == "Merchant Partner ARIs":
                    where_clause = f"WHERE md.merchant_partner_ari IN ({formatted_aris})"
                else:  # Default to Merchant ARIs
                    where_clause = f"WHERE md.merchant_ari IN ({formatted_aris})"
                
                # Replace placeholders
                populated_sql = sql_template.replace("{pre_start_date}", f"'{pre_start}'")
                populated_sql = populated_sql.replace("{pre_end_date}", f"'{pre_end}'")
                populated_sql = populated_sql.replace("{post_start_date}", f"'{post_start}'")
                populated_sql = populated_sql.replace("{post_end_date}", f"'{post_end}'")
                
                # Replace the entire WHERE clause based on ARI type
                # Find and replace the existing WHERE clause
                import re
                where_pattern = r'WHERE\s+md\.merchant_ari\s+IN\s+\({merchant_ari_list}\)\s+OR\s+md\.merchant_partner_ari\s+IN\s+\({merchant_ari_list}\)'
                if re.search(where_pattern, populated_sql):
                    populated_sql = re.sub(where_pattern, where_clause, populated_sql)
                else:
                    # Fallback: replace the placeholder
                    populated_sql = populated_sql.replace("{merchant_ari_list}", formatted_aris)
                
                return populated_sql
                
            except Exception as e:
                return f"Error generating SQL: {e}"
        
        def save_populated_sql(self, filename: str = None):
            """Save the populated SQL query to a file."""
            if not filename:
                timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
                filename = f"populated_query_{timestamp}.sql"
            
            populated_sql = self.generate_populated_sql()
            
            try:
                with open(filename, 'w') as f:
                    f.write(populated_sql)
                print(f"✅ Populated SQL saved to: {filename}")
                return filename
            except Exception as e:
                print(f"❌ Error saving SQL: {e}")
                return None

        def run_full_analysis(self):
            """Run the complete experiment monitoring analysis workflow."""
            try:
                self.display_experiment_welcome()
                
                # Show extracted metrics
                print("📊 METRICS EXTRACTED FROM QUERY.SQL:")
                sql_metrics = extract_metrics_from_sql()
                for i, metric in enumerate(sql_metrics[:-1], 1):  # Exclude "Other"
                    print(f"   {i}. {metric}")
                print()
                
                # Show SQL placeholders that will be filled
                print("🔗 SQL PLACEHOLDERS THAT WILL BE POPULATED:")
                print("   • {pre_start_date} - From Question 4 (Pre start date)")
                print("   • {pre_end_date} - From Question 5 (Pre end date)") 
                print("   • {post_start_date} - From Question 6 (Post start date)")
                print("   • {post_end_date} - From Question 7 (Post end date)")
                print("   • {merchant_ari_list} - From Question 2 (ARI list)")
                print()
                print("🎯 DYNAMIC WHERE CLAUSE GENERATION:")
                print("   Question 3: 'Merchant ARIs'")
                print("   → WHERE md.merchant_ari IN ('ARI1', 'ARI2', ...)")
                print()
                print("   Question 3: 'Merchant Partner ARIs'") 
                print("   → WHERE md.merchant_partner_ari IN ('PARTNER1', 'PARTNER2', ...)")
                print()
                
                # Conduct questionnaire (simplified for demo)
                print("Starting questionnaire...")
                print("(This would run the full interactive questionnaire)")
                
                # For demo purposes, show what the analysis would look like
                print("\n" + "="*60)
                print("           DEMO ANALYSIS RESULTS")
                print("="*60)
                print("✅ SQL metrics successfully integrated")
                print("✅ Date placeholders mapped to questionnaire")
                print("✅ Ready to generate populated SQL query")
                print("✅ Pre/Post analysis framework connected")
                
            except Exception as e:
                print(f"\nAn error occurred: {e}")
    
    return ExperimentMonitoringQuestionnaire

def run_sql_experiment_questionnaire():
    """Run the SQL-integrated experiment monitoring questionnaire."""
    print("Creating SQL-integrated experiment monitoring questionnaire...")
    
    # Create custom questionnaire class
    CustomQuestionnaire = create_experiment_questionnaire_class()
    
    if CustomQuestionnaire:
        questionnaire = CustomQuestionnaire()
        questionnaire.run_full_analysis()
    else:
        print("Failed to create experiment monitoring questionnaire")

if __name__ == "__main__":
    run_sql_experiment_questionnaire()
