# Drift Transaction Exports

Place your exported Drift transaction CSV files in this directory.

## Required Files

Export these 3 files from [https://app.drift.trade/portfolio/history?table=exports](https://app.drift.trade/portfolio/history?table=exports):

1. **Funding Payments** - `funding-payments-*.csv`
2. **Deposits/Withdrawals** - `deposits-*.csv`
3. **Settle PnL Records** - `settle-pnl-records-*.csv`

The converter script will automatically detect and process these files.

## Note

The actual CSV files are ignored by git (see `.gitignore`) to protect your personal transaction data.
