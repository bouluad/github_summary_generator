import os
import requests
import logging

class GPTAPI:
    def __init__(self, api_url):
        self.api_url = api_url
        self.headers = self.get_headers()

    def get_headers(self):
        application_name = os.getenv("GPT_API_APPLICATION_NAME")
        key_name = os.getenv("GPT_API_KEY_NAME")
        key_value = os.getenv("GPT_API_KEY_VALUE")

        if not all([application_name, key_name, key_value]):
            logging.error("Missing environment variables for GPT API authentication")
            raise ValueError("Missing environment variables for GPT API authentication")

        return {
            "Content-Type": "application/json",
            application_name: key_name,
            key_name: key_value
        }

    def request_completion(self, prompt, max_tokens=50):
        data = {
            "prompt": prompt,
            "max_tokens": max_tokens
        }
        response = requests.post(self.api_url, headers=self.headers, json=data)
        if response.status_code == 200:
            return response.json()
        else:
            response.raise_for_status()
