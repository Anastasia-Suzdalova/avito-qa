import requests

from urllib.parse import urljoin


class Host:
    def __init__(self):
        self.url = "https://qa-internship.avito.com/"

    def create_item(self, data):
        url = "/api/1/item"
        return requests.post(urljoin(self.url, url), json=data)

    def get_item_info(self, id: str):
        url = f"/api/1/item/{id}"
        return requests.get(urljoin(self.url, url))

    def get_item_statistics(self, id: str):
        url = f"/api/1/item/statistics/{id}"
        return requests.get(urljoin(self.url, url))

    def get_seller_items(self, seller_id):
        url = f"/api/1/{seller_id}/item"
        return requests.get(urljoin(self.url, url))
