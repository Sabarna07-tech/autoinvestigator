import json

def string_to_json(string:str):
	try:
		clean_json = string.strip("`").split("\n", 1)[-1].rsplit("\n", 1)[0]
		data = json.loads(clean_json)
		return data
	except Exception as e:
		return None
        
if __name__=='__main__':
    op = """```{
                    "cik": "12345", 
                    "ticker": "afd"
               }```"""
    data = string_to_json(op)
    print(data)