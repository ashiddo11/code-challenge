#!/usr/bin/env python

# Please install dependencies and add auth token

import pygithub3
import subprocess
import git
import requests

gh = None
user = "ashiddo11"
repos_edit = []
repo_names = []
auth_token = ""

def get_repos(all_repos):
	for repo in all_repos:
		yield repo.clone_url

def replace_prefix(filenames):
	for filename in filenames:
		f = open(filename)
		lines = f.readlines()
		f.close()
		f = open(filename, 'w')
		for line in lines:
			f.write(line[1:])
			f.close()

def extract_repo_name(repos):
	for repo in repos:
		repo_name = repo.split("/")[1]
		repo_names.append(repo_name)
	return repo_names

def find_repo_edit(filename):
	repos_edit = subprocess.check_output(['find', '.', '-name', filename])
	#repos_edit = repos_edit.rstrip('\n')
	return repos_edit

def create_push(repos, filename):
	for repo in repos:
		print repo
		repo_url = repo
		repo = "./" + repo
		repo = git.Repo(repo)
		repo.git.branch('fix')
		replace_prefix(repos_edit)
		repo.git.add(filename)
		repo.git.commit( m='Removed common prefix' )
		repo.git.push("origin", "fix")
		headers = {
		'Authorization': 'token %s' % auth_token,
		}

		data = '{ "title": "Testing", "body": "Hotfix", "head": "fix", "base": "master" }'

		requests.post("https://api.github.com/repos/%s/%s/pulls" % (user,repo_url), headers=headers, data=data)

if __name__ == '__main__':
	gh = pygithub3.Github()

	all_repos = gh.repos.list(user=user).all()
	repos = get_repos(all_repos)

	for url in repos:
		subprocess.call(['git', 'clone', url])
	repos_edit = find_repo_edit("VERSION.txt")
	repos_edit = repos_edit.splitlines()
	repo_names = extract_repo_name(repos_edit)
	print repo_names
	create_push(repo_names, "VERSION.txt")
	
