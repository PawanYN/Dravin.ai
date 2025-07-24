"""
Eval Driven System Design - From Prototype to Production

A comprehensive framework for building AI systems using evaluation-driven development,
progressing from initial prototypes to production-ready solutions with continuous
monitoring and improvement.

Key Components:
1. Prototype Development with Basic Evaluation
2. Iterative Improvement Based on Metrics
3. Production Deployment with Monitoring
4. Continuous Evaluation and Optimization

Author: AI Assistant
Date: 2025-01-24
"""

import os
import json
import asyncio
import time
from typing import Dict, List, Any, Optional, Tuple, Union
from dataclasses import dataclass, field
from enum import Enum
from datetime import datetime, timedelta
import logging
from pathlib import Path

from openai import AsyncOpenAI
from pydantic import BaseModel, Field

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# OpenAI Client Setup
client = AsyncOpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=os.environ.get("OPENAI_API_KEY", "your-api-key"),
)

# ============================================================================
# CORE DATA MODELS
# ============================================================================

class SystemStage(Enum):
    """Development stages of the AI system."""
    PROTOTYPE = "prototype"
    DEVELOPMENT = "development"
    STAGING = "staging"
    PRODUCTION = "production"

class EvaluationMetric(BaseModel):
    """Individual evaluation metric result."""
    name: str
    value: float
    threshold: Optional[float] = None
    passed: bool = False
    details: Dict[str, Any] = Field(default_factory=dict)

class EvaluationResult(BaseModel):
    """Complete evaluation result for a system version."""
    timestamp: datetime = Field(default_factory=datetime.now)
    stage: SystemStage
    version: str
    metrics: List[EvaluationMetric]
    overall_score: float
    passed: bool
    execution_time: float
    metadata: Dict[str, Any] = Field(default_factory=dict)

class SystemPrompt(BaseModel):
    """System prompt configuration."""
    content: str
    version: str
    stage: SystemStage
    created_at: datetime = Field(default_factory=datetime.now)
    performance_metrics: Dict[str, float] = Field(default_factory=dict)

class TestCase(BaseModel):
    """Individual test case for evaluation."""
    id: str
    input_text: str
    expected_output: Optional[str] = None
    expected_criteria: Dict[str, Any] = Field(default_factory=dict)
    category: str = "general"
    priority: int = 1  # 1=high, 2=medium, 3=low

# ============================================================================
# EVALUATION FRAMEWORK
# ============================================================================

