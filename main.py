from langchain.agents import create_agent
from langchain.chat_models import init_chat_model
from langchain_core.messages import HumanMessage, SystemMessage
from pydantic import BaseModel

from sql_tools import SQL_TOOLS, SYSTEM_PROMPT

MODEL_NAME = "gemini-3.1-flash-lite"
MODEL_PROVIDER = "google_genai"
DB_FILE = "sample.db"


def invoke_llm(llm) -> None:
    # Call the model and print the full response at once
    system_prompt = "Answer concisely."
    user_prompt = "Tell me about the history of the Eiffel Tower."
    response = llm.invoke(
        [SystemMessage(content=system_prompt), HumanMessage(content=user_prompt)]
    )
    print(response.text)


def stream_llm(llm) -> None:
    # Stream the model response chunk by chunk
    system_prompt = "Answer concisely."
    user_prompt = "Tell me a story about a brave knight."
    for chunk in llm.stream(
        [SystemMessage(content=system_prompt), HumanMessage(content=user_prompt)]
    ):
        print(chunk.text, end="", flush=True)


class MoveTarget(BaseModel):
    x: float
    y: float
    z: float


def invoke_llm_structured(llm) -> None:
    # Call the model and parse the response into a MoveTarget
    system_prompt = "Respond with a JSON object"
    user_prompt = "Move the robot to (1.5, -2.0, 0.5)"
    structured_llm = llm.with_structured_output(MoveTarget)
    response = structured_llm.invoke(
        [SystemMessage(content=system_prompt), HumanMessage(content=user_prompt)]
    )
    print(response)


def invoke_llm_with_db(llm) -> None:
    user_prompt = "営業部の人の社員IDを教えて"

    # Create agent
    agent = create_agent(llm, SQL_TOOLS, system_prompt=SYSTEM_PROMPT)
    
    # Execute agent
    result = agent.invoke({"messages": [{"role": "user", "content": user_prompt}]})
    
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
    
    invoke_llm(llm)
    stream_llm(llm)
    invoke_llm_structured(llm)
    invoke_llm_with_db(llm)


if __name__ == "__main__":
    main()