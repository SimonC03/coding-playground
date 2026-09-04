import os
import sys

import requests
from dotenv import load_dotenv
from PyQt5.QtCore import Qt, QThread, pyqtSignal
from PyQt5.QtWidgets import (
    QApplication,
    QFrame,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QPushButton,
    QVBoxLayout,
    QWidget,
)

load_dotenv()

API_KEY = os.getenv("open-weather-cred")
API_URL = "https://api.openweathermap.org/data/2.5/weather"

HTTP_ERRORS = {
    400: "Bad request\nPlease check your input",
    401: "Unauthorized\nYour API key is invalid",
    403: "Forbidden\nAccess to this resource is denied",
    404: "City not found\nCheck the spelling and try again",
    429: "Too many requests\nSlow down and try again later",
    500: "Internal server error\nPlease try again later",
    502: "Bad gateway\nInvalid response from the server",
    503: "Service unavailable\nThe server is down right now",
    504: "Gateway timeout\nNo response from the server",
}


def weather_emoji(weather_id):
    """Översätt OpenWeather:s condition-id till en emoji."""
    if 200 <= weather_id <= 232:
        return "⛈"
    if 300 <= weather_id <= 321:
        return "🌦"
    if 500 <= weather_id <= 531:
        return "🌧"
    if 600 <= weather_id <= 622:
        return "❄"
    if 701 <= weather_id <= 741:
        return "🌫"
    if weather_id == 762:
        return "🌋"
    if weather_id == 771:
        return "💨"
    if weather_id == 781:
        return "🌪"
    if weather_id == 800:
        return "☀"
    if weather_id == 801:
        return "🌤"
    if 802 <= weather_id <= 804:
        return "☁"
    return "🌡"


class WeatherWorker(QThread):
    """Hämtar vädret i en egen tråd så att fönstret inte fryser."""

    succeeded = pyqtSignal(dict)
    failed = pyqtSignal(str)

    def __init__(self, city, parent=None):
        super().__init__(parent)
        self.city = city

    def run(self):
        params = {"q": self.city, "appid": API_KEY, "units": "metric"}
        try:
            response = requests.get(API_URL, params=params, timeout=10)
            response.raise_for_status()
            data = response.json()
        except requests.exceptions.HTTPError as http_error:
            message = HTTP_ERRORS.get(
                response.status_code, f"HTTP error\n{http_error}"
            )
            self.failed.emit(message)
        except requests.exceptions.Timeout:
            self.failed.emit("Request timed out\nThe server took too long to answer")
        except requests.exceptions.ConnectionError:
            self.failed.emit("Connection error\nCheck your internet connection")
        except requests.exceptions.TooManyRedirects:
            self.failed.emit("Too many redirects\nCheck the request URL")
        except requests.exceptions.RequestException as request_error:
            self.failed.emit(f"Request failed\n{request_error}")
        except ValueError:
            self.failed.emit("Invalid response\nThe server did not return JSON")
        else:
            self.succeeded.emit(data)