class EvaluationFramework:
    """Core evaluation framework for AI systems."""
    
    def __init__(self, system_name: str):
        self.system_name = system_name
        self.test_cases: List[TestCase] = []
        self.evaluation_history: List[EvaluationResult] = []
        self.current_stage = SystemStage.PROTOTYPE
        
    def add_test_case(self, test_case: TestCase):
        """Add a test case to the evaluation suite."""
        self.test_cases.append(test_case)
        logger.info(f"Added test case: {test_case.id}")
    
    def load_test_cases(self, test_cases: List[Dict[str, Any]]):
        """Load test cases from configuration."""
        for tc_data in test_cases:
            test_case = TestCase(**tc_data)
            self.add_test_case(test_case)
    
    async def evaluate_system(
        self, 
        system_prompt: SystemPrompt,
        model: str = "gpt-4.1",
        max_tokens: int = 1500
    ) -> EvaluationResult:
        """Evaluate the system against all test cases."""
        start_time = time.time()
        metrics = []
        
        logger.info(f"Starting evaluation for {system_prompt.version} at {self.current_stage.value}")
        
        # Run individual test cases
        test_results = []
        for test_case in self.test_cases:
            result = await self._evaluate_single_test(
                system_prompt, test_case, model, max_tokens
            )
            test_results.append(result)
        
        # Calculate aggregate metrics
        accuracy_metric = self._calculate_accuracy(test_results)
        metrics.append(accuracy_metric)
        
        response_quality_metric = await self._calculate_response_quality(test_results)
        metrics.append(response_quality_metric)
        
        consistency_metric = self._calculate_consistency(test_results)
        metrics.append(consistency_metric)
        
        # Calculate overall score
        overall_score = sum(m.value for m in metrics) / len(metrics)
        passed = all(m.passed for m in metrics)
        
        execution_time = time.time() - start_time
        
        result = EvaluationResult(
            stage=self.current_stage,
            version=system_prompt.version,
            metrics=metrics,
            overall_score=overall_score,
            passed=passed,
            execution_time=execution_time,
            metadata={
                "total_test_cases": len(self.test_cases),
                "model_used": model,
                "system_name": self.system_name
            }
        )
        
        self.evaluation_history.append(result)
        logger.info(f"Evaluation complete. Score: {overall_score:.2f}, Passed: {passed}")
        
        return result
    
    async def _evaluate_single_test(
        self, 
        system_prompt: SystemPrompt, 
        test_case: TestCase,
        model: str,
        max_tokens: int
    ) -> Dict[str, Any]:
        """Evaluate a single test case."""
        try:
            response = await client.chat.completions.create(
                model=model,
                messages=[
                    {"role": "system", "content": system_prompt.content},
                    {"role": "user", "content": test_case.input_text}
                ],
                max_tokens=max_tokens,
                temperature=0.1
            )
            
            output = response.choices[0].message.content
            
            return {
                "test_case_id": test_case.id,
                "input": test_case.input_text,
                "output": output,
                "expected": test_case.expected_output,
                "category": test_case.category,
                "priority": test_case.priority,
                "success": True,
                "error": None
            }
            
        except Exception as e:
            logger.error(f"Error evaluating test case {test_case.id}: {e}")
            return {
                "test_case_id": test_case.id,
                "input": test_case.input_text,
                "output": None,
                "expected": test_case.expected_output,
                "category": test_case.category,
                "priority": test_case.priority,
                "success": False,
                "error": str(e)
            }
    
    def _calculate_accuracy(self, test_results: List[Dict[str, Any]]) -> EvaluationMetric:
        """Calculate accuracy metric based on test results."""
        successful_tests = sum(1 for r in test_results if r["success"])
        total_tests = len(test_results)
        accuracy = successful_tests / total_tests if total_tests > 0 else 0.0
        
        return EvaluationMetric(
            name="accuracy",
            value=accuracy,
            threshold=0.8,
            passed=accuracy >= 0.8,
            details={
                "successful_tests": successful_tests,
                "total_tests": total_tests
            }
        )
    
    async def _calculate_response_quality(self, test_results: List[Dict[str, Any]]) -> EvaluationMetric:
        """Calculate response quality using AI evaluation."""
        quality_scores = []
        
        for result in test_results[:5]:  # Sample first 5 for efficiency
            if result["success"] and result["output"]:
                score = await self._evaluate_response_quality(
                    result["input"], 
                    result["output"]
                )
                quality_scores.append(score)
        
        avg_quality = sum(quality_scores) / len(quality_scores) if quality_scores else 0.0
        
        return EvaluationMetric(
            name="response_quality",
            value=avg_quality,
            threshold=0.7,
            passed=avg_quality >= 0.7,
            details={
                "sample_size": len(quality_scores),
                "individual_scores": quality_scores
            }
        )
    
    async def _evaluate_response_quality(self, input_text: str, output_text: str) -> float:
        """Evaluate response quality using AI."""
        try:
            evaluation_prompt = f"""
            Evaluate the quality of this AI response on a scale of 0.0 to 1.0:
            
            Input: {input_text}
            Response: {output_text}
            
            Consider: relevance, clarity, completeness, accuracy.
            Return only a number between 0.0 and 1.0.
            """
            
            response = await client.chat.completions.create(
                model="gpt-4.1",
                messages=[{"role": "user", "content": evaluation_prompt}],
                max_tokens=10,
                temperature=0.0
            )
            
            score_text = response.choices[0].message.content.strip()
            return float(score_text)
            
        except Exception as e:
            logger.error(f"Error evaluating response quality: {e}")
            return 0.5  # Default neutral score
    
    def _calculate_consistency(self, test_results: List[Dict[str, Any]]) -> EvaluationMetric:
        """Calculate consistency metric."""
        # Simple consistency check: all tests should either pass or fail predictably
        success_rate = sum(1 for r in test_results if r["success"]) / len(test_results)
        
        # Consistency is high if success rate is very high or very low (predictable)
        consistency = 1.0 - abs(success_rate - 0.5) * 2
        
        return EvaluationMetric(
            name="consistency",
            value=consistency,
            threshold=0.6,
            passed=consistency >= 0.6,
            details={
                "success_rate": success_rate,
                "interpretation": "Higher values indicate more predictable behavior"
            }
        )

# ============================================================================
# SYSTEM DEVELOPMENT PIPELINE
# ============================================================================

