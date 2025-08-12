import express, { Request, Response } from 'express';

const app = express();
const port = 3000;

app.use(express.json());

// A simple data store for the server
const contextData: { [key: string]: string[] } = {
    "financial report": [
        "Q4 2023 Financial Report: Revenue up 15%",
        "Stock price stable."
    ],
    "company news": [
        "New partnership announced with Acme Corp.",
        "Upcoming product launch in Q1 2024."
    ]
};

app.get('/context', (req: Request, res: Response) => {
    const query = req.query.q as string;

    if (!query) {
        return res.status(400).send({ error: 'Query parameter "q" is required.' });
    }

    console.log(`Server: Received query for: "${query}"`);

    let results: string[] = [];
    for (const key in contextData) {
        if (key.includes(query.toLowerCase())) {
            results = [...results, ...contextData[key]];
        }
    }

    res.json(results);
});

app.listen(port, () => {
    console.log(`MCP Server listening at http://localhost:${port}`);
});
