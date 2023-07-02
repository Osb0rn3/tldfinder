# TLDFinder
TLDFinder is a powerful Python package designed to effortlessly identify the valid top-level domains (TLDs) for a provided list of domains that include a wildcard character in the TLD.

# Usage
The usage of TLDFinder is simple. You can provide the domain using a wildcard character in the TLD scope through standard input (stdin). Here's an example:
```shell
echo "example.*" | tldfinder
cat domains.txt | tldfinder
```
Please note that the first time you run the script, it may take a little more time to fetch the TLDs from the source. Subsequent runs should be faster as the TLDs will be cached.

# Contributing
Contributions to TLDFinder are welcome! If you find any issues or have suggestions for improvements, we appreciate your contribution. Your feedback helps us make TLDFinder better for everyone.