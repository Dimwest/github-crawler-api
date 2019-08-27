from chalice import Chalice
from chalicelib.crawler import get_monthly_new_contributors
from github import GithubException, RateLimitExceededException, BadCredentialsException

app = Chalice(app_name='github-crawler')


@app.route('monthly_new_contributors/<username>')
def monthly_new_contributors_per_user(username: str):

    try:
        data = get_monthly_new_contributors(username)
        print(data)
        return data
    except RateLimitExceededException:
        return {
            'status_code': 429,
            'message': f'Rate Limit Exceeded Error: Github API hourly limit has been exceeded'
        }
    except BadCredentialsException:
        return {
            'status_code': 401,
            'message': f'Bad Credentials Error: Invalid Github authentication token'
        }
    except GithubException as e:
        return {
            'status_code': 500,
            'message': f'Github API Error: {type(e)} -> {e.args}'
        }
    except Exception as e:
        return {
            'status_code': 500,
            'message': f'Internal server Error: {type(e)} -> {e.args}'
        }


# @app.route('monthly_new_contributors/<username>/<repo>')
# def monthly_new_contributors_per_repo(username: str, repo: str):
#     return get_monthly_new_contributors(username)
