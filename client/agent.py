# client/agent.py

import json
import requests
import uuid
import re
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

from client.pydantic_models import RequestPayload
from client.config import SERVER_URL, GEMINI_API_KEY

class AutoInvestigatorAgent:
    """
    The client-side agent that interacts with the user, the LLM, and the MCP server.
    """
    def __init__(self):
        """
        Initializes the agent, setting up the LLM and the server URL.
        """
        self.server_url = SERVER_URL
        self.llm = ChatGoogleGenerativeAI(model="gemini-2.0-flash", google_api_key=GEMINI_API_KEY)

    def _get_main_prompt(self) -> str:
        """
        Fetches the main prompt from the server.
        """
        print("Fetching main prompt from server...")
        payload = {
            "id": f"prompt-request-{uuid.uuid4()}",
            "requests": [
                {
                    "id": f"prompt-main-{uuid.uuid4()}",
                    "method": "prompt/main_prompt"
                }
            ]
        }
        response = requests.post(self.server_url, json=payload)
        response.raise_for_status()
        return response.json()["results"][0]["results"][0]

    def _get_llm_request_json(self, prompt_template: str, user_query: str) -> str:
        """
        Uses the LLM to generate the tool invocation JSON based on the user query.
        """
        print("Getting LLM to generate tool invocation JSON...")
        # Construct the prompt directly, placing the user query inside the template from the server
        # This avoids the langchain templating error.
        full_prompt = f"{prompt_template}\n\nHere is the user's query:\n---{user_query}\n---"

        # We still use ChatPromptTemplate, but now it's just a simple wrapper
        prompt = ChatPromptTemplate.from_template("{input}")
        chain = prompt | self.llm | StrOutputParser()
        return chain.invoke({"input": full_prompt})


    def _parse_llm_output(self, llm_output: str) -> dict:
        """
        Parses the string output from the LLM to a dictionary.
        This version is more robust and handles markdown code blocks.
        """
        print("Parsing LLM output...")
        # Use regex to find the JSON block, even if it's inside markdown
        match = re.search(r"```(json)?\s*(\{.*?\})\s*```", llm_output, re.DOTALL)
        if match:
            json_string = match.group(2)
        else:
            # Fallback to finding the first and last curly brace
            start = llm_output.find('{')
            end = llm_output.rfind('}') + 1
            if start != -1 and end != -1:
                json_string = llm_output[start:end]
            else:
                raise ValueError("No JSON object found in the LLM output.")

        try:
            return json.loads(json_string)
        except json.JSONDecodeError as e:
            print(f"Error parsing JSON from LLM output: {e}")
            raise ValueError(f"Could not decode JSON from LLM output: {json_string}") from e


    def _execute_server_request(self, request_json: dict) -> dict:
        """
        Sends the request to the server and gets the results.
        """
        print("Sending request to server...")
        # Validate the request payload using Pydantic
        request_payload = RequestPayload(**request_json)
        response = requests.post(self.server_url, json=request_payload.dict())
        response.raise_for_status()
        return response.json()

    def _get_final_response(self, user_query: str, server_results: dict) -> str:
        """
        Gets the final, summarized response from the LLM.
        """
        print("Getting final response from LLM...")
        # Use a template for the final summarization
        template = """
        Based on the original query and the results from the tools, provide a comprehensive answer.

        Original User Query:
        ---
        {query}
        ---

        Tool Results:
        ---
        {results}
        ---

        Final Answer:
        """
        prompt = ChatPromptTemplate.from_template(template)
        chain = prompt | self.llm | StrOutputParser()
        
        # Convert server results to a clean JSON string for the prompt
        results_str = json.dumps(server_results, indent=2)
        
        return chain.invoke({"query": user_query, "results": results_str})


    def run(self, user_query: str):
        """
        The main execution flow of the agent.
        """
        try:
            # 1. Get the main prompt from the server
            main_prompt = self._get_main_prompt()

            # 2. Get the tool invocation JSON from the LLM
            llm_request_str = self._get_llm_request_json(main_prompt, user_query)
            print(f"\nLLM Generated Request:\n{llm_request_str}\n")

            # 3. Parse the LLM's string output
            request_json = self._parse_llm_output(llm_request_str)

            # 4. Execute the request on the server
            server_response = self._execute_server_request(request_json)
            print(f"\nServer Response:\n{json.dumps(server_response, indent=2)}\n")


            # 5. Get the final, summarized response from the LLM
            final_answer = self._get_final_response(user_query, server_response)
            print(f"\nFinal Answer:\n{final_answer}\n")

        except requests.exceptions.RequestException as e:
            print(f"Error communicating with the server: {e}")
        except ValueError as e:
            print(f"A data-related error occurred: {e}")
        except Exception as e:
            print(f"An unexpected error occurred: {e}")