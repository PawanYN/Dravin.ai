# Eval-Driven Receipt Processing System

Personal reference for eval-driven development implementation following OpenAI cookbook methodology.

## Core Architecture

**Pipeline**: Image → Structured Data → Business Decision → Auto-approve/Audit

**Evaluation**: Ground Truth → Graders → Metrics → Business Impact → Deploy Decision

## Data Models

```python
class ReceiptDetails(BaseModel):
    merchant: str | None
    location: Location
    time: str | None
    items: list[LineItem]
    subtotal: str | None
    tax: str | None
    total: str | None
    handwritten_notes: list[str]

class AuditDecision(BaseModel):
    not_travel_related: bool    # Non-travel = needs audit
    amount_over_limit: bool     # >$50 = needs audit
    math_error: bool           # Math wrong = needs audit
    handwritten_x: bool        # "X" marks = needs audit
    reasoning: str
    needs_audit: bool          # ANY violation = True
```

## Key Functions

```python
# Core processing
async def extract_receipt_details(image_path: str, model: str = "gpt-4o-mini") -> ReceiptDetails
async def evaluate_receipt_for_audit(receipt_details: ReceiptDetails, model: str = "gpt-4o-mini") -> AuditDecision

# Evaluation
async def evaluate_extraction_quality(predicted: ReceiptDetails, ground_truth: ReceiptDetails) -> EvaluationResult
async def evaluate_multi_step_pipeline(image_path, ground_truth_receipt, ground_truth_audit) -> MultiStepEvaluationResult

# Dataset creation
async def create_evaluation_record(image_path: Path, model: str) -> EvaluationRecord
async def create_dataset_content(receipt_image_dir: Path, model: str) -> list[dict]
```

#### 2. **Development Pipeline** 🔄
- **Version Management**: Track prompt iterations and improvements
- **Automated Improvement**: AI-powered prompt optimization
- **Stage Progression**: Controlled advancement through development stages
- **Continuous Integration**: Automated testing and deployment

#### 3. **Monitoring System** 📈
- **Real-time Metrics**: Live performance monitoring
- **Alert System**: Automated issue detection
- **Performance Analytics**: Detailed insights and reporting
- **Rollback Capability**: Quick reversion to stable versions

## 🛠️ Technical Implementation

### Core Data Models

```python
class SystemStage(Enum):
    PROTOTYPE = "prototype"
    DEVELOPMENT = "development" 
    STAGING = "staging"
    PRODUCTION = "production"

class EvaluationMetric(BaseModel):
    name: str
    value: float
    threshold: Optional[float] = None
    passed: bool = False
    details: Dict[str, Any] = Field(default_factory=dict)

class EvaluationResult(BaseModel):
    timestamp: datetime
    stage: SystemStage
    version: str
    metrics: List[EvaluationMetric]
    overall_score: float
    passed: bool
    execution_time: float
```

### Key Classes

#### **EvaluationFramework**
```python
class EvaluationFramework:
    async def evaluate_system(self, system_prompt: SystemPrompt) -> EvaluationResult:
        """Evaluate system against all test cases with multiple metrics."""
        
    def _calculate_accuracy(self, test_results: List[Dict]) -> EvaluationMetric:
        """Calculate success rate of test cases."""
        
    async def _calculate_response_quality(self, test_results: List[Dict]) -> EvaluationMetric:
        """AI-powered quality assessment."""
        
    def _calculate_consistency(self, test_results: List[Dict]) -> EvaluationMetric:
        """Measure behavioral predictability."""
```

#### **SystemDevelopmentPipeline**
```python
class SystemDevelopmentPipeline:
    async def run_development_cycle(
        self,
        initial_prompt: str,
        test_cases: List[Dict[str, Any]],
        target_score: float = 0.8,
        max_iterations: int = 5
    ) -> Dict[str, Any]:
        """Complete development cycle with iterative improvement."""
        
    async def _improve_prompt(
        self, 
        current_prompt: SystemPrompt, 
        eval_result: EvaluationResult
    ) -> SystemPrompt:
        """AI-powered prompt improvement based on evaluation results."""
```

## 🧪 Evaluation Metrics

### 1. **Accuracy** 🎯
- **Measurement**: Percentage of successful test case executions
- **Threshold**: 80% success rate
- **Purpose**: Ensure basic functionality works reliably

### 2. **Response Quality** ⭐
- **Measurement**: AI-evaluated quality score (0.0-1.0)
- **Criteria**: Relevance, clarity, completeness, accuracy
- **Threshold**: 0.7 average quality score
- **Purpose**: Maintain high-quality user experience

