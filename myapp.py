# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    myapp.py                                           :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: skawai <skawai@student.42tokyo.jp>         +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2023/02/27 15:14:41 by skawai            #+#    #+#              #
#    Updated: 2023/02/27 15:14:42 by skawai           ###   ########.fr        #
#                                                                              #
# **************************************************************************** #

from mymouse import Mouse
import kivy
kivy.require('1.11.1') # 使用するKivyのバージョンを指定
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.slider import Slider
import threading

class MyApp(App):
    def build(self):
        self.title = 'AirMouse'
        self.mouse_running = False
        defaults = {
                'mousepad_size': 0.8,
                'gestures_se': 0.5,
                'scroll_se': 0.5,
                'click_interval': 10
                }
        mouse = Mouse(*defaults.values())
        layout = BoxLayout(orientation='vertical')

        mousepad_size_slider = Slider(min=0, max=1, value=defaults['mousepad_size'], step = 0.1, size_hint=(1, 0.5))
        mousepad_size_label = Label(text='Mousepad size', size_hint=(1, 0.5), font_size=30)
        mousepad_size_value_label = Label(text=str(float(mousepad_size_slider.value)), size_hint=(1, 0.5), font_size=25)
        mousepad_size_layout = BoxLayout(orientation='horizontal')
        mousepad_size_layout.add_widget(mousepad_size_label)
        mousepad_size_layout.add_widget(mousepad_size_value_label)

        gestures_se_slider = Slider(min=0, max=1, value=defaults['gestures_se'], step=0.1)
        gestures_se_label = Label(text="Gestures sensitivity", size_hint=(1, 0.5), font_size=30)
        gestures_se_value_label = Label(text=str(float(gestures_se_slider.value)), size_hint=(1, 0.5), font_size=25)
        gestures_se_layout = BoxLayout(orientation='horizontal')
        gestures_se_layout.add_widget(gestures_se_label)
        gestures_se_layout.add_widget(gestures_se_value_label)

        scroll_se_slider = Slider(min=0, max=1, value=defaults['scroll_se'], step=0.1)
        scroll_se_label = Label(text="Scroll sensitivity", size_hint=(1, 0.5), font_size=30)
        scroll_se_value_label = Label(text=str(float(scroll_se_slider.value)), size_hint=(1, 0.5), font_size=25)
        scroll_se_layout = BoxLayout(orientation='horizontal')
        scroll_se_layout.add_widget(scroll_se_label)
        scroll_se_layout.add_widget(scroll_se_value_label)

        click_interval_slider = Slider(min=0, max=60, value=defaults['click_interval'], step=1)
        click_interval_label = Label(text="Click interval", size_hint=(1, 0.5), font_size=30)
        click_interval_value_label = Label(text=str(float(click_interval_slider.value)), size_hint=(1, 0.5), font_size=25)
        click_interval_layout = BoxLayout(orientation='horizontal')
        click_interval_layout.add_widget(click_interval_label)
        click_interval_layout.add_widget(click_interval_value_label)

        state_label = Label(text='State: Not working', size_hint=(1, 0.5), font_size=30)
        start_button = Button(text='Start', font_size=30)
        stop_button = Button(text='Stop', font_size=30)
        apply_button = Button(text='Apply settings', font_size=30)

        layout.add_widget(mousepad_size_layout)
        layout.add_widget(mousepad_size_slider)
        layout.add_widget(gestures_se_layout)
        layout.add_widget(gestures_se_slider)
        layout.add_widget(scroll_se_layout)
        layout.add_widget(scroll_se_slider)
        layout.add_widget(click_interval_layout)
        layout.add_widget(click_interval_slider)
        layout.add_widget(state_label)
        layout.add_widget(start_button)
        layout.add_widget(stop_button)
        layout.add_widget(apply_button)

        mousepad_size_slider.bind(value=lambda instance, value: on_value_change(instance, value, mousepad_size_value_label))
        gestures_se_slider.bind(value=lambda instance, value: on_value_change(instance, value, gestures_se_value_label))
        scroll_se_slider.bind(value=lambda instance, value: on_value_change(instance, value, scroll_se_value_label))
        click_interval_slider.bind(value=lambda instance, value: on_value_change(instance, value, click_interval_value_label))

        def start_button_pressed(button):
            if not self.mouse_running:
                threading.Thread(target=mouse.air_mouse).start()
                state_label.text = 'State: Working'
                self.mouse_running = True

        def stop_button_pressed(button):
            if self.mouse_running:
                mouse.stop_mouse()
                state_label.text = 'State: Not working'
                self.mouse_running = False

        def apply_button_pressed(button):
            args = [mousepad_size_slider.value, gestures_se_slider.value, scroll_se_slider.value, click_interval_slider.value]
            mouse.apply_params(*args)

        def on_value_change(instance, value, label):
            label.text = str(round(float(value), 1))

        start_button.bind(on_press=start_button_pressed)
        stop_button.bind(on_press=stop_button_pressed)
        apply_button.bind(on_press=apply_button_pressed)

        return layout

if __name__ == '__main__':
    MyApp().run()
