import chainlit as cl
import asyncio
import os
@cl.on_message
async def main(message: cl.Message):
    print ("Hi from chainlit chatbot")
# D:\Panaverse\AgentSdk\class_agent\src\class_agent\chatbot.py