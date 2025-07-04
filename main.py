import os
import asyncio
from typing import Any, Dict, List
from dotenv import load_dotenv

from google.adk.agents import Agent
from google.adk.sessions import InMemorySessionService
from google.adk.runners import Runner
from google.genai import types
from couchbase.cluster import Cluster
from couchbase.options import ClusterOptions
from couchbase.auth import PasswordAuthenticator
from couchbase.exceptions import DocumentNotFoundException

# Load environment variables from .env file
load_dotenv()

# Configuration
DEFAULT_USER_ID = "user_001"  # Change this or make it dynamic
SCOPE_NAME = "agent"          # Change this to match your setup
COLLECTION_NAME = "memory"     # Change this to match your setup


# --- Couchbase Memory Class ---
class CouchbaseMemory:
    """Couchbase memory storage for agent data.
    
    This class provides basic memory operations for storing and retrieving
    user data in Couchbase Capella. Perfect for building AI agents that need
    persistent memory across sessions.
    """
    
    def __init__(
        self,
        conn_str: str,
        username: str,
        password: str,
        bucket_name: str,
        scope_name: str = SCOPE_NAME,
        collection_name: str = COLLECTION_NAME,
    ):
        self.cluster = Cluster(
            conn_str, ClusterOptions(PasswordAuthenticator(username, password))
        )
        self.bucket = self.cluster.bucket(bucket_name)
        self.scope = self.bucket.scope(scope_name)
        self.collection = self.scope.collection(collection_name)
        print(f"[Memory System] Connected to Couchbase Capella - Bucket: {bucket_name}, Scope: {scope_name}, Collection: {collection_name}")

    def _doc_id(self, user_id: str):
        return f"user::{user_id}"

    def add(self, user_id: str, category: str, data: str):
        doc_id = self._doc_id(user_id)
        try:
            doc = self.collection.get(doc_id).content_as[dict]
        except DocumentNotFoundException:
            doc = {}

        doc.setdefault(category, [])
        if data not in doc[category]:
            doc[category].append(data)
            self.collection.upsert(doc_id, doc)
            print(
                f"[Memory System] Saved data for user '{user_id}' in category '{category}': '{data}'"
            )
        return True

    def search_by_category(self, user_id: str, category: str) -> list:
        doc_id = self._doc_id(user_id)
        try:
            doc = self.collection.get(doc_id).content_as[dict]
            results = doc.get(category, [])
        except DocumentNotFoundException:
            results = []
        print(
            f"[Memory System] Retrieved {len(results)} items from category '{category}' for user '{user_id}'."
        )
        return results


# --- Initialize Couchbase Memory ---
COUCHBASE_CONN_STR = os.getenv("COUCHBASE_CONN_STR")
COUCHBASE_USERNAME = os.getenv("COUCHBASE_USERNAME")
COUCHBASE_PASSWORD = os.getenv("COUCHBASE_PASSWORD")
COUCHBASE_BUCKET = os.getenv("COUCHBASE_BUCKET")

# Initialize the memory system
memory = CouchbaseMemory(
    conn_str=COUCHBASE_CONN_STR,
    username=COUCHBASE_USERNAME,
    password=COUCHBASE_PASSWORD,
    bucket_name=COUCHBASE_BUCKET,
    scope_name=SCOPE_NAME,
    collection_name=COLLECTION_NAME,
)


# --- Memory Tool Functions ---
def save_memory(category: str, data: str) -> Dict[str, Any]:
    """Save data to user's memory in a specific category.
    
    Args:
        category: The category to save data under (e.g., 'preferences', 'facts', 'notes')
        data: The data to save
        
    Returns:
        Dict with status and message
    """
    user_id = getattr(save_memory, "user_id", DEFAULT_USER_ID)
    memory.add(user_id=user_id, category=category, data=data)
    return {
        "status": "success",
        "message": f"Data saved in category '{category}': {data}",
    }


