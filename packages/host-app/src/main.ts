import { MCPClient } from 'client-mcp';

class MCPHost {
    private clients: MCPClient[] = [];

    constructor() {
        // In a real application, the host would discover and instantiate clients.
        const client = new MCPClient('server-mcp-url'); // Example URL
        this.clients.push(client);
    }

    async getContext(query: string): Promise<string[]> {
        console.log(`Host: Getting context for query: "${query}"`);
        const allContext: string[] = [];

        for (const client of this.clients) {
            const context = await client.getContext(query);
            allContext.push(...context);
        }

        return allContext;
    }
}

async function main() {
    const host = new MCPHost();
    const context = await host.getContext("latest financial report");
    console.log("Host: Received context:", context);
}

main();
