# Imports & API connection
from openai import OpenAI
from pydantic import BaseModel, Field
from typing import Any, Dict, Iterable, List, Optional
import tiktoken
import html
from html import escape  
import difflib
import sys
import os

from IPython.display import display, HTML

try:
    from IPython.display import HTML, display
    _IN_IPYTHON = True
except ImportError:
    _IN_IPYTHON = False

# Configuration
API_key = os.getenv("OPENAI_API_KEY")
client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=API_key
)
MODEL = "gpt-4.1"

# Data Models
class Instruction(BaseModel):
    instruction_title: str = Field(description="A 2-8 word title of the instruction that the LLM has to follow.")
    extracted_instruction: str = Field(description="The exact text that was extracted from the system prompt that the instruction is derived from.")

class InstructionList(BaseModel):
    instructions: list[Instruction] = Field(description="A list of instructions and their corresponding extracted text that the LLM has to follow.")

class CritiqueIssue(BaseModel):
    issue: str = Field(description="1-6 word label for the issue")
    snippet: str = Field(description="≤50-word excerpt from the prompt")
    explanation: str = Field(description="Why this issue matters")
    suggestion: str = Field(description="Actionable fix for the issue")

class CritiqueIssues(BaseModel):
    issues: List[CritiqueIssue] = Field(..., min_length=1, max_length=6, description="List of critique issues found in the prompt")

class Assistant:
    def __init__(self, name, model, tools, instructions):
        self.name = name
        self.model = model
        self.tools = tools
        self.instructions = instructions

# Constants
EXTRACT_INSTRUCTIONS_SYSTEM_PROMPT = """
## Role & Objective
You are an **Instruction-Extraction Assistant**.  
Your job is to read a System Prompt provided by the user and distill the **mandatory instructions** the target LLM must obey.

## Instructions
1. **Identify Mandatory Instructions**  
   • Locate every instruction in the System Prompt that the LLM is explicitly required to follow.  
   • Ignore suggestions, best-practice tips, or optional guidance.

2. **Generate Rules**  
   • Re-express each mandatory instruction as a clear, concise rule.
   • Provide the extracted text that the instruction is derived from.
   • Each rule must be standalone and imperative.

## Output Format
Return a json object with a list of instructions which contains an instruction_title and their corresponding extracted text that the LLM has to follow. Do not include any other text or comments.

## Constraints
- Include **only** rules that the System Prompt explicitly enforces.
- Omit any guidance that is merely encouraged, implied, or optional.
"""

CRITIQUE_SYSTEM_PROMPT = """
## Role & Objective
You are a **Prompt-Critique Assistant**.
Examine a user-supplied LLM prompt (targeting GPT-4.1 or compatible) and surface any weaknesses.

## Instructions
Check for the following issues:
- Ambiguity: Could any wording be interpreted in more than one way?
- Lacking Definitions: Are there any class labels, terms, or concepts that are not defined that might be misinterpreted by an LLM?
- Conflicting, missing, or vague instructions: Are directions incomplete or contradictory?
- Unstated assumptions: Does the prompt assume the model has to be able to do something that is not explicitly stated?

## Do **NOT** list issues of the following types:
- Invent new instructions, tool calls, or external information. You do not know what tools need to be added that are missing.
- Issues that you are not sure about.

## Output Format
Return a JSON object with an "issues" array containing 1-6 items, each following this schema:

{
  "issue":      "<1-6 word label>",
  "snippet":    "<≤50-word excerpt>",
  "explanation":"<Why it matters>",
  "suggestion": "<Actionable fix>"
}

If the prompt is already clear, complete, and effective, return an object with an empty issues array: {"issues": []}.
"""

REVISE_SYSTEM_PROMPT = """
## Role & Objective
Revise the user's original prompt to resolve most of the listed issues, while preserving the original wording and structure as much as possible.

## Instructions
1. Carefully review the original prompt and the list of issues.
2. Apply targeted edits directly addressing the listed issues. The edits should be as minimal as possible while still addressing the issue.
3. Do not introduce new content or make assumptions beyond the provided information.
4. Maintain the original structure and format of the prompt.

## Output Format
Return only the fully revised prompt. Do not include commentary, summaries, or code fences.
"""

SAMPLE_PROMPT = """
[System]
Please act as an impartial judge and evaluate the quality of the responses provided by two
AI assistants to the user question displayed below. You should choose the assistant that
follows the user's instructions and answers the user's question better. Your evaluation
should consider factors such as the helpfulness, relevance, accuracy, depth, creativity,
and level of detail of their responses. Begin your evaluation by comparing the two
responses and provide a short explanation. Avoid any position biases and ensure that the
order in which the responses were presented does not influence your decision. Do not allow
the length of the responses to influence your evaluation. Do not favor certain names of
the assistants. Be as objective as possible. After providing your explanation, output your
final verdict by strictly following this format: "[[A]]" if assistant A is better, "[[B]]"
if assistant B is better, and "[[C]]" for a tie.

[User Question]
{question}

[The Start of Assistant A's Answer]
{answer_a}
[The End of Assistant A's Answer]

[The Start of Assistant B's Answer]
{answer_b}
[The End of Assistant B's Answer]
"""

