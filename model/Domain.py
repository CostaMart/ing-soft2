""" contains domain objects """

class Repository:
    def __init__(self, name, html_url, description,releases=None):
        self.name = name
        self.url = html_url
        self.description = description
        self.releases=releases

class Commit:
    def __init__(self, sha, node_id, author_name, author_email, author_date, committer_name, committer_email, committer_date, message, tree_sha, tree_url, commit_url, html_url, comments_url, author_login, author_id, author_avatar_url):
        self.sha = sha
        self.node_id = node_id
        self.author = {
            "name": author_name,
            "email": author_email,
            "date": author_date
        }
        self.committer = {
            "name": committer_name,
            "email": committer_email,
            "date": committer_date
        }
        self.message = message
        self.tree = {
            "sha": tree_sha,
            "url": tree_url
        }
        self.url = commit_url
        self.html_url = html_url
        self.comments_url = comments_url
        self.author_info = {
            "login": author_login,
            "id": author_id,
            "avatar_url": author_avatar_url
        }

