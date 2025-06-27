# mcp dev real-mcp-server.py --with requests --with simple_salesforce
# mcp install real-mcp-server.py
# mcp run real-mcp-server.py
# uv run real-mcp-server.py

# FastMCP: https://gofastmcp.com/getting-started/welcome
# Model Context Protocol: https://modelcontextprotocol.io/quickstart/server

import typing

import os
from contextlib import asynccontextmanager

import httpx
import requests
from dotenv import load_dotenv
from mcp.server.fastmcp import FastMCP, Context
from simple_salesforce import Salesforce

load_dotenv()
API_VERSION = os.getenv("SF_API_VERSION", "63.0")

def _login_salesforce() -> Salesforce:
    """Authenticate once and return a ready Salesforce session."""
    token_resp = requests.post(
        os.getenv("SF_TOKEN_URL"),
        data={
            "grant_type": "client_credentials",
            "client_id": os.getenv("SF_CLIENT_ID"),
            "client_secret": os.getenv("SF_CLIENT_SECRET"),
        },
        timeout=30,
    )
    token_resp.raise_for_status()
    tok = token_resp.json()

    return Salesforce(
        instance_url=tok["instance_url"],
        session_id=tok["access_token"],
        version=API_VERSION,
    )


@asynccontextmanager
async def sf_lifespan(_server: FastMCP):
    """Run once at server start – keep one SF connection for all calls."""
    globals()["_salesforce"] = _login_salesforce()
    try:
        yield {"sf": _salesforce}
    finally:
        pass

mcp = FastMCP("salesforce-mcp", lifespan=sf_lifespan, dependencies=["requests", "simple_salesforce"])

####################################################################################################
############################################ TOOLS #################################################
####################################################################################################

@mcp.tool(description="Execute query")
def salesforce_query(soql: str) -> list[dict[str, typing.Any]]:
    """Run a SOQL query – example: SELECT Id, Name FROM Account LIMIT 5."""
    return _salesforce.query_all(soql)["records"]


@mcp.tool(description="Create records")
def salesforce_create(sobject: str, payload: dict[str, typing.Any]) -> str:
    """Insert a record and return the new Id."""
    return _salesforce.__getattr__(sobject).create(payload)["id"]


@mcp.tool(description="Update records")
def salesforce_update(sobject: str, record_id: str, payload: dict[str, typing.Any]) -> bool:
    """Patch a record; returns True when no exception is raised."""
    _salesforce.__getattr__(sobject).update(record_id, payload)
    return True

# This feature of MCP is not yet supported in the Claude Desktop client.

#@mcp.tool(description="Analyze sentiment")
#async def analyze_sentiment(text: str, ctx: Context) -> dict:
#    """Analyze the sentiment of a text using the client's LLM."""
    # Create a sampling prompt asking for sentiment analysis
#    prompt = f"Analyze the sentiment of the following text as positive, negative, or neutral. Just output a single word - 'positive', 'negative', or 'neutral'. Text to analyze: {text}"

    # Send the sampling request to the client's LLM (provide a hint for the model you want to use)
#    response = await ctx.sample(prompt, model_preferences="claude-3-sonnet")
    
    # Process the LLM's response
#    sentiment = response.text.strip().lower()

#    ctx.debug(f"Analyzed sentiment: {sentiment}")
    
    # Map to standard sentiment values
#    if "positive" in sentiment:
#        sentiment = "positive"
#    elif "negative" in sentiment:
#        sentiment = "negative"
#    else:
#        sentiment = "neutral"
    
#    return {"text": text, "sentiment": sentiment}


##########################################################################################
####################################### RESOURCES ########################################
##########################################################################################

# RESOURCE TEMPLATE
@mcp.resource("record://{sobject}/{record_id}")
def get_record(sobject: str, record_id: str) -> dict[str, typing.Any]:
    """Return a full JSON record, e.g. record://Account/001⋯."""
    return _salesforce.__getattr__(sobject).get(record_id)

# RESOURCE LIST
@mcp.resource(uri="data://app-status", name="Application Status", description="Provides the current status of the application.", mime_type="application/json")
async def get_application_status() -> dict:
    """Provides system status information."""
    ctx = mcp.get_context()
    await ctx.debug(f"Starting analysis on the context: {ctx}")
    return {
        "status": "operational",
        "request_id": ctx.request_id
    }


##########################################################################################
######################################## PROMPTS #########################################
##########################################################################################

# RESOURCE PROMPT
@mcp.prompt(description="Code Review")
def review_code(code: str) -> str:
    return f"Please review this code:\n\n{code}"


if __name__ == "__main__":
    mcp.run(transport="stdio")