from prompts.programming import BASE_PROMPT, LANGUAGE_PROMPTS

def build_programming_prompt(language: str) -> str:
    base = BASE_PROMPT.format(language=language)
    extra = LANGUAGE_PROMPTS.get(language, "")
    return f"{base}\n\n{extra}"