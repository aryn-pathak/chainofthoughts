import requests
import ast
import prompts #file with all system prompts

print("Get AI to solve complex questions with steps!")

#CODE USES PERPLEXITY API AND IT'S DOCUMENTATION.

#First model: break the question down into steps for other models to solve.
url = "https://api.perplexity.ai/chat/completions"
payload = {
    "model": "llama-3.1-sonar-huge-128k-online",
    "messages": [
        {
            "role": "system",
            "content": prompts.stepPrompt
        },
        {
            "role": "user",
            "content": input("Enter your question: ")
        }
    ],
    "temperature": 0.01,
    "top_p": 0.3,
    "presence_penalty": 0.6,
    "response_format": None
}
headers = {
    "Authorization": "Bearer API_KEY_HERE",
    "Content-Type": "application/json"
}

response = requests.request("POST", url, json=payload, headers=headers)

def extract_response(api_json):
    return api_json["choices"][0]["message"]["content"] #remove any metadata

steps = ast.literal_eval(extract_response(response.json()))
numSteps = len(steps)

print("broken down steps")

solvedSteps = []

for i in range(numSteps-2):
    currentStep = steps[i]

#Second model: solve each step individually
    payload = {
        "model": "llama-3.1-sonar-large-128k-online",
        "messages": [
            {
                "role": "system",
                "content": prompts.solvePrompt
            },
            {
                "role": "user",
                "content": f"Question: {currentStep}"
            }
        ],
        "temperature": 0.05,
        "top_p": 0.9,
        "frequency_penalty": 1,
        "response_format": None
    }
    
    headers = {
        "Authorization": "Bearer API_KEY_HERE",
        "Content-Type": "application/json"
    }

    responseStep = requests.request("POST", url, json=payload, headers=headers)
    solvedSteps.append(extract_response(responseStep.json()))
    print(f"solved step: {currentStep}")

print("solved all steps!")
print("processing answer...")

url = "https://api.perplexity.ai/chat/completions"

payload = {
    "model": "llama-3.1-sonar-huge-128k-online",
    "messages": [
        {
            "role": "system",
            "content": prompts.summarizePrompt
        },
        {
            "role": "user",
            "content": f"instructions: {steps[numSteps-1]} text: {solvedSteps}"
        }
    ],
    "temperature": 0.01,
    "top_p": 0.9,
    "top_k": 0,
    "stream": False,
    "presence_penalty": 0,
    "frequency_penalty": 1,
    "response_format": None
}
headers = {
    "Authorization": "Bearer API_KEY_HERE",
    "Content-Type": "application/json"
}

responseFinal = requests.request("POST", url, json=payload, headers=headers)
final_answer = extract_response(responseFinal.json())
print("done processing!")
print(final_answer)
