# lets put a gradio interface on top of this
# https://gradio.app/getting_started

import gradio as gr
import requests
import json

session = requests.Session()
url = 'http://localhost:8000/conversation'

headers = {
    'Content-Type': 'application/json'
}


def emergency_room_triage(text: str) -> str:
    """this function is the interface between the gradio interface and the backend
    it takes the text input from the gradio interface and sends it to the backend"""

    data = {
        'human_input': text
    }
    # Make a POST request within the session
    response = session.post(url, json=data, headers=headers)

    # Check the status code and handle the response accordingly
    if response.status_code == 200:
        print('Request was successful:', response.text)
    else:
        print('Failed to make a request:', response.status_code, response.text)

    json_payload = json.loads(response.text)

    return str(json_payload['output'])


gr.Interface(fn=emergency_room_triage, inputs="text", outputs="text").launch()
