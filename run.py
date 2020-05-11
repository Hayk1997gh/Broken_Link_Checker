import argparse
import scraper
import reporting
import helper

parser = argparse.ArgumentParser()
parser.add_argument('--url', type=str,
                    help='What is the url to check the broken links?')
args = parser.parse_args()


def main():
    print(args.url)
    scraper.main(args.url, args.url)
    reporting.create_reporting()
    print(helper.broken_links_count())


if __name__ == '__main__':
    main()
