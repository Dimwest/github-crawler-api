import os
import itertools
import pandas as pd
from pandas.tseries.offsets import MonthBegin
from typing import List, Dict, Any
from github import Github, GithubException, Repository
from github.NamedUser import NamedUser
from chalicelib.log import logger, with_logging
from concurrent.futures import ThreadPoolExecutor
from chalicelib.secretsmanager import retrieve_secret


def get_repo_commits(repo: Repository.Repository) -> List[Dict[str, Any]]:

    """
    Fetches and formats all commits for a specific Github repository.
    Runs in multiple threads, which requires specific retrying logic.

    :param repo: Github Repository object
    :return: list of dicts containing commits information
    """

    results = []

    try:

        commits = repo.get_commits()
        for c in commits:
            r = {
                "repo": repo.name,
                "author": c.commit.author.name,
                "date": c.commit.author.date,
            }
            results.append(r)

    except GithubException as e:

        if e.args[0] == 409 \
                and e.args[1]["message"] == "Git Repository is empty.":
            logger.warning(f"Repository {repo.name} is empty, "
                           f"returning empty list")
            return []

        else:
            raise e

    return results


def get_github_user(username: str) -> NamedUser:

    """
    Authenticates to Github API and fetches the specified user.

    :param username: name of the user to fetch
    :return: Github NamedUser object
    """

    token = (
        os.environ.get("GITHUB_API_TOKEN")
        or retrieve_secret(
            os.environ.get("GITHUB_SECRETNAME"))["github_api_token"]
    )
    if not token:
        logger.warning(
            f"Environment variable GITHUB_API_TOKEN is not set, "
            f"unauthenticated requests have lower rate limits "
            f"(60 per hour)"
        )
        g = Github()
    else:
        g = Github(token)
    user = g.get_user(username)
    return user


@with_logging
def get_user_commits(username: str) -> List[Dict[str, Any]]:

    """
    Fetches the specified user's repositories, then fetches
    all their commits in separate threads and chains
    result as a list.

    :param username: name of the user to fetch commits from
    :return: list of dicts containing commits information
    """

    user = get_github_user(username)

    with ThreadPoolExecutor(
            max_workers=int(os.environ["MAX_WORKERS"])
    ) as executor:
        commits = executor.map(get_repo_commits, user.get_repos())

    commits = list(itertools.chain.from_iterable(commits))
    return commits


@with_logging
def count_new_contributors(commits_data: List[Dict[str, Any]]) -> pd.DataFrame:

    """
    Processes API results in a Pandas DataFrame to compute the monthly
    count of new contributors per repository.

    :param commits_data: list of dicts containing commits information
    :return: Pandas DataFrame containing aggregated data
    """

    df = (
        pd.DataFrame.from_records(commits_data)
        .groupby(["repo", "author"])["date"]
        .min()
        .reset_index()
    )
    df["datemonth"] = (pd.to_datetime(df["date"]) - MonthBegin(1)).dt.date
    df = df.groupby(["repo", "datemonth"]).size().reset_index()
    return df


@with_logging
def get_monthly_new_contributors(username: str):

    commits = get_user_commits(username)
    results = count_new_contributors(commits)
    results = results.to_json(orient="records", date_format="iso")
    return results
