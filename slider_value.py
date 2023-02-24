from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.slider import Slider

class SliderApp(App):
    def build(self):
        layout = BoxLayout(orientation='vertical')
        slider = Slider(min=0, max=100, value=50)
        label = Label(text=str(int(slider.value)))
        layout.add_widget(label)
        layout.add_widget(slider)
        
        def on_value_change(instance, value):
            label.text = str(int(value))
            
        slider.bind(value=on_value_change)
        return layout

if __name__ == '__main__':
    SliderApp().run()

