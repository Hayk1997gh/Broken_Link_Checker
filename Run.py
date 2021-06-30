import argparse
import Scraper
import Reporting
import Helper

parser = argparse.ArgumentParser()
parser.add_argument('--url', type=str,
                    help='What is the url to check the broken links?')
args = parser.parse_args()


def main():
    print(args.url)
    Scraper.main(args.url, args.url)
    Reporting.create_reporting()
    print(Helper.broken_links_count())


if __name__ == '__main__':
    main()
