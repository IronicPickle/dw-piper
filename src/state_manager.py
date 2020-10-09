from os import path
import json

from vars import Env

state_path = path.join(Env.appdata_path, "state.json")

def get():
  with open(state_path, "r", encoding='utf-8') as state_file:
    return json.loads(state_file.read())

def update(state, updates):
  with open(state_path, "w", encoding='utf-8') as state_file:
    for i in updates:
      state[i] = updates[i]
    json.dump(state, state_file, ensure_ascii=False, indent=4)
