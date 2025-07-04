# Google ADK + Couchbase Capella Starter Template

A starter template for building AI agents using Google's Agent Development Kit (ADK) with **Couchbase Capella** for persistent memory. This template provides a foundation for creating any type of AI agent that needs to remember information across sessions.

## 🌟 Why Couchbase Capella?

- **☁️ Cloud-native**: Fully managed database service
- **⚡ High Performance**: Sub-millisecond data access
- **📈 Scalable**: Automatic scaling based on demand
- **🔒 Secure**: Built-in security and compliance
- **🌍 Global**: Multi-region deployment options
- **💪 Reliable**: 99.99% uptime SLA
- **👥 Multi-user**: Supports concurrent users seamlessly

## Requirements

- Python 3.10 or higher
- Google API Key (for Gemini AI)
- **Couchbase Capella account and cluster**

## Setup Instructions

Choose one of the following setup methods:

### Option 1: Setup with uv (Recommended)

[uv](https://docs.astral.sh/uv/) is a fast Python package installer and resolver. It's recommended for its speed and reliability.

#### 1. Install uv

```bash
# On macOS and Linux
curl -LsSf https://astral.sh/uv/install.sh | sh

# On Windows
powershell -c "irm https://astral.sh/uv/install.ps1 | iex"

# Or with pip
pip install uv
```

#### 2. Create and activate a virtual environment

```bash
# Create a virtual environment
uv venv

# Activate the virtual environment
# On macOS/Linux:
source .venv/bin/activate

# On Windows:
.venv\Scripts\activate
```

#### 3. Install dependencies

```bash
# Install project dependencies
uv pip install -e .
```

#### 4. Setup environment variables

Create a `.env` file in the project root:

```bash
touch .env
```

Add your API keys and Couchbase configuration to the `.env` file:

```env
# Google API Key (required)
GOOGLE_API_KEY=your_google_api_key_here

# Couchbase Capella Configuration (required)
COUCHBASE_CONN_STR=couchbases://cb.your-endpoint.cloud.couchbase.com
COUCHBASE_USERNAME=your_username
COUCHBASE_PASSWORD=your_password
COUCHBASE_BUCKET=your_bucket_name
```

#### 5. Run the application

```bash
uv run python main.py
```

### Option 2: Setup with pip (Traditional)

#### 1. Create and activate a virtual environment

```bash
# Create a virtual environment
python -m venv .venv

# Activate the virtual environment
# On macOS/Linux:
source .venv/bin/activate

# On Windows:
.venv\Scripts\activate
```

#### 2. Install dependencies

```bash
# Upgrade pip (recommended)
pip install --upgrade pip

# Install project dependencies
pip install -e .

# Or install dependencies directly:
pip install "google-adk>=1.5.0" "python-dotenv>=1.0.0" "couchbase>=4.0.0"
```

#### 3. Setup environment variables

Create a `.env` file in the project root:

```bash
touch .env
```

Add your API keys and Couchbase configuration to the `.env` file:

```env
# Google API Key (required)
GOOGLE_API_KEY=your_google_api_key_here

# Couchbase Capella Configuration (required)
COUCHBASE_CONN_STR=couchbases://cb.your-endpoint.cloud.couchbase.com
COUCHBASE_USERNAME=your_username
COUCHBASE_PASSWORD=your_password
COUCHBASE_BUCKET=your_bucket_name
```

#### 4. Run the application

```bash
python main.py
```

## Getting a Google API Key

1. Go to the [Google AI Studio](https://aistudio.google.com/)
2. Sign in with your Google account
3. Click on "Get API key" or "Create API key"
4. Follow the instructions to create a new API key
5. Copy the API key and add it to your `.env` file

## 🏗️ Setting up Couchbase Capella

### Prerequisites

1. **Create a Couchbase Capella Account**: Sign up at [Couchbase Capella](https://cloud.couchbase.com/sign-up?utm_source=giveago&utm_medium=community)
2. **Create a Cluster**: Set up a new cluster in Capella
3. **Create a Bucket**: Create a bucket for storing agent data
4. **Configure Database Access**: Create database credentials

### Capella Setup Steps

1. **Sign up for Couchbase Capella**
   - Go to [cloud.couchbase.com](https://cloud.couchbase.com/)
   - Create a free account
   - Verify your email address

2. **Create a Cluster**
   - Click "Create Cluster"
   - Choose your cloud provider (AWS, Azure, or GCP)
   - Select a region close to your users
   - Choose "Developer Pro" for testing (free tier available)

3. **Create a Bucket**
   - Navigate to "Data Tools" > "Buckets"
   - Click "Add Bucket"
   - Name: `agent-memory` (or your preferred name)
   - Memory Quota: 100 MB (minimum)
   - Click "Add Bucket"

4. **Create Database Credentials**
   - Go to "Security" > "Database Access"
   - Click "Create Database Access"
   - Username: Choose a username
   - Password: Create a strong password
   - Bucket Access: Select your bucket and choose "Read/Write"
   - Click "Create User"

5. **Get Connection Details**
   - Go to "Connect" tab in your cluster
   - Copy the connection string (starts with `couchbases://`)
   - Note your username and password

### Database Structure

**Bucket Structure**:
- **Bucket**: Your chosen bucket name (e.g., `agent-memory`)
- **Scope**: `agent` (configurable in code)
- **Collection**: `memory` (configurable in code)

**Document Structure**:
```json
{
  "user::user_001": {
    "preferences": [
      "I prefer dark mode",
      "Send me daily summaries"
    ],
    "facts": [
      "My favorite color is blue",
      "I work in software development"
    ],
    "notes": [
      "Interested in AI and machine learning",
      "Uses Python primarily"
    ]
  }
}
```

## Environment Variables

The application requires the following environment variables:

### Required Variables
- `GOOGLE_API_KEY`: Your Google API key for accessing Gemini AI services
- `COUCHBASE_CONN_STR`: Couchbase Capella connection string (e.g., `couchbases://cb.xxx.cloud.couchbase.com`)
- `COUCHBASE_USERNAME`: Your Couchbase database username
- `COUCHBASE_PASSWORD`: Your Couchbase database password
- `COUCHBASE_BUCKET`: Your bucket name (e.g., `agent-memory`)

## Usage

1. **Make sure your virtual environment is activated**
2. **Ensure your `.env` file contains all required variables**:
   - Google API key
   - Couchbase connection string
   - Couchbase username and password
   - Couchbase bucket name
3. **Verify Couchbase Capella cluster is running**
4. **Run the application**: `python main.py`
5. **Start chatting with your AI agent!**
6. **Type 'quit' or 'exit' to end the session**

> **Note**: The agent will automatically connect to your Couchbase Capella cluster and store/retrieve information in real-time.

### Example Conversation

```
> Hi there!
<<< Assistant: Hello! I'm your AI assistant with persistent memory capabilities. I can remember information across our conversations. How can I help you today?

> Remember that my favorite color is blue
<<< Assistant: I'll remember that your favorite color is blue! I've saved this information so I can refer to it in future conversations.

> What's my favorite color?
<<< Assistant: Your favorite color is blue! I remembered that from our earlier conversation.
```

## Project Structure

```
.
├── README.md          # This file
├── main.py            # Your AI agent with Couchbase memory
├── pyproject.toml     # Project configuration and dependencies
├── .env               # Environment variables (create this)
└── .venv/             # Virtual environment (created during setup)
```

## 🚀 What's Included

- **💾 Persistent Memory**: Store and retrieve data using Couchbase Capella
- **🛠️ Memory Tools**: Pre-built `save_memory()` and `retrieve_memory()` functions
- **🤖 Agent Framework**: Google ADK setup with session management
- **📝 Example Tool**: Template for adding custom business logic
- **🔧 Easy Configuration**: Simple environment variable setup
- **🌐 Multi-user Ready**: Each user gets separate memory space
- **⚡ Production Ready**: Scalable cloud database backend

## 🎨 Customizing Your Agent

This is a starter template - here's how to make it your own:

### 1. Update Agent Configuration

In `main.py`, customize these sections:

```python
# Change these constants
DEFAULT_USER_ID = "your_user_001"  # Your default user ID
SCOPE_NAME = "your_scope"          # Your Couchbase scope
COLLECTION_NAME = "your_collection" # Your Couchbase collection

# Update agent details
agent = Agent(
    name="your_agent_name",
    description="Your agent description",
    instruction="Your custom instructions...",
    tools=[save_memory, retrieve_memory, your_custom_tools],
)
```

### 2. Add Custom Tools

Replace the example tool with your business logic:

```python
def your_custom_tool(param1: str, param2: int) -> Dict[str, Any]:
    """Your custom tool description."""
    # Your business logic here
    # Examples: API calls, calculations, data processing
    
    return {
        "status": "success",
        "result": "your_result"
    }
```

### 3. Memory Categories

Use meaningful category names for organizing data:

```python
# Examples of memory categories
save_memory("user_preferences", "I prefer dark mode")
save_memory("conversation_history", "User asked about pricing")
save_memory("user_profile", "Expert level user")
save_memory("custom_settings", "Notification frequency: daily")
```

### 4. Agent Instructions

Customize the agent's behavior by updating the instruction string:

```python
instruction="""
You are a [YOUR AGENT TYPE] that specializes in [YOUR DOMAIN].

Your capabilities:
- [Capability 1]
- [Capability 2]
- Remember information using save_memory(category, data)
- Recall information using retrieve_memory(category)

Always [YOUR SPECIFIC GUIDELINES].
"""
```

## 💡 Use Case Examples

This starter template can be adapted for various use cases:

- **💼 Customer Support Agent**: Remember customer preferences, issues, and solutions
- **📚 Learning Assistant**: Track learning progress, preferences, and knowledge gaps
- **🛒 Shopping Assistant**: Remember product preferences, budgets, and purchase history
- **📅 Scheduling Assistant**: Remember availability, meeting preferences, and constraints
- **🏥 Healthcare Assistant**: Track symptoms, medications, and care preferences
- **💰 Finance Assistant**: Remember financial goals, risk tolerance, and investment preferences

## Troubleshooting

### Common Issues

1. **"GOOGLE_API_KEY not set" error**

   - Make sure you've created a `.env` file in the project root
   - Verify your API key is correctly added to the `.env` file
   - Ensure there are no extra spaces or quotes around the API key

2. **Import errors**

   - Make sure your virtual environment is activated
   - Verify all dependencies are installed with `pip list` or `uv pip list`

3. **Python version issues**
   - This project requires Python 3.10 or higher
   - Check your Python version: `python --version`

4. **Couchbase connection errors**
   - Verify your Couchbase Capella cluster is running
   - Check your connection string format: `couchbases://cb.xxx.cloud.couchbase.com`
   - Ensure your database credentials are correct
   - Verify the bucket name exists in your cluster
   - Check if your IP is allowlisted in Capella (if using IP restrictions)

5. **"Bucket not found" error**
   - Make sure the bucket name in your `.env` file matches exactly
   - Verify the bucket exists in your Couchbase Capella cluster
   - Check that your user has access to the bucket

6. **"Authentication failed" error**
   - Verify your username and password are correct
   - Ensure the database user has the right permissions (Read/Write)
   - Check if the user is enabled in Capella

### Virtual Environment Commands

```bash
# Activate virtual environment
# macOS/Linux:
source .venv/bin/activate
# Windows:
.venv\Scripts\activate

# Deactivate virtual environment
deactivate

# Check if virtual environment is active
which python  # Should show path to .venv/bin/python
```

## Development

To contribute to this project:

1. Fork the repository
2. Create a virtual environment using either uv or pip method above
3. Install dependencies in development mode: `pip install -e .`
4. Make your changes
5. Test your changes by running the application
6. Submit a pull request
