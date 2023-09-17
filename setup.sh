curl -L https://github.com/mozilla/geckodriver/releases/download/v0.30.0/geckodriver-v0.30.0-linux64.tar.gz > geckodriver.tar.gz
tar -xf geckodriver.tar.gz
rm geckodriver.tar.gz
python3 -m pip install selenium
