import requests

def brandfetch(name: str) -> list[dict]:
    url = f"https://api.brandfetch.io/v2/search/{name}"
    querystring = { "c": "1idcJMH79P9Ec7yWgdQ" }
    response = requests.get(url, params=querystring)
    
    companies = [{"name": c["name"], "domain": c["domain"]} for c in response.json()]
    
    return companies

    
if __name__ == "__main__":
    brandfetch("domino")