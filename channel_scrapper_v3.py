from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup

# Webdriver-Optionen konfigurieren, um den Browser unsichtbar zu machen
chrome_options = Options()
chrome_options.headless = True

# Pfad zum Chromedriver angeben (stellen Sie sicher, dass Sie den Chromedriver heruntergeladen haben)
chromedriver_path = "C:\Program Files\Google\Chrome\Application\chrome.exe"

# URL der Website
URL_list = ["https://nindo.de/charts/youtube/views", "https://nindo.de/charts/youtube/likes"]
quotes = {} # a list to store quotes
# Selenium-Webdriver initialisieren
for URL in URL_list:
    driver = webdriver.Chrome(options=chrome_options)
    driver.get(URL)
    driver.implicitly_wait(10)
    page_source = driver.page_source
    soup = BeautifulSoup(page_source, 'html.parser')
    driver.quit()
    

    table = soup.find('div', attrs = {'class':'mx-auto max-w-screen-md'})

    for row in table.findAll('a'):
        if "https://nindo.de/charts/youtube/views" ==  URL:
            quotes[row.findAll('span')[2].text] = {
                'url': row['href'],
                'views': row.div.span.text
            }
        elif "https://nindo.de/charts/youtube/likes" == URL:
            if row.findAll('span')[2].text in quotes :
                 quotes[row.findAll('span')[2].text]["likes"] = row.div.span.text
            else:
                quotes[row.findAll('span')[2].text] = {
                'url': row['href'],
                'likes': row.div.span.text
            }
              

# Jetzt enthält das 'quotes'-Dictionary die gewünschten Daten



print(quotes)
exit()
filename = 'inspirational_quotes.csv'
with open(filename, 'w', newline='') as f:
	w = csv.DictWriter(f,['theme','url','img','lines','author'])
	w.writeheader()
	for quote in quotes:
		w.writerow(quote)
