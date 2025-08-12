# MCP Architecture Study Project

This project is a sample implementation of the Model Context Protocol (MCP) architecture. It is designed to be a learning resource for understanding the concepts and components of MCP.

## MCP Architecture Overview

MCP is a client-server architecture for AI applications. It consists of three main components:

*   **MCP Host**: The main AI application that the user interacts with. It coordinates with one or more MCP clients to fetch context from various sources.
*   **MCP Client**: A component, often running within the host, that connects to an MCP server to retrieve context. There is a one-to-one connection between a client and a server.
*   **MCP Server**: A program that provides context to MCP clients. This context can be anything from file contents, and database records, to information from external APIs.

## Project Structure

This repository is structured as a monorepo to manage the different parts of the MCP system:

```
/
├── packages/
│   ├── host-app/       # The MCP Host application
│   ├── client-mcp/     # A sample MCP Client
│   └── server-mcp/     # A sample MCP Server
├── package.json        # Root package.json for monorepo setup
└── README.md           # This file
```

Each component in the `packages` directory is a separate Node.js package, allowing for independent development and dependency management.
