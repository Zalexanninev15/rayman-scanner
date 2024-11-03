# Script for scanning the site and extracting links leading to the site pages
# Has extended support for sites created in the Jimdo website builder
# Copyright (C) 2023-2025 Zalexanninev15

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

import requests
from bs4 import BeautifulSoup

print('''rayman-scanner  Copyright (C) 2023  Zalexanninev15
This program comes with ABSOLUTELY NO WARRANTY.
This is free software, and you are welcome to redistribute it
under certain conditions.''')
print("\nrayman-scanner v1.1-1 by Zalexanninev15\nGitHub: https://github.com/Zalexanninev15/rayman-scanner\n")

base_url = input("Write site link (home page): ")
write_to_file = input("Write links to file \"links.txt\"? (Y/n), default - n: ")

base_url = base_url.replace(" ", "")
if base_url.endswith('/'):
    base_url = base_url[:-1]
if not base_url.startswith("http"):
    base_url = f"https://{base_url}"

scanned = []

def clean(a_eles):
    links = []
    skip_links = []
    for a in a_eles:
        link = a['href']
        # What should not be included in the list of links (filters)
        if link.startswith('#') or link.startswith('mailto:') or link == '/' or link == f"{base_url}/" or 'www.jimdo.com' in link or "login" in link or "signup" in link or "javascript" in link or "privacy" in link:
            skip_links.append(link)
            continue

        if link.startswith('/'):
            link = '{}{}'.format(base_url, link)

        if not link.startswith('http://') and not link.startswith('https://'):
            link = '{}/{}'.format(base_url, link)

        if not link.startswith(base_url):
            continue

        if link not in links:
            links.append(link)

    return links

def get_next_scan_urls(urls):
    links = []
    for u in urls:
        if not u in scanned:
            links.append(u)
    return links

def scan(url):
    if url not in scanned:
        if not 'y' in write_to_file.lower():
            print('{}'.format(url))
        scanned.append(url)
        data = requests.get(url)
        soup = BeautifulSoup(data.text, 'html5lib')
        a_eles = soup.find_all('a', href=True)
        links = clean(a_eles)
        next_scan_urls = get_next_scan_urls(links)
        if len(next_scan_urls) != 0:
            for l in next_scan_urls:
                scan(l)
    return scanned

def site_checker():
    try:
        response = requests.get(base_url)
        if response.ok:
            return True
        else:
            return False
    except:
        return False

def main():
    if site_checker() and "http" in base_url:
        print("\nFound pages:")
        if 'y' in write_to_file.lower():
            print("Already looking, you can see the result in the \"list.txt\" file when I do work.")
        links = scan(base_url)
        if 'y' in write_to_file.lower():
            with open("pages.txt", 'w') as file:
                file.writelines(f"{line}\n" for line in links)
        print("Done!")
    else:
        print("\nThis page either does not exist or is out!\nRun the script again and enter/paste the link")

if __name__ == '__main__':
    main()
