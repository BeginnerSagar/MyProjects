import requests
import tkinter as tk
from tkinter import ttk, messagebox

class WeatherApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Weather App")

        self.api_key = "6e6b0dddce2cef1a097eaf63c9b2ac4b"  # Replace with your actual API key
        self.base_url = "http://api.openweathermap.org/data/2.5/weather"
        self.history = []

        self.create_widgets()

    def create_widgets(self):
        # GUI components
        self.location_label = ttk.Label(self.root, text="Enter Location:")
        self.location_entry = ttk.Entry(self.root, width=20)
        self.get_weather_button = ttk.Button(self.root, text="Get Weather", command=self.get_weather)
        self.weather_label = ttk.Label(self.root, text="Weather: N/A")

        # Graphical weather representation
        self.weather_canvas = tk.Canvas(self.root, width=200, height=200)
        self.weather_canvas.grid(row=0, column=2, rowspan=3, padx=10, pady=10)

        # Search history
        self.history_label = ttk.Label(self.root, text="Search History:")
        self.history_text = tk.Text(self.root, height=5, width=30, state=tk.DISABLED)
        self.clear_history_button = ttk.Button(self.root, text="Clear History", command=self.clear_history)

        # Layout
        self.location_label.grid(row=0, column=0, padx=10, pady=10)
        self.location_entry.grid(row=0, column=1, padx=10, pady=10)
        self.get_weather_button.grid(row=1, column=0, columnspan=2, pady=10)
        self.weather_label.grid(row=2, column=0, columnspan=2, pady=10)
        self.history_label.grid(row=3, column=0, pady=10)
        self.history_text.grid(row=3, column=1, padx=10, pady=10)
        self.clear_history_button.grid(row=4, column=1, pady=10)

    def get_weather(self):
        location = self.location_entry.get()
        if not location:
            messagebox.showinfo("Error", "Please enter a location.")
            return

        params = {
            "q": location,
            "appid": self.api_key,
            "units": "metric"
        }

        try:
            response = requests.get(self.base_url, params=params)
            data = response.json()
            if response.status_code == 200:
                weather_description = data['weather'][0]['description']
                temperature = data['main']['temp']
                self.weather_label.config(text=f"Weather: {weather_description}, Temperature: {temperature}°C")
                self.draw_weather_icon(data['weather'][0]['icon'])
                self.add_to_history(location)
            else:
                messagebox.showinfo("Error", f"Failed to get weather data. {data['message']}")
        except Exception as e:
            messagebox.showinfo("Error", f"An error occurred: {str(e)}")

    def draw_weather_icon(self, icon):
        # This is a simplified example. You might want to use a library for more advanced graphics.
        self.weather_canvas.delete("all")
        # Draw a simple representation of the weather icon (e.g., a colored circle or image)

    def add_to_history(self, location):
        self.history.append(location)
        self.update_history_text()

    def update_history_text(self):
        self.history_text.config(state=tk.NORMAL)
        self.history_text.delete("1.0", tk.END)
        for item in self.history:
            self.history_text.insert(tk.END, f"{item}\n")
        self.history_text.config(state=tk.DISABLED)

    def clear_history(self):
        self.history = []
        self.update_history_text()

if __name__ == "__main__":
    root = tk.Tk()
    app = WeatherApp(root)
    root.mainloop()
