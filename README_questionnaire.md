# Analysis Questionnaire Tool

A comprehensive Python-based tool for conducting structured analysis through predefined questions and generating insights based on user responses.

## Features

- **Multiple Analysis Categories**: Choose from business analysis, investment analysis, project management, and customer satisfaction
- **Flexible Question Types**: Support for multiple choice, multi-select, text, numeric, and rating questions
- **Intelligent Analysis**: Automated analysis with industry-specific insights and recommendations
- **Customizable**: Easy to create custom questionnaires and analysis logic
- **Results Export**: Save analysis results to JSON files for further processing
- **Progress Tracking**: Visual progress indicators during questionnaire completion

## Files Overview

### Core Files

1. **`analysis_questionnaire.py`** - Basic questionnaire tool with business analysis questions
2. **`enhanced_questionnaire.py`** - Advanced tool with multiple question sets and categories
3. **`questionnaire_config.py`** - Configuration file with predefined question sets
4. **`custom_questionnaire_example.py`** - Example of creating custom questionnaires

### Question Sets Available

- **Business Analysis**: Company type, size, revenue, growth, market position, challenges
- **Investment Analysis**: Investment type, risk tolerance, market conditions, portfolio diversification
- **Project Management**: Project scope, resources, risks, timeline, stakeholder complexity
- **Customer Satisfaction**: Satisfaction levels, pain points, loyalty, recommendation likelihood

## Quick Start

### 1. Basic Usage

Run the basic business analysis questionnaire:

```bash
python analysis_questionnaire.py
```

### 2. Enhanced Usage

Run the enhanced questionnaire with multiple categories:

```bash
python enhanced_questionnaire.py
```

### 3. Custom Questionnaire

Run the custom employee satisfaction example:

```bash
python custom_questionnaire_example.py
```

## Installation

### Prerequisites

- Python 3.7 or higher
- No external dependencies required (uses only standard library)

### Setup

1. Clone or download the files to your local directory
2. Ensure all files are in the same directory
3. Run any of the Python scripts

## Usage Examples

### Running a Predefined Analysis

1. **Start the tool**:
   ```bash
   python enhanced_questionnaire.py
   ```

2. **Select analysis category**:
   - Choose from available question sets
   - View descriptions and question counts

3. **Answer questions**:
   - Follow the prompts for each question
   - Use numeric inputs for multiple choice
   - Use comma-separated numbers for multi-select
   - Type text for open-ended questions

4. **Review results**:
   - View detailed analysis by category
   - See risk assessments and recommendations
   - Save results to file if desired

### Creating Custom Questions

You can easily create custom questionnaires by defining questions in the same format:

```python
custom_questions = [
    {
        "id": "question_id",
        "question": "Your question text here?",
        "type": "multiple_choice",  # or "multi_select", "text", "numeric", "rating"
        "options": ["Option 1", "Option 2", "Option 3"],  # for choice questions
        "required": True
    }
]
```

### Question Types Supported

- **`multiple_choice`**: Single selection from predefined options
- **`multi_select`**: Multiple selections from predefined options
- **`text`**: Free-form text input
- **`numeric`**: Numeric input with validation
- **`rating`**: Rating scale (e.g., 1-5, 1-10)

## Customization

### Adding New Question Sets

1. **Define questions** in `questionnaire_config.py`:
   ```python
   NEW_ANALYSIS_QUESTIONS = [
       # Your questions here
   ]
   ```

2. **Add to QUESTION_SETS**:
   ```python
   "new_analysis": {
       "name": "New Analysis",
       "description": "Description of your analysis",
       "questions": NEW_ANALYSIS_QUESTIONS,
       "category": "your_category"
   }
   ```

3. **Add analysis logic** in `enhanced_questionnaire.py`:
   ```python
   def _analyze_new_responses(self):
       # Your custom analysis logic here
       pass
   ```

### Creating Custom Analysis Classes

Extend the base class for specialized analysis:

