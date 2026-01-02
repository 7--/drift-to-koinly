# How to create a custom CSV file with your data

Written by Robin Singh
Updated over 11 months ago

In most cases, you should not need to create a custom file as Koinly can handle almost every csv and excel file out there. However, if your exchange or wallet does not have export functionality then you can follow these instructions to create your own.

---

## Instructions

1. Select one of the templates below and click on the link to go to the Google Sheets page for it.
2. Click on File > Make a Copy in the top right corner (you will need a Google account for this - if you don't have one then click on File > Download > CSV to download the file and edit it using Excel or another tool)
3. Remove the sample data rows once you understand how to enter your own data.
4. When you have finished entering the data click on File > Download > Comma-separated values (CSV) to download the file and import it into Koinly.

### Update January 2025 ℹ️

The custom Koinly formats now supports currency addresses in the format `SYMBOL:ADDRESS:BLOCKCHAIN` (the blockchain is optional)

For example, you can set the currency to:
- `WIF:EKpQGSJtjMFqKZ9KQanSqYXRcF8fBopzLHYxdM65zcjm`
- `WIF:EKpQGSJtjMFqKZ9KQanSqYXRcF8fBopzLHYxdM65zcjm:SOL`

This will ensure that the correct WIF is synced, since our system will match the specific address.

---

## 1. For importing deposits/withdrawals/mining

📥 [Download our simple template](https://docs.google.com/spreadsheets/d/13H9kREcrNJmCNxkpYK-AaRlkWh8PSshbpPBmewmDX4o/edit?usp=sharing)

This format is ideal for importing deposits and withdrawals from wallets/blockchains/mining pools etc. Basically, anywhere you have incoming and outgoing transactions.

If you also need to import trades then you can use the second file format that we have created specifically for trades. You can also look at the Universal file format which will allow you to import all deposits/withdrawals/trades using a single file.

### Simple template explained

The simple template will allow you to import deposits and withdrawals/send transactions where there is only one asset.

Here you would need to enter:

- **Koinly Date** - the date in Koinly format (YYYY-MM-DD 00:00 UTC)
  - Note - these must be in UTC even if you live in another timezone
- **Amount** - the number of tokens sent or received
  - Note - if you are sending/withdrawing the tokens, it must be a negative number
- **Currency** - the token symbol, e.g. BTC, ETH, USDT
- **Label** - an optional label (tag) if the transaction is something other than a normal deposit/withdrawal
  - Note - you can find the [list of available tags here](https://support.koinly.io/en/articles/9490023-what-are-tags-labels)
- **TxHash** - the transaction hash from the blockchain. This is optional.

---

## 2. For importing Trades

📥 [Download a sample of our trade template](https://docs.google.com/spreadsheets/d/1MEVrdiS941S-s0igBZKh-pbW5TqJb4mpfkmnDzDkCcg/edit?usp=sharing)

This file is ideal for importing trades that are displayed using their market pair/side, instead of the amount you sent/received.

If your exchange shows you the amount you have sent and the amount you have received separately then you should look at the universal import format instead.

### Trade template explained

The trade template is for importing trades where one token is being exchanged for another.

Here you would need to enter:

- **Koinly Date** - the date in Koinly format (YYYY-MM-DD 00:00 UTC)
  - Note - these must be in UTC even if you live in another timezone
- **Pair** - the token pair that is being traded
  - Note - keep this consistent, don't have BTC-USD in one row and USD-BTC in another
- **Side** - Is this a buy or sell of the first asset in the pair
  - In the example, you can see the trade in row 2 is a buy of BTC and row 3 is a sell of BTC
- **Amount** - the amount of the first asset in the pair
  - In the example, row 2 shows a buy of 1 BTC and row 3 shows a sell of 1 BTC
- **Total** - the amount of the second asset in the pair
  - In this example, row 2 shows 1,000 USD and row 3 shows 900 USD
- **Fee Amount** - The fee amount, if any.
- **Fee Currency** - The currency that the fee was paid in
- **Order ID and Trade ID**
  - Note - this is optional but adding both an order ID and a Trade ID will allow Koinly to group trades for the same Order (e.g. Avalanche Trades)

---

## 3. Universal format

📥 [Download a sample universal template](https://docs.google.com/spreadsheets/d/1dESkilY70aLlo18P3wqXR_PX1svNyAbkYiAk2tBPJng/edit?usp=sharing)

This format can be used for importing any kind of data. You have to specify the amount you are sending and the amount you are receiving in separate fields. This means you can use the file for deposits/withdrawals and even trades.

### Universal template explained

The universal template (also known as the advanced template) can be used to import a mixture of deposits, withdrawals and trades.

Using this template, not all of the boxes in each column/row need to be completed. This will depend on the type of transaction you are entering.

For example, if you are entering a deposit into row 2, you would only fill in columns D & E, columns B & C would not be needed.

Here you would enter:

- **Date** - the date in Koinly format (YYYY-MM-DD 00:00 UTC)
  - Note - these must be in UTC even if you live in another timezone
- **Sent Amount** - the number of tokens sent/withdrawn
- **Sent Currency** - the token being sent/withdrawn
- **Received Amount** - the number of tokens received/bought
- **Received Currency** - the token being received/bought
- **Fee Amount** - The fee amount
- **Fee Currency** - the currency the fee was paid in
- **Net Worth Amount and Net Worth Currency** - You can set these if you know what the market rate of the transaction was at the time of the transaction.
  - Note - See the full description here
- **Label** - the tag, e.g. Cost, Lost, Gift
  - Note - you can find the [list of available tags here](https://support.koinly.io/en/articles/9490023-what-are-tags-labels)
- **Description** - a description of the transaction. This is optional and has no effect on the import/calculations, but can be useful for record-keeping purposes
- **TxHash** - the transaction hash from the blockchain. This is optional.

---

## Fields explained

### Decimal separators

Always use the dot as a decimals separator in your files. We do not support comma separators. Ex: 0.55 BTC is good and 0,55 BTC is bad. A decimal separator (Ex: #.00) is required for all amounts.

### Dates (timestamps)

All date fields must be formatted like this: **YYYY-MM-DD HH:mm:ss**. For example, if you want to enter 5th Jan 2019 the date will be 2019-01-05. It's best for timestamps to be in UTC but if they aren't, you don't have to edit them in the file - see [How to import a CSV file using a different timezone](https://support.koinly.io/en/articles/9489985-how-to-import-a-csv-file-using-a-different-timezone)

### Order ID / Trade ID

Entering both an order ID and a Trade ID will allow Koinly to group trades for the same Order (Avalanche Trades).

### Net worth amount & currency

You can set these if you know what the market rate of the transaction was at the time of the transaction. If it is empty Koinly will determine the market rate automatically. Read more about [market prices on Koinly here](https://support.koinly.io/en/articles/9489964-how-koinly-sets-the-market-price-for-your-transactions).

The Net worth amount/currency is ignored if you bought or sold some coins using a fiat currency, in such cases Koinly will use the fiat as the market value instead.

The Net worth currency must be a fiat currency like USD, EUR, GBP, etc. The net worth amount should NOT include the value of the fee. If you have paid fees in a different cryptocurrency and want to specify the exact worth of the fee as well, you can use the Fee Worth and Fee Worth Currency columns instead.

### Fee amount & currency

These are the fees you paid when trading and can be in any fiat or cryptocurrency. Fees can not be added to incoming or outgoing transactions. If you paid a transfer fee, Koinly will calculate it automatically when it matches an outgoing txn to an incoming txn on another wallet. Only use this field for entering trading fees.

Ex. if you bought 1 BTC for 100 USD and paid a 10 USD fee enter this as:
- 100 USD Sent
- 10 USD Fee
- 1 BTC Received

or as:
- 110 USD Sent
- 1 BTC Received
- (no fee)

Both are the same. Just don't enter the fee if it's already included.

### Tags

Tags can be added as appropriate. For regular deposits/withdrawals/trades, no tag is required.

**Koinly allows the following tags for outgoing transactions:**
- gift
- lost
- donation
- cost
- loan fee
- margin fee
- loan repayment
- margin repayment
- stake
- realized gain

**The following tags are allowed for incoming transactions:**
- airdrop
- fork
- mining
- reward
- income
- lending interest
- cashback
- salary
- fee refund
- loan
- margin loan
- stake
- realized gain

If you are unsure about what a tag does then you should refer to the below guide:
[Learn more about tags](https://support.koinly.io/en/articles/9490023-what-are-tags-labels)

---

## FAQ

### How can I import a Transfer?

Since Koinly follows a double-ledger model, you can't import a "transfer" between wallets.

Instead, you need to:
- Add an incoming transaction into the "receiving" wallet (deposit)
- Add an outgoing transaction into the "sending" wallet (withdrawal)

Koinly will then match these two transactions and turn them into a single Transfer transaction automatically. See [How Koinly handles transfers between your own wallets](https://support.koinly.io/en/articles/9490024-how-koinly-handles-transfers-between-your-own-wallets)

### Can I import the same file again without duplicates?

If you need to import the same file again, this can be done without worrying about duplicates.

### Can I import Excel (XLS, XLSX) files or does it have to be CSV?

Koinly can handle these files too but if you encounter some errors (due to encoding etc) just export the file to csv (make sure it is comma delimited!).

### Error: "Zip end of central directory signature not found"

If you are getting this error when trying to import a file to Koinly, follow these steps:

1. Open the file in a text editor (not excel!) and remove any invalid lines or quotes.
2. Then go to [Google Sheets](https://docs.google.com/spreadsheets/u/0/) > create a Blank document > paste the csv data into the first column "A".
3. Then click on the "A" column to select all rows. Next click on Data > Split text to columns in the menu.
4. Your data should now be displayed in separate columns unless the file still contains bad data/quotes.
5. Now click on File > Download > Comma separated values (csv) and upload the downloaded file to Koinly.

### How to fix a token that is imported as the wrong token?

If you try to import a token that shares its symbol with another token then Koinly will import the token that is more common. If this is not the token that you were intending to import then you can fix this in your file. The way to do this is to replace the token symbol with the Koinly ID, or using the token address.

#### Option 1: using the Koinly ID

1. Go to the Markets tab on Koinly and search for the token you want to import. Let's say that I wanted to import the BitTorrent (old) token but Koinly is only importing the Bittorrent (new) token when I import BTT.

2. After clicking on the token you want, you will see the Koinly ID in the URL:
   `https://app.koinly.io/p/markets/3361`
   In this URL, we can see that the ID is 3361

3. You can now replace the symbols in your file. The easiest way to do this would be to use the Find & Replace feature that most editors have. In this example, I would replace all instances of BTT with the text ID:3361.
   
   Note that it's important to include the "ID:" in front of the number and there should be no space in between.
   
   After all instances of BTT have been replaced with the ID, the file will import the correct token!

#### Option 2: using the token address

If you are using the universal format, then you can populate any currency field like this:
`<symbol>:<address>:<blockchain>`

Example for the WIF token on Solana:
`WIF:EKpQGSJtjMFqKZ9KQanSqYXRcF8fBopzLHYxdM65zcjm:SOL`

Importing currencies like this will allow you to specify the token that you want, so that Koinly will not select another token that shares the same symbol.

---

**Source:** https://support.koinly.io/en/articles/9489976-how-to-create-a-custom-csv-file-with-your-data
