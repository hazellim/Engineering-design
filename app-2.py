import kivy
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.slider import Slider
from kivy.uix.label import Label
from kivy.uix.button import Button
import requests

# Define the URL of your Arduino server
webhook_url = 'http://your_arduino_ip:your_port/webhook'

class ServoControlApp(App):
    def build(self):
        layout = BoxLayout(orientation='vertical')

        self.label = Label(text='Control the Servos')
        self.slider = Slider(min=0, max=180, value=90)
        self.button = Button(text='Send Rotation')

        self.slider.bind(value=self.on_slider_change)
        self.button.bind(on_press=self.send_rotation_data)

        layout.add_widget(self.label)
        layout.add_widget(self.slider)
        layout.add_widget(self.button)

        return layout

    def on_slider_change(self, instance, value):
        self.label.text = f'Rotation: {int(value)}'
        self.send_rotation_data()

    def send_rotation_data(self, instance):
        rotation = self.slider.value
        data = {'servo_position': rotation}
        response = requests.post(webhook_url, json=data)
        if response.status_code == 200:
            print('Data sent successfully')
        else:
            print('Failed to send data')

if __name__ == '__main__':
    ServoControlApp().run()
    