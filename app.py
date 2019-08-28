from chalice import Chalice, Response
from chalicelib.crawler import get_monthly_new_contributors
from github import GithubException, \
    RateLimitExceededException, BadCredentialsException

app = Chalice(app_name="github-crawler")


@app.route("/monthly_new_contributors/{username}", methods=["GET"])
def monthly_new_contributors_per_user(username: str):

    try:
        data = get_monthly_new_contributors(username)
        return Response(
            status_code=200,
            body={
                "data": data,
                "message": f"Successfully retrieved new contributors "
                           f"statistics for user {username}",
            },
        )

    except RateLimitExceededException:
        return Response(
            status_code=429,
            body={
                "data": {},
                "message": f"Rate Limit Exceeded Error: Github API "
                           f"hourly limit has been exceeded",
            },
        )
    except BadCredentialsException:
        return Response(
            status_code=401,
            body={
                "data": {},
                "message": f"Bad Credentials Error: Invalid Github "
                           f"authentication token",
            },
        )
    except GithubException:
        return Response(
            status_code=500,
            body={
                "data": {},
                "message": f"Github API Error: could not retrieve "
                           f"data for user {username}",
            },
        )
    except Exception:
        return Response(
            status_code=500, body={"data": {},
                                   "message": f"Internal Server Error"}
        )
