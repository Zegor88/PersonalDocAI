# File: src/familydoc_ai/prompting/prompt_builder.py

from typing import Dict, Optional

def _format_section(value) -> str:
    """
    Converts a string, list, or dictionary to a formatted text for the prompt.
    - If value is a list, returns a multiline string with markers.
    - If value is a dict, formats as markers with sub-items.
    - If a string — just strip().
    """
    if isinstance(value, list):
        return "\n".join(f"- {str(v).strip()}" for v in value)
    if isinstance(value, dict):
        lines = []
        for k, v in value.items():
            if isinstance(v, (list, dict)):
                lines.append(f"- {str(k).strip()}:")
                sub = _format_section(v)
                lines.extend("  " + line for line in sub.splitlines())
            else:
                lines.append(f"- {str(k).strip()}: {str(v).strip()}")
        return "\n".join(lines)
    return str(value).strip()

def build_prompt_from_config(
    config: Dict,
    config_reasoning: Optional[Dict] = None,
    locale: str = "ru"
) -> str:
    """
    Builds a declarative system prompt from a compact YAML config.
    Args:
        config: Dictionary with prompt sections.
        config_reasoning: Additional map of reasoning strategies (by key).
        locale: Language of the section headings ('ru' or 'en').
    Returns:
        String — a declarative system prompt.
    """
    # Секция: заголовок -> ключ
    headings = {
        "ru": {
            "role": "Роль",
            "backstory": "Профессиональная предыстория",
            "objective": "Цель работы",
            "tasks": "Ключевые задачи",
            "instruction": "Инструкции",
            "context": "Контекст работы",
            "prompt_protection": "Меры защиты промпта",
            "reasoning_strategy": "Стратегия рассуждения",
            "final_instruction": "Выполняй задачи строго в соответствии с этими инструкциями."
        },
        "en": {
            "role": "Role",
            "backstory": "Professional background",
            "objective": "Objective",
            "tasks": "Key tasks",
            "instruction": "Instructions",
            "context": "Operational context",
            "prompt_protection": "Prompt protection policy",
            "reasoning_strategy": "Reasoning strategy",
            "final_instruction": "Proceed with the above instructions precisely and comprehensively."
        }
    }
    h = headings["ru"] if locale == "ru" else headings["en"]

    parts = []

    # Add each section only if it exists in the config
    if config.get("role"):
        parts.append(f"{h['role']}:\n{_format_section(config['role'])}")
    if config.get("backstory"):
        parts.append(f"{h['backstory']}:\n{_format_section(config['backstory'])}")
    if config.get("objective"):
        parts.append(f"{h['objective']}:\n{_format_section(config['objective'])}")
    if config.get("tasks"):
        parts.append(f"{h['tasks']}:\n{_format_section(config['tasks'])}")
    if config.get("instruction"):
        parts.append(f"{h['instruction']}:\n{_format_section(config['instruction'])}")
    if config.get("context"):
        parts.append(f"{h['context']}:\n{_format_section(config['context'])}")
    if config.get("prompt_protection"):
        parts.append(f"{h['prompt_protection']}:\n{_format_section(config['prompt_protection'])}")

    # Reasoning strategy (reasoning) — via lookup by key
    reasoning_key = config.get("reasoning_strategy")
    if reasoning_key and config_reasoning:
        strategies = config_reasoning.get("reasoning_strategies", {})
        strategy_text = strategies.get(reasoning_key)
        if strategy_text:
            parts.append(f"{h['reasoning_strategy']}:\n{_format_section(strategy_text)}")

    # Final instruction
    parts.append(h["final_instruction"])

    return "\n\n".join(parts)