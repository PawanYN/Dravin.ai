# Import required modules
from openai import AsyncOpenAI
import asyncio
import json
import os
from enum import Enum
from typing import Any, List, Dict
from pydantic import BaseModel, Field
# from agents import Agent, Runner, set_default_openai_client, trace  # Package not available

# OpenAI Client Setup
client = AsyncOpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=os.environ.get("OPENAI_API_KEY", "your-api-key"),
)

# Data Models
class Role(str, Enum):
    """Role enum for chat messages."""
    user = "user"
    assistant = "assistant"

class ChatMessage(BaseModel):
    """Single chat message used in few-shot examples."""
    role: Role
    content: str

class Issues(BaseModel):
    """Structured output returned by checkers."""
    has_issues: bool
    issues: List[str]

    @classmethod
    def no_issues(cls) -> "Issues":
        return cls(has_issues=False, issues=[])

class FewShotIssues(Issues):
    """Output for few-shot contradiction detector including optional rewrite suggestions."""
    rewrite_suggestions: List[str] = Field(default_factory=list)

    @classmethod
    def no_issues(cls) -> "FewShotIssues":
        return cls(has_issues=False, issues=[], rewrite_suggestions=[])

class MessagesOutput(BaseModel):
    """Structured output returned by `rewrite_messages_agent`."""

    messages: list[ChatMessage]


class DevRewriteOutput(BaseModel):
    """Rewriter returns the cleaned-up developer prompt."""

    new_developer_message: str

# Agent Instructions
CONTRADICTION_CHECKER_INSTRUCTIONS = """
You are **Dev-Contradiction-Checker**.

Goal
Detect *genuine* self-contradictions or impossibilities **inside** the developer prompt supplied in the variable `DEVELOPER_MESSAGE`.

Definitions
• A contradiction = two clauses that cannot both be followed.
• Overlaps or redundancies in the DEVELOPER_MESSAGE are *not* contradictions.

What you MUST do
1. Compare every imperative / prohibition against all others.
2. List at most FIVE contradictions (each as ONE bullet).
3. If no contradiction exists, say so.

Output format (**strict JSON**)
Return **only** an object that matches the `Issues` schema:

```json
{"has_issues": <bool>,
"issues": [
    "<bullet 1>",
    "<bullet 2>"
]
}
- has_issues = true IFF the issues array is non-empty.
- Do not add extra keys, comments or markdown.
"""

FEWSHOT_CONSISTENCY_CHECKER_INSTRUCTIONS = """
You are FewShot-Consistency-Checker.

Goal
Find conflicts between the DEVELOPER_MESSAGE rules and the accompanying **assistant** examples.

USER_EXAMPLES:      <all user lines>          # context only
ASSISTANT_EXAMPLES: <all assistant lines>     # to be evaluated

Method
Extract key constraints from DEVELOPER_MESSAGE:
- Tone / style
- Forbidden or mandated content
- Output format requirements

Compliance Rubric - read carefully
Evaluate only what the developer message makes explicit.

Objective constraints you must check when present:
- Required output type syntax (e.g., "JSON object", "single sentence", "subject line").
- Hard limits (length ≤ N chars, language required to be English, forbidden words, etc.).
- Mandatory tokens or fields the developer explicitly names.

Out-of-scope (DO NOT FLAG):
- Whether the reply "sounds generic", "repeats the prompt", or "fully reflects the user's request" - unless the developer text explicitly demands those qualities.
- Creative style, marketing quality, or depth of content unless stated.
- Minor stylistic choices (capitalisation, punctuation) that do not violate an explicit rule.

Pass/Fail rule
- If an assistant reply satisfies all objective constraints, it is compliant, even if you personally find it bland or loosely related.
- Only record an issue when a concrete, quoted rule is broken.

Empty assistant list ⇒ immediately return has_issues=false.

For each assistant example:
- USER_EXAMPLES are for context only; never use them to judge compliance.
- Judge each assistant reply solely against the explicit constraints you extracted from the developer message.
- If a reply breaks a specific, quoted rule, add a line explaining which rule it breaks.
- Optionally, suggest a rewrite in one short sentence (add to rewrite_suggestions).
- If you are uncertain, do not flag an issue.
- Be conservative—uncertain or ambiguous cases are not issues.

be a little bit more conservative in flagging few shot contradiction issues
Output format
Return JSON matching FewShotIssues:

{
"has_issues": <bool>,
"issues": ["<explanation 1>", "..."],
"rewrite_suggestions": ["<suggestion 1>", "..."] // may be []
}
List max five items for both arrays.
Provide empty arrays when none.
No markdown, no extra keys.
"""

