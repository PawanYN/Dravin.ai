## ✅ Summary

#### 1)Reasoning + Function Calling
---

##### **#How Model works in reasoning and function call - importance of it.**

Step	                What happens

1\. Model reasons	Creates a reasoning item — internal thoughts

2\. Model calls tool	Like calling a function to get real data

3\. You run the tool	Get the result (e.g. weather in Paris)

4\. You send back:	(a) result + (b) model’s reasoning

5\. Model continues smartly	Uses that reasoning to respond properly

##### 🧠 Simple Summary: Caching & Reasoning in Responses API

- Models like `o4-mini` generate two kinds of tokens:
  - **Reasoning tokens**: the model’s internal thought process
  - **Completion tokens**: the visible output message

- **Caching** helps reuse earlier results for faster and cheaper responses.

- In multi-turn conversations:
  - The model **does not reuse previous reasoning** by default.
  - However, you **can include them manually**, especially when tool use (e.g., function calling) is involved.
  - Including unused reasoning is harmless — the system ignores it if not needed.

- Caching **only benefits longer prompts** (more than 1024 tokens).

- Switching from the **Completions API to the Responses API** improves performance:
  - Cache hit rate increases from **40% to 80%**
  - Cached tokens are **up to 75% cheaper**
  - Resulting in **lower latency and reduced cost**

> 💡 Tip: Always include reasoning items when function/tool use is involved, to preserve model intelligence.


