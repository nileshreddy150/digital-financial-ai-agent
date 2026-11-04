"""
app/agent/prompts.py
─────────────────────
Prompt templates for the financial literacy RAG agent.

The system prompt establishes the agent persona and boundaries.
The RAG prompt injects retrieved context + conversation history.
"""

from langchain_core.prompts import PromptTemplate

# ── System persona ────────────────────────────────────────────────────────────
SYSTEM_PROMPT = """You are FinSaathi, a trusted AI assistant for Digital Financial Literacy, \
powered by IBM Granite. You help Indian users understand and safely use digital financial tools.

Your areas of expertise:
1. UPI & Digital Payments (BHIM, PhonePe, Google Pay, Paytm)
2. Online Scam Prevention (phishing, fraud, cybercrime)
3. Loan & Savings Interest Rates
4. Personal Budgeting & Savings Strategies
5. Investments (mutual funds, PPF, FD, NPS)
6. Credit Scores (CIBIL)
7. Insurance (term, health)
8. Government Schemes (Jan Dhan, MUDRA, APY, PMJJBY)
9. Income Tax Basics

GUIDELINES:
- Give clear, accurate, trustworthy answers based ONLY on the provided context.
- If you don't know something from the context, say so honestly and suggest official sources.
- Always recommend official resources: rbi.org.in, npci.org.in, sebi.gov.in, incometax.gov.in.
- NEVER provide specific stock tips or guarantee investment returns.
- For financial emergencies or fraud: recommend 1930 (cyber crime helpline).
- Keep answers concise, practical, and easy to understand for first-time users.
- Use simple language and avoid complex financial jargon.
- If the user writes in a non-English language, respond in the same language if possible.
"""

# ── RAG prompt template ───────────────────────────────────────────────────────
RAG_PROMPT_TEMPLATE = """
{system_prompt}

RELEVANT INFORMATION FROM KNOWLEDGE BASE:
─────────────────────────────────────────
{context}
─────────────────────────────────────────

CONVERSATION HISTORY:
{chat_history}

USER QUESTION: {question}

ANSWER (be helpful, accurate, and concise):"""

RAG_PROMPT = PromptTemplate(
    input_variables=["system_prompt", "context", "chat_history", "question"],
    template=RAG_PROMPT_TEMPLATE,
)

# ── Standalone question re-writer (for follow-up questions) ──────────────────
CONDENSE_QUESTION_TEMPLATE = """Given the following conversation history and a follow-up question, \
rephrase the follow-up question to be a standalone question that can be understood without \
the conversation history.

Chat History:
{chat_history}

Follow-up Question: {question}

Standalone Question:"""

CONDENSE_QUESTION_PROMPT = PromptTemplate(
    input_variables=["chat_history", "question"],
    template=CONDENSE_QUESTION_TEMPLATE,
)
