import sys
import requests
import concurrent.futures
import os
import argparse
import re
import subprocess

class TLDReplacer:
    def __init__(self, domain, tlds_file):
        self.domain = domain
        self.available_tlds = self._get_available_tlds(tlds_file)

    def _get_available_tlds(self, tlds_file):
        if tlds_file and os.path.exists(tlds_file):
            with open(tlds_file, 'r') as file:
                return file.read().splitlines()

        url = 'https://data.iana.org/TLD/tlds-alpha-by-domain.txt'
        response = requests.get(url)
        tlds = response.text.splitlines()
        tlds = [tld.lower() for tld in tlds]
        tlds = tlds[1:]

        if tlds_file:
            with open(tlds_file, 'w') as file:
                file.write('\n'.join(tlds))

        return tlds  # Skip the first line

    def replace_tld_with_wildcard(self):
        wildcard_domains = []

        if not re.search(r'\.\*$', self.domain):
            return [self.domain]

        domain_without_tld = self.domain.replace(".*", "")

        for tld in self.available_tlds:
            wildcard_domain = f"{domain_without_tld}.{tld}"
            wildcard_domains.append(wildcard_domain)

        return wildcard_domains

class ShellCommandRunner:
    def run_command(self, command, input_list=None):
        if input_list:
            input_text = '\n'.join(input_list)
            result = subprocess.run(
                command, input=input_text, shell=True, capture_output=True, text=True)
        else:
            result = subprocess.run(
                command, shell=True, capture_output=True, text=True)

        if result.returncode == 0:
            output_lines = result.stdout.strip().split('\n')
            return output_lines
        else:
            error_message = result.stderr.strip()
            raise Exception(f"Command failed with error: {error_message}")

def main():
    # Parse command-line arguments
    parser = argparse.ArgumentParser(
        prog='TLDFinder', description='Discover bug bounty scopes associated with star top-level domains (TLDs).')
    parser.add_argument('-f', '--tlds-file', metavar='TLDs_file', type=str,
                        help='Path to the file containing top-level domains (TLDs)')
    parser.add_argument('-d', '--dnsx-path', metavar='DNSX_path', type=str,
                        help='Path to the dnsx binary file',
                        default='dnsx')
    parser.add_argument('-r', '--resolvers', metavar='Resolvers', type=str,
                        help='Enable DNS resolution using the provided resolvers')

    args = parser.parse_args()

    # Set default TLDs file path
    default_tlds_file = os.path.expanduser('~/.tldfinder/tlds.txt')

    # Create ~/.tldfinder directory if it doesn't exist
    os.makedirs(os.path.dirname(default_tlds_file), exist_ok=True)

    # Use default TLDs file if not provided
    tlds_file = args.tlds_file if args.tlds_file else default_tlds_file

    # Read domains from stdin
    domains = sys.stdin.read().splitlines()

    # Process each domain in parallel using multithreading
    with concurrent.futures.ThreadPoolExecutor() as executor:
        results = [executor.submit(TLDReplacer(
            domain, tlds_file).replace_tld_with_wildcard) for domain in domains]

        # Get the wildcard domains from completed tasks
        wildcard_domains = [result.result()
                            for result in concurrent.futures.as_completed(results)]

    domains = sum(wildcard_domains, [])

    if args.resolvers:
        runner = ShellCommandRunner()
        domains = runner.run_command(
            f'{args.dnsx_path} -r {args.resolvers} -a -silent', domains)

    print("\n".join(domains))

if __name__ == '__main__':
    main()