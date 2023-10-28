""" contains domain objects """

class Repository:
    def __init__(self, name, html_url, description):
        self.name = name
        self.url = html_url
        self.description = description