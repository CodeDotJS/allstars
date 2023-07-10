import requests
import json
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from os import system, name

def clear():
    if name == 'nt':
        _ = system('cls')
    else:
        _ = system('clear')

def remove_escaped_sequences(text):
    cleaned_text = text.encode('ascii', 'ignore').decode('ascii')
    cleaned_text = cleaned_text.replace('\n', ' ').strip()
    return cleaned_text

def bookmark(username):
    base_url = f"https://github.com/{username}?tab=stars"
    starred_repos = []

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.82 Safari/537.36",
        "Accept-Language": "en-US,en;q=0.9",
        "Accept-Encoding": "gzip, deflate, br",
        "Referer": "https://github.com/",
        "Connection": "keep-alive",
        "Cache-Control": "no-cache",
    }

    print('----------------------------------------')
    print("| GitHub Starred Repositories Exporter |")
    print('----------------------------------------')

    response = requests.get(base_url, headers=headers)

    if response.status_code == 200:
        page_count = 1
        while True:
            print(f"  Exported details from page : {page_count}", end='\r')

            soup = BeautifulSoup(response.text, 'html.parser')
            repositories = soup.find_all('div', class_='d-inline-block mb-1')

            for repo in repositories:
                repo_name_with_username = repo.find('a').text.strip()
                repo_name = repo_name_with_username.split(' / ')[-1]

                description_elem = repo.find_next_sibling('div', class_='py-1')
                if description_elem:
                    description = description_elem.text.strip()
                else:
                    description_elem = repo.find_next('p', class_='mb-1')
                    description = description_elem.text.strip() if description_elem else ""

                url = repo.find('a')['href']
                full_url = urljoin("https://github.com/", url)

                starred_repo = {
                    'name': repo_name,
                    'description': remove_escaped_sequences(description),
                    'url': full_url
                }

                starred_repos.append(starred_repo)

            next_button = soup.find('a', class_='btn btn-outline BtnGroup-item', text='Next')
            if not next_button:
                break

            next_url = next_button['href']
            response = requests.get(next_url, headers=headers)
            page_count += 1

        json_data = json.dumps(starred_repos, indent=4)

        filename = f"{username}.json"
        with open(filename, 'w') as file:
            file.write(json_data)

        print(f"\n\n  Bookmark saved as : {filename} \n")
    else:
        print("  Username not found!  \n")

username = input("\n Enter your username: ")
clear()

bookmark(username)
