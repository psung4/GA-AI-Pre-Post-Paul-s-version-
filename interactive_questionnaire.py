#!/usr/bin/env python3
"""
Interactive Questionnaire for Experiment Monitoring
"""

from updated_experiment_monitoring_questionnaire import create_experiment_questionnaire_class
import json
from datetime import datetime

def run_interactive_questionnaire():
    """Run the interactive questionnaire and generate SQL."""
    
    print("🎯 INTERACTIVE EXPERIMENT MONITORING QUESTIONNAIRE")
    print("=" * 70)
    print("Please answer each question. Press Enter after each response.")
    print()
    
    # Create questionnaire
    QuestionnaireClass = create_experiment_questionnaire_class()
    questionnaire = QuestionnaireClass()
    
    responses = {}
    
    # Go through each question
    for i, question in enumerate(questionnaire.questions, 1):
        print(f"━━━ QUESTION {i} ━━━")
        print(f"{question['question']}")
        
        if 'options' in question and question['options']:
            print("\nAvailable options:")
            for j, option in enumerate(question['options'], 1):
                print(f"   {j}. {option}")
            print()
        
        # Get user input
        if question['required']:
            while True:
                answer = input("Your answer (REQUIRED): ").strip()
                if answer:
                    break
                print("❌ This question is required. Please provide an answer.")
        else:
            answer = input("Your answer (optional): ").strip()
        
        # Store response
        responses[question['id']] = answer
        
        print("✅ Answer recorded!")
        print("-" * 70)
        print()
    
    # Set responses in questionnaire object
    questionnaire.responses = responses
    
    print("🎉 QUESTIONNAIRE COMPLETED!")
    print("=" * 70)
    
    # Show collected responses
    print("📋 YOUR RESPONSES:")
    for q_id, answer in responses.items():
        if answer:  # Only show non-empty answers
            print(f"   {q_id}: {answer}")
    
    print()
    print("🔄 GENERATING POPULATED SQL QUERY...")
    
    # Generate populated SQL
    try:
        populated_sql = questionnaire.generate_populated_sql()
        
        # Save the populated SQL
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        sql_filename = f"your_experiment_query_{timestamp}.sql"
        
        with open(sql_filename, 'w') as f:
            f.write(populated_sql)
        
        print("✅ SQL QUERY GENERATED!")
        print(f"📁 Saved to: {sql_filename}")
        print()
        print("📋 GENERATED SQL QUERY:")
        print("=" * 70)
        print(populated_sql)
        print("=" * 70)
        
        # Save responses as JSON for reference
        json_filename = f"questionnaire_responses_{timestamp}.json"
        with open(json_filename, 'w') as f:
            json.dump(responses, f, indent=2)
        print(f"📄 Responses also saved to: {json_filename}")
        
        return sql_filename, populated_sql, responses
        
    except Exception as e:
        print(f"❌ Error generating SQL: {e}")
        return None, None, responses

if __name__ == "__main__":
    sql_file, sql_query, responses = run_interactive_questionnaire()
    
    if sql_file:
        print()
        print("🚀 NEXT STEPS:")
        print("   1. Review the generated SQL above")
        print(f"   2. The query is saved in: {sql_file}")
        print("   3. Ready to run this query in Snowflake!")
        print("   4. Let me know if you want me to execute it!")
