#!/usr/bin/env python3
"""
Convert Drift Protocol CSV files to Koinly-compatible universal format CSV.

This script processes:
1. Deposits/withdrawals
2. Funding payments (summarized by day to reduce transaction count)
3. Settled PnL records (realized gains/losses)
"""

import csv
from datetime import datetime
from collections import defaultdict
from decimal import Decimal
import os


def parse_drift_datetime(dt_str):
    """Parse Drift datetime format: 'Tue 14 Oct 2025 05:01:33 GMT'"""
    return datetime.strptime(dt_str, '%a %d %b %Y %H:%M:%S %Z')


def format_koinly_datetime(dt):
    """Format datetime for Koinly: 'YYYY-MM-DD HH:MM:SS UTC'"""
    return dt.strftime('%Y-%m-%d %H:%M:%S UTC')


def extract_currency_from_market(market_str):
    """Extract currency from market identifier (e.g., 'SOL-PERP' -> 'SOL', 'USDC' -> 'USDC')"""
    if '-PERP' in market_str:
        return market_str.replace('-PERP', '')
    return market_str


def process_deposits(input_file, output_rows):
    """Process deposits/withdrawals file."""
    if not os.path.exists(input_file):
        print(f"Warning: {input_file} not found, skipping deposits")
        return
    
    with open(input_file, 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            dt = parse_drift_datetime(row['datetime'])
            amount = Decimal(row['amount'])
            currency = row['symbol']
            direction = row['direction']
            
            # For Koinly universal format:
            # - Deposits: positive amount in 'Received Amount'
            # - Withdrawals: positive amount in 'Sent Amount'
            
            koinly_row = {
                'Date': format_koinly_datetime(dt),
                'Sent Amount': '',
                'Sent Currency': '',
                'Received Amount': '',
                'Received Currency': '',
                'Fee Amount': '',
                'Fee Currency': '',
                'Net Worth Amount': '',
                'Net Worth Currency': '',
                'Label': '',
                'Description': f"Drift {direction}",
                'TxHash': row['txSig']
            }
            
            if direction == 'deposit':
                koinly_row['Received Amount'] = str(amount)
                koinly_row['Received Currency'] = currency
            elif direction == 'withdraw':
                koinly_row['Sent Amount'] = str(amount)
                koinly_row['Sent Currency'] = currency
            
            output_rows.append(koinly_row)


def process_funding_payments(input_file, output_rows):
    """
    Process funding payments, summarizing by currency and day.
    
    Funding payments are periodic payments between long/short positions.
    We'll sum them by day to reduce transaction count while maintaining accuracy.
    """
    if not os.path.exists(input_file):
        print(f"Warning: {input_file} not found, skipping funding payments")
        return
    
    # Group by date and currency
    daily_funding = defaultdict(lambda: defaultdict(Decimal))
    
    with open(input_file, 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            dt = parse_drift_datetime(row['datetime'])
            date_key = dt.strftime('%Y-%m-%d')  # Group by day
            
            currency = extract_currency_from_market(row['market'])
            funding_payment = Decimal(row['fundingPayment'])
            
            daily_funding[date_key][currency] += funding_payment
    
    # Convert to Koinly rows
    for date_str, currencies in sorted(daily_funding.items()):
        for currency, total_funding in currencies.items():
            # Set time to end of day for daily summaries
            dt = datetime.strptime(date_str, '%Y-%m-%d').replace(hour=23, minute=59, second=59)
            
            koinly_row = {
                'Date': format_koinly_datetime(dt),
                'Sent Amount': '',
                'Sent Currency': '',
                'Received Amount': '',
                'Received Currency': '',
                'Fee Amount': '',
                'Fee Currency': '',
                'Net Worth Amount': '',
                'Net Worth Currency': '',
                'Label': '',
                'Description': f"Drift funding payment for {currency} (daily summary)",
                'TxHash': ''
            }
            
            # Funding payments can be positive (received) or negative (paid)
            if total_funding > 0:
                koinly_row['Received Amount'] = str(abs(total_funding))
                koinly_row['Received Currency'] = 'USDC'  # Funding payments are in USDC
                koinly_row['Label'] = 'income'  # Funding received is income
            else:
                koinly_row['Sent Amount'] = str(abs(total_funding))
                koinly_row['Sent Currency'] = 'USDC'
                koinly_row['Label'] = 'cost'  # Funding paid is a cost
            
            output_rows.append(koinly_row)


def process_settle_pnl(input_file, output_rows):
    """
    Process settled PnL records (realized gains/losses from closing positions).
    
    These are realized gains/losses that should be tagged appropriately for tax purposes.
    """
    if not os.path.exists(input_file):
        print(f"Warning: {input_file} not found, skipping settle PnL")
        return
    
    with open(input_file, 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            dt = parse_drift_datetime(row['datetime'])
            pnl = Decimal(row['pnl'])
            currency = extract_currency_from_market(row['market'])
            
            koinly_row = {
                'Date': format_koinly_datetime(dt),
                'Sent Amount': '',
                'Sent Currency': '',
                'Received Amount': '',
                'Received Currency': '',
                'Fee Amount': '',
                'Fee Currency': '',
                'Net Worth Amount': '',
                'Net Worth Currency': '',
                'Label': 'realized gain',  # This is a realized gain/loss
                'Description': f"Drift settled PnL for {currency} position",
                'TxHash': row['txSig']
            }
            
            # PnL is settled in USDC
            if pnl > 0:
                koinly_row['Received Amount'] = str(abs(pnl))
                koinly_row['Received Currency'] = 'USDC'
            else:
                koinly_row['Sent Amount'] = str(abs(pnl))
                koinly_row['Sent Currency'] = 'USDC'
            
            output_rows.append(koinly_row)


def main():
    """Main conversion function."""
    base_dir = 'DriftCSVs'
    wallet_id = '22UGNEfinjGB2qvV9PsRtWDjNgag1beg8drA6fkj7JJi'
    date_range = '20250101-20251231'
    
    # Input files
    deposits_file = f'{base_dir}/deposits-{wallet_id}-{date_range}.csv'
    funding_file = f'{base_dir}/funding-payments-{wallet_id}-{date_range}.csv'
    settle_pnl_file = f'{base_dir}/settle-pnl-records-{wallet_id}-{date_range}.csv'
    
    # Collect all rows
    output_rows = []
    
    print("Processing Drift transactions...")
    print(f"1. Processing deposits/withdrawals from {deposits_file}...")
    process_deposits(deposits_file, output_rows)
    
    print(f"2. Processing funding payments from {funding_file} (summarizing by day)...")
    process_funding_payments(funding_file, output_rows)
    
    print(f"3. Processing settled PnL from {settle_pnl_file}...")
    process_settle_pnl(settle_pnl_file, output_rows)
    
    # Sort by date
    output_rows.sort(key=lambda x: x['Date'])
    
    # Determine actual date range from transactions
    if output_rows:
        first_date = datetime.strptime(output_rows[0]['Date'], '%Y-%m-%d %H:%M:%S UTC')
        last_date = datetime.strptime(output_rows[-1]['Date'], '%Y-%m-%d %H:%M:%S UTC')
        start_date_str = first_date.strftime('%Y-%m-%d')
        end_date_str = last_date.strftime('%Y-%m-%d')
        output_file = f'drift_koinly_{start_date_str}_to_{end_date_str}.csv'
    else:
        output_file = f'drift_koinly_import.csv'
    
    # Write to CSV
    fieldnames = [
        'Date',
        'Sent Amount',
        'Sent Currency',
        'Received Amount',
        'Received Currency',
        'Fee Amount',
        'Fee Currency',
        'Net Worth Amount',
        'Net Worth Currency',
        'Label',
        'Description',
        'TxHash'
    ]
    
    with open(output_file, 'w', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(output_rows)
    
    print(f"\n✓ Conversion complete!")
    print(f"  Total transactions: {len(output_rows)}")
    print(f"  Output file: {output_file}")
    print(f"  Date range: {start_date_str} to {end_date_str}")
    print(f"\nYou can now upload {output_file} to Koinly using the Universal CSV format.")
    
    # Print summary
    deposits = sum(1 for r in output_rows if 'deposit' in r['Description'])
    withdrawals = sum(1 for r in output_rows if 'withdraw' in r['Description'])
    funding = sum(1 for r in output_rows if 'funding payment' in r['Description'])
    pnl = sum(1 for r in output_rows if 'settled PnL' in r['Description'])
    
    print(f"\nBreakdown:")
    print(f"  - Deposits: {deposits}")
    print(f"  - Withdrawals: {withdrawals}")
    print(f"  - Funding payments (daily summaries): {funding}")
    print(f"  - Settled PnL: {pnl}")


if __name__ == '__main__':
    main()
