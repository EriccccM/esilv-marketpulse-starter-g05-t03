
from pathlib import Path
import csv
import json


DATA_DIR = Path("data/sample")

# These starter values mirror config/settings.yml.
# settings.yml is a human-readable configuration contract in the CORE.
# Parsing YAML is optional and is not required by the 18-hour lab sequence.
LOOKBACK_LABEL = "1 month"
INTERVAL_LABEL = "Daily"


def load_instruments():
    with open(DATA_DIR / "instruments.json", encoding="utf-8") as file:
        return json.load(file)


def load_prices():
    with open(DATA_DIR / "prices.csv", encoding="utf-8") as file:
        return list(csv.DictReader(file))


def filter_prices(prices, ticker):
    return [row for row in prices if row["ticker"] == ticker]


def summarize_prices(prices):
    """Return the first close, last close and observation count."""
    closes = [float(row["close"]) for row in prices]

    return {
        "first_close": closes[0],
        "last_close": closes[-1],
        "observations": len(closes),
    }


def main():
    instruments = load_instruments()
    prices = load_prices()

    instrument = instruments["instrument"]
    benchmark = instruments["benchmark"]

    instrument_prices = filter_prices(prices, instrument["ticker"])
    benchmark_prices = filter_prices(prices, benchmark["ticker"])

    instrument_summary = summarize_prices(instrument_prices)
    benchmark_summary = summarize_prices(benchmark_prices)

    print("=== MarketPulse ===")
    print()
    print("Instrument")
    print(f"{instrument['ticker']} - {instrument['name']}")
    print(f"First close: {instrument_summary['first_close']:.2f} {instrument['currency']}")
    print(f"Last price: {instrument_summary['last_close']:.2f} {instrument['currency']}")
    print()
    print("Benchmark")
    print(f"{benchmark['ticker']} - {benchmark['name']}")
    print(f"First close: {benchmark_summary['first_close']:.2f}")
    print(f"Last level: {benchmark_summary['last_close']:.2f}")
    print()
    print(f"Period: {LOOKBACK_LABEL}")
    print(f"Interval: {INTERVAL_LABEL}")
    print()
    print("Observations")
    print(f"{instrument['ticker']}: {instrument_summary['observations']}")
    print(f"{benchmark['ticker']}: {benchmark_summary['observations']}")


if __name__ == "__main__":
    main()
