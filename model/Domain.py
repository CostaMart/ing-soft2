""" contains domain objects """
from model import FilterProject


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

class MetadataRepository:
    def __init__(self, data):
        self.id = data['id']
        self.node_id = data['node_id']
        self.name = data['name']
        self.full_name = data['full_name']
        self.private = data['private']
        self.owner = data['owner']
        self.html_url = data['html_url']
        self.description = data['description']
        self.fork = data['fork']
        self.url = data['url']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.pushed_at = data['pushed_at']
        self.git_url = data['git_url']
        self.ssh_url = data['ssh_url']
        self.clone_url = data['clone_url']
        self.svn_url = data['svn_url']
        self.homepage = data['homepage']
        self.size = data['size']
        self.stargazers_count = data['stargazers_count']
        self.watchers_count = data['watchers_count']
        self.language = data['language']
        self.has_issues = data['has_issues']
        self.has_projects = data['has_projects']
        self.has_downloads = data['has_downloads']
        self.has_wiki = data['has_wiki']
        self.has_pages = data['has_pages']
        self.has_discussions = data['has_discussions']
        self.forks_count = data['forks_count']
        self.archived = data['archived']
        self.disabled = data['disabled']
        self.open_issues_count = data['open_issues_count']
        self.license = data['license']
        self.allow_forking = data['allow_forking']
        self.is_template = data['is_template']
        self.web_commit_signoff_required = data['web_commit_signoff_required']
        self.topics = data['topics']
        self.visibility = data['visibility']
        self.forks = data['forks']
        self.open_issues = data['open_issues']
        self.watchers = data['watchers']
        self.default_branch = data['default_branch']
        self.temp_clone_token = data['temp_clone_token']
        self.organization = data['organization']
        self.network_count = data['network_count']
        self.subscribers_count = data['subscribers_count']
        self.tag_releases = None  # Imposta l'attributo tag_releases come nullo all'inizio

    def set_release_tags(self, owner, repo_name):
        """Metodo che setta le versioni delle release nell'oggetto
        che modella i metadati del progetto github"""
        release_tags = FilterProject.get_all_release_tag_repo(owner, repo_name)
        if release_tags:
            self.tag_releases = release_tags
        else:
            print("Impossibile impostare i tag delle release.")
