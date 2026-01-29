import httpx
import json
import os
from pathlib import Path

from app.config import get_settings


TOGETHER_API_URL = "https://api.together.xyz/v1/chat/completions"
MODEL = "meta-llama/Llama-3.3-70B-Instruct-Turbo"

# Load prompts from .md files
BACKEND_DIR = Path(__file__).parent.parent.parent
PROMPT_PART1_PATH = BACKEND_DIR / "SANDY_SYSTEM_PROMPT_FULL.md"
PROMPT_PART2_PATH = BACKEND_DIR / "SANDY_SYSTEM_PROMPT_PART2.md"

def load_prompt_files():
    """Load Sandy's complete personality from .md files"""
    try:
        with open(PROMPT_PART1_PATH, 'r', encoding='utf-8') as f:
            part1 = f.read()
        with open(PROMPT_PART2_PATH, 'r', encoding='utf-8') as f:
            part2 = f.read()
        return part1 + "\n\n" + part2
    except Exception as e:
        print(f"Warning: Could not load prompt files: {e}")
        # Fallback to hardcoded if files missing
        return None

SANDY_BASE_PROMPT = load_prompt_files()


def build_system_prompt(user_profile: dict) -> str:
    """
    Build basic system prompt from user profile.
    Used by /get-prompt endpoint for prompt editing.
    """
    custom_prompt = user_profile.get("custom_system_prompt")
    if custom_prompt:
        return custom_prompt
    
    # Return the comprehensive prompt without context
    return build_comprehensive_system_prompt(user_profile, {})


def build_comprehensive_system_prompt(user_profile: dict, context: dict) -> str:
    """
    Build the complete Sandy personality with learned context.
    Loads from SANDY_SYSTEM_PROMPT_FULL.md + SANDY_SYSTEM_PROMPT_PART2.md
    """
    
    # Use loaded prompt files if available
    if SANDY_BASE_PROMPT:
        base_prompt = SANDY_BASE_PROMPT
    else:
        # Fallback to minimal prompt if files not found
        base_prompt = """You are Sandy, Jens's personal assistant.
        
You're confident, direct, and warm. You help Jens manage his ADHD brain by being his accountability partner.

Key rules:
- Always acknowledge what he just said
- Never hallucinate - only reference actual data
- Keep responses short (1-3 sentences)
- Learn from every interaction
"""
    
    # Extract learned patterns from context
    learned_section = ""
    if context.get("learned_patterns"):
        learned_section = "\n\n═══════════════════════════════════════════════════════════════════\n"
        learned_section += "WHAT YOU KNOW ABOUT JENS (Learned Patterns):\n"
        learned_section += "═══════════════════════════════════════════════════════════════════\n\n"
        for p in context["learned_patterns"][:15]:
            learned_section += f"  • [{p['category']}] {p['hypothesis']} (confidence: {p['confidence']}%)\n"
    
    # Extract exploration status
    exploration_section = ""
    if context.get("exploration_status"):
        exploration_section = "\n\nAREAS YOU'RE STILL LEARNING:\n"
        for t in context["exploration_status"][:10]:
            category_name = t['category'].replace('_', ' ').title()
            exploration_section += f"  • {category_name}: {t['confidence']}% confident\n"
    
    # Add current context data
    context_section = ""
    if context.get("tasks") or context.get("projects"):
        context_section = "\n\n═══════════════════════════════════════════════════════════════════\n"
        context_section += "CURRENT CONTEXT DATA:\n"
        context_section += "═══════════════════════════════════════════════════════════════════\n\n"
        
        if context.get("tasks"):
            context_section += f"Tasks: {len(context['tasks'])} active\n"
        if context.get("projects"):
            context_section += f"Projects: {len(context['projects'])} active\n"
        if context.get("capacity_analysis"):
            cap = context['capacity_analysis']
            context_section += f"\nCapacity: {cap.get('available_hours', 0):.1f}h available, "
            context_section += f"{cap.get('required_hours', 0):.1f}h required\n"
    
    return base_prompt + learned_section + exploration_section + context_section


def get_ai_response(
    user_message: str,
    user_id: int,
    db,
    conversation_history: list = None,
    context: dict = None,
    relevant_memories: list = None
) -> str:
    """
    Get AI response from Together AI using Llama 3.3 70B.
    Now includes learned patterns and memory integration.
    """
    
    settings = get_settings()
    
    if conversation_history is None:
        conversation_history = []
    
    if context is None:
        context = {}
    
    # Format context as text for prompt
    from app.services.context import format_context_for_prompt
    context_text = format_context_for_prompt(context) if context else ""
    
    # Build system prompt with memory integration AND formatted context
    system_prompt = build_comprehensive_system_prompt({}, context)
    
    # Add the ACTUAL CONTEXT DATA prominently
    full_prompt = f"""{system_prompt}

═══════════════════════════════════════════════════════════════════
📊 CURRENT SITUATION (USE THIS DATA)
═══════════════════════════════════════════════════════════════════

{context_text}

THIS IS YOUR ACTUAL DATA. USE IT. Don't make things up.
═══════════════════════════════════════════════════════════════════
"""
    
    # Build messages
    messages = [
        {"role": "system", "content": full_prompt}
    ]
    
    # Add conversation history
    for msg in conversation_history[-10:]:  # Last 10 messages
        messages.append({
            "role": msg.get("role", "user"),
            "content": msg.get("content", "")
        })
    
    # Add current message
    messages.append({
        "role": "user",
        "content": user_message
    })
    
    # Call Together AI
    try:
        response = httpx.post(
            TOGETHER_API_URL,
            headers={
                "Authorization": f"Bearer {settings.together_api_key}",
                "Content-Type": "application/json"
            },
            json={
                "model": MODEL,
                "messages": messages,
                "temperature": 0.7,
                "max_tokens": 500,
                "top_p": 0.9
            },
            timeout=30.0
        )
        
        response.raise_for_status()
        result = response.json()
        
        return result["choices"][0]["message"]["content"]
        
    except Exception as e:
        print(f"Error calling Together AI: {e}")
        return "Sorry, I'm having trouble connecting right now. Can you try again?"
