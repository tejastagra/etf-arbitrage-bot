import os
import requests
from bs4 import BeautifulSoup
from datetime import datetime
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from dotenv import load_dotenv
import time

# Load environment variables from .env
load_dotenv()

SENDER_EMAIL = os.getenv("EMAIL_USER")
SENDER_PASSWORD = os.getenv("EMAIL_PASS")
RECIPIENT_EMAIL = os.getenv("RECIPIENT_EMAIL")

if not SENDER_EMAIL or not SENDER_PASSWORD or not RECIPIENT_EMAIL:
    raise EnvironmentError("Missing required environment variables. Check .env file.")

# Scrape MoneyControl for Hang Seng ETF arbitrage opportunities
def get_hang_seng_etf_arbitrage():
    headers = {'User-Agent': 'Mozilla/5.0'}
    url = "https://www.moneycontrol.com/mutual-funds/performance-tracker/etfs/nav-performance.html"

    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        print(f"Failed to fetch data: {e}")
        return []

    soup = BeautifulSoup(response.text, 'html.parser')
    table = soup.find('table', class_=['responsive', 'tblpor'])
    opportunities = []

    if not table:
        print("ETF table not found.")
        return opportunities

    rows = table.find_all('tr')[1:]
    for row in rows:
        cols = row.find_all('td')
        if len(cols) >= 5:
            name = cols[0].text.strip()
            if "hang seng" not in name.lower():
                continue

            nav = cols[2].text.strip().replace(',', '')
            price = cols[3].text.strip().replace(',', '')
            try:
                nav = float(nav)
                price = float(price)
                diff = nav - price
                if diff > 0:
                    spread = (diff / nav) * 100
                    opportunities.append((name, nav, price, round(spread, 2)))
            except ValueError as e:
                print(f"Could not parse NAV/Price for {name}: {e}")
                continue

    opportunities.sort(key=lambda x: x[3], reverse=True)
    return opportunities[:5]

# Build the body of the email
def create_etf_email_body(opportunities):
    today = datetime.now().strftime("%d %B %Y, %I:%M %p")
    lines = [
        f"Tejas Tagra Experiments\nHang Seng ETF Arbitrage Watch – {today}\n",
        "Top Hang Seng ETFs trading below NAV:\n"
    ]

    if not opportunities:
        lines.append("No Hang Seng ETF arbitrage opportunities found right now.")
    else:
        for i, (name, nav, price, spread) in enumerate(opportunities, 1):
            lines.append(f"{i}. {name}\n   NAV: ₹{nav} | Market Price: ₹{price} | Discount: {spread}%\n")

    lines.append("This is an auto-generated message from the arbitrage tracker script.")
    return "\n".join(lines)

# Email sending logic
def send_email(body_text):
    msg = MIMEMultipart()
    msg['From'] = SENDER_EMAIL
    msg['To'] = RECIPIENT_EMAIL
    msg['Subject'] = "Hang Seng ETF Arbitrage Alert – Top Buys Below NAV"
    msg.attach(MIMEText(body_text, 'plain'))

    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(SENDER_EMAIL, SENDER_PASSWORD)
        server.send_message(msg)
        server.quit()
        print("✅ Email sent successfully.")
    except Exception as e:
        print(f"❌ Failed to send email: {e}")

# Main script logic
if __name__ == "__main__":
    try:
        print("📈 Checking for arbitrage opportunities...")
        etf_opps = get_hang_seng_etf_arbitrage()
        time.sleep(2)  # Add delay in case of rapid triggers
        body = create_etf_email_body(etf_opps)
        send_email(body)
    except Exception as e:
        print(f"Unexpected error: {e}")
