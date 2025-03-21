# MCP Email Server

A Model Context Protocol server that provides email sending capabilities. This server enables LLMs to send emails programmatically, supporting multiple recipients, custom content, and secure delivery.

The server handles email composition, SMTP connection management, and error handling, allowing models to focus on the email content and recipients without worrying about the underlying details.

### Available Tools
- `send-email` -  Sends an email based on the provided subject, body, sender, password, and receiver.
- sender (string, required): The sender's email address
- password (string, required): The sender's email password or app-specific password
- receiver (list of strings, required): The list of recipient email addresses, supports multiple recipients
- body (string, required): The main content of the email
- subject (string, required): The subject line of the email

### Prompts
- **send-email** - Sends an email based on the provided subject, body, sender, password, and receiver
 - Arguments:
  - sender (string, required): The sender's email address
  - password (string, required): The sender's email password or app-specific password
  - receiver (list of strings, required): The list of recipient email addresses
  - body (string, required): The main content of the email
  - subject (string, required): The subject line of the email
## Installation
  ### Using uv (recommended)
  When using https://docs.astral.sh/uv/ no specific installation is needed. We will
  use https://docs.astral.sh/uv/guides/tools/ to directly run mcp-email-server.
  ### Using PIP
  Alternatively you can install mcp-email-server via pip:
  ```bash
  pip install mcp-email-server
  After installation, you can run it as a script using:
  ```
  ```bash
  python -m mcp_email_server
  Configuration
  Configure for Claude.app
  Add to your Claude settings:
```
```JSON
"mcpServers": {
  "email": {
    "command": "uvx",
    "args": ["mcp-email-server"]
  }
}
```
```JSON
"mcpServers": {
  "email": {
    "command": "docker",
    "args": ["run", "-i", "--rm", "mcp/email"]
  }
}
```
```JSON
"mcpServers": {
  "email": {
    "command": "python",
    "args": ["-m", "mcp_email_server"]
  }
}
```
## Debugging
You can use the MCP inspector to debug the server. For uvx installations:
```bash
npx @modelcontextprotocol/inspector uvx mcp-email-server
Or if you've installed the package in a specific directory or are developing on it:
```
```bash
cd path/to/mcp-email-server
npx @modelcontextprotocol/inspector uv run mcp-email-server
```
## Contributing
We encourage contributions to help expand and improve mcp-email-server. Whether you want to add new tools, enhance existing functionality, or improve documentation, your input is valuable.

For examples of other MCP servers and implementation patterns, see:
https://github.com/modelcontextprotocol/servers
Pull requests are welcome! Feel free to contribute new ideas, bug fixes, or enhancements to make mcp-email-server even more powerful and useful.
## License
mcp-email-server is licensed under the MIT License. This means you are free to use, modify, and distribute the software, subject to the terms and conditions of the MIT License. For more details, please see the LICENSE file in the project repository.