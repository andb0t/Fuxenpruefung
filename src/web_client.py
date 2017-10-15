import argparse
import requests

import tabulate

URL_READ = 'https://fuxenserver.herokuapp.com/highscore'
URL_POST = 'https://fuxenserver.herokuapp.com/scores'


def read_highscore():
    print('Retrieving info from', URL_READ, '...')

    response = requests.get(URL_READ)
    scores = response.json()

    print('Got response from server')
    try:
        keys = sorted(scores[0].keys())
    except IndexError:
        print('No entry present')
        return
    table = []
    for s in scores:
        table.append([s[key] for key in keys])
    print(tabulate.tabulate(table, headers=keys, tablefmt='grid'))
    return scores


def post_score(username, score, message):
    print('Posting info to', URL_POST, '...')
    response = requests.post(URL_POST,
                             json={
                                   'username': username,
                                   'score': score,
                                   'message': message,
                                   }
                             )
    # if request fails or throws error
    response.raise_for_status()


def main():
    parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('task', choices=['read', 'post'], help='Type of server interaction')
    parser.add_argument('--name', default='', help='Name of user')
    parser.add_argument('--msg', default='', help='Optional message')
    parser.add_argument('--score', default=0, type=int, help='Achieved score')
    args = parser.parse_args()

    if args.task == 'post':
        post_score(username=args.name, score=args.score, message=args.msg)
    elif args.task == 'read':
        read_highscore()


if __name__ == '__main__':
    main()
