.PHONY: help check test demo

help:
	@echo "make check  - validate market configs"
	@echo "make test   - run 10 regression assertion groups"
	@echo "make demo   - run a small end-to-end slice"

check:
	python3 lib/market_config.py --check

test:
	python3 tests/run_asserts.py

demo:
	python3 modules/01-market-research/scripts/category_parser.py tests/fixtures/parse-fixture.csv --number-locale us -o /tmp/tiktok-agent-data.json
	python3 modules/01-market-research/scripts/market_metrics.py /tmp/tiktok-agent-data.json --top 5 --currency USD --format md
	python3 modules/02-product-strategy/scripts/sku_pricing.py calc --market us --cost 12 --price 39.99 --referral-pct 6 --payment-pct 2 --affiliate-pct 15 --return-pct 2
