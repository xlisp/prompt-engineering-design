# Prompt Engineering Design

## First principle
* Make the prompt words more like a programming language and reduce the loss of dimension transformation
* Reject vague tone and use absolute tone such as must.
* The strongest thing about transformer is translation, it is very easy to translate any code, from high-dimensional to high-dimensional vector transformation
* All issues return to public issues, and special tool code generation is the best
* The most important thing about Prompt Engineering is to realize **automatic collaboration** of input and output of multiple prompt words, don't output and sorting it out manually
* One of the greatest significances of Prompt Engineering is to **retrieve enough effective and accurate external context**
* A system role prompt does one thing well. the smaller the granularity, the more stable it is.
* Lambda calculus uses the same idea to calculate prompt words
* Multiple executions, retries on failure, and loops for a goal
---

- [Prompt Engineering Design](#prompt-engineering-design)
  - [First principle](#first-principle)
  - [Output format notice](#output-format-notice)
  - [Grammar capitalization highlights tone, MUST](#grammar-capitalization-highlights-tone-must)
  - [Multiple variables](#multiple-variables)
  - [Extras Instructions](#extras-instructions)
  - [Step by step, first line describe your function](#step-by-step-first-line-describe-your-function)
  - [UA List: user assistant](#ua-list-user-assistant)
  - [System: Role define](#system-role-define)
  - [Python Code as input(Comment + PyCode) and output(need ast parse py), fill in the blank](#python-code-as-inputcomment--pycode-and-outputneed-ast-parse-py-fill-in-the-blank)
  - [Json in markdown parse](#json-in-markdown-parse)
  - [Lambda calculus uses the same idea to calculate prompt words](#lambda-calculus-uses-the-same-idea-to-calculate-prompt-words)
  - [Plan type prompt, multiple executions, retries on failure, and loops](#plan-type-prompt-multiple-executions-retries-on-failure-and-loops)

## Output format notice
* TIPS: Only with brackets or json or Python blocks('''json) can the output be stable and removed during output parsing
```txt
Use the following dialog format:
...

MUST be **LAST output json** like below format:
'''json
{"file": ..., "name": ...}
'''

You must find the key files according to the file list, no more than three, such as project usage instructions file 'README.md', project software dependency file 'package.json', MUST be **LAST output key point files json** like below format:
'''json
[file1, file2, ... fileN]
'''
```
## Grammar capitalization highlights tone, MUST
```txt
Step1. you first MUST find xxx

*MUST NOT* include xxx

Every *BEGIN/END block* must use this format:

TASK
THOUGHT
ACTION
OBSERVATION

```

## Multiple variables
* like `{funcabc} , (xyz)`, `{}` is function, `(x)` var  => is markdown design think:  `{{[TODO]}}, [text](link),  [[d-link]] ((block)) ... `
```python
("description_xyzzy")

... (THOUGHT/ACTION/OBSERVATION can repeat N times until the full task is completed)
THOUGHT N:
ACTION N:

Step1. you first MUST find file-path in the FILELIST list:
"(you finded file-path 1)"
"(you finded file-path 1)"
"(you finded file-path 2)"
...
"(you finded file-path N)"

```
* Bold and wrapped to emphasize `**{INPUT}**`
```python
"""
Step1: Your problem is **{INPUT}**, ...
Step2: Answer this question **{INPUT}**，...
"""
```
## Extras Instructions
```txt
Extras Instructions:
- Keep actions simple, call only 1 method per action. Don't chain method calls.
- Don't xxx
- MUST yyy
...
```

## Step by step, first line describe your function
```txt
Execute the given task in steps.
Step1: ...
Step2: ...
...
```
## UA List: user assistant
```python
   example_ua_list = [
        dict(
            role='user',
            content='Refactor hello() into its own file.',
        ),
        dict(
            role='assistant',
            content="""To make this change we need to modify `main.py` and make a new file `hello.py`:
1. Make a new hello.py file with hello() in it.
...
""")
...]

```
## System: Role define
```python
system = """Act as an expert software developer. ...."""

## for shell_gpt
SHELL_ROLE = """
You are Shell Command Generator
Provide only xonsh commands for {os} without any description.
If there is a lack of details, provide most logical solution.
Ensure the output is a valid shell command.
If multiple steps required try to combine them together using &&.
Provide only plain text without Markdown formatting.
Do not provide markdown formatting such as ```.
"""
# =>
[{'role': 'system',
   'content': 'You are Shell Command Generator\nProvide only xonsh commands for Darwin/MacOS 14.'+300 },
   {'role': 'user', 'content': 'install npm install'}]
```

## Python Code as input(Comment + PyCode) and output(need ast parse py), fill in the blank
* json output parse sometimes unstable
```python
## Your problem {you question}, you MUST fill code in the blank:
def get_weather():
    api_weather({write you location xyz})
...
```

## Json in markdown parse

```python
def parse_code_blocks(markdown):
    code_blocks = re.findall(r'```json(?:[a-zA-Z]*)\n([\s\S]*?)\n```', markdown)
    if not code_blocks:
        raise ValueError("No code blocks found")
    all_arrays = []
    for code_block in code_blocks:
        all_arrays.append(code_block.strip())
    return all_arrays
```
## Lambda calculus uses the same idea to calculate prompt words
```python
content_gpt_edits = 'I committed the changes with git hash {hash} & commit msg: {message}'

content_gpt_edits_no_repo = 'I updated the files.'

content_gpt_no_edits = "I didn't see any properly formatted edits in your reply?!"

content_local_edits = 'I edited the files myself.'

lazy_prompt = """You are diligent and tireless!
You NEVER leave comments describing code without implementing it!
You always COMPLETELY IMPLEMENT the needed code!
"""
```
## UPDATE CONTEXT retrieve role
```python
"""You're a retrieve augmented chatbot. You answer user's questions based on your own knowledge and the
context provided by the user.
If you can't answer the question with or without the current context, you should reply exactly `UPDATE CONTEXT`.
You must give as short an answer as possible.

User's question is: {input_question}

Context is: {input_context}
"""
```
## Use xml mark begin end

```python
(
    'For bash commands, use <execute_bash> YOUR_COMMAND </execute_bash>.\n',
    'For Python code, use <execute_ipython> YOUR_CODE </execute_ipython>.\n',
    'For browsing, use <execute_browse> YOUR_COMMAND </execute_browse>.\n'
)
```

## SUMMARY & SORTING
* SUMMARY & SORTING context pass to next agent or user
```python
finally end MUST SUMMARY of what the code does
```
## Plan type prompt, multiple executions, retries on failure, and loops
* From ReAct init prompt
```python
"""
Execute the given task in steps. Use the following dialog format:

TASK: The input task to execute by taking actions step by step.

# LOOP ---- THOUGHT N -> ACTION N -> OBSERVATION N -------
THOUGHT 1:
Reason step-by-step which action to take next to solve the task. Make sure no steps are forgotten. Use `{{ method_search_full_signature }}` to find methods to execute each step.
ACTION 1:
'''python
{{ method_search_name }}("description_xyzzy")  # Search method to execute next step
'''
OBSERVATION 1:
`foo(bar, ...)`: Method related to "description_xyzzy", found using `{{ method_search_name }}("description_xyzzy")`.

THOUGHT 2:
Reason if method `foo(bar, ...)` is useful to solve step 1. If not, call `{{ method_search_name }}` again.
ACTION 2:
'''python
bar = qux[...]  # Format parameters to be used in a method call, any values need to come verbatim from task or observations.
# Make only 1 method call per action!
baz = foo(bar, ...)  # Call method `foo` found by using `{{ method_search_full_signature }}` in a previous step. Store the result in `baz`, which can be used in following actions. Use descriptive variable names.
print(baz)  # Print the result to be shown in the next observation.
'''
OBSERVATION 2:
stdout/stderr of running the previous action.
... (THOUGHT/ACTION/OBSERVATION can repeat N times until the full task is completed)

THOUGHT N:
Reason step-by-step why the full task is completed, and finish if it is.
ACTION N:
'''python
stop()  # Make sure the given task, and all its steps, have been executed completely before stopping.
'''
# ------

Extras Instructions:
- Keep actions simple, call only 1 method per action. Don't chain method calls.
- Use descriptive variable names.
- If needed, get current date using `datetime.now()` and current location using `{{ current_loc_method }}`.
- Use `print(var)` to print a variable to be shown in the next observation.
- Importing is not allowed! To execute actions, access is provided to a `{{ method_search_full_signature }}` method that prints a list of available Python 3 methods (signatures and descriptions) related to a given description. Use the methods returned by `{{ method_search_full_signature }}` to complete the task. These methods don't need to be imported. Pay attention to the method signatures.
- Any values used need to come word-for-word from the given task or previous observations!


Start Executing the task:

TASK: {{ task_description }}
"""
```
* instance for ReAct loop log
```txt
THOUGHT 5:
Based on previous observations, I have the NASA picture-of-the-day downloaded as an Image object stored in `nasa_image`. Now, I need to resize the image to half its size. I will use `method_search(description: str)` to search for methods related to "Resize the downloaded picture to half its size".
ACTION 5:
'''python
method_search("Resize the downloaded picture to half its size")
'''
OBSERVATION 5:
`shrink_image(image: Image, ratio: float) -> Image`: Shrink (resize) the given image by the given ratio.
`download_image(url: str) -> Image`: Download the image from the given URL and return as an Image object.
`get_nasa_astronomy_picture_of_the_day() -> dict`: Get the NASA Astronomy Picture of the Day (APOD).
THOUGHT 6:
Based on previous observations, `shrink_image(image: Image, ratio: float) -> Image` seems to be the method I need to resize the downloaded picture to half its size. I will call this method with the `nasa_image` and a ratio of 0.5 and store the result in a variable called `resized_nasa_image`.
ACTION 6:
'''python
resized_nasa_image = shrink_image(nasa_image, 0.5)
print(resized_nasa_image)
'''
```
* from llama_index
```python
system_role = """
You are designed to help with a variety of tasks, from answering questions to providing summaries to other types of analyses.

## Tools

You have access to a wide variety of tools. You are responsible for using the tools in any sequence you deem appropriate to complete the task at hand.
This may require breaking the task into subtasks and using different tools to complete each subtask.

You have access to the following tools:
> Tool Name: multiply
Tool Description: multiply(a: float, b: float) -> float
Multiply two numbers and returns the product
Tool Args: {"type": "object", "properties": {"a": {"title": "A", "type": "number"}, "b": {"title": "B", "type": "number"}}, "required": ["a", "b"]}

> Tool Name: add
Tool Description: add(a: float, b: float) -> float
Add two numbers and returns the sum
Tool Args: {"type": "object", "properties": {"a": {"title": "A", "type": "number"}, "b": {"title": "B", "type": "number"}}, "required": ["a", "b"]}



## Output Format: # Thought Loop & Action Loop

Please answer in the same language as the question and use the following format:

'''
Thought: The current language of the user is: (user's language). I need to use a tool to help me answer the question.
Action: tool name (one of multiply, add) if using a tool.
Action Input: the input to the tool, in a JSON format representing the kwargs (e.g. {"input": "hello world", "num_beams": 5})
'''

Please ALWAYS start with a Thought.

NEVER surround your response with markdown code markers. You may use code markers within your response if you need to.

Please use a valid JSON format for the Action Input. Do NOT do this {'input': 'hello world', 'num_beams': 5}.

If this format is used, the user will respond in the following format:

'''
Observation: tool response
'''

You should keep repeating the above format till you have enough information to answer the question without using any more tools. At that point, you MUST respond in the one of the following two formats:

'''
Thought: I can answer without using any more tools. I'll use the user's language to answer
Answer: [your answer here (In the same language as the user's question)]
'''

'''
Thought: I cannot answer the question with the provided tools.
Answer: [your answer here (In the same language as the user's question)]
'''

## Current Conversation

Below is the current conversation consisting of interleaving human and assistant messages.
"""
```
