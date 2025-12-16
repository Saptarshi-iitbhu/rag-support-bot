import os
from dotenv import load_dotenv
from openai import OpenAI
from typing import List, Dict

from .faq_engine import faq_engine 

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


def generate_response(messages: List[Dict[str, str]]) -> str:
    """
    Generate a reply for the current conversation.

    1. Get the last user message from `messages`.
    2. Try to answer directly from FAQs (MakTek dataset).
    3. If no good FAQ match, call the LLM with FAQ context + history.
    """
    if not messages:
        return "Hello! How can I help you today?"

    last_message = messages[-1]["content"]

    faq_hit = faq_engine.search_faq(last_message)

    if faq_hit:
        return faq_hit["answer"]

    faq_context = ""
    if faq_hit:
        faq_context = (
            f"FAQ match (score {faq_hit['score']:.2f}):\n"
            f"Q: {faq_hit['question']}\n"
            f"A: {faq_hit['answer']}\n"
        )

    system_prompt = (
        "You are a helpful customer support agent for an e-commerce website. "
        "Use the FAQ context if provided. Be concise and polite."
    )

    llm_messages: List[Dict[str, str]] = [
        {"role": "system", "content": system_prompt},
    ]

    if faq_context:
        llm_messages.append(
            {"role": "system", "content": f"FAQ context:\n{faq_context}"}
        )

    llm_messages.extend(messages)

    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",  
            messages=llm_messages,
            temperature=0.7,
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        print(f"Error generating response: {e}")
        return "I'm sorry, I'm having trouble connecting to my brain right now."


async def analyze_escalation(last_user_message: str, bot_response: str) -> bool:
    """
    Simple rule-based escalation detection.

    If the bot sounds unsure or apologetic, mark for escalation.
    """
    escalation_keywords = [
        "sorry",
        "apologize",
        "don't know",
        "do not know",
        "cannot help",
        "can't help",
        "not sure",
        "escalate",
        "support team",
        "human agent",
    ]

    bot_lower = bot_response.lower()
    return any(keyword in bot_lower for keyword in escalation_keywords)
