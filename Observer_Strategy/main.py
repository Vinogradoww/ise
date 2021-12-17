from typing import List
import requests
import smtplib
import time
import os


class WeatherNotification:
    _strategy = None
    recipients = []
    temp = -100
    wind = -100

    def update(self, temp, wind):
        self.temp = temp
        self.wind = wind

    def action(self):
        pass


class StrategyEmailNotification(WeatherNotification):
    def action(self):
        server = smtplib.SMTP("smtp.yandex.ru", 587)
        server.ehlo()
        server.starttls()
        server.login(os.environ["mail_login"], os.environ["mail_pass"])
        msg = f"Attention! The wind speed is {self.wind}, temperature is {self.temp}."
        for recipient in self.recipients:
            server.sendmail(os.environ["mail_login"], recipient, msg)
        server.quit()
        print("Email sent")


class StrategyPrintToConsole(WeatherNotification):
    def action(self):
        print(f"StrategyPrintToConsole: Attention! The wind speed is {self.wind}, temperature is {self.temp}.")


#################################################
#################################################
#################################################


class Weather:
    api_key = "503caaddf4ec81af0e40a148bcaf27d4"
    city = ''
    weather = {}
    temp = -100
    wind = -100
    _observers: List[WeatherNotification] = []

    def __init__(self, city):
        self.city = city

    def get_weather(self):
        req = requests.get("http://api.openweathermap.org/data/2.5/weather",
                           params={'q': self.city, 'units': 'metric', 'APPID': self.api_key})
        data = req.json()
        self.weather = data
        self.temp = data["main"]['temp']
        self.wind = data["wind"]['speed']
        self.notify()

    def attach(self, observer: WeatherNotification) -> None:
        print("Subject: Attached an observer.")
        self._observers.append(observer)

    def detach(self, observer: WeatherNotification) -> None:
        self._observers.remove(observer)

    def notify(self):
        for _observer in self._observers:
            _observer.update(self.temp, self.wind)

    # def get_weather_periodically(self, step):
    #     while True:
    #         self.get_weather()
    #         time.sleep(step)


#################################################
#################################################
#################################################


class Context:
    _strategy = None
    subject = None

    def __init__(self, strategy: WeatherNotification, city: str = '') -> None:
        self._strategy = strategy
        if not city:
            city = "Moscow,RU"
        self.subject = Weather(city)
        self.subject.attach(strategy)
        self.subject.get_weather()

    @property
    def strategy(self) -> WeatherNotification:
        return self._strategy

    @strategy.setter
    def strategy(self, strategy: WeatherNotification) -> None:
        """
        Заменить объект Стратегии во время выполнения.
        """
        self._strategy = strategy

    def action(self) -> None:
        self._strategy.action()


if __name__ == "__main__":
    # context = Context(StrategyPrintToConsole())
    # context.action()

    strategy = StrategyEmailNotification()
    strategy.recipients = ["nik-rostov@mail.ru"]
    context = Context(strategy)
    context.action()

