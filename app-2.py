from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.slider import Slider
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.image import AsyncImage
from kivy.uix.widget import Widget
from kivy.utils import get_color_from_hex
import requests

arduino_port = '60000'
arduino_ip = '192.168.0.184'
webhook = 'solar_guardian'
webhook_url = f'http://{arduino_ip}:{arduino_port}/{webhook}'

class ServoControlApp(App):
    def build(self):
        layout = BoxLayout(orientation='vertical', padding = 20, spacing = 20, size_hint =(None, None))
        layout.width = 300
        layout.height = 300
        self.label = Label(text='Adjust The Angles', size_hint = (None, None), size = (300, 50), halign = 'center')
        self.slider = Slider(min=0, max=180, value=90, step = 1, size_hint = (None, None), size = (800, 50))
        self.reset_button = Button(text = 'Reset Louvers', size_hint = (None, None), size = (300, 50), background_color =get_color_from_hex('#FF0000'))

        self.slider.bind(value=self.on_slider_change)
        self.reset_button.bind(on_press = self.reset_louvers)

        background = AsyncImage(source='https://img.freepik.com/free-photo/white-cloud-blue-sky_74190-7709.jpg?size=626&ext=jpg&ga=GA1.1.386372595.1697846400&semt=sph', 
                                allow_stretch = True,
                                keep_ratio = False)

        layout.add_widget(self.label)
        layout.add_widget(self.slider)
        layout.add_widget(self.reset_button)
        layout.add_widget(background)

        self.user_active = False

        return layout

    def on_slider_change(self, value):
        try:
            self.label.text = f'Rotation: {int(value)}'
            self.send_rotation_data(int(value))
            self.user_active = True
            if self.user_active:
                self.send_rotation_data()
        except Exception as e:
            print(f'Error: {e}')

    def send_rotation_data(self, rotation):
        data = {'servo_position': rotation}
        try:
            response = requests.post(webhook_url, json=data)
            if response.status_code == 200:
                print('Data sent successfully')
            else:
                print('Failed to send data')
        except requests.exceptions.RequestException as e:
            print(f'Error: {e}')

    def on_pause(self):
        self.user_active = False

    def reset_louvers(self):
        self.slider.value = 90


if __name__ == '__main__':
    ServoControlApp().run()




#manual mode <-> automatic mode(tells the user what the angle of the current louvers)