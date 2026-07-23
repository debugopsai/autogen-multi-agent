# AutoGen Multi-Agent Registration Framework

A multi-agent workflow built with [AutoGen](https://github.com/microsoft/autogen) that automates user registration end-to-end: pulling data from a MySQL database, calling a REST API to register and log in, and saving the results to an Excel file.

## How it works

Three agents run sequentially in a round-robin team:

1. **DatabaseAgent** — queries MySQL for user registration data and formats it for the next agent
2. **APIAgent** — reads a Postman collection from the filesystem, calls the registration and login REST APIs using the database data
3. **ExcelAgent** — writes the successfully logged-in user's details to an Excel file with a timestamp

Each agent signals completion via a sentinel string in its message, which triggers the next agent to act.

## Requirements

- Python 3.11
- Node.js (for `npx`-based MCP servers)
- `uvx` (for the MySQL MCP server)
- A running MySQL instance
- An OpenRouter API key (or OpenAI-compatible LLM provider)

## Setup

```bash
# Create and activate virtual environment
python3.11 -m venv .venv
source .venv/bin/activate

# Install dependencies
pip install autogen-agentchat autogen-ext autogen-core python-dotenv
```

Copy `.env.example` to `.env` and fill in your values:

```bash
cp .env.example .env
```

## Environment Variables

| Variable | Description |
|---|---|
| `OPENROUTER_API_KEY` | API key for OpenRouter (or your LLM provider) |
| `MYSQL_HOST` | MySQL host (default: `127.0.0.1`) |
| `MYSQL_PORT` | MySQL port (default: `3306`) |
| `MYSQL_USER` | MySQL username |
| `MYSQL_PASSWORD` | MySQL password |
| `MYSQL_DATABASE` | Target database name |
| `REST_BASE_URL` | Base URL of the REST API under test |
| `FILES_DIR` | Directory accessible to the filesystem MCP server |
| `EXCEL_FILE_PATH` | Absolute path to the output `.xlsx` file |
| `EXCEL_MCP_PAGING_CELLS_LIMIT` | Max cells per page for Excel MCP (default: `4000`) |

## Running

```bash
source .venv/bin/activate
python scenario2.py
```

The workflow terminates automatically when ExcelAgent writes `"REGISTRATION PROCESS COMPLETE"`.

## How to Use

### 1. Prepare the database

Make sure your MySQL instance is running and the credentials in `.env` are correct. The DatabaseAgent will automatically create the `RegistrationDetails` and `Usernames` tables and insert sample data if they don't exist.

### 2. Prepare the output Excel file

Create an empty Excel file at the path set in `EXCEL_FILE_PATH` before running:

```bash
# Example using Python
python3 -c "import openpyxl; openpyxl.Workbook().save('/path/to/newdata.xlsx')"
```

### 3. Point to your REST API

Set `REST_BASE_URL` in `.env` to the base URL of the API you want to test. The APIAgent expects these two endpoints to exist:

| Endpoint | Method | Body fields |
|---|---|---|
| `/api/postAddToCart` (registration) | POST | `userEmail`, `userPassword`, `userMobile` |
| `/api/login` (login) | POST | `userEmail`, `userPassword` |

Adjust the agent's system message in `scenario2.py` if your API uses different endpoint paths or field names.

### 4. Run the workflow

```bash
python scenario2.py
```

You will see a live stream of each agent's thoughts and tool calls in the terminal. The run completes when one of the following happens:

- **Success**: ExcelAgent saves the data and prints `REGISTRATION PROCESS COMPLETE`
- **API failure**: If the REST API is unreachable or login fails, ExcelAgent will skip saving and the team will stop at the turn limit

### 5. Check the output

Open the Excel file at `EXCEL_FILE_PATH`. Successful registrations are appended to `Sheet1` with a timestamp column.

### Customising the workflow

- **Change the model**: Edit the `model` field in `scenario2.py` — any OpenAI-compatible model string works (e.g. `openai/gpt-4o`, `anthropic/claude-3-5-sonnet`)
- **Add a turn limit**: Pass `max_turns=N` to `RoundRobinGroupChat` to prevent infinite loops on failure
- **Add a new agent**: See the "Adding New Agents" section in `CLAUDE.md`

## Project Structure

```
framework/
├── scenario2.py      # Entry point — wires up agents and runs the team
├── agentFactory.py   # Creates AssistantAgent instances with MCP workbenches
├── mcp_config.py     # Configures MCP server connections (MySQL, REST, filesystem, Excel)
├── .env              # Local secrets (not committed)
└── .venv/            # Python virtual environment
```
