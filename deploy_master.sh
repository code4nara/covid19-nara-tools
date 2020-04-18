curl -X POST -H "Authorization: token ${GITHUB_TOKEN}" \
             -H "Content-Type: application/json" \
             https://api.github.com/repos/code4nara/covid19/deployments \
             --data '{"ref": "master", "environment": "production"}'}'