```python
class CustomQuestionnaire(EnhancedAnalysisQuestionnaire):
    def analyze_responses(self):
        # Override with custom analysis logic
        pass
    
    def _custom_analysis_method(self):
        # Add custom analysis methods
        pass
```

## Output Format

### Analysis Results Structure

```json
{
  "timestamp": "2024-01-01T12:00:00",
  "question_set": "business_analysis",
  "set_info": {
    "name": "Business Analysis",
    "description": "Comprehensive business analysis...",
    "category": "business"
  },
  "responses": {
    "business_type": "Technology",
    "company_size": "51-200 employees",
    // ... other responses
  },
  "analysis": {
    "business_insights": {
      "type": "Technology",
      "characteristics": ["Innovation-driven", "Fast-paced", ...]
    },
    "overall_assessment": {
      "risk_level": "Medium",
      "risk_score": 3,
      "overall_health": "Fair",
      "key_recommendations": [...]
    }
  }
}
```

### Key Analysis Components

- **Business Insights**: Industry characteristics and implications
- **Size Analysis**: Company size implications and management approaches
- **Financial Health**: Revenue-based stage assessment
- **Growth Analysis**: Growth stage identification and focus areas
- **Market Analysis**: Position-based strategic implications
- **Risk Assessment**: Challenge prioritization and mitigation strategies
- **Overall Assessment**: Risk scoring and key recommendations

## Use Cases

### Business Analysis
- Company performance evaluation
- Strategic planning and positioning
- Risk assessment and mitigation
- Growth opportunity identification

### Investment Analysis
- Portfolio risk assessment
- Investment strategy development
- Market condition analysis
- Diversification planning

### Project Management
- Project risk assessment
- Resource planning and allocation
- Stakeholder management planning
- Success criteria definition

### Customer Satisfaction
- Customer experience evaluation
- Pain point identification
- Loyalty and retention analysis
- Service improvement planning

### Custom Applications
- Employee satisfaction surveys
- Product feedback collection
- Market research studies
- Performance evaluations

## Best Practices

### Question Design
- Keep questions clear and concise
- Use consistent response formats
- Balance required vs. optional questions
- Provide meaningful answer options

### Analysis Logic
- Base recommendations on industry best practices
- Consider response patterns and correlations
- Provide actionable insights
- Include risk assessment where appropriate

### Data Management
- Save results for historical tracking
- Use consistent naming conventions
- Consider data privacy and security
- Plan for data analysis and reporting

## Troubleshooting

### Common Issues

1. **Import Errors**: Ensure all files are in the same directory
2. **Question Validation**: Check question format against supported types
3. **Analysis Errors**: Verify response data structure matches expectations
4. **File Save Issues**: Check write permissions in target directory

### Debug Mode

Add debug prints to custom analysis methods:

```python
def _custom_analysis_method(self):
    print(f"Debug: Processing response: {self.responses}")
    # Your analysis logic here
```

## Extending the Tool

### Adding New Question Types

1. **Define the type** in `QUESTION_TYPES`
2. **Add input handling** in `get_user_input()`
3. **Update validation** in `validate_question_format()`

### Adding New Analysis Categories

1. **Create question set** in configuration
2. **Add analysis method** to main class
3. **Update question set selection**
4. **Add to analysis categories**

### Integration with External Systems

- **Database Storage**: Modify save methods to use databases
- **API Integration**: Add web service endpoints
- **Reporting**: Integrate with reporting tools
- **Analytics**: Connect to business intelligence platforms

## Contributing

### Guidelines
- Follow existing code structure and naming conventions
- Add comprehensive documentation for new features
- Include error handling and validation
- Test with various question types and responses

### Testing
- Test with different question combinations
- Verify analysis logic accuracy
- Check error handling scenarios
- Validate output format consistency

## License

This tool is provided as-is for educational and business use. Feel free to modify and extend for your specific needs.

## Support

For questions or issues:
1. Check the troubleshooting section
2. Review the code examples
3. Examine the configuration files
4. Test with simple question sets first

---

**Note**: This tool is designed to provide structured analysis and recommendations. Always use professional judgment when applying insights to real business decisions.
