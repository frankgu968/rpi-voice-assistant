import requests
from urllib.parse import urljoin

class MemoryStore:
  def __init__(self):
    self.store = None

  def get(self):
    return self.store

  def put(self, value):
    self.store = value

class Voiceflow:
  def __init__(self, apiKey, stateStore=MemoryStore):
    self.apiKey = apiKey
    self.stateStore = stateStore()
    self.url = "https://general-runtime.voiceflow.com"

  def clear_state(self):
    self.stateStore.put(None)

  def interact(self, diagramID, versionID, input):
    # Get state
    state = self.stateStore.get()
    if state is None:
      state = self.initState(diagramID, versionID)

    # Call interactions
    body = {
      "state": state,
      "request": {
        "type": 'text',
        "payload": input,
      },
      "config": {
        "tts": "true",
      },
    }
    response = requests.post(urljoin(self.url, "/interact/"+versionID), json=body, headers={"Authorization":self.apiKey}).json()

    # Save state
    self.stateStore.put(response["state"])

    # Return response
    return response

  def initState(self, diagramID, versionID):
    initialState = requests.get(urljoin(self.url, "/interact/"+versionID+"/state"), headers={"Authorization":self.apiKey}).json()

    response = requests.post(urljoin(self.url, "/interact/"+versionID), json=initialState, headers={"Authorization":self.apiKey}).json()
    return response["state"]
