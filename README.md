## Site Performance

Loads a list of sites from a text file and prints the 5 fastest and slowest sites.

Requires requests package.

Should work with both python 2 and 3.

Input file should contain sites to visit separated by newlines.

Quantcast top site formatted with the following:
  head -n 56 Quantcast-Top-Million.txt | tail -n 50 | cut -d$'\t' -f 2 > sitelist.txt


```
usage: top_site_perf.py [-h] [-v] path

positional arguments:
  path        path to file that contains a list of sites

optional arguments:
  -h, --help  show this help message and exit
  -v          show more verbose output
```