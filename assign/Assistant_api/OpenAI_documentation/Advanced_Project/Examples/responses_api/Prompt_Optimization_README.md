# 🚀 Multi-Agent Prompt Optimization System

A sophisticated AI-powered system that automatically detects and fixes issues in developer prompts and few-shot examples using multiple specialized agents working in parallel.

## 🎯 Overview

This project implements a multi-agent architecture to optimize prompts by:
- **Detecting contradictions** in developer instructions
- **Validating few-shot examples** against prompt requirements
- **Automatically rewriting** problematic content
- **Running all checks in parallel** for maximum efficiency

## 🏗️ Architecture

### Core Components

```
┌─────────────────────────────────────────────────────────────┐
│                 optimize_prompt_parallel()                  │
│                    Main Orchestrator                        │
└─────────────────────┬───────────────────────────────────────┘
                      │
        ┌─────────────┼─────────────┐
        │             │             │
        ▼             ▼             ▼
┌─────────────┐ ┌─────────────┐ ┌─────────────┐
│Contradiction│ │   Format    │ │  Few-shot   │
│  Checker    │ │  Checker    │ │ Consistency │
│             │ │             │ │   Checker   │
└─────────────┘ └─────────────┘ └─────────────┘
        │             │             │
        └─────────────┼─────────────┘
                      │
        ┌─────────────┼─────────────┐
        │             │             │
        ▼             ▼             ▼
┌─────────────┐ ┌─────────────┐ ┌─────────────┐
│    Dev      │ │   Format    │ │  Few-shot   │
│  Rewriter   │ │  Rewriter   │ │  Rewriter   │
│             │ │             │ │             │
└─────────────┘ └─────────────┘ └─────────────┘
```

### Agent Specifications

#### 1. **Contradiction Checker** 🔍
- **Purpose**: Detects genuine self-contradictions in developer prompts
- **Input**: Developer message text
- **Output**: List of contradictions found
- **Example**: Finds conflict between "Always answer in English" and "Nunca respondas en inglés"

#### 2. **Few-shot Consistency Checker** 📝
- **Purpose**: Validates assistant examples against developer requirements
- **Input**: Developer message + few-shot examples
- **Output**: Issues found + rewrite suggestions
- **Example**: Flags assistant response with explanations when prompt says "only yes/no"

#### 3. **Format Checker** 📋
- **Purpose**: Ensures structured output requirements are clearly specified
- **Input**: Developer message
- **Output**: Missing format specifications
- **Status**: Template ready for implementation

## 🛠️ Technical Implementation

### Data Models

```python
class Issues(BaseModel):
    """Base class for issue detection results."""
    has_issues: bool
    issues: List[str] = Field(default_factory=list)

class FewShotIssues(Issues):
    """Extended with rewrite suggestions."""
    rewrite_suggestions: List[str] = Field(default_factory=list)

class ChatMessage(BaseModel):
    """Represents a single chat message."""
    role: Role  # user | assistant
    content: str
```

### Core Function

```python
async def optimize_prompt_parallel(
    developer_message: str,
    messages: List[ChatMessage],
) -> Dict[str, Any]:
    """
    Main optimization pipeline that:
    1. Runs all checkers in parallel
    2. Conditionally triggers rewriters
    3. Returns unified optimization results
    """
```

## 🧪 Testing Examples

### Test Case 1: Contradiction Detection
```python
# Input
developer_message = "Always answer in **English**.\nNunca respondas en inglés."

# Expected Output
{
    "changes": True,
    "contradiction_issues": "Instruction to always answer in English conflicts with instruction to never respond in English"
}
```

### Test Case 2: Few-shot Consistency
```python
# Input
developer_message = "Respond with **only 'yes' or 'no'** – no explanations."
messages = [
    {"role": "user", "content": "Is the sky blue?"},
    {"role": "assistant", "content": "Yes, because wavelengths …"}  # ❌ Violates rule
]

# Expected Output
{
    "changes": True,
    "few_shot_contradiction_issues": "Assistant response includes explanation when prompt requires only yes/no"
}
```

## 🚀 Usage

### Basic Usage
```python
import asyncio
from Optimize_Prompts import optimize_prompt_parallel, ChatMessage, Role

async def main():
    result = await optimize_prompt_parallel(
        developer_message="Your prompt here",
        messages=[
            ChatMessage(role=Role.user, content="Example user message"),
            ChatMessage(role=Role.assistant, content="Example assistant response")
        ]
    )
    
    print(f"Changes needed: {result['changes']}")
    print(f"Issues found: {result['contradiction_issues']}")

asyncio.run(main())
```

### Running Tests
```bash
python Optimize_Prompts.py
```

## 📊 Output Format

The optimization function returns a comprehensive dictionary:

```python
{
    "changes": bool,                           # Whether any issues were found
    "new_developer_message": str,              # Optimized prompt (if rewritten)
    "new_messages": List[Dict[str, str]],      # Optimized few-shot examples
    "contradiction_issues": str,               # Contradiction problems found
    "few_shot_contradiction_issues": str,      # Few-shot problems found
    "format_issues": str                       # Format problems found
}
```

## 🔧 Configuration

### OpenAI Client Setup
```python
client = AsyncOpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=os.environ.get("OPENAI_API_KEY", "your-api-key"),
)
```

### Environment Variables
```bash
export OPENAI_API_KEY="your-openrouter-api-key"
```

## 🎯 Key Features

### ✅ **Parallel Processing**
- All checkers run simultaneously using `asyncio.gather()`
- Significantly faster than sequential execution
- Efficient resource utilization

### ✅ **Conservative Approach**
- Only flags genuine, objective issues
- Avoids false positives and subjective judgments
- Focuses on concrete rule violations

### ✅ **Conditional Rewriting**
- Rewriters only run when issues are detected
- Preserves original intent while fixing problems
- Minimal unnecessary changes

### ✅ **Comprehensive Coverage**
- Handles contradictions, format issues, and few-shot problems
- Unified interface for all optimization needs
- Extensible architecture for new checkers

## 📝 Files Structure

```
responses_api/
├── Optimize_Prompts.py                    # Main implementation
├── Prompt_Optimization_README.md          # This documentation
```

