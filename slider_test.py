from kivy.app import App
from kivy.lang import Builder
from kivy.uix.slider import Slider
from kivy.uix.widget import Widget
from kivy.properties import StringProperty

Builder.load_string('''
<CustomLabel>:
    Label:
        text: root.text
        font_size: sp(16)
        size_hint: None, None
        size: self.texture_size
        pos: root.center
        color: 0, 0, 0, 1
''')

class CustomLabel(Widget):
    text = StringProperty('')

class MySlider(Slider):
    def __init__(self, **kwargs):
        super(MySlider, self).__init__(**kwargs)
        self.tracker = CustomLabel(pos=self.center)
        self.bind(value=self.update_tracker)
        self.bind(pos=self.update_tracker)
        self.bind(size=self.update_tracker)
        self.parent.add_widget(self.tracker)

    def update_tracker(self, *args):
        self.tracker.pos = (self.center_x, self.y + self.height)
        self.tracker.text = str(int(self.value))

class MyApp(App):
    def build(self):
        return MySlider(min=0, max=100, value=50)

if __name__ == '__main__':
    MyApp().run()

