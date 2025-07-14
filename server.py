from flask import Flask,request,jsonify
from dotenv import load_dotenv


app=Flask(__name__)


"""
Basic Request Format:
{
    id : <id>,
    requests:[
        {
            id:<request_id>,
            method : "tools/<tool_name>",
            params : {
                param1:value1,
                param2:value2,
                ...
            }
        },
        {
            id:<request_id>,
            method : "tools/<tool_name>",
            params : {
                param1:value1,
                param2:value2,
                ...
            }
        },
        ...
        {
            id:<prompt id>,
            method : "prompt/<prompt_name>"
        }
        ...
        {
            id:<resource_id>,
            method : "resource/<resource_name>",
            action : [
                action1,
                action2,
                ...
            ]
        }
    ]
}

Basic Response Format:
{
    id:<id>
    results:[
        {
            id:<request_id>,
            method: "tools/<tool_name>",
            results:[...]
        },
        {
            id:<request_id>,
            method: "tools/<tool_name>,
            results:[...]
        },
        ...
        {
            id:<prompt id>,
            method : "prompt/<prompt_name>"
            results : [...]
        }
        ...
        {
            id:<resource_id>,
            method : "resource/<resource_name>",
            results : [...]
        }
    ]
}
"""

from server.interface import UTIL
from server.prompts.primary_prompts import BASIC_REQUEST_TEMPLATE,BASIC_PROMPT
from server.tool_descriptor import get_tool_description, get_prompt_list

util = UTIL()

def request_handler(request):
    try:
        id = request['id'] if 'id' in request else None
        response = {'id':id, 'results':[]}
        
        for req in request['requests']:
            res = {}
            res['id'] = req['id']
            res['method'] = req['method']
            n, method = req['method'].strip().split('/') 
            
            if n=='tools':
                if method == "websearch":
                    query = req['params']['query']
                    ans = util.get_web_search(query)
                    res['results'] = [ans]
                elif method == "financial_descriptor":
                    ticker = req['params'].get('ticker')
                    if ticker is None:
                        ticker = "Unknown"
                    cik = req['params'].get('cik')
                    if cik is None:
                        cik = "Unknown"
                    print(f"Ticker: {ticker}, CIK: {cik}")
                    ans = util.get_financial_data(ticker=ticker,cik=cik)
                    res['results'] = [ans]
                elif method == "news":
                    name = req['params']['name']
    # Call the tool once and store the result in 'ans'
                    ans = util.get_news(name=name)
    # Reuse the result
                    res['results'] = [ans]
                elif method == "send_mail":
                    subject = req['params']['subject']
                    message = req['params']['message']
                    receiver = req['params']['receiver']
                    res['results']=[util.send_mail(subject=subject, message=message, receiver=receiver)]
                elif method == "list":
                    ans = get_tool_description()
                    res['results'] = [ans]
                elif method == "gemini":
                    query = req['params']['query']
                    ans = util.llm.run(query) # 'util.llm' is the GeminiAgent instance
                    res['results'] = [ans]
                else:
                    res['results'] = []
                    
            elif n=="prompt":
                if method == "request_template":
                    res['results'] = [BASIC_REQUEST_TEMPLATE]
                elif method == "main_prompt":
                    res['results'] = [BASIC_PROMPT]
                elif method == "list":
                    L = get_prompt_list()
                    res['results'] = L
                else:
                    res['results'] = []
                          
            elif n=="resources":
                pass
                
            response['results'].append(res)
        return response
    except Exception as e:
        raise e
        return {"message":"Bad Request. Please check the format"}


@app.route('/requests',methods=['POST'])
def base():
    data = request.get_json()
    print(data)
    res = request_handler(data)
    return jsonify(res)
    
   

if __name__ == '__main__':
    load_dotenv()
    app.run(debug=True, port=5001)