# Display and diff utilities for prompt migration
_COLORS = {
    '+': ("#d2f5d6", "#22863a"),   # additions  (green)
    '-': ("#f8d7da", "#b31d28"),   # deletions  (red)
    '@': (None,      "#6f42c1"),   # hunk header (purple)
}

def _css(**rules: str) -> str:
    """Convert kwargs to a CSS string (snake_case → kebab-case)."""
    return ";".join(f"{k.replace('_', '-')}: {v}" for k, v in rules.items())

def _render(html_str: str) -> None:
    """Render inside Jupyter if available, else save to file."""
    # Always save to file for browser viewing
    with open("Prompt_Migration_Guide_Refactored_output.html", "a", encoding="utf-8") as f:
        f.write(html_str + "\n\n")

    # Also try to display in Jupyter if available
    try:
        display  # type: ignore[name-defined]
        from IPython.display import HTML  # noqa: WPS433
        display(HTML(html_str))
    except NameError:
        print("HTML content saved to Prompt_Migration_Guide_Refactored_output.html", flush=True)

# ---------- diff helpers ------------------------------------------------------

def _style(line: str) -> str:
    """Wrap a diff line in a <span> with optional colors."""
    bg, fg = _COLORS.get(line[:1], (None, None))
    css = ";".join(s for s in (f"background:{bg}" if bg else "",
                               f"color:{fg}" if fg else "") if s)
    return f'<span style="{css}">{html.escape(line)}</span>'

def _wrap(lines: Iterable[str]) -> str:
    body = "<br>".join(lines)
    return (
        "<details>"
        "<summary>🕵️‍♂️ Critique & Diff (click to expand)</summary>"
        f'<div style="font-family:monospace;white-space:pre;">{body}</div>'
        "</details>"
    )

def show_critique_and_diff(old: str, new: str) -> str:
    """Display & return a GitHub-style HTML diff between *old* and *new*."""
    diff = difflib.unified_diff(old.splitlines(), new.splitlines(),
                                fromfile="old", tofile="new", lineterm="")
    html_block = _wrap(map(_style, diff))
    _render(html_block)
    return html_block

# ---------- "card" helpers ----------------------------------------------------

CARD    = _css(background="#f8f9fa", border_radius="8px", padding="18px 22px",
               margin_bottom="18px", border="1px solid #e0e0e0",
               box_shadow="0 1px 4px #0001")
TITLE   = _css(font_weight="600", font_size="1.1em", color="#2d3748",
               margin_bottom="6px")
LABEL   = _css(color="#718096", font_size="0.95em", font_weight="500",
               margin_right="6px")
EXTRACT = _css(font_family="monospace", background="#f1f5f9", padding="7px 10px",
               border_radius="5px", display="block", margin_top="3px",
               white_space="pre-wrap", color="#1a202c")

def display_cards(
    items: Iterable[Any],
    *,
    title_attr: str,
    field_labels: Optional[Dict[str, str]] = None,
    card_title_prefix: str = "Item",
) -> None:
    """Render objects as HTML "cards" (or plaintext when not in IPython)."""
    items = list(items)
    if not items:
        _render("<em>No data to display.</em>")
        return

    # auto-derive field labels if none supplied
    if field_labels is None:
        sample = items[0]
        field_labels = {
            a: a.replace("_", " ").title()
            for a in dir(sample)
            if not a.startswith("_")
            and not callable(getattr(sample, a))
            and a != title_attr
        }

    cards = []
    for idx, obj in enumerate(items, 1):
        title_html = html.escape(str(getattr(obj, title_attr, "<missing title>")))
        rows = [f'<div style="{TITLE}">{card_title_prefix} {idx}: {title_html}</div>']

        for attr, label in field_labels.items():
            value = getattr(obj, attr, None)
            if value is None:
                continue
            rows.append(
                f'<div><span style="{LABEL}">{html.escape(label)}:</span>'
                f'<span style="{EXTRACT}">{html.escape(str(value))}</span></div>'
            )

        cards.append(f'<div style="{CARD}">{"".join(rows)}</div>')

    _render("\n".join(cards))

# Utility Functions
def initialize_html_file():
    """Initialize the HTML output file with proper structure."""
    with open("Prompt_Migration_Guide_Refactored_output.html", "w", encoding="utf-8") as f:
        f.write("""<!DOCTYPE html>
<html>
<head>
    <title>Prompt Migration Guide Output</title>
    <meta charset="utf-8">
    <style>
        body { font-family: Arial, sans-serif; margin: 20px; background: #f5f5f5; }
        .container { max-width: 1200px; margin: 0 auto; background: white; padding: 20px; border-radius: 8px; }
        h1 { color: #333; border-bottom: 2px solid #007acc; padding-bottom: 10px; }
    </style>
</head>
<body>
    <div class="container">
        <h1>Prompt Migration Guide Output</h1>
""")

