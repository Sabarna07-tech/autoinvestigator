def get_tool_description():
    description = """
Tool 1:
    name : "websearch"
    params : 
        1. query:string(proper query to ask search about a company. example = "Detail Company profile of <company name> company profile site:investopedia.com OR site:crunchbase.com OR site:forbes.com OR site:finance.yahoo.com OR site:sec.gov")
    description : given tool searches about the company given in 'query' and gives a detail report. Mainly used for gathering online available data
Tool 2:
    name : "financial_descriptor"
    params :
        1. ticker:string (name of the company)
        2. cik:string (cik number of the company)
    description : This tool takes the company name and gives current and recent financial report of that company.
Tool 3:
    name : "news"
    params :
        1. name:string (name of the company)
    description : This tool takes the company name and scans recent news articles related to lawsuits, fraud, or other risks for a given company.
Tool 4:
    name: "send_mail"
    params :
        1. subject:string(Subject of the mail)
        2. message:string(The actual mail body)
        3. receiver:string(email or name of receiver)
    description : This tool sends a designated to send a mail to a designated sender.
"""
    return description
    
    
def get_prompt_list():
    prompt_names = ['request_template','main_prompt']
    return prompt_names