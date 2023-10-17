from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.slider import Slider
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.image import Image
from kivy.utils import get_color_from_hex

import requests

# Define the URL of your Arduino server
webhook_url = 'http://your_arduino_ip:your_port/webhook'

class ServoControlApp(App):
    def build(self):
        layout = BoxLayout(orientation='vertical', padding = 20, spacing = 20, size_hint =(None, None))
        layout.width = 300
        layout.height = 300
        background = Image(source='sun.jpg')

        self.label = Label(text='Control the Servos', size_hint = (None, None), size = (300, 50), halign = 'center')
        self.slider = Slider(min=0, max=180, value=90, step = 1, size_hint = (None, None), size = (300, 50))
        self.reset_button = Button(text = 'Reset Louvers', size_hint = (None, None), size = (300, 50), background_color = get_color_from_hex('#FF0000'))

        self.slider.bind(value=self.on_slider_change)
        self.reset_button.bind(on_press = self.reset_louvers)

        background = Image(source='background.jpg')

        layout.add_widget(self.label)
        layout.add_widget(self.slider)
        layout.add_widget(self.reset_button)
        layout.add_widget(background)

        self.user_active = False

        return layout

    def on_slider_change(self, value):
        self.label.text = f'Rotation: {int(value)}'
        self.send_rotation_data(int(value))
        self.user_active = True

        if self.user_active:
            self.send_rotation_data()

    def send_rotation_data(self):
        rotation = self.slider.value
        data = {'servo_position': rotation}

        if self.user_active:
            response = requests.post(webhook_url, json=data)
        if response.status_code == 200:
            print('Data sent successfully')
        else:
            print('Failed to send data')

    def on_pause(self):
        self.user_active = False

    def reset_louvers(self):
        self.slider.value = 90

if __name__ == '__main__':
    ServoControlApp().run()

#modify UI

