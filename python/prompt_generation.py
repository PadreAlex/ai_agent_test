from state import State
from consts import default_cant_be_answered


def generate_sql_prompt(state: State) -> str:
    return (
        "Given the following user question, corresponding SQL query, and SQL result, answer the user question.\n\n"
        f"Question: {state['question']}\n\n"
        f"SQL Query: {state['query']}\n\n"
        f"SQL Result: {state['result']}\n\n"
        f"If you cannot answer your question based on the given context, or you have multiple return options, return '{default_cant_be_answered}'"
    )


def generate_is_in_db_prompt(question: str) -> str:
    return (
        "You are an AI assistant. Your task is to decide whether the following question "
        "can be answered using a relational SQL database containing order tracking information, "
        "such as order ID, delivery status, customer address, and city.\n\n"
        f"Question: {question}\n\n"
        "Answer 'YES' if it can be answered using such a database, otherwise answer 'NO'."
    )


def generate_kb_prompt(kb_context: str, state: State) -> str:
    return (
        f"Use the following knowledge base context to help answer the question.\n\n"
        f"Context:\n{kb_context}\n\n"
        f"Question: {state['question']}\n\n"
        f"If you cannot answer your question based on the given context, or you have multiple return options, return '{default_cant_be_answered}'"
    )
