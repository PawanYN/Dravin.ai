# Responses API Projects

A collection of advanced OpenAI API projects focusing on response analysis, prompt engineering, and API migration patterns.

## Project Index

### 📊 [Eval Driven System Design](./Eval_Driven_System_Design.py)

**Complete receipt processing system using evaluation-driven development methodology**

**Files:**
- [`Eval_Driven_System_Design.py`](./Eval_Driven_System_Design.py) - Main implementation
- [`Eval_Driven_System_Design_README.md`](./Eval_Driven_System_Design_README.md) - Developer reference

**Description:** Production-ready framework demonstrating eval-driven development from prototype to production. Implements receipt processing with image extraction, business rule evaluation, and systematic quality assessment.

**Key Features:**
- ✅ Receipt image → structured data extraction
- ✅ 4-criteria audit decision system (travel/non-travel, amount limits, math validation, handwritten notes)
- ✅ Multi-step evaluation framework (extraction quality + decision logic + end-to-end)
- ✅ Three grader types: string_check, text_similarity, score_model
- ✅ Business impact analysis with cost/ROI calculations
- ✅ Real dataset integration (Roboflow receipt handwriting detection)
- ✅ OpenRouter API integration for cost-effective development

**Use Case:** Automates manual receipt review workflows, reducing $5/receipt human review cost to $2-3 automated processing with 80%+ accuracy.

---

### 🔧 [Prompt Optimization](./Optimize_Prompts.py)

**Advanced prompt engineering and optimization techniques**

**Files:**
- [`Optimize_Prompts.py`](./Optimize_Prompts.py) - Optimization framework
- [`Prompt_Optimization_README.md`](./Prompt_Optimization_README.md) - Documentation

**Description:** Systematic approach to prompt improvement using evaluation metrics and iterative refinement.

**Key Features:**
- ✅ Iterative development with automated improvement
- ✅ Multi-metric evaluation system (accuracy, quality, consistency)
- ✅ Stage-based progression (Prototype → Development → Staging → Production)
- ✅ AI-powered prompt optimization based on evaluation results
- ✅ Historical performance tracking and analytics
- ✅ Automated testing and continuous integration

---

### 🔄 [Prompt Migration Guide](./Prompt_Migration_Guide.md)

**Migration patterns for OpenAI API updates**

**Files:**
- [`Prompt_Migration_Guide.md`](./Prompt_Migration_Guide.md) - Migration documentation
- [`Prompt_Migration_Guide_Refactored.py`](./Prompt_Migration_Guide_Refactored.py) - Implementation examples

**Description:** Best practices and patterns for migrating prompts across OpenAI API versions.

---

### 🛠️ [Multi-tool Orchestration](./Multi_tool_Orchestration.md)

**Coordinating multiple AI tools and APIs**

**Description:** Patterns for orchestrating complex workflows involving multiple AI services and tools.

---

### 🧠 [Reasoning Items](./Reasoning_items.py)

**Advanced reasoning and logic patterns**

**Description:** Implementation of complex reasoning patterns and logical decision-making systems.

---

### 🔗 [Tool Orchestration](./responses_api_tool_orchestration.py)

**Response API tool coordination**

**Description:** Framework for coordinating multiple tools and APIs in response generation workflows.

---

### 📄 [Qdrant Integration](./Qdrant.md)

**Vector database integration patterns**

**Description:** Implementation patterns for integrating Qdrant vector database with OpenAI APIs.

---

### 📋 [Summary](./Summary.md)

**Project summaries and overviews**

**Description:** Comprehensive summaries of all projects and their key learnings.

---

## Getting Started

1. **Install Dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Set Environment Variables:**
   ```bash
   export OPENAI_API_KEY="your-api-key"
   ```

3. **Run Individual Projects:**
   ```bash
   python Eval_Driven_System_Design.py
   python Optimize_Prompts.py
   python Reasoning_items.py
   python responses_api_tool_orchestration.py
   ```

## Project Structure

```
responses_api/
├── README.md                                    # This file
├── requirements.txt                             # Dependencies
├── .gitignore                                   # Git ignore patterns
├── Eval_Driven_System_Design.py                # Eval-driven development framework
├── Eval_Driven_System_Design_README.md         # Eval-driven documentation
├── Optimize_Prompts.py                         # Prompt optimization framework
├── Prompt_Optimization_README.md               # Prompt optimization docs
├── Prompt_Migration_Guide.md                   # API migration guide
├── Prompt_Migration_Guide_Refactored.py        # Migration examples
├── Multi_tool_Orchestration.md                 # Tool orchestration patterns
├── Reasoning_items.py                          # Reasoning implementations
├── responses_api_tool_orchestration.py         # Tool coordination
├── Qdrant.md                                   # Vector database integration
├── Summary.md                                  # Project summaries
├── data/                                       # Dataset files (gitignored)
│   ├── train/test/valid/                       # Receipt images
│   └── ground_truth/                           # Expert labels
└── [output files...]                           # Generated reports
```

## Key Learnings

- **Eval-driven development** enables systematic improvement vs intuition-based development
- **Multi-step evaluation** prevents AI systems from "gaming" individual components
- **Business-aligned metrics** connect technical performance to real-world impact
- **Structured outputs** with Pydantic enable reliable data processing
- **Cost optimization** through model selection and prompt engineering
- **Iterative improvement** through automated evaluation and optimization

## Dependencies

Core requirements across projects:
- `openai` - API integration
- `pydantic` - Data validation
- `python-dotenv` - Environment management
- `rich` - Enhanced output formatting
- `asyncio` - Async processing

See individual project READMEs for specific requirements.
