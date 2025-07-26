from ollama import Client

client = Client()

response = client.chat(
    model="gemma:2b",
    messages=[
        {"role": "user", "content": "Привет, расскажи анекдот про Python"}
    ]
)

print(response['message']['content'])
