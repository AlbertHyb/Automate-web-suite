import requests

class ApiHelper:
    def __init__(self, base_url):
        self.base_url = base_url.rstrip('/')

    def is_service_up(self):
        try:
            response = requests.get(f"{self.base_url}/docs")
            return response.status_code == 200
        except Exception:
            return False

    def make_request(self, endpoint, method="GET", data=None, headers=None, use_form_data=False):
        url = f"{self.base_url}/{endpoint.lstrip('/')}"
        if headers is None:
            headers = {}
        try:
            if method.upper() == "POST":
                if use_form_data:
                    headers = {**headers, "Content-Type": "application/x-www-form-urlencoded"}
                    response = requests.post(url, data=data, headers=headers)
                else:
                    response = requests.post(url, json=data, headers=headers)
            else:
                response = requests.get(url, params=data, headers=headers)
            return response
        except requests.ConnectionError as e:
            raise RuntimeError(f"No se pudo conectar a la API en {url}: {e}")
