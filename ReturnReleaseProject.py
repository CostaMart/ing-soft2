import requests

class CommitInfo:
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

def get_commits_for_release(repo_owner, repo_name, release_tag, access_token):
    url = f"https://api.github.com/repos/{repo_owner}/{repo_name}/commits?sha={release_tag}"
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Accept": "application/vnd.github.v3+json"
    }

    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        commits = response.json()
        commit_list = [CommitInfo(
            sha=commit["sha"],
            node_id=commit["node_id"],
            author_name=commit["commit"]["author"]["name"],
            author_email=commit["commit"]["author"]["email"],
            author_date=commit["commit"]["author"]["date"],
            committer_name=commit["commit"]["committer"]["name"],
            committer_email=commit["commit"]["committer"]["email"],
            committer_date=commit["commit"]["committer"]["date"],
            message=commit["commit"]["message"],
            tree_sha=commit["commit"]["tree"]["sha"],
            tree_url=commit["commit"]["tree"]["url"],
            commit_url=commit["url"],
            html_url=commit["html_url"],
            comments_url=commit["comments_url"],
            author_login=commit["author"]["login"],
            author_id=commit["author"]["id"],
            author_avatar_url=commit["author"]["avatar_url"]
        ) for commit in commits]
        return commit_list
    else:
        print(f"Errore {response.status_code}: Impossibile ottenere i commit associati alla release.")
        return None

# Esempio di utilizzo
# repo_owner = "R2Northstar"
# repo_name = "Northstar"
# release_tag = "v1.19.9"
# access_token = "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"
# commits = get_commits_for_release(repo_owner,repo_name, release_tag, access_token)
#
# if isinstance(commits, list):
#     for commit in commits:
#         print("SHA:", commit.sha)
#         print("Author:", commit.author)
#         print("Committer:", commit.committer)
#         print("Message:", commit.message)
#         print("URL:", commit.url)
#         print("HTML URL:", commit.html_url)
#         print("Comments URL:", commit.comments_url)
#         print("Author Info:", commit.author_info)
#         print("-----")
# else:
#     print(commits)