def finalize_html_file():
    """Close the HTML file with proper structure."""
    with open("Prompt_Migration_Guide_Refactored_output.html", "a", encoding="utf-8") as f:
        f.write("""
    </div>
</body>
</html>""")



def count_tokens(text: str, model: str = "gpt-4") -> int:
    """Count tokens in the given text."""
    encoding = tiktoken.encoding_for_model(model)
    return len(encoding.encode(text))

def extract_instructions(prompt: str) -> InstructionList:
    """Extract instructions from a system prompt using AI."""
    response = client.beta.chat.completions.parse(
        model=MODEL,
        messages=[
            {"role": "system", "content": EXTRACT_INSTRUCTIONS_SYSTEM_PROMPT},
            {"role": "user", "content": "SYSTEM_PROMPT TO ANALYZE: " + prompt}
        ],
        temperature=0.0,
        max_tokens=2000,  # Reduced to stay within credit limits
        response_format=InstructionList,
    )
    return response.choices[0].message.parsed

def critique_prompt(prompt: str) -> CritiqueIssues:
    """Critique a prompt for clarity, completeness, and effectiveness."""
    critique_user_prompt = f"""
Evaluate the following prompt for clarity, completeness, and effectiveness:
###
{prompt}
###
Return your critique using the specified JSON format only.
"""

    response = client.beta.chat.completions.parse(
        model=MODEL,
        messages=[
            {"role": "system", "content": CRITIQUE_SYSTEM_PROMPT},
            {"role": "user", "content": critique_user_prompt}
        ],
        temperature=0.0,
        max_tokens=2000,
        response_format=CritiqueIssues,
    )
    return response.choices[0].message.parsed

def revise_prompt(original_prompt: str, issues_str: str) -> str:
    """Revise a prompt to address the identified issues."""
    revise_user_prompt = f"""
Here is the original prompt:
---
{original_prompt}
---

Here are the issues to fix:
{issues_str}

Please return **only** the fully revised prompt. Do not include commentary, summaries, or explanations.
"""

    response = client.chat.completions.create(
        model=MODEL,
        messages=[
            {"role": "system", "content": REVISE_SYSTEM_PROMPT},
            {"role": "user", "content": revise_user_prompt}
        ],
        temperature=0.0,
        max_tokens=2000
    )
    return response.choices[0].message.content

def main():
    """Main function to run the prompt migration guide."""
    # Initialize HTML output
    initialize_html_file()
    
    print(f"Client initialized with model: {MODEL}")
    print(f"Base URL: {client.base_url}")

    # Compare old vs new assistant configuration
    old_config = "tools: [{'type': 'retrieval'}]"
    new_config = "tools: [{'type': 'file_search'}]"
    show_critique_and_diff(old_config, new_config)

    # Analyze sample prompt
    token_count = count_tokens(SAMPLE_PROMPT)
    print(f"Original prompt length: {token_count} tokens")

    # Extract instructions from the prompt
    instructions_list = extract_instructions(SAMPLE_PROMPT)

    # Display the extracted instructions
    display_cards(
        instructions_list.instructions,
        title_attr="instruction_title",
        field_labels={"extracted_instruction": "Extracted Text"},
        card_title_prefix="Instruction"
    )

    # Critique the prompt for issues
    print("\n🔍 Analyzing prompt for potential issues...")
    critique_result = critique_prompt(SAMPLE_PROMPT)

    if critique_result.issues:
        print(f"Found {len(critique_result.issues)} potential issues")
        display_cards(
            critique_result.issues,
            title_attr="issue",
            field_labels={
                "snippet": "Problematic Snippet",
                "explanation": "Why This Matters",
                "suggestion": "Suggested Fix"
            },
            card_title_prefix="Issue"
        )
    else:
        _render("<div style='padding: 20px; background: #d4edda; border: 1px solid #c3e6cb; border-radius: 8px; color: #155724;'><strong>✅ No Issues Found!</strong><br>The prompt appears to be clear, complete, and effective.</div>")
        print("✅ No issues found in the prompt!")

    # Finalize HTML output
    finalize_html_file()

    print("\n✅ Complete HTML output saved to 'Prompt_Migration_Guide_Refactored_output.html'")
    print("📂 Open 'Prompt_Migration_Guide_Refactored_output.html' in your browser to see the visual results!")
    print("💡 To serve locally: python -m http.server 8000")
    
    # Create a string of the issues
    issues_str = "\n".join(
        f"Issue: {issue.issue}\nSnippet: {issue.snippet}\nExplanation: {issue.explanation}\nSuggestion: {issue.suggestion}\n"
        for issue in critique_result.issues
    )

    print(issues_str)

    # Generate revised prompt if issues were found
    if critique_result.issues:
        print("\n🔄 Generating revised prompt...")
        revised_prompt = revise_prompt(SAMPLE_PROMPT, issues_str)
        print("\n🔄 Revised prompt:\n------------------")
        print(revised_prompt)

if __name__ == "__main__":
    main()
