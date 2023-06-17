import argparse
import requests
from concurrent.futures import ThreadPoolExecutor, as_completed
from colorama import Fore, Style

developer_name = "0x4hm3d0x"

def fuzz_url(url, wordlist, selected_status_code, ignored_status_code, timeout, selected_content, ignored_content, selected_length, ignored_length, post_data, selected_title, ignored_title):
    with open(wordlist, 'r') as f:
        words = f.read().splitlines()

    wordlist_size = len(words)
    tries = 0

    with ThreadPoolExecutor(max_workers=10) as executor:
        futures = []
        for word in words:
            tries += 1
            fuzzed_url = url.replace("FUZZ", word)
            future = executor.submit(send_request, fuzzed_url, timeout, post_data)
            futures.append((fuzzed_url, future))

        print(f"\n{Fore.CYAN}Fuzzing started!")
        print(f"Developer: {developer_name}")
        print(f"URL: {url}")
        print(f"Wordlist: {wordlist}{Style.RESET_ALL}\n")

        for i, (fuzzed_url, future) in enumerate(futures, 1):
            response = future.result()
            if response is None:
                continue

            status_code = response.status_code
            content_length = len(response.content)
            content = response.text
            title = get_title(fuzzed_url)

            if selected_status_code and status_code != selected_status_code:
                continue

            if ignored_status_code and status_code == ignored_status_code:
                continue

            if selected_content and selected_content not in content:
                continue

            if ignored_content and ignored_content in content:
                continue

            if selected_length and content_length != selected_length:
                continue

            if ignored_length and content_length == ignored_length:
                continue

            if selected_title and not title_match(title, selected_title):
                continue

            if ignored_title and title_match(title, ignored_title):
                continue

            result = f"[{Fore.GREEN}{i}{Style.RESET_ALL}] URL: {fuzzed_url} | Status Code: {status_code} | Content Length: {content_length} bytes | Title: {title}"
            print(f"{result}")

    print(f"\n{Fore.CYAN}Fuzzing completed!")
    print(f"Developer: {developer_name}")
    print(f"URL: {url}")
    print(f"Wordlist: {wordlist}")
    print(f"Wordlist Size: {wordlist_size}")
    print(f"Tries: {tries}{Style.RESET_ALL}")

def send_request(url, timeout, post_data):
    try:
        response = requests.post(url, timeout=timeout, data=post_data)
        return response
    except requests.exceptions.RequestException:
        return None

def get_title(url):
    try:
        response = requests.get(url)
        if response.ok:
            title_start = response.text.find("<title>")
            title_end = response.text.find("</title>")
            if title_start != -1 and title_end != -1:
                title = response.text[title_start + 7: title_end]
                return title.strip()
    except requests.exceptions.RequestException:
        pass
    return ""

def title_match(title, keyword):
    return keyword.lower() in title.lower()

def main():
    parser = argparse.ArgumentParser(description='Python3 Fuzz Tool')
    parser.add_argument('-u', '--url', type=str, help='Target URL with FUZZ placeholder')
    parser.add_argument('-w', '--wordlist', type=str, help='Path to the wordlist file')
    parser.add_argument('-s', '--selected', type=int, help='Select a specific HTTP status code')
    parser.add_argument('-i', '--ignored', type=int, help='Ignore a specific HTTP status code')
    parser.add_argument('-t', '--timeout', type=int, default=5, help='Request timeout in seconds (default: 5)')
    parser.add_argument('-sc', '--selected_content', type=str, help='Select URLs with matching content')
    parser.add_argument('-ic', '--ignored_content', type=str, help='Ignore URLs with matching content')
    parser.add_argument('-sl', '--selected_length', type=int, help='Select URLs with a specific content length')
    parser.add_argument('-il', '--ignored_length', type=int, help='Ignore URLs with a specific content length')
    parser.add_argument('-pd', '--post_data', type=str, help='POST data for URL')
    parser.add_argument('-st', '--selected_title', type=str, help='Select URLs with matching title')
    parser.add_argument('-it', '--ignored_title', type=str, help='Ignore URLs with matching title')

    args = parser.parse_args()
    url = args.url
    wordlist = args.wordlist
    selected_status_code = args.selected
    ignored_status_code = args.ignored
    timeout = args.timeout
    selected_content = args.selected_content
    ignored_content = args.ignored_content
    selected_length = args.selected_length
    ignored_length = args.ignored_length
    post_data = args.post_data
    selected_title = args.selected_title
    ignored_title = args.ignored_title

    if url and wordlist:
        fuzz_url(url, wordlist, selected_status_code, ignored_status_code, timeout, selected_content, ignored_content, selected_length, ignored_length, post_data, selected_title, ignored_title)
    else:
        parser.print_help()

if __name__ == '__main__':
    main()
