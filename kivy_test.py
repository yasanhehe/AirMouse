import cv2
import time
import pyautogui as pag
import mediapipe as mp
import math
import kivy
kivy.require('1.11.1') # 使用するKivyのバージョンを指定
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.slider import Slider

pag.FAILSAFE = False
pag.MINIMUM_DURATION = 0.0

mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles
mp_hands = mp.solutions.hands

class Mouse:
    def __init__(self, mousepad_size, mouse_se, gestures_se, scroll_se, click_interval):
        self.fingers = {
            'thumb': {
                'x': 0.0, 'y': 0.0
                },
            'index': {
                'x': 0.0, 'y': 0.0
                },
            'middle': {
                'x': 0.0, 'y': 0.0
                },
            'ring': {
                'x': 0.0, 'y': 0.0
                }
            }
        self.prev_fingers = self.fingers.copy()
        self.gestures = {'scroll': False, 'click': False}

        self.stop_flag = False
        self.click_interval = False
        self.mousepad_size = mousepad_size
        self.mouse_se = mouse_se
        self.gestures_se = gestures_se
        self.scroll_se = scroll_se
        self.click_interval = click_interval

    def get_hand_landmarks(self, results):
        if results.multi_handedness is None:
            return None
        multi_hand_landmarks = results.multi_hand_landmarks
        multi_handedness = results.multi_handedness

        hands_labels = [item.classification[0].label for item in multi_handedness if item.classification[0].label]

        if len(hands_labels) == 1:
            hands_index = 0
        else:
            if 'Right' in hands_labels and len(set(hands_labels)) == 2:
                hands_index = hands_labels.index('Right')
            else:
                return None
        hand_landmarks = multi_hand_landmarks[hands_index]
        return hand_landmarks

    def th_check(self, value, min_th, max_th):
        if value < min_th:
            return -1
        if value > max_th:
            return 1
        return 0

    def landmark_to_location(self, landmark, width, height, min_th, max_th):
        x_out_of_range = self.th_check(landmark.x, min_th, max_th)
        y_out_of_range = self.th_check(landmark.y, min_th, max_th)
        if x_out_of_range == 1:
            landmark.x = 1
        elif x_out_of_range == -1:
            landmark.x = 0
        if y_out_of_range == 1:
            landmark.y = 1
        elif y_out_of_range == -1:
            landmark.y = 0
        # flip and align to window size
        aligned_x = width - ((landmark.x - min_th) * (1 / (max_th - min_th))) * width
        aligned_y = ((landmark.y - min_th) * (1 / (max_th - min_th))) * height
        location = {'x': aligned_x, 'y': aligned_y, 'z': landmark.z}
        return location

    def landmark_to_distance(self, landmark_a, landmark_b):
        distance_x = (landmark_a.x - landmark_b.x) ** 2
        distance_y = (landmark_a.y - landmark_b.y) ** 2
        distance = math.sqrt(distance_x + distance_y)
        return distance

    def move_mouse(self, location, interval):
        if not location is None:
            try:
                pag.moveTo(location['x'], location['y'], duration=interval)
            except:
                pass

    def stop_mouse(self):
        self.stop_flag = True

    def air_mouse(self):
        cap = cv2.VideoCapture(0)
        with mp_hands.Hands(
            model_complexity=0,
            min_detection_confidence=0.5,
            min_tracking_confidence=0.5) as hands:
            while cap.isOpened():
                success, image = cap.read()
                if not success:
                    print("Ignoring empty camera frame.")
                    continue

                image.flags.writeable = False
                image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
                results = hands.process(image)

                image.flags.writeable = True
                image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
                if results.multi_hand_landmarks:
                    hand_landmarks = self.get_hand_landmarks(results)
                    if hand_landmarks:
                        for i, k in zip(range(4, 17, 4), self.fingers):
                            self.fingers[k] = hand_landmarks.landmark[i]

                        width, height = pag.size()

                        thumb_middle_distance = self.landmark_to_distance(self.fingers['thumb'], self.fingers['middle'])
                        index_middle_distance = self.landmark_to_distance(self.fingers['index'], self.fingers['middle'])
                        thumb_ring_distance = self.landmark_to_distance(self.fingers['thumb'], self.fingers['ring'])

                        if thumb_middle_distance < 0.09 and not self.click_interval:
                            pag.click()
                            print('clicked')
                        elif index_middle_distance < 0.07 and thumb_ring_distance < 0.07:
                            if self.gestures['scroll']:
                                scroll_range = self.prev_fingers['index'].y - self.fingers['index'].y
                                print('scrolled', scroll_range)
                                pag.scroll(-scroll_range * (height / 10))
                            else:
                                print('scroll_false')
                                self.gestures['scroll'] = True
                        else:
                            for k in self.gestures:
                                self.gestures[k] = False
                            location = self.landmark_to_location(self.fingers['index'], width, height, 0.1, 0.9)
                            self.move_mouse(location, 0)
                            self.prev_fingers = self.fingers.copy()
                            print(location)
                if self.stop_flag:
                    break
        cap.release()

