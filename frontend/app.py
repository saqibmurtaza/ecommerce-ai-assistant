# frontend/app.py
import chainlit as cl
import requests

BACKEND_URL = "http://localhost:8000"  # update this if deploying

@cl.on_message
def handle_message(message: cl.Message):
    if "product" in message.content.lower():
        products = requests.get(f"{BACKEND_URL}/products").json()
        text = "\n".join([f"🪑 {p['title']}: ${p['price']}" for p in products])
        cl.Message(content=f"Here are some products:\n\n{text}").send()
    elif "promo" in message.content.lower():
        promos = requests.get(f"{BACKEND_URL}/promos").json()
        text = "\n".join([f"🎉 {p['message']} → {p['ctaLink']}" for p in promos])
        cl.Message(content=f"Active promotions:\n\n{text}").send()
    else:
        cl.Message(content="Hi! Ask me about our products or promotions!").send()
