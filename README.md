# Chain of Thoughts: step solving model structure
**A model arrangement that can solve complex problems by using steps.**

**Working**:
1) first model takes the user's question, breaks it down into smaller tasks, and stores the tasks in an array, and also stores instructions for "assembling" the final answer.

2) models solve the question in pieces by solving the smaller tasks, and appends the responses.

3) a final model takes all the small responses and assembles them seamlessly using the instructions given by original model

Benefit over standalone models:
**Ability to solve complex tasks** standalone models cannot solve complex tasks on it's own, this structure's ability to divide tasks and solve them in parallel enables complex problem solving.

*Note*: code uses perplexity API documentation, refer to your documentation to use the model.
