# ETF Arbitrage Bot

Real-time Hang Seng ETF arbitrage alerts based on NAV-price gaps.

---

## Overview

This Python bot scrapes Moneycontrol to find Hang Seng Index ETFs trading below their NAV (Net Asset Value) and sends an email alert highlighting potential arbitrage opportunities.

---

## Features

- Tracks NAV vs. market price for Hang Seng ETFs
- Flags potential buy-low arbitrage opportunities
- Sends automated email alerts
- Lightweight and easy to configure

---

## Setup

1. Clone the repo

```bash
git clone https://github.com/yourusername/etf-arbitrage-bot.git
cd etf-arbitrage-bot
```

2. Install dependencies

```bash
pip install -r requirements.txt
```

3. Create a `.env` file

```
EMAIL_USER=your_email@gmail.com
EMAIL_PASS=your_app_password
```

Make sure you generate a Gmail App Password if you have 2FA enabled.

4. Run the bot

```bash
python main.py
```

---

## Output Example

```
Tejas Tagra Experiments
Hang Seng ETF Arbitrage Watch – 15 June 2025, 12:00 PM

Top Hang Seng ETFs trading below NAV:

1. XYZ Hang Seng ETF
   NAV: ₹128.23 | Market Price: ₹125.45 | Discount: 2.17%

...
```

---

## License

This project is licensed under the MIT License. You are free to use, modify, and distribute the code as you wish. Please note that the software is provided "as is", without any warranty of any kind. Use at your own risk.

---

## Acknowledgements

- Moneycontrol for ETF data
- Python libraries including requests, BeautifulSoup, and python-dotenv for simplifying development.
