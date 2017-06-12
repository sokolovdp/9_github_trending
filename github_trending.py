import requests
import sys
import argparse


def get_response(url: "str", parameters: "dict"):
    response = requests.get(url, parameters)
    if response.ok:
        return response.json()['items']
    else:
        print("github api error: ", response)


def get_trending_repositories(number_of_repos: "int", from_date: "str"):
    parameters = {'q': 'created:>{}'.format(from_date), 'sort': 'stars', 'order': 'desc'}
    return get_response('https://api.github.com/search/repositories', parameters)[:number_of_repos]


def main(number_of_repos: "int", from_date: "str"):
    for repo in get_trending_repositories(number_of_repos, from_date):
        print("{} {}, open issues: {}".format(repo['html_url'], repo['description'].strip(), repo['open_issues_count']))


if __name__ == '__main__':
    ap = argparse.ArgumentParser(description='this program prints N top GitHub repositories from the given date')
    ap.add_argument("--n", dest="n", action="store", type=int, default=20, help="  number of repositories")
    ap.add_argument("--date", dest="date", action="store", required=True, help="  date, in the format: YYYY-MM-DD")
    args = ap.parse_args(sys.argv[1:])

    main(args.n, args.date)
