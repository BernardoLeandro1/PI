import datetime

class WeatherProvider:
    def __init__(self):
        self.credential = "ed0608b1055e5035974de17e8422daab"
        self.lang = "pt"
        self.units = "metric"
        self.currentURL = "https://api.openweathermap.org/data/2.5/weather"
        self.forecastURL = "https://api.openweathermap.org/data/2.5/forecast"

    def request(date, local):
        if date is None:
            date = datetime.now()