class WeatherApp(QWidget):
    def __init__(self):
        super().__init__()
        self.worker = None

        self.title_label = QLabel("Weather", self)
        self.subtitle_label = QLabel("Live conditions from OpenWeather", self)

        self.city_input = QLineEdit(self)
        self.search_button = QPushButton("Search", self)

        self.card = QFrame(self)
        self.location_label = QLabel("", self)
        self.emoji_label = QLabel("🌤", self)
        self.temperature_label = QLabel("", self)
        self.description_label = QLabel("Search for a city to get started", self)

        self.feels_like_value, self.feels_like_card = self.create_stat("Feels like")
        self.humidity_value, self.humidity_card = self.create_stat("Humidity")
        self.wind_value, self.wind_card = self.create_stat("Wind")

        self.status_label = QLabel("", self)

        self.init_ui()


    def create_stat(self, title):
        """Bygg ett litet statistikkort och returnera (värde-label, kort)."""
        card = QFrame(self)
        card.setObjectName("stat_card")

        title_label = QLabel(title, card)
        title_label.setObjectName("stat_title")
        title_label.setAlignment(Qt.AlignCenter)

        value_label = QLabel("--", card)
        value_label.setObjectName("stat_value")
        value_label.setAlignment(Qt.AlignCenter)

        layout = QVBoxLayout(card)
        layout.setContentsMargins(12, 14, 12, 14)
        layout.setSpacing(4)
        layout.addWidget(title_label)
        layout.addWidget(value_label)

        return value_label, card

    def init_ui(self):
        self.setWindowTitle("Weather App")
        self.setObjectName("root")
        self.setMinimumSize(460, 660)

        self.title_label.setObjectName("title_label")
        self.subtitle_label.setObjectName("subtitle_label")
        self.city_input.setObjectName("city_input")
        self.search_button.setObjectName("search_button")
        self.card.setObjectName("card")
        self.location_label.setObjectName("location_label")
        self.emoji_label.setObjectName("emoji_label")
        self.temperature_label.setObjectName("temperature_label")
        self.description_label.setObjectName("description_label")
        self.status_label.setObjectName("status_label")

        for label in (
            self.title_label,
            self.subtitle_label,
            self.location_label,
            self.emoji_label,
            self.temperature_label,
            self.description_label,
            self.status_label,
        ):
            label.setAlignment(Qt.AlignCenter)

        self.card.setMinimumHeight(400)
        self.temperature_label.setMinimumHeight(86)
        self.description_label.setWordWrap(True)
        self.status_label.setWordWrap(True)

        self.city_input.setPlaceholderText("Enter a city name…")
        self.search_button.setCursor(Qt.PointingHandCursor)

        search_row = QHBoxLayout()
        search_row.setSpacing(10)
        search_row.addWidget(self.city_input)
        search_row.addWidget(self.search_button)

        stats_row = QHBoxLayout()
        stats_row.setSpacing(10)
        stats_row.addWidget(self.feels_like_card)
        stats_row.addWidget(self.humidity_card)
        stats_row.addWidget(self.wind_card)

        card_layout = QVBoxLayout(self.card)
        card_layout.setContentsMargins(24, 28, 24, 24)
        card_layout.setSpacing(6)
        card_layout.addWidget(self.location_label)
        card_layout.addWidget(self.emoji_label)
        card_layout.addWidget(self.temperature_label)
        card_layout.addWidget(self.description_label)
        card_layout.addSpacing(14)
        card_layout.addLayout(stats_row)

        root_layout = QVBoxLayout(self)
        root_layout.setContentsMargins(28, 28, 28, 28)
        root_layout.setSpacing(16)
        root_layout.addWidget(self.title_label)
        root_layout.addWidget(self.subtitle_label)
        root_layout.addSpacing(8)
        root_layout.addLayout(search_row)
        root_layout.addWidget(self.card)
        root_layout.addWidget(self.status_label)
        root_layout.addStretch()

        self.setStyleSheet(STYLESHEET)

        self.search_button.clicked.connect(self.get_weather)
        self.city_input.returnPressed.connect(self.get_weather)

        if not API_KEY:
            self.show_status(
                "No API key found — add 'open-weather-cred' to your .env", error=True
            )
            self.search_button.setEnabled(False)

    @staticmethod
    def set_state(widget, state):
        """Byt dynamisk state-property och tvinga om-styling."""
        widget.setProperty("state", state)
        widget.style().unpolish(widget)
        widget.style().polish(widget)


    def get_weather(self):
        if self.worker is not None and self.worker.isRunning():
            return

        city = self.city_input.text().strip()
        if not city:
            self.show_status("Please enter a city name")
            return

        self.set_loading(True)
        self.show_status(f"Searching for {city}…")

        self.worker = WeatherWorker(city, self)
        self.worker.succeeded.connect(self.display_weather)
        self.worker.failed.connect(self.display_error)
        self.worker.finished.connect(lambda: self.set_loading(False))
        self.worker.start()

    def set_loading(self, loading):
        self.search_button.setEnabled(not loading and bool(API_KEY))
        self.search_button.setText("Searching…" if loading else "Search")
        self.city_input.setEnabled(not loading)

    def show_status(self, message, error=False):
        self.status_label.setText(message)
        self.set_state(self.status_label, "error" if error else "")

    def display_error(self, message):
        headline, _, detail = message.partition("\n")

        self.location_label.setText("")
        self.emoji_label.setText("⚠")
        self.temperature_label.setText(headline)
        self.set_state(self.temperature_label, "error")
        self.description_label.setText(detail or "Please try again")
        for value_label in (self.feels_like_value, self.humidity_value, self.wind_value):
            value_label.setText("--")
        self.show_status("")

    def display_weather(self, data):
        main = data["main"]
        weather = data["weather"][0]

        city = data.get("name") or self.city_input.text().strip()
        country = data.get("sys", {}).get("country", "")
        self.location_label.setText(f"{city}, {country}" if country else city)

        self.emoji_label.setText(weather_emoji(weather["id"]))
        self.temperature_label.setText(f"{round(main['temp'])}°C")
        self.set_state(self.temperature_label, "")
        self.description_label.setText(weather["description"].capitalize())

        self.feels_like_value.setText(f"{round(main['feels_like'])}°C")
        self.humidity_value.setText(f"{main['humidity']}%")
        self.wind_value.setText(f"{data.get('wind', {}).get('speed', 0):.1f} m/s")

        self.show_status("")

    def closeEvent(self, event):
        if self.worker is not None and self.worker.isRunning():
            self.worker.wait(2000)
        super().closeEvent(event)


