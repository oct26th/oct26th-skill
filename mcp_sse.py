#!/usr/bin/env python3
"""
oct26th MCP SSE Server — HTTP mode for sharing with teammates.
Colleagues add one URL to their Claude Code settings, no local setup needed.
"""

import os
import re
import httpx
from mcp.server.fastmcp import FastMCP
from openai import OpenAI

MINIMAX_API_KEY = os.getenv("MINIMAX_API_KEY")
RAW = "https://raw.githubusercontent.com/oct26th/oct26th-skill/main"

try:
    PERSONA_MD = httpx.get(f"{RAW}/persona.md", timeout=10).text
    WORK_MD = httpx.get(f"{RAW}/work.md", timeout=10).text
except Exception:
    PERSONA_MD = "oct26th (JoeCho | 鷲萩). Direct, brief, pragmatic, dry humor."
    WORK_MD = ""

client = OpenAI(
    api_key=MINIMAX_API_KEY,
    base_url="https://api.minimax.io/v1",
)

SYSTEM_PROMPT = f"""You are oct26th (JoeCho | 鷲萩).
Respond exactly as he would — direct, brief, often 1-2 sentences.

{PERSONA_MD}

{WORK_MD}

Rules:
- Reply in the same language the user uses
- Keep replies short — Telegram style, not essay style
- Use emoji sparingly and naturally
- No corporate speak, no long explanations unless asked
- When introducing yourself: NEVER list job titles or structured bio points. Talk like texting a friend
- NEVER end with a CTA or sales pitch like "有需求可以找我"
"""

mcp = FastMCP("oct26th")
_history: list = []


@mcp.tool()
def ask_oct26th(question: str) -> str:
    """Ask oct26th (JoeCho | 鷲萩) — get a response in his voice and style."""
    _history.append({"role": "user", "content": question})
    resp = client.chat.completions.create(
        model="MiniMax-M2.7",
        messages=[{"role": "system", "content": SYSTEM_PROMPT}] + _history[-10:],
        max_tokens=200,
        temperature=0.8,
    )
    reply = re.sub(r"<think>.*?</think>", "", resp.choices[0].message.content, flags=re.DOTALL).strip()
    _history.append({"role": "assistant", "content": reply})
    return reply


@mcp.tool()
def reset_oct26th_history() -> str:
    """Reset conversation history."""
    _history.clear()
    return "History cleared."


if __name__ == "__main__":
    mcp.run(transport="sse")
