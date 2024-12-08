import requests

url = "http://127.0.0.1:5000/"
data = {
    "input_text": "Here is an email to an employee. Please write a formal response acknowledging their resignation."
}

response = requests.post(url, json=data)

print("Response Status Code:", response.status_code)
print("Response Data:", response.json())