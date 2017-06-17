import requests
import sys
import argparse


def make_response(data: "list", error: "str") -> "dict":
    return {'data': data, 'err': error, 'ok': error is None}


def get_response(url: "str", parameters: "dict") -> "make_response":
    response = requests.get(url, parameters)
    if response.ok:
        return make_response(response.json()['items'], None)
    else:
        return make_response(None, "api error")


def get_trending_repositories(number_of_repos: "int", from_date: "str"):
    parameters = {'q': 'created:>{}'.format(from_date), 'sort': 'stars', 'order': 'desc', 'per_page': number_of_repos}
    github_response = get_response('https://api.github.com/search/repositories', parameters)
    if github_response['ok']:
        return github_response['data']


def main(number_of_repos: "int", from_date: "str"):
    trending_repos = get_trending_repositories(number_of_repos, from_date)
    if trending_repos is not None:
        for repo in trending_repos:
            print("{} {}, open issues: {}".format(repo['html_url'], repo['description'].strip(),
                                                  repo['open_issues_count']))
    else:
        print("github api response error")


if __name__ == '__main__':
    ap = argparse.ArgumentParser(description='this program prints N top GitHub repositories from the given date')
    ap.add_argument("--n", dest="n", action="store", type=int, default=20, help="  number of repositories")
    ap.add_argument("--date", dest="date", action="store", required=True, help="  date, in the format: YYYY-MM-DD")
    args = ap.parse_args(sys.argv[1:])

    main(args.n, args.date)
