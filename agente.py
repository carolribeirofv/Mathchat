from dotenv import load_dotenv
import os 
load_dotenv()

from langchain.chat_models import init_chat_model
model = init_chat_model("groq:openai/gpt-oss-120b")

from langchain_core.tools import tool 
import math

@tool
def add(a: float, b: float) -> float: 
    """Add two numbers together. Use for addition operations."""
    return a + b

@tool
def multiply(a: float, b: float) -> float: 
    """Multiply two numbers together. Use for multiplication operations."""
    return a * b

@tool
def divide(a: float, b: float) -> float:
    """Divide the first number by the second. Use for division operations. Returns an error message if the second number is zero."""
    if b == 0:
        return " Error: Cannot divide by zero."
    return a / b


@tool 
def square_root(number: float) -> float: 
    """Calculate the square root of a number. Use for square root operations."""
    if number < 0:
        return " Error: Cannot compute the square root of a negative number."
    return math.sqrt(number)
    
tools = [add, multiply, divide, square_root]

from langchain.agents import create_agent

agent = create_agent (
    model = model,
    tools = tools,
    system_prompt="""Você é um assistente que resolve problemas matemáticos. Sempre responda em português. Sempre responda em português, de forma clara e direta. Nunca use notação LaTeX (como \\[ \\], \\frac{}{}, ou $$) nas suas respostas."""
    )

def run_agent (question: str):
    """Run the agent and print the execution trace"""
    print(f"User: {question}")
    print("-" * 50)

    result = agent.invoke ({
        "messages" : [("user", question)]
    })

    print("Agent:", result["messages"][-1].content)

if __name__ == "__main__":
    while True:
        pergunta = input("Digite sua pergunta (ou 'sair' para encerrar): ")
        if pergunta.lower() in ["sair", "exit", "quit"]:
            print("Encerrando o agente. Até mais!")
            break
        run_agent(pergunta)