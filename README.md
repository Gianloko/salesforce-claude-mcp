
# `real-mcp-server.py` - MCP Server with Salesforce Integration

This project sets up an **MCP (Model Context Protocol)** server to interact with **Salesforce** using **FastMCP**, and it also integrates basic weather tools (as detailed in the original script). It provides a series of tools for interacting with Salesforce, such as querying records, creating, and updating records, while also using environment variables securely via `.env` files.

## Prerequisites

### Python Libraries

Before starting the server, make sure the necessary libraries are installed. These include:

- `httpx` - For asynchronous HTTP requests.
- `requests` - For synchronous HTTP requests.
- `python-dotenv` - For managing environment variables.
- `simple-salesforce` - For interacting with Salesforce's REST API.
- `fastmcp` - The core library for the Model Context Protocol (MCP).

### Install Required Libraries

Run the following command to install all the necessary dependencies:

```bash
pip install httpx requests python-dotenv simple-salesforce fastmcp
```

### Salesforce API Credentials

Make sure you have a **Salesforce Developer Account** and that you have the following credentials from Salesforce:

- `SF_TOKEN_URL` (OAuth2 token endpoint)
- `SF_CLIENT_ID` (Client ID for your Salesforce app)
- `SF_CLIENT_SECRET` (Client Secret for your Salesforce app)

These credentials will be used to authenticate and connect to your Salesforce instance.

Create a `.env` file in the project root with the following content:

```bash
SF_TOKEN_URL=https://your-salesforce-instance-url/oauth2/token
SF_CLIENT_ID=your-client-id
SF_CLIENT_SECRET=your-client-secret
SF_API_VERSION=63.0  # Optional, set your Salesforce API version
```

## Running the MCP Server

### Step 1: Development Mode

To run the server in development mode (for testing and debugging), use the following command:

```bash
mcp dev real-mcp-server.py --with requests --with simple_salesforce
```

This will launch the server in development mode, ensuring that the necessary libraries (`requests` and `simple_salesforce`) are available to the server.

### Step 2: Installing the Server

Once you’ve developed or tested your server, you can install it using:

```bash
mcp install real-mcp-server.py
```

This installs the server and registers all of its tools, resources, and prompts.

### Step 3: Running the Server (direct or through MCP Client, for example Claude Desktop)

![alt text](https://github.com/Gianloko/images/check_claude_settings.png?raw=true)

To run the server, you can use either of these commands:

- **MCP transport (via `mcp run`)**:

    ```bash
    mcp run real-mcp-server.py
    ```

    This will run the server using the **MCP transport**, which connects to any compatible client that supports MCP.

- **UVicorn (via `uv run`)**:

    ```bash
    uv run real-mcp-server.py
    ```

    This starts the server using **Uvicorn**, which provides better performance in production environments.

---

## Server Features

The server provides several tools and resources that interact with Salesforce. Some of the key features include:

### Tools

- **`salesforce_query`**: Run SOQL queries on Salesforce.
    - Example:
    ```python
    salesforce_query("SELECT Id, Name FROM Account LIMIT 5")
    ```

- **`salesforce_create`**: Insert a new record into Salesforce and return its ID.
    - Example:
    ```python
    salesforce_create("Account", {"Name": "Test Account"})
    ```

- **`salesforce_update`**: Update an existing record in Salesforce.
    - Example:
    ```python
    salesforce_update("Account", "001xxxxxx", {"Name": "Updated Account"})
    ```

### Resources

- **`get_record`**: Fetch a record from Salesforce by its `sobject` and `record_id`.
    - Example:
    ```python
    get_record("Account", "001xxxxxx")
    ```

- **`get_application_status`**: Provides system status information for the application.
    - Example:
    ```python
    get_application_status()
    ```

### Prompts

- **`review_code`**: A prompt for reviewing code, which outputs a code review message.
    - Example:
    ```python
    review_code("print('Hello, world!')")
    ```

---

## Troubleshooting

1. **Missing Dependencies:**
   If you encounter any errors related to missing libraries, ensure that all dependencies are installed using `pip install`:

   ```bash
   pip install httpx requests python-dotenv simple-salesforce fastmcp
   ```

2. **Salesforce Authentication Issues:**
   If the server is unable to authenticate with Salesforce, double-check your Salesforce credentials in the `.env` file and make sure they are correct.

3. **Server Not Starting:**
   If the server doesn’t start properly, check the logs for errors related to the dependencies. Make sure the environment variables are loaded correctly, and all necessary libraries are installed.

---

## Contributing

Feel free to open issues or pull requests if you encounter any bugs or would like to enhance the server's functionality. Contributions are welcome!

---

## License

This project is licensed under the MIT License – see the [LICENSE](LICENSE) file for details.
