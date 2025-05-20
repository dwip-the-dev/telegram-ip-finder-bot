# Telegram IP Finder Bot 🌍📡

A powerful Telegram bot for IP, phone, and domain information lookup with multiple investigative tools.

## 🔥 Features

- **IP Lookup** 🌍 - Detailed geolocation, ISP, and network information
- **Phone Number Lookup** 📞 - Carrier detection and location information
- **Country Information** 🌎 - Comprehensive country data
- **WHOIS Lookup** 🔍 - Domain registration details
- **DNS Lookup** 📜 - DNS record inspection
- **Port Scanner** 🚪 - Scan for open ports
- **User/Chat Info** 👤 - Telegram profile information
- **Logging System** 📝 - Tracks all user commands

## ⚙️ Installation

### Prerequisites
- Python 3.8+
- Telegram Bot Token from [@BotFather](https://t.me/BotFather)

### Deployment

#### 1. Clone the repository
```bash
git clone https://github.com/dwip-the-dev/telegram-ip-finder-bot.git
cd telegram-ip-finder-bot
```

#### 2. Configure API keys directly in code
Edit the main bot file and set these variables at the top:

```python
# API KEYS (Set these directly in code)
TOKEN = "YOUR_TELEGRAM_BOT_TOKEN"  # From @BotFather
NUMVERIFY_API_KEY = "YOUR_NUMVERIFY_KEY"  # From numverify.com
OPENCAGE_API_KEY = "YOUR_OPENCAGE_KEY"  # From opencagedata.com
LOG_CHANNEL_ID = "YOUR_LOG_CHANNEL_ID"  # Telegram channel ID for logs
```

#### 3. Install dependencies
```bash
pip install -r requirements.txt
```

#### 4. Run the bot
```bash
python main.py
```

## 🚀 Railway Deployment

This bot includes a `Procfile` ready for Railway deployment:

1. Create a new Railway project
2. Connect your GitHub repository
3. Deploy!

## 🛠️ Commands

| Command | Description | Example |
|---------|-------------|---------|
| `/start` | Start the bot | `/start` |
| `/help` | Show help message | `/help` |
| `/ip <address>` | IP lookup | `/ip 1.1.1.1` |
| `/phone <number>` | Phone lookup | `/phone +14155552671` |
| `/country <code>` | Country info | `/country US` |
| `/whois <domain>` | WHOIS lookup | `/whois google.com` |
| `/dns <domain>` | DNS lookup | `/dns github.com` |
| `/portscan <ip>` | Port scan | `/portscan 1.1.1.1` |
| `/info <username>` | User/chat info | `/info @username(testing)` |

## 📊 API Services Used

- [ip-api.com](https://ip-api.com) - IP geolocation
- [Numverify](https://numverify.com) - Phone number validation
- [REST Countries](https://restcountries.com) - Country information
- [OpenCage](https://opencagedata.com) - Geocoding services

## ⚠️ Security Note

For production use, consider:
1. Using environment variables instead of hardcoded keys
2. Restricting bot access to trusted users
3. Regularly rotating API keys

## 📜 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🤝 Contributing

Contributions are welcome! Please open an issue or submit a pull request.

## 📧 Contact

For questions or support, contact [@dwip-the-dev](https://github.com/dwip-the-dev)
