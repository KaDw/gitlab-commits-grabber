# gitlab-commits-grabber

Script to extract commits contributed to all repositories by specific user.
You need to provide following information:
* '-u', '--url', dest='gitlab_url', required=True, help='Gitlab url, exmaple: https://gitlab.xxxxx.com'
* '-t', '--token', dest='token', required=True, help='Private token or personal token authentication, can be read only'
* '-e', '--user_email', dest='user_email', required=True, help='Commits will be grabbed by user email'
* '-o', '--output', dest='output_filename', required=True, help='Output file, it will be json'
