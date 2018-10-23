# quote_downloader

quote_downloader is a quote scraper. It will download quotes from creativequotations.com

## Usage

To fetch first 50 quotes about `god`:

    god_quotes = fetch_quotes('god')

To fetch all quotes:

    god_quotes = fetch_all_quotes('god')

Save quotes to csv

    write_to_csv(god_quotes, filename="god.csv")

