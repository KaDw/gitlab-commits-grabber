#!/usr/bin/python3

# ----------------------------------------------------------------------------
# "THE BEER-WARE LICENSE" (Revision 42):
# KaDw wrote this file.  As long as you retain this notice you
# can do whatever you want with this stuff. If we meet some day, and you think
# this stuff is worth it, you can buy me a beer in return.
# ----------------------------------------------------------------------------

# python3 gitlab-commits-grabber.py -u https://gitlab.xxxxx.com -t 8L5c8IMDayZvHSBowCuW -e user@xxxxx.com -o commits_dump
import gitlab
import json
import argparse

def getContributedProjectsId(projects, user_email):
    contributed_projects = []
    for project in projects:
        try:
            contributors = project.repository_contributors()
        except: # nasty stuff, how to catch GitlabHttpError?
            print('Skipping {} due to GitlabHttpError'.format(project.name))
            continue
        for contributor in contributors:
            if(contributor['email'] == user_email):
                contributed_projects.append(project)
    return contributed_projects

def getUserCommits(projects, user_email):
    user_commits = []
    for project in projects:
        print(project.name)
        commits = project.commits.list(all=True,
                               query_parameters={'all': True})
        for commit in commits:
            if commit.author_email == user_email:
                user_commits.append({'project': project.name, 'committed_date': commit.committed_date, 'message': commit.message, 'short_id': commit.short_id})
    return user_commits

parser = argparse.ArgumentParser(description='Gitlab commit grabber')
parser.add_argument('-u', '--url', dest='gitlab_url', required=True, help='Gitlab url, exmaple: https://gitlab.xxxxx.com')
parser.add_argument('-t', '--token', dest='token', required=True, help='Private token or personal token authentication, can be read only')
parser.add_argument('-e', '--user_email', dest='user_email', required=True, help='Commits will be grabbed by user email')
parser.add_argument('-o', '--output', dest='output_filename', required=True, help='Output file, it will be json')
args = parser.parse_args()
# private token or personal token authentication
gl = gitlab.Gitlab(args.gitlab_url, private_token=args.token)
gl.auth()

print('Getting all projects visible to {}... (it might take a while)'.format(args.user_email))
projects = gl.projects.list(all=True)
print('Filtering contributed projects...')
contrib_projects = getContributedProjectsId(projects, args.user_email)
print('Getting user commits...')
commits = getUserCommits(contrib_projects, args.user_email)
print('Saving to json file...')
filename = args.user_email.split('@')[0] + '_' + args.output_filename + '.json' 
print('Contributed repositories: {}'.format(len(contrib_projects)))
print('Total commits: {}'.format(len(commits)))
with open(filename, 'w') as fout:
    json.dump(commits, fout)
