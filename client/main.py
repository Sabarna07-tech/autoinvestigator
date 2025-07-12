# client/main.py

from client.agent import AutoInvestigatorAgent

if __name__ == "__main__":
    # Initialize the agent
    agent = AutoInvestigatorAgent()

    # Get user input
    user_query = input("Please enter your query about a company: ")

    # Run the agent with the user's query
    if user_query:
        agent.run(user_query)