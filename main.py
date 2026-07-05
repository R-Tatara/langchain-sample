from langchain.agents import create_agent
from langchain.chat_models import init_chat_model
from langchain_core.messages import HumanMessage
from pydantic import BaseModel

from sql_tools import SQL_TOOLS, SYSTEM_PROMPT

MODEL_NAME = "gemini-3.1-flash-lite"
MODEL_PROVIDER = "google_genai"
DB_FILE = "sample.db"


class MoveTarget(BaseModel):
    x: float
    y: float
    z: float


def invoke_llm(llm, prompt) -> None:
    # Call the model and print the full response at once
    response = llm.invoke([HumanMessage(content=prompt)])
    print(response.text)


def stream_llm(llm, prompt) -> None:
    # Stream the model response chunk by chunk
    for chunk in llm.stream([HumanMessage(content=prompt)]):
        print(chunk.text, end="", flush=True)


def invoke_llm_structured(llm, prompt) -> None:
    # Call the model and parse the response into a MoveTarget
    llm_structured = llm.with_structured_output(MoveTarget)
    response = llm_structured.invoke([HumanMessage(content=prompt)])
    print(response)


def invoke_llm_with_db(llm, prompt) -> None:
    # Use SQL tools from sql_tools module
    tools = SQL_TOOLS
    system_prompt = SYSTEM_PROMPT
    
    # Create agent
    agent = create_agent(llm, tools, system_prompt=system_prompt)
    
    # Execute agent
    result = agent.invoke({"messages": [{"role": "user", "content": prompt}]})
    
    # Extract text from the response
    content = result["messages"][-1].content
    if isinstance(content, list):
        text_parts = [block['text'] for block in content if block.get('type') == 'text']
        print('\n'.join(text_parts))
    else:
        print(content)


def main() -> None:
    # Initialize the Gemini model
    llm = init_chat_model(MODEL_NAME, model_provider=MODEL_PROVIDER)

    print("--- invoke ---")
    prompt = "Tell me about the history of the Eiffel Tower"
    invoke_llm(llm, prompt)

    print("--- stream ---")
    prompt = "Tell me a story about a brave knight"
    stream_llm(llm, prompt)

    print("--- structured ---")
    structured_prompt = "Move the robot to (1.5, -2.0, 0.5)"
    invoke_llm_structured(llm, structured_prompt)

    print("--- SQL Agent ---")
    prompt = "営業部の人の社員IDを教えて"
    invoke_llm_with_db(llm, prompt)


if __name__ == "__main__":
    main()