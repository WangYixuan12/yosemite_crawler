# Installation
`pip install selenium==3.14.0 google-api-python-client google-auth google-auth-oauthlib`

# Run
1. Create your own `credentials.json` on `http://console.cloud.google.com/` (APIs & Services --> Credentials --> Create credentials --> OAuth client ID)
2. Download chromedriver that matches your system
3. Change email address and searching date in `crawl.py`
4. `python crawl.py`

# What will happen
It will keep searching every 5 minutes and notify you if there is one.