### 3. **Consistency** 🔄
- **Measurement**: Behavioral predictability across test runs
- **Calculation**: Based on success rate variance
- **Threshold**: 0.6 consistency score
- **Purpose**: Ensure reliable system behavior

## 🚀 Usage Examples

### Basic Development Cycle

```python
# Initialize pipeline
pipeline = SystemDevelopmentPipeline("customer_support_bot")

# Define initial prompt
initial_prompt = """
You are a helpful customer support assistant. 
Answer customer questions politely and accurately.
"""

# Define test cases
test_cases = [
    {
        "id": "test_1",
        "input_text": "What are your business hours?",
        "category": "hours",
        "priority": 1
    },
    {
        "id": "test_2", 
        "input_text": "I want to return a product",
        "category": "returns",
        "priority": 1
    }
]

# Run development cycle
results = await pipeline.run_development_cycle(
    initial_prompt=initial_prompt,
    test_cases=test_cases,
    target_score=0.75,
    max_iterations=3
)
```

### Custom Evaluation

```python
# Create evaluation framework
evaluator = EvaluationFramework("my_system")

# Add test cases
evaluator.add_test_case(TestCase(
    id="custom_test",
    input_text="Test input",
    expected_criteria={"tone": "professional", "length": "concise"}
))

# Evaluate specific prompt
prompt = SystemPrompt(content="Your system prompt", version="v1.0")
result = await evaluator.evaluate_system(prompt)

print(f"Overall Score: {result.overall_score}")
print(f"Passed: {result.passed}")
```

## 📊 Output Examples

### Development Cycle Results
```python
{
    "final_version": "v0.1.3",
    "final_score": 0.82,
    "iterations": 3,
    "target_achieved": True,
    "evaluation_history": [
        {
            "version": "v0.1.0",
            "overall_score": 0.65,
            "metrics": [
                {"name": "accuracy", "value": 0.8, "passed": True},
                {"name": "response_quality", "value": 0.6, "passed": False},
                {"name": "consistency", "value": 0.55, "passed": False}
            ]
        },
        # ... more iterations
    ]
}
```

### Evaluation Metrics
```
📊 Development Results:
Final Version: v0.1.3
Final Score: 0.82
Iterations: 3
Target Achieved: True

📈 Evaluation History:
  Iteration 1: Score 0.65
    ✅ accuracy: 0.80
    ❌ response_quality: 0.60
    ❌ consistency: 0.55
  Iteration 2: Score 0.74
    ✅ accuracy: 0.85
    ✅ response_quality: 0.72
    ❌ consistency: 0.65
  Iteration 3: Score 0.82
    ✅ accuracy: 0.90
    ✅ response_quality: 0.78
    ✅ consistency: 0.78
```

## 🔧 Configuration

### Environment Setup
```bash
export OPENAI_API_KEY="your-openrouter-api-key"
```

### Test Case Configuration
```python
test_cases = [
    {
        "id": "unique_test_id",
        "input_text": "User input to test",
        "expected_output": "Optional expected response",
        "expected_criteria": {
            "tone": "professional",
            "includes_keywords": ["support", "help"]
        },
        "category": "support",
        "priority": 1  # 1=high, 2=medium, 3=low
    }
]
```

### Evaluation Thresholds
```python
# Customize metric thresholds
accuracy_threshold = 0.8      # 80% success rate
quality_threshold = 0.7       # 70% quality score
consistency_threshold = 0.6   # 60% consistency
```

## 🎯 Key Features

### ✅ **Iterative Improvement**
- Automated prompt optimization based on evaluation results
- AI-powered analysis of failure patterns
- Continuous refinement until target metrics achieved

### ✅ **Multi-Stage Development**
- Prototype → Development → Staging → Production progression
- Stage-appropriate evaluation criteria
- Controlled advancement with quality gates

### ✅ **Comprehensive Evaluation**
- Multiple evaluation metrics (accuracy, quality, consistency)
- AI-powered response quality assessment
- Historical performance tracking

### ✅ **Production Ready**
- Monitoring and alerting capabilities
- Version management and rollback
- Scalable architecture for high-volume usage


## 📝 Running the Demo

```bash
python Eval_Driven_System_Design.py
```

This will demonstrate:
1. Creating a customer support bot prototype
2. Running iterative improvement cycles
3. Tracking evaluation metrics over time
4. Achieving target performance scores

---

**🔗 Navigation:**
- 🏠 [Repository Root](../../../)
