import subprocess
import importlib
import sys
import os

version = "v1.0.9 BETA"

def clear_console():
  if os.name == "nt":
    _ = os.system("cls")
  else:
    _ = os.system("clear")


print("FREEPYCHATGPT: Checking if dependencies are installed...")


def install_module(module_name):
  try:
    importlib.import_module(module_name)
  except ImportError:
    print(f"FREEPYCHATGPT: {module_name} not found!")
    print(f"FREEPYCHATGPT: Installing {module_name}...")
    subprocess.check_call(
      [sys.executable, "-m", "pip", "install", module_name])


required_modules = ["colorama", "requests", "json", "time"]

for module in required_modules:
  install_module(module)

print("\nImporting Modules...")
import requests

print("\n'Requests' imported!")
import json

print("\n'JSON' imported!")
import time

print("\n'Time' imported!")
import colorama as color

color.init()
print("\n'Colorama' imported!")
time.sleep(0.5)
clear_console()
print(color.Fore.GREEN +
      f"Welcome to FreePyChatGPT by Kathool! {version}\n" +
      color.Style.RESET_ALL)

conversation_history = []


def get_completions(prompt):
  global conversation_history

  url = "https://free.churchless.tech/v1/chat/completions"  #url = "https://chatgpt-api.shn.hk/v1/" # Alternate API Endpoint
  headers = {
    "Content-Type": "application/json",
  }
  data = {
    "messages": conversation_history + [{
      "role": "user",
      "content": prompt
    }],
    "max_tokens": 100,
  }

  response = requests.post(url, headers=headers, json=data)

  if response.status_code == 200:
    return response.json()
  else:
    return None


def user_input():
  global conversation_history
  prompt_text = input(color.Fore.YELLOW + "\nYou: " + color.Style.RESET_ALL)
  conversation_history.append({
    "role":
    "system",
    "content":
    "You are an AI language model. Please respond with a greeting."
  })
  conversation_history.append({"role": "user", "content": prompt_text})
  response_data = get_completions(prompt_text)
  return response_data


while True:
  response_data = user_input()

  if response_data:
    response_str = response_data["choices"][0]["message"]["content"]
    conversation_history.append({"role": "assistant", "content": response_str})
    print(color.Fore.CYAN + "\nAI: " + color.Style.RESET_ALL + response_str)
  else:
    print(color.Fore.CYAN + "\nAI: " + color.Fore.RED +
          "Sorry, there was an error processing your request." +
          color.Style.RESET_ALL)
    break

input("Press Enter to exit...")
