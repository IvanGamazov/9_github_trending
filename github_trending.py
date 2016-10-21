import requests
import datetime


GITHUB_API_URL = 'https://api.github.com/search/repositories?q=created:>'


def input_time_period():
    return int(input('За какой промежуток времени искать репозитории? -->'))


def input_quantity_for_search():
    return int(input('Сколько репозиториев подбирать? -->'))


def get_start_search_date(days):
    search_date = datetime.date.today() - datetime.timedelta(days=days)
    return search_date


def get_trending_repositories(date, repos_count):
    str_date = str(date)
    payload = {'q': 'created:>'+str_date, 'sort': 'stars', 'order': 'desc'}
    response = requests.get(GITHUB_API_URL, params=payload)
    repositories = response.json()['items'][:repos_count]
    return repositories


def get_top_repos(repositories):
    top_repos = []
    for repo in repositories:
        top_repo = {'name': repo['name'],
                    'url': repo['html_url'],
                    'issues': repo['open_issues_count'],
                    'stars': repo['stargazers_count']}
        top_repos.append(top_repo)
    return top_repos


if __name__ == '__main__':
    length_in_days = input_time_period()
    start_date = get_start_search_date(length_in_days)
    amount_of_repos = input_quantity_for_search()
    repositories_list = get_trending_repositories(start_date, amount_of_repos)
    top_repositories = get_top_repos(repositories_list)
    sorted_repos = sorted(top_repositories, key=lambda rep: rep['issues'])
    print('Популярные репозитории:')
    for repo in sorted_repos:
        print('Название:', repo['name'], ' Ссылка:', repo['url'],
              ' Проблем:', repo['issues'], ' Звезд:', repo['stars'])


