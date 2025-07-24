# 🚀 Prompt Migration Guide

A comprehensive AI-powered tool for analyzing, critiquing, and improving system prompts while demonstrating OpenAI API migration patterns from legacy `retrieval` to modern `file_search` tools.

## 📁 Project Files

### Core Files
- **[Prompt_Migration_Guide_Refactored.py](./Prompt_Migration_Guide_Refactored.py)** - Main script with complete analysis pipeline
- **[Prompt_Migration_Guide_Refactored_output.html](./Prompt_Migration_Guide_Refactored_output.html)** - Generated HTML report (created after running script)
- **[Prompt_Migration_Guide.md](./Prompt_Migration_Guide.md)** - This documentation file

### Related Files
- **[requirements.txt](./requirements.txt)** - Python dependencies
- **[README.md](./README.md)** - Master project index

## 🎯 What This Tool Does

### 1. **🔄 API Migration Analysis**
- Shows visual diff between old `{'type': 'retrieval'}` and new `{'type': 'file_search'}`
- Demonstrates proper OpenAI API migration patterns
- Color-coded GitHub-style diff visualization

### 2. **📋 Instruction Extraction**
- Uses GPT-4.1 to extract structured instructions from system prompts
- Converts unstructured prompts into organized instruction lists
- Each instruction includes title and extracted text

### 3. **🔍 Prompt Critique**
- AI-powered analysis identifying specific issues:
  - **Ambiguity**: Phrases open to multiple interpretations
  - **Missing Definitions**: Undefined terms or concepts
  - **Conflicting Instructions**: Contradictory or overlapping rules
  - **Vague Requirements**: Subjective or unclear specifications

### 4. **✨ Auto-Revision**
- Generates improved prompts addressing identified issues
- Preserves original structure and intent
- Applies minimal, targeted edits

### 5. **📊 Professional Reporting**
- Beautiful HTML output with visual cards
- Console text output for easy copying
- Professional styling with responsive design

## 🛠️ Installation & Setup

### Prerequisites
```bash
# Ensure you have Python 3.8+
python --version

# Install dependencies
pip install -r requirements.txt

# Set your API key
export OPENAI_API_KEY="your-api-key-here"
```

### Dependencies
- `openai>=1.0.0` - OpenAI API integration
- `pydantic>=2.0.0` - Data validation and structured output
- `tiktoken>=0.5.0` - Token counting
- `ipython>=8.0.0` - HTML display capabilities

## 🚀 Usage

### Run the Analysis
```bash
python Prompt_Migration_Guide_Refactored.py
```

### Expected Output
```
Client initialized with model: gpt-4.1
Base URL: https://openrouter.ai/api/v1/
Original prompt length: 244 tokens

🔍 Analyzing prompt for potential issues...
Found 3 potential issues

🔄 Generating revised prompt...
✅ Complete HTML output saved to 'Prompt_Migration_Guide_Refactored_output.html'
```

### View Results
1. **Console**: See analysis directly in terminal
2. **HTML Report**: Open `Prompt_Migration_Guide_Refactored_output.html`
3. **Local Server**: `python -m http.server 8000` → `http://localhost:8000`

## ⚙️ How It Works

### Architecture Overview
```python
# 1. Initialize HTML output
initialize_html_file()

# 2. Show API migration diff
show_critique_and_diff(old_config, new_config)

# 3. Extract instructions using AI
instructions_list = extract_instructions(SAMPLE_PROMPT)

# 4. Critique prompt for issues
critique_result = critique_prompt(SAMPLE_PROMPT)

# 5. Generate revised prompt
revised_prompt = revise_prompt(SAMPLE_PROMPT, issues_str)

# 6. Finalize HTML report
finalize_html_file()
```

### Key Functions
- **`extract_instructions()`** - AI-powered instruction extraction
- **`critique_prompt()`** - Issue identification and analysis
- **`revise_prompt()`** - Automated prompt improvement
- **`show_critique_and_diff()`** - Visual diff generation
- **`display_cards()`** - Professional HTML card rendering

## 📊 Sample Output

### Console Critique Example
```
Issue: Ambiguous evaluation criteria
Snippet: Your evaluation should consider factors such as...
Explanation: The prompt lists several criteria but does not define them...
Suggestion: Briefly define each criterion and clarify priorities...
```

### HTML Report Features
- **📋 Instruction Cards**: Each extracted instruction in styled cards
- **🔍 Critique Issues**: Visual problem identification with solutions
- **📊 API Migration Diff**: Color-coded comparison visualization
- **🎨 Professional Design**: Clean, responsive layout

## 🔄 API Migration Guide

### Legacy Format (Deprecated)
```python
# Old way - being phased out
assistant = client.beta.assistants.create(
    tools=[{'type': 'retrieval'}]  # ❌ Legacy
)
```

### Modern Format (Current)
```python
# New way - current standard
assistant = client.beta.assistants.create(
    tools=[{'type': 'file_search'}]  # ✅ Modern
)
```

### Migration Benefits
- **Enhanced Performance**: Better search algorithms
- **Improved Accuracy**: More precise file content retrieval
- **Future Compatibility**: Aligned with OpenAI roadmap
- **Additional Features**: Extended functionality options

## 🎯 Use Cases

### For Prompt Engineers
- **Quality Assurance**: Identify issues before production
- **Optimization**: Improve prompt clarity and effectiveness
- **Documentation**: Generate reports for stakeholder review

### For Developers
- **API Learning**: Understand OpenAI integration patterns
- **Migration Guide**: Learn proper API transition methods
- **Code Reference**: Professional implementation examples

### For Teams
- **Standardization**: Consistent prompt analysis workflows
- **Training**: Educational tool for prompt engineering
- **Automation**: Integrate into CI/CD for prompt validation

## 🔧 Technical Details

### Data Models
```python
class Instruction(BaseModel):
    instruction_title: str
    extracted_instruction: str

class CritiqueIssue(BaseModel):
    issue: str
    snippet: str
    explanation: str
    suggestion: str
```

### Configuration
- **Model**: GPT-4.1 via OpenRouter
- **Temperature**: 0.0 for consistent results
- **Max Tokens**: 2000 (optimized for cost)
- **Output Format**: Structured JSON with Pydantic validation

## 🤝 Contributing

### Development Guidelines
1. Follow existing code structure and naming conventions
2. Add docstrings to all new functions
3. Include type hints for better maintainability
4. Test with different prompt types and lengths

### Code Standards
- **Style**: Follow PEP 8 guidelines
- **Documentation**: Comprehensive docstrings
- **Error Handling**: Graceful failure with informative messages
- **Modularity**: Keep functions focused and reusable

## 📄 License & Usage

This tool is designed for educational and development purposes. Ensure compliance with OpenAI's usage policies when using their APIs.

---

**Part of the Responses API Project Collection**  
📂 [Back to Main Project Index](./README.md)