# Utility Functions
def _normalize_messages(messages: List[Any]) -> List[Dict[str, str]]:
    """Convert list of pydantic message models to JSON-serializable dicts."""
    result = []
    for m in messages:
        if hasattr(m, "model_dump"):
            result.append(m.model_dump())
        elif isinstance(m, dict) and "role" in m and "content" in m:
            result.append({"role": str(m["role"]), "content": str(m["content"])})
    return result

# Core Optimization Function
async def optimize_prompt_parallel(
    developer_message: str,
    messages: List[ChatMessage],
) -> Dict[str, Any]:
    """
    Runs contradiction, format, and few-shot checkers in parallel,
    then rewrites the prompt/examples if needed.
    Returns a unified dict suitable for an API or endpoint.
    """

    print("🔍 Starting prompt optimization...")

    # 1. Run all checkers in parallel (contradiction, format, fewshot if there are examples)
    tasks = []

    # Always run contradiction and format checkers
    tasks.append(evaluate_contradiction_checker(developer_message))

    # Run few-shot checker if messages exist
    if messages:
        tasks.append(evaluate_fewshot_consistency_checker(developer_message, messages))
    else:
        tasks.append(asyncio.create_task(asyncio.sleep(0, result=FewShotIssues.no_issues())))

    results = await asyncio.gather(*tasks)

    # Unpack results
    cd_issues: Issues = results[0]
    fs_issues: FewShotIssues = results[1] if messages else FewShotIssues.no_issues()

    print(f"✅ Analysis complete:")
    print(f"   - Contradiction issues: {cd_issues.has_issues}")
    print(f"   - Few-shot issues: {fs_issues.has_issues}")

    # 3. For now, return the analysis results (rewriting can be added later)
    final_prompt = developer_message
    final_messages = messages

    return {
        "changes": cd_issues.has_issues or fs_issues.has_issues,
        "new_developer_message": final_prompt,
        "new_messages": _normalize_messages(final_messages),
        "contradiction_issues": "\n".join(cd_issues.issues),
        "few_shot_contradiction_issues": "\n".join(fs_issues.issues),
        "format_issues": "",  # Format checker not implemented yet
    }

# Evaluation Functions (for testing)
async def evaluate_contradiction_checker(developer_message: str) -> Issues:
    """Evaluate the contradiction checker agent."""

    response = await client.beta.chat.completions.parse(
        model="gpt-4.1",
        messages=[
            {"role": "system", "content": CONTRADICTION_CHECKER_INSTRUCTIONS},
            {"role": "user", "content": f"DEVELOPER_MESSAGE: {developer_message}"}
        ],
        response_format=Issues,
        temperature=0.0,
        max_tokens=1500
    )

    return response.choices[0].message.parsed

async def evaluate_fewshot_consistency_checker(developer_message: str, messages: List[ChatMessage]) -> FewShotIssues:
    """Evaluate the few-shot consistency checker agent."""

    # Separate user and assistant examples
    user_examples = [msg.content for msg in messages if msg.role == Role.user]
    assistant_examples = [msg.content for msg in messages if msg.role == Role.assistant]

    prompt = f"""DEVELOPER_MESSAGE: {developer_message}

USER_EXAMPLES: {user_examples}
ASSISTANT_EXAMPLES: {assistant_examples}"""

    response = await client.beta.chat.completions.parse(
        model="gpt-4.1",
        messages=[
            {"role": "system", "content": FEWSHOT_CONSISTENCY_CHECKER_INSTRUCTIONS},
            {"role": "user", "content": prompt}
        ],
        response_format=FewShotIssues,
        temperature=0.0,
        max_tokens=1500
    )

    return response.choices[0].message.parsed

