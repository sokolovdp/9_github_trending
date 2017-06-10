import requests
import sys
import argparse
from pprint import pprint


def get_response(url, par):
    response = requests.get(url, par)
    if response.ok:
        return response.json()['items']
    else:
        print("github api error:")
        pprint(response)


def main(n: "int", date: "str"):
    parameters = {'q': 'created:>{}'.format(date), 'sort': 'stars', 'order': 'desc'}
    trending_repositories = get_response('https://api.github.com/search/repositories', parameters)[:n]
    for rep in trending_repositories:
        print("{} {}, open issues: {}".format(rep['html_url'], rep['description'].strip(), rep['open_issues_count']))


if __name__ == '__main__':
    ap = argparse.ArgumentParser(description='this program prints N top GitHub repositories from the given date')
    ap.add_argument("--n", dest="n", action="store", type=int, required=True, help="  number of repositories")
    ap.add_argument("--date", dest="date", action="store", required=True, help="  date, in the format: YYYY-MM-DD")
    args = ap.parse_args(sys.argv[1:])

    main(args.n, args.date)
