import requests
import datetime


def get_time_period():
    return int(input('За какой промежуток времени искать репозитории? -->'))


def get_quantity_for_search():
    return int(input('Сколько репозиториев подбирать? -->'))


def get_start_search_date():
    search_date = datetime.date.today() - datetime.timedelta(days=get_time_period())
    return search_date


def get_trending_repositories():
    response = requests.request('GET', 'https://api.github.com/search/repositories?q=created:>'
                                + str(get_start_search_date())+'&sort=stars&order=desc')
    repositories = response.json()['items'][:get_quantity_for_search()]
    return repositories


def get_open_issues_amount(repository):
    response = requests.request('GET', repository['url']+'/issues')
    return len(response.json())


def get_top_repos(repositories):
    top_repos = []
    for repo in repositories:
        top_repo = {'name': repo['name'],
                    'url': repo['html_url'],
                    'issues': get_open_issues_amount(repo),
                    'stars': repo['stargazers_count']}
        top_repos.append(top_repo)
    return top_repos


if __name__ == '__main__':
    repositories_list = get_trending_repositories()
    top_repositories = get_top_repos(repositories_list)
    sorted_repos = sorted(top_repositories, key=lambda rep: rep['issues'])
    print('Популярные репозитории:')
    for repo in sorted_repos:
        print('Название:', repo['name'], ' Ссылка:', repo['url'], ' Проблем:', repo['issues'], ' Звезд:', repo['stars'])


