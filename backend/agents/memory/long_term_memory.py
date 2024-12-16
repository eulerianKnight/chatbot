from agents.prompts import CREATE_MEMORY_INSTRUCTION, MODEL_SYSTEM_MESSAGE

from langgraph.graph import MessagesState
from langgraph.store.postgres import AsyncPostgresStore
from langchain_core.runnables import RunnableConfig
from langchain_core.language_models import BaseChatModel

async with AsyncPostgresStore.from_conn_string(
    "postgresql://user:pass@localhost:5432/dbname",
    index={
        "dims": 1536,
        "embed": init_embeddings("openai:text-embedding-3-small"),
        "fields": ["text"]
    }
) as store:
    await store.setup()


def write_memory(
    model: BaseChatModel, 
    state: MessagesState, 
    config: RunnableConfig):

    """Reflect on the chat history and save a memory to the store."""
    
    # Get the user ID from the config
    user_id = config["configurable"]["user_id"]

    # Retrieve existing memory from the store
    namespace = ("memory", user_id)
    existing_memory = store.get(namespace, "user_memory")
        
    # Extract the memory
    if existing_memory:
        existing_memory_content = existing_memory.value.get('memory')
    else:
        existing_memory_content = "No existing memory found."

    # Format the memory in the system prompt
    system_msg = CREATE_MEMORY_INSTRUCTION.format(memory=existing_memory_content)
    new_memory = model.invoke([SystemMessage(content=system_msg)]+state['messages'])

    # Overwrite the existing memory in the store 
    key = "user_memory"

    # Write value as a dictionary with a memory key
    store.put(namespace, key, {"memory": new_memory.content})