class MyApp(App):
    def build(self):
        self.title = 'AirMouse'
        self.mouse_running = False
        defaults = {
                'mousepad_size': 50,
                'mouse_se': 50,
                'gestures_se': 50,
                'scroll_se': 50,
                'click_interval': 50
                }
        mouse = Mouse(*defaults.values())
        layout = BoxLayout(orientation='vertical')

        mousepad_size_slider = Slider(min=0, max=100, value=defaults['mousepad_size'])
        mousepad_size_label = Label(text='Mousepad size', size_hint=(1, 0.8), font_size=40)
        mousepad_size_value_label = Label(text=str(int(mousepad_size_slider.value)), size_hint=(1, 0.8), font_size=40)

        mouse_se_slider = Slider(min=0, max=100, value=defaults['mouse_se'])
        mouse_se_label = Label(text="Mouse sensitivity", size_hint=(1, 0.8), font_size=40)
        mouse_se_value_label = Label(text=str(int(mouse_se_slider.value)), size_hint=(1, 0.8), font_size=40)

        gestures_se_slider = Slider(min=0, max=100, value=defaults['gestures_se'])
        gestures_se_label = Label(text="Gestures sensitivity", size_hint=(1, 0.8), font_size=40)
        gestures_se_value_label = Label(text=str(int(mouse_se_slider.value)), size_hint=(1, 0.8), font_size=40)

        scroll_se_slider = Slider(min=0, max=100, value=defaults['scroll_se'])
        scroll_se_label = Label(text="Scroll sensitivity", size_hint=(1, 0.8), font_size=40)
        scroll_se_value_label = Label(text=str(int(scroll_se_slider.value)), size_hint=(1, 0.8), font_size=40)

        click_interval_slider = Slider(min=0, max=100, value=defaults['click_interval'])
        click_interval_label = Label(text="Scroll sensitivity", size_hint=(1, 0.8), font_size=40)
        click_interval_value_label = Label(text=str(int(click_interval_slider.value)), size_hint=(1, 0.8), font_size=40)

        start_button = Button(text='Start', font_size=40)
        stop_button = Button(text='Stop', font_size=40)
        apply_button = Button(text='Apply settings', font_size=40)

        layout.add_widget(mousepad_size_label)
        layout.add_widget(mousepad_size_value_label)
        layout.add_widget(mousepad_size_slider)
        layout.add_widget(mouse_se_label)
        layout.add_widget(mouse_se_value_label)
        layout.add_widget(mouse_se_slider)
        layout.add_widget(gestures_se_label)
        layout.add_widget(gestures_se_value_label)
        layout.add_widget(gestures_se_slider)
        layout.add_widget(scroll_se_label)
        layout.add_widget(scroll_se_value_label)
        layout.add_widget(scroll_se_slider)
        layout.add_widget(click_interval_label)
        layout.add_widget(click_interval_value_label)
        layout.add_widget(click_interval_slider)
        layout.add_widget(start_button)
        layout.add_widget(stop_button)
        layout.add_widget(apply_button)

        mousepad_size_slider.bind(value=lambda instance, value: on_value_change(instance, value, mousepad_size_value_label))
        mouse_se_slider.bind(value=lambda instance, value: on_value_change(instance, value, mouse_se_value_label))
        gestures_se_slider.bind(value=lambda instance, value: on_value_change(instance, value, gestures_se_value_label))
        scroll_se_slider.bind(value=lambda instance, value: on_value_change(instance, value, scroll_se_value_label))
        click_interval_slider.bind(value=lambda instance, value: on_value_change(instance, value, click_interval_value_label))

        def start_button_pressed(button):
            if not self.mouse_running:
                mouse.air_mouse()
                self.mouse_running = True

        def stop_button_pressed(button):
            print('stop_button_pressed')
            if self.mouse_running:
                mouse.stop_mouse()

        def apply_button_pressed(button):
            mouse.mousepad_size = float(mousepad_size_slider.value)
            mouse.mouse_se = float(mouse_se_slider.value)
            mouse.gestures_se = float(gestures_se_slider.value)
            mouse.scroll_se = float(scroll_se_slider.value)
            mouse.click_interval = float(mousepad_size_slider.value)

        def on_value_change(instance, value, label):
            label.text = str(int(value))

        start_button.bind(on_press=start_button_pressed)
        stop_button.bind(on_press=stop_button_pressed)
        apply_button.bind(on_press=apply_button_pressed)

        return layout

if __name__ == '__main__':
    MyApp().run()

