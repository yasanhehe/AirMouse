import kivy
kivy.require('1.11.1') # 使用するKivyのバージョンを指定

from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.slider import Slider

# 必要なスライダー
#   マウスの可動範囲を決めるしきい値 Mouse_Fie
#   マウスの動く感度
#   ジェスチャーの感度



class MyApp(App):
    def build(self):
        self.title = 'AirMouse'
        layout = BoxLayout(orientation='vertical')

        mousepad_size_slider = Slider(min=0, max=100, value=50)
        mousepad_size_label = Label(text='Mousepad size', size_hint=(1, 0.8), font_size=40)
        mousepad_size_value_label = Label(text=str(int(mousepad_size_slider.value)), size_hint=(1, 0.8), font_size=40)

        mouse_se_slider = Slider(min=0, max=100, value=50)
        mouse_se_label = Label(text="Mouse sensitivity", size_hint=(1, 0.8), font_size=40)
        mouse_se_value_label = Label(text=str(int(mouse_se_slider.value)), size_hint=(1, 0.8), font_size=40)

        gestures_se_slider = Slider(min=0, max=100, value=50)
        gestures_se_label = Label(text="Gestures sensitivity", size_hint=(1, 0.8), font_size=40)
        gestures_se_value_label = Label(text=str(int(mouse_se_slider.value)), size_hint=(1, 0.8), font_size=40)

        start_button = Button(text='Start', font_size=40)
        stop_button = Button(text='Stop', font_size=40)

        layout.add_widget(mousepad_size_label)
        layout.add_widget(mousepad_size_value_label)
        layout.add_widget(mousepad_size_slider)
        layout.add_widget(mouse_se_label)
        layout.add_widget(mouse_se_value_label)
        layout.add_widget(mouse_se_slider)
        layout.add_widget(gestures_se_label)
        layout.add_widget(gestures_se_value_label)
        layout.add_widget(gestures_se_slider)
        layout.add_widget(start_button)
        layout.add_widget(stop_button)

        mousepad_size_slider.bind(value=lambda instance, value: on_value_change(instance, value, mousepad_size_value_label))
        mouse_se_slider.bind(value=lambda instance, value: on_value_change(instance, value, mouse_se_value_label))
        gestures_se_slider.bind(value=lambda instance, value: on_value_change(instance, value, gestures_se_value_label))

        def start_button_pressed(button):
            pass

        def stop_button_pressed(button):
            pass

        def on_value_change(instance, value, label):
            label.text = str(int(value))

        start_button.bind(on_press=start_button_pressed)

        return layout

if __name__ == '__main__':
    MyApp().run()

