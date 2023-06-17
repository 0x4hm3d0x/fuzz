# Fuzz Tool

The Fuzz Tool is a Python script that performs URL fuzzing by replacing a placeholder (FUZZ) in the URL with words from a wordlist. It sends HTTP requests to the fuzzed URLs and provides information about the responses.

## Features

- Fuzz URLs by replacing a placeholder (FUZZ) with words from a wordlist.
- Send HTTP requests to the fuzzed URLs.
- Filter URLs based on selected or ignored HTTP status codes.
- Filter URLs based on selected or ignored content.
- Filter URLs based on selected or ignored content length.
- Support for POST data in the request.
- Multithreaded execution for faster fuzzing.
- Detailed output with URL, status code, content length, and title.

## Usage

python3 fuzz.py -u <url> -pd "<post_data>" -w <wordlist> [-s <selected_status_code>] [-i <ignored_status_code>] [-sc <selected_content>] [-ic <ignored_content>] [-sl <selected_length>] [-il <ignored_length>]

- `-u <url>`: The target URL with the FUZZ placeholder.
- `-pd "<post_data>"`: POST data for the URL.
- `-w <wordlist>`: Path to the wordlist file.
- `-s <selected_status_code>`: Select a specific HTTP status code (optional).
- `-i <ignored_status_code>`: Ignore a specific HTTP status code (optional).
- `-sc <selected_content>`: Select URLs with matching content (optional).
- `-ic <ignored_content>`: Ignore URLs with matching content (optional).
- `-sl <selected_length>`: Select URLs with a specific content length (optional).
- `-il <ignored_length>`: Ignore URLs with a specific content length (optional).

## Examples

Fuzz the login endpoint with a wordlist and select URLs with a status code of 200:

python3 fuzz.py -u https://example.com/login -w wordlist.txt -s 200

Fuzz the login endpoint with a wordlist and filter URLs that contain the word "error":

python3 fuzz.py -u https://example.com/login -w wordlist.txt -ic error

## Contributing

Contributions are welcome! If you find any issues or have suggestions for improvements, feel free to open an issue or submit a pull request.

## License

This project is licensed under the MIT License.