async def run_optimization_tests():
    """Run optimization tests using the complete pipeline."""
    print("� Testing Complete Prompt Optimization Pipeline\n")

    # Test 1: Contradiction Issues
    print("=" * 60)
    print("TEST 1: Optimization with Contradiction Issues")
    print("=" * 60)

    contradiction_example = {
        "developer_message": "Always answer in **English**.\nNunca respondas en inglés.",
        "messages": [
            ChatMessage(role=Role.user, content="¿Qué hora es?")
        ]
    }

    print(f"Developer Message: {contradiction_example['developer_message']}")
    print(f"Messages: {len(contradiction_example['messages'])} message(s)")

    try:
        result = await optimize_prompt_parallel(
            contradiction_example['developer_message'],
            contradiction_example['messages']
        )

        print(f"\n📊 Optimization Results:")
        print(f"Changes Made: {result['changes']}")
        print(f"Contradiction Issues: {result['contradiction_issues'] or 'None'}")
        print(f"Few-shot Issues: {result['few_shot_contradiction_issues'] or 'None'}")

    except Exception as e:
        print(f"❌ Error in optimization: {e}")

    # Test 2: Few-shot Consistency Issues
    print("\n" + "=" * 60)
    print("TEST 2: Optimization with Few-shot Issues")
    print("=" * 60)

    fewshot_example = {
        "developer_message": "Respond with **only 'yes' or 'no'** – no explanations.",
        "messages": [
            ChatMessage(role=Role.user, content="Is the sky blue?"),
            ChatMessage(role=Role.assistant, content="Yes, because wavelengths …"),
            ChatMessage(role=Role.user, content="Is water wet?"),
            ChatMessage(role=Role.assistant, content="Yes.")
        ]
    }

    print(f"Developer Message: {fewshot_example['developer_message']}")
    print(f"Messages: {len(fewshot_example['messages'])} message(s)")

    try:
        result = await optimize_prompt_parallel(
            fewshot_example['developer_message'],
            fewshot_example['messages']
        )

        print(f"\n📊 Optimization Results:")
        print(f"Changes Made: {result['changes']}")
        print(f"Contradiction Issues: {result['contradiction_issues'] or 'None'}")
        print(f"Few-shot Issues: {result['few_shot_contradiction_issues'] or 'None'}")

        if result['new_messages']:
            print(f"\nOptimized Messages:")
            for i, msg in enumerate(result['new_messages'], 1):
                print(f"  {i}. {msg['role']}: {msg['content']}")

    except Exception as e:
        print(f"❌ Error in optimization: {e}")

    # Test 3: Clean Prompt (No Issues)
    print("\n" + "=" * 60)
    print("TEST 3: Clean Prompt (Should have no issues)")
    print("=" * 60)

    clean_example = {
        "developer_message": "You are a helpful assistant. Answer questions clearly and concisely.",
        "messages": [
            ChatMessage(role=Role.user, content="What is the capital of France?"),
            ChatMessage(role=Role.assistant, content="The capital of France is Paris.")
        ]
    }

    print(f"Developer Message: {clean_example['developer_message']}")
    print(f"Messages: {len(clean_example['messages'])} message(s)")

    try:
        result = await optimize_prompt_parallel(
            clean_example['developer_message'],
            clean_example['messages']
        )

        print(f"\n📊 Optimization Results:")
        print(f"Changes Made: {result['changes']}")
        print(f"Contradiction Issues: {result['contradiction_issues'] or 'None'}")
        print(f"Few-shot Issues: {result['few_shot_contradiction_issues'] or 'None'}")

    except Exception as e:
        print(f"❌ Error in optimization: {e}")

    print("\n" + "=" * 60)
    print("🎉 Optimization Pipeline Testing Complete!")
    print("=" * 60)

async def main():
    """Main function to run the prompt optimization pipeline."""
    await run_optimization_tests()

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())