STYLESHEET = """
    QWidget#root {
        background-color: qlineargradient(x1:0, y1:0, x2:0.4, y2:1,
                                          stop:0 #1d2b53, stop:0.55 #131c36, stop:1 #0b1020);
    }
    QLabel, QPushButton, QLineEdit {
        font-family: "Segoe UI", "SF Pro Text", Calibri, sans-serif;
        color: #e2e8f0;
    }
    QLabel#title_label {
        font-size: 34px;
        font-weight: 600;
        letter-spacing: 1px;
        color: #f8fafc;
    }
    QLabel#subtitle_label {
        font-size: 13px;
        color: #8ea0c0;
    }
    QLineEdit#city_input {
        font-size: 17px;
        padding: 12px 16px;
        border: 1px solid rgba(255, 255, 255, 0.14);
        border-radius: 14px;
        background-color: rgba(255, 255, 255, 0.07);
        selection-background-color: #38bdf8;
        selection-color: #0b1020;
    }
    QLineEdit#city_input:focus {
        border: 1px solid #38bdf8;
        background-color: rgba(255, 255, 255, 0.12);
    }
    QLineEdit#city_input:disabled {
        color: #64748b;
    }
    QPushButton#search_button {
        font-size: 16px;
        font-weight: 600;
        padding: 12px 26px;
        border: none;
        border-radius: 14px;
        background-color: #38bdf8;
        color: #0b1020;
    }
    QPushButton#search_button:hover {
        background-color: #7dd3fc;
    }
    QPushButton#search_button:pressed {
        background-color: #0ea5e9;
    }
    QPushButton#search_button:disabled {
        background-color: rgba(255, 255, 255, 0.10);
        color: #64748b;
    }
    QFrame#card {
        background-color: rgba(255, 255, 255, 0.06);
        border: 1px solid rgba(255, 255, 255, 0.10);
        border-radius: 24px;
    }
    QLabel#location_label {
        font-size: 15px;
        font-weight: 600;
        letter-spacing: 2px;
        color: #94a3b8;
    }
    QLabel#emoji_label {
        font-size: 80px;
        font-family: "Apple Color Emoji", "Segoe UI Emoji", "Noto Color Emoji", sans-serif;
    }
    QLabel#temperature_label {
        font-size: 68px;
        font-weight: 300;
        color: #f8fafc;
    }
    QLabel#temperature_label[state="error"] {
        font-size: 24px;
        font-weight: 600;
        color: #fca5a5;
    }
    QLabel#description_label {
        font-size: 18px;
        color: #cbd5e1;
    }
    QFrame#stat_card {
        background-color: rgba(255, 255, 255, 0.05);
        border: 1px solid rgba(255, 255, 255, 0.08);
        border-radius: 16px;
    }
    QLabel#stat_title {
        font-size: 12px;
        letter-spacing: 1px;
        color: #8ea0c0;
    }
    QLabel#stat_value {
        font-size: 20px;
        font-weight: 600;
        color: #f1f5f9;
    }
    QLabel#status_label {
        font-size: 13px;
        color: #8ea0c0;
    }
    QLabel#status_label[state="error"] {
        color: #fca5a5;
    }
"""


if __name__ == "__main__":
    app = QApplication(sys.argv)
    weather_app = WeatherApp()
    weather_app.show()
    sys.exit(app.exec_())
