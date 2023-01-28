# Script for scanning the site and extracting links leading to the site pages
# Has extended support for sites created in the Jimdo website builder
# Copyright (C) 2023 Zalexanninev15

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

print('''rayman-scanner v1.0 Copyright (C) 2023  Zalexanninev15
This program comes with ABSOLUTELY NO WARRANTY.
This is free software, and you are welcome to redistribute it
under certain conditions.''')

website = input("\nWrite site link (home page): ")
write_to_file = input("Write links to file? (Y/n), default - n: ")
next = input("Print the number of next scans? (Y/n), default - n: ")

base_url = website
if website.endswith('/'):
    base_url = website[:-1]

scanned = []

def clean(a_eles):
    links = []
    skip_links = []
    for a in a_eles:
        link = a['href']
        # What should not be included in the list of links
        if link.startswith('#') or link.startswith('mailto:') or link == '/' or 'www.jimdo.com' in link or "/" * 2 in link or "login" in link or "javascript" in link or "privacy" in link:
            skip_links.append(link)
            continue

        if link.startswith('/'):
            link = '{}{}'.format(base_url, link)

        if link.startswith('http://') != True and link.startswith('https://') != True:
            link = '{}/{}'.format(base_url, link)

        if link.startswith(base_url) is False:
            continue

        if link not in links:
            links.append(link)

    return [links, skip_links]


def get_next_scan_urls(urls):
    links = []
    for u in urls:
        if u not in scanned:
            links.append(u)
    return links


def scan(url):
    if url not in scanned:
        print('{}'.format(url))
        scanned.append(url)
        data = requests.get(url)
        soup = BeautifulSoup(data.text, 'html5lib')
        a_eles = soup.find_all('a', href=True)
        links, skip_links = clean(a_eles)
        next_scan_urls = get_next_scan_urls(links)
        if 'y' in next.lower():
            print('Number of next scans: {}'.format(len(next_scan_urls)))
        if len(next_scan_urls) != 0:
            for l in next_scan_urls:
                scan(l)
    return scanned


def main():
    print("\nFound pages::")
    links = scan(website)
    if 'y' in write_to_file.lower():
        with open("site.txt", 'w') as file:
            file.writelines(line + '\n' for line in links)

if __name__ == '__main__':
    main()
