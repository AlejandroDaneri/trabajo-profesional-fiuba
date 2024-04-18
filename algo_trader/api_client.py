import requests

class ApiClient:
    def __init__(self):
        self.base_url = "http://algo_api:8080/api"

    def get_full_url(self, path):
        return f"{self.base_url}/{path}"

    def get(self, path, **kwargs):
        return requests.get(self.get_full_url(path), **kwargs)

    def post(self, path, **kwargs):
        return requests.post(self.get_full_url(path), **kwargs)

    def put(self, path, **kwargs):
        return requests.put(self.get_full_url(path), **kwargs)

    def delete(self, path, **kwargs):
        return requests.delete(self.get_full_url(path), **kwargs)
