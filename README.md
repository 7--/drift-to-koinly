# Drift to Koinly Converter

Convert your Drift Protocol transactions to Koinly-compatible CSV format for tax reporting.

## Quick Start

### 1. Export your Drift transaction history

Go to [https://app.drift.trade/portfolio/history?table=exports](https://app.drift.trade/portfolio/history?table=exports) and export these 3 files:

1. **Funding Payments**
2. **Deposits/Withdrawals**  
3. **Settle PnL Records**

Place all three CSV files in the `DriftCSVs/` directory.

### 2. Run the converter

```bash
python3 convert_drift_to_koinly.py
```

### 3. Import to Koinly

Upload the generated `drift_koinly_YYYY-MM-DD_to_YYYY-MM-DD.csv` file to Koinly using the **Universal** format.

---

## What it does

The script processes three types of Drift transactions:

1. **Deposits/Withdrawals** - Direct transfers in/out of your Drift account
2. **Funding Payments** - Periodic payments between long/short positions (summarized by day)
3. **Settled PnL** - Realized gains/losses from closing positions

## Key Features

### Funding Payment Summarization
To keep your Koinly import manageable, the script summarizes funding payments by:
- **Grouping by day and currency** - All funding payments for the same currency on the same day are summed
- **Proper labeling** - Positive payments are labeled as "income", negative as "cost"
- This significantly reduces the number of transactions (e.g., thousands of hourly payments become daily summaries)

This approach is acceptable in accounting because:
- The total amount remains accurate
- Daily granularity is sufficient for tax purposes
- It maintains the distinction between income and expenses
- Each currency is tracked separately

### Transaction Mapping

| Drift Transaction | Koinly Format | Label |
|-------------------|---------------|-------|
| Deposit | Received Amount | (none) |
| Withdrawal | Sent Amount | (none) |
| Funding Payment (positive) | Received Amount | income |
| Funding Payment (negative) | Sent Amount | cost |
| Settled PnL (gain) | Received Amount | realized gain |
| Settled PnL (loss) | Sent Amount | realized gain |

## Usage

```bash
python3 convert_drift_to_koinly.py
```

This will generate a file with the actual transaction date range:
```
drift_koinly_2025-10-11_to_2025-12-31.csv
```

## Importing to Koinly

1. Log into your Koinly account
2. Go to your wallet and click "Add transactions"
3. Select "Upload file"
4. Choose the generated CSV file
5. Select **"Universal"** as the file format
6. Click "Import"

Koinly will automatically:
- Recognize the Universal format columns
- Apply the appropriate labels (income, cost, realized gain)
- Calculate your tax liability based on the transactions

## File Structure

- `convert_drift_to_koinly.py` - Main conversion script
- `DriftCSVs/` - Directory containing your Drift export files
  - `deposits-*.csv` - Deposit/withdrawal transactions
  - `funding-payments-*.csv` - Funding payment transactions
  - `settle-pnl-records-*.csv` - Settled PnL transactions
- `drift_koinly_YYYY-MM-DD_to_YYYY-MM-DD.csv` - Generated Koinly import file

## Notes

- All dates are in UTC timezone as required by Koinly
- Funding payments and settled PnL are recorded in USDC
- Transaction hashes are included where available for audit trail
- The script uses Python's Decimal type for accurate financial calculations
