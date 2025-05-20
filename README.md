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
- Numverify API Key (for phone lookup)
- OpenCage API Key (for geocoding)

### Deployment

#### 1. Clone the repository
```bash
git clone https://github.com/dwip-the-dev/telegram-ip-finder-bot.git
cd telegram-ip-finder-bot
```

#### 2. Set up environment variables
Create a `.env` file with:
```env
TOKEN=your_telegram_bot_token
NUMVERIFY_API_KEY=your_numverify_key
OPENCAGE_API_KEY=your_opencage_key
LOG_CHANNEL_ID=your_log_channel_id
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
3. Add the required environment variables
4. Deploy!


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

## 📊 API Services Used

- [ip-api.com](https://ip-api.com) - IP geolocation
- [Numverify](https://numverify.com) - Phone number validation
- [REST Countries](https://restcountries.com) - Country information
- [OpenCage](https://opencagedata.com) - Geocoding services

## 📜 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🤝 Contributing

Contributions are welcome! Please open an issue or submit a pull request.

## 📧 Contact

For questions or support, contact [@dwip-the-dev](https://github.com/dwip-the-dev)