def retrieve_memory(category: str) -> Dict[str, Any]:
    """Retrieve all data from a specific category in user's memory.
    
    Args:
        category: The category to retrieve data from
        
    Returns:
        Dict with status, data list, and count
    """
    user_id = getattr(retrieve_memory, "user_id", DEFAULT_USER_ID)
    results = memory.search_by_category(user_id=user_id, category=category)
    return {
        "status": "success", 
        "data": results, 
        "category": category,
        "count": len(results)
    }


# --- Example Custom Tool Function ---
def example_tool(query: str) -> Dict[str, Any]:
    """Example tool function - replace this with your own business logic.
    
    Args:
        query: User query or input
        
    Returns:
        Dict with status and response
    """
    # This is where you'd implement your custom business logic
    # For example: API calls, calculations, data processing, etc.
    
    return {
        "status": "success",
        "message": f"Processed query: {query}",
        "example_data": "This is example output - replace with your logic"
    }


# --- Create Your Agent ---
agent = Agent(
    name="memory_agent_starter",  # Change this to your agent name
    model="gemini-2.5-flash",     # You can change the model if needed
    description="A helpful AI assistant with persistent memory capabilities.",  # Update description
    instruction="""
You are a helpful AI assistant with persistent memory capabilities powered by Couchbase Capella.

You have access to memory functions that allow you to:
1. Save information using `save_memory(category, data)` - use categories like 'preferences', 'facts', 'notes', etc.
2. Retrieve information using `retrieve_memory(category)` - get all data from a specific category
3. Process requests using `example_tool(query)` - replace this with your custom tools

Always use memory functions to:
- Remember user preferences and important information
- Retrieve context from previous conversations
- Provide personalized responses based on stored data

Be conversational, helpful, and make good use of the memory system to provide a personalized experience.
""",  # Update instructions for your use case
    tools=[save_memory, retrieve_memory, example_tool],  # Add your custom tools here
)


# --- Session Configuration ---
session_service = InMemorySessionService()
APP_NAME = "memory_agent_starter"  # Change this to your app name
SESSION_ID = "session_001"

runner = Runner(
    agent=agent,
    app_name=APP_NAME,
    session_service=session_service,
)


# --- Agent Communication Functions ---
async def call_agent_async(query: str, user_id: str, session_id: str):
    """Send a query to the agent and get a response."""
    print(f"\n>>> User ({user_id}): {query}")
    content = types.Content(role="user", parts=[types.Part(text=query)])
    
    # Set user_id for memory functions
    setattr(save_memory, "user_id", user_id)
    setattr(retrieve_memory, "user_id", user_id)

    async for event in runner.run_async(
        user_id=user_id, session_id=session_id, new_message=content
    ):
        if event.is_final_response() and event.content and event.content.parts:
            final_response = event.content.parts[0].text
            print(f"<<< Assistant: {final_response}")
            return final_response

    return "No response received."


async def interactive_chat():
    """Start an interactive chat session with the agent."""
    print("--- Starting Interactive Memory Agent ---")
    print("Your agent has persistent memory powered by Couchbase Capella!")
    print("Type 'quit' or 'exit' to end the session.")
    print("\nTry asking the agent to remember something, then ask about it later!")
    
    while True:
        user_query = input("\n> ")
        if user_query.lower() in ["quit", "exit"]:
            print("Ending session. Goodbye!")
            break
        await call_agent_async(query=user_query, user_id=DEFAULT_USER_ID, session_id=SESSION_ID)


async def create_session():
    """Create a new session for the agent."""
    await session_service.create_session(
        app_name=APP_NAME, user_id=DEFAULT_USER_ID, session_id=SESSION_ID
    )


if __name__ == "__main__":
    if (
        not os.getenv("GOOGLE_API_KEY")
        or os.getenv("GOOGLE_API_KEY") == "YOUR_GOOGLE_API_KEY_HERE"
    ):
        print(
            "ERROR: Please set your GOOGLE_API_KEY environment variable to run this script."
        )
    else:
        asyncio.run(create_session())
        asyncio.run(interactive_chat())
