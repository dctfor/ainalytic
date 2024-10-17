doc_prompt = """Analyze the provided code and generate comprehensive documentation following this structure:
1. MODULE OVERVIEW
- Purpose: {brief description}
- Key Dependencies: [list all import statements]
2. FOR EACH CLASS:
```
class ClassName(inheritance):
    Purpose: {what this class does}
    Attributes:
        attr_name (type): description
```
3. FOR EACH METHOD:
```python
def method_name(params) -> return_type:
    Description: Clear explanation of method's purpose
    Args:
        param_name (type): description
    Returns:
        type: description of return value
    Raises:
        ExceptionType: when/why
    Dependencies:
        - Internal calls: [all self.method() calls]
        - External calls: [all other function/method calls]
    Flow:
        1. First step
        2. Second step
    Example:
        >>> method_name(example_input)
        expected_output
```
REQUIREMENTS:
1. ALWAYS list ALL method calls, no matter how many
2. Use type hints
3. Flag any deprecated/internal methods with "_private" prefix
4. For each method, explicitly state if any attributes are modified
5. Mark any thread-safety issues or side effects
6. Use concrete types, never "object" or generic terms
FORMAT:
- Use Markdown code blocks for code
- Keep descriptions concise but complete
- No placeholder terms like "etc." or "and so on"
- Use bullet points for lists
- Include actual code examples
ERROR HANDLING:
If any part of the code is unclear or could have multiple interpretations, flag it with:
[CLARIFICATION NEEDED]: specific_question"""
