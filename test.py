import requests, json

def run_post(n):
    url = 'http://localhost:5000/api/n'
    data = {'number': n}
    headers = {'Content-Type' : 'application/json'}
    r = requests.post(url, data=json.dumps(data), headers=headers)
    return r.json()

if __name__ == "__main__":
    run_post(3)