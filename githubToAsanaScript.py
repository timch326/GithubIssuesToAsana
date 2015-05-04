from github import Github
from asana import Client
import getpass

githubUsername = raw_input("Enter Your Github Username: ")
githubPassword = getpass.getpass("Enter Your Github Password: ")
githubRepoName = raw_input("Enter Your Full Github Repository Name (owner/repoName): ")
asanaAPIKey = getpass.getpass("Enter Your Asana API Key: ")
asanaWorkplaceId = raw_input("Enter Your Asana Workplace ID: ")
asanaProjectId = raw_input("Enter Your Asana Project ID: ")

asanaClient = Client.basic_auth(asanaAPIKey)
github = Github(githubUsername, githubPassword)

repo = github.get_repo(githubRepoName)

labels = repo.get_labels()
tagMapping = {}

for label in labels:
	print(label.name)
	tagId = asanaClient.tags.create(
		name = label.name, 
		workspace = asanaWorkplaceId
		)["id"]
	tagMapping[label.name] = tagId

issues = repo.get_issues()
for issue in issues:
	print(issue.title)
	taskId = asanaClient.tasks.create(
		name = issue.title,
		notes = issue.body, 
		projects = [asanaProjectId],
		workspace = asanaWorkplaceId)["id"]
	for label in issue.labels:
		asanaClient.tasks.add_tag(task_id = taskId, tag=tagMapping[label.name])
