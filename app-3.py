from kivy.app import App
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.slider import Slider
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.image import AsyncImage
from kivy.utils import get_color_from_hex
from kivy.clock import Clock
import requests
import aiohttp

arduino_port = '60000'
arduino_ip = '192.168.0.184'
webhook = 'solar_guardian'
webhook_url = f'http://{arduino_ip}:{arduino_port}/{webhook}'
api_key = '49149c3c44b44dd269d4ccd896fba3f6'
city = 'Eindhoven' 

class ServoControlApp(App):
    def build(self):
        layout = FloatLayout()
        
        background = AsyncImage(
            source='https://img.freepik.com/free-photo/white-cloud-blue-sky_74190-7709.jpg?size=626&ext=jpg&ga=GA1.1.386372595.1697846400&semt=sph',
            allow_stretch=True,
            keep_ratio=True)
        layout.add_widget(background)
        
        self.label = Label(text='Adjust The Angles', 
                           size_hint=(None, None), 
                           size=(400, 150), 
                           halign='center', 
                           pos_hint={'x': 0.3, 'top': 0.95},
                           color = (0,0,0,1)
        )

        self.weather_label = Label( 
            text='Fetching weather...',
            size_hint=(None, None),
            size=(400, 50),
            halign='center',
            pos_hint={'x': 0.3, 'top': 0.7}
        )

        self.slider = Slider(min=0, max=180, value=90, step=1, size_hint=(None, None), size=(800, 50), pos_hint={'x': 0.1, 'top': 0.8})
        self.reset_button = Button(text='Reset Louvers', size_hint=(None, None), size=(300, 50), background_color=get_color_from_hex('#FF0000'), pos_hint={'x': 0.35, 'top': 0.2})
        self.fetch_weather_data()

        self.reset_button.bind(on_press=self.reset_louvers)
        self.slider.bind(value=self.on_slider_change)

        layout.add_widget(self.label)
        layout.add_widget(self.slider)
        layout.add_widget(self.reset_button)
        layout.add_widget(self.weather_label)

        self.user_active = False

        return layout

    def on_slider_change(self, instance, value):
        self.label.text = f'Rotation: {int(value)}'
        Clock.schedule_once(lambda dt: self.send_rotation_data(int(value)))

    async def send_rotation_data(self, rotation):
        data = {'servo_position': rotation}
        try:
            async with aiohttp.ClientSession() as session:
                async with session.post(webhook_url, json=data) as response:
                    if response.status == 200:
                        print('Data sent successfully')
                    else:
                        print('Failed to send data')
        except aiohttp.ClientError as e:
            print(f'Error: {e}')

    def on_pause(self):
        self.user_active = False

    def reset_louvers(self, instance):
        self.slider.value = 90
        Clock.schedule_once(lambda dt: self.send_rotation_data(90))

    def fetch_weather_data(self):
        try:
            weather_data = requests.get(f'https://api.openweathermap.org/data/2.5/weather?q={city}&units=metric&appid={api_key}')
            if weather_data.json().get('cod') == 200:
                weather = weather_data.json()['weather'][0]['main']
                temp = round(weather_data.json()['main']['temp'])
                temp_min = round(weather_data.json()['main']['temp_min'])
                temp_max = round(weather_data.json()['main']['temp_max'])
                self.weather_label.text = f'Weather: {weather}, Temp: {temp}°C (Min: {temp_min}°C, Max: {temp_max}°C)'
            else:
                self.weather_label.text = 'No city found'
        except Exception as e:
            self.weather_label.text = 'Error fetching weather'

if __name__ == '__main__':
    import aiohttp
    from kivy import require
    require('2.0.0')
    ServoControlApp().run()