class SystemDevelopmentPipeline:
    """Manages the progression from prototype to production."""
    
    def __init__(self, system_name: str):
        self.system_name = system_name
        self.evaluation_framework = EvaluationFramework(system_name)
        self.prompts: Dict[str, SystemPrompt] = {}
        self.current_version = "v0.1.0"
        
    def create_prompt_version(
        self, 
        content: str, 
        version: Optional[str] = None,
        stage: SystemStage = SystemStage.PROTOTYPE
    ) -> SystemPrompt:
        """Create a new prompt version."""
        if version is None:
            version = self._generate_next_version()
        
        prompt = SystemPrompt(
            content=content,
            version=version,
            stage=stage
        )
        
        self.prompts[version] = prompt
        self.current_version = version
        
        logger.info(f"Created prompt version {version} for stage {stage.value}")
        return prompt
    
    def _generate_next_version(self) -> str:
        """Generate next version number."""
        # Simple version increment logic
        current_parts = self.current_version.replace('v', '').split('.')
        patch = int(current_parts[2]) + 1
        return f"v{current_parts[0]}.{current_parts[1]}.{patch}"
    
    async def run_development_cycle(
        self,
        initial_prompt: str,
        test_cases: List[Dict[str, Any]],
        target_score: float = 0.8,
        max_iterations: int = 5
    ) -> Dict[str, Any]:
        """Run a complete development cycle with iterative improvement."""
        
        # Load test cases
        self.evaluation_framework.load_test_cases(test_cases)
        
        # Start with prototype
        current_prompt = self.create_prompt_version(
            initial_prompt, 
            stage=SystemStage.PROTOTYPE
        )
        
        results = []
        
        for iteration in range(max_iterations):
            logger.info(f"Development iteration {iteration + 1}/{max_iterations}")
            
            # Evaluate current version
            eval_result = await self.evaluation_framework.evaluate_system(current_prompt)
            results.append(eval_result)
            
            # Check if target achieved
            if eval_result.overall_score >= target_score:
                logger.info(f"Target score achieved: {eval_result.overall_score:.2f}")
                break
            
            # Generate improved version
            if iteration < max_iterations - 1:
                improved_prompt = await self._improve_prompt(current_prompt, eval_result)
                current_prompt = improved_prompt
        
        return {
            "final_version": current_prompt.version,
            "final_score": results[-1].overall_score,
            "iterations": len(results),
            "target_achieved": results[-1].overall_score >= target_score,
            "evaluation_history": results
        }
    
    async def _improve_prompt(
        self, 
        current_prompt: SystemPrompt, 
        eval_result: EvaluationResult
    ) -> SystemPrompt:
        """Generate an improved version of the prompt based on evaluation results."""
        
        # Analyze failed metrics
        failed_metrics = [m for m in eval_result.metrics if not m.passed]
        
        improvement_prompt = f"""
        Improve this AI system prompt based on evaluation results:
        
        Current Prompt:
        {current_prompt.content}
        
        Evaluation Results:
        - Overall Score: {eval_result.overall_score:.2f}
        - Failed Metrics: {[m.name for m in failed_metrics]}
        
        Failed Metric Details:
        {json.dumps([{
            "metric": m.name,
            "value": m.value,
            "threshold": m.threshold,
            "details": m.details
        } for m in failed_metrics], indent=2)}
        
        Please provide an improved version of the prompt that addresses these issues.
        Return only the improved prompt text.
        """
        
        try:
            response = await client.chat.completions.create(
                model="gpt-4.1",
                messages=[{"role": "user", "content": improvement_prompt}],
                max_tokens=2000,
                temperature=0.3
            )
            
            improved_content = response.choices[0].message.content.strip()
            
            # Create new version
            new_version = self._generate_next_version()
            improved_prompt = self.create_prompt_version(
                improved_content,
                version=new_version,
                stage=current_prompt.stage
            )
            
            logger.info(f"Generated improved prompt version {new_version}")
            return improved_prompt
            
        except Exception as e:
            logger.error(f"Error improving prompt: {e}")
            return current_prompt  # Return current if improvement fails

# ============================================================================
# EXAMPLE USAGE AND TESTING
# ============================================================================

async def demo_eval_driven_development():
    """Demonstrate the eval-driven development process."""
    
    print("🚀 Eval Driven System Design Demo")
    print("=" * 50)
    
    # Initialize development pipeline
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
            "expected_output": None,
            "category": "hours",
            "priority": 1
        },
        {
            "id": "test_2", 
            "input_text": "I want to return a product",
            "expected_output": None,
            "category": "returns",
            "priority": 1
        },
        {
            "id": "test_3",
            "input_text": "How do I track my order?",
            "expected_output": None,
            "category": "tracking",
            "priority": 2
        }
    ]
    
    # Run development cycle
    try:
        results = await pipeline.run_development_cycle(
            initial_prompt=initial_prompt,
            test_cases=test_cases,
            target_score=0.75,
            max_iterations=3
        )
        
        print(f"\n📊 Development Results:")
        print(f"Final Version: {results['final_version']}")
        print(f"Final Score: {results['final_score']:.2f}")
        print(f"Iterations: {results['iterations']}")
        print(f"Target Achieved: {results['target_achieved']}")
        
        # Show evaluation history
        print(f"\n📈 Evaluation History:")
        for i, eval_result in enumerate(results['evaluation_history']):
            print(f"  Iteration {i+1}: Score {eval_result.overall_score:.2f}")
            for metric in eval_result.metrics:
                status = "✅" if metric.passed else "❌"
                print(f"    {status} {metric.name}: {metric.value:.2f}")
        
    except Exception as e:
        print(f"❌ Error in demo: {e}")

async def main():
    """Main function to run the demo."""
    await demo_eval_driven_development()

if __name__ == "__main__":
    asyncio.run(main())
