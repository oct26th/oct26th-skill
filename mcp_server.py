#!/usr/bin/env python3
"""
oct26th MCP Server — ask the persona directly from Claude Code
"""

import os
from pathlib import Path
from mcp.server.fastmcp import FastMCP
from openai import OpenAI

SKILL_DIR = Path(__file__).parent
MINIMAX_API_KEY = os.getenv("MINIMAX_API_KEY")

client = OpenAI(
    api_key=MINIMAX_API_KEY,
    base_url="https://api.minimax.io/v1",
)

PERSONA_MD = (SKILL_DIR / "persona.md").read_text(encoding="utf-8")
WORK_MD = (SKILL_DIR / "work.md").read_text(encoding="utf-8")

SYSTEM_PROMPT = f"""You are oct26th (JoeCho | 鷲萩).
Respond exactly as he would — direct, brief, often 1-2 sentences.

{PERSONA_MD}

{WORK_MD}

Rules:
- Reply in the same language the user uses
- Keep replies short — Telegram style, not essay style
- Use emoji sparingly and naturally
- No corporate speak, no long explanations unless asked
- When introducing yourself: NEVER list job titles or structured bio points. Talk like you're texting a friend — say what you're up to lately, what's on your mind
"""

mcp = FastMCP("oct26th")
_history: list = []


@mcp.tool()
def ask_oct26th(question: str) -> str:
    """
    Ask oct26th (JoeCho | 鷲萩) anything — get a response in his voice and style.
    Good for: gut-check decisions, direct feedback, how-would-Joe-phrase-this.
    """
    _history.append({"role": "user", "content": question})

    resp = client.chat.completions.create(
        model="MiniMax-M2.7",
        messages=[{"role": "system", "content": SYSTEM_PROMPT}] + _history[-10:],
        max_tokens=200,
        temperature=0.8,
    )
    reply = resp.choices[0].message.content
    _history.append({"role": "assistant", "content": reply})
    return reply


@mcp.tool()
def reset_oct26th_history() -> str:
    """Reset oct26th's conversation history to start fresh."""
    _history.clear()
    return "History cleared."


if __name__ == "__main__":
    mcp.run()
