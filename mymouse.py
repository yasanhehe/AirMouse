import cv2
import pyautogui as pag
import mediapipe as mp
import time
import math

pag.FAILSAFE = False
pag.MINIMUM_DURATION = 0.0

mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles
mp_hands = mp.solutions.hands

class Mouse:
    def __init__(self, mousepad_size, gestures_se, scroll_se, click_interval):
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
        self.apply_params(mousepad_size, gestures_se, scroll_se, click_interval)

    def apply_params(self, mousepad_size, gestures_se, scroll_se, click_interval):
        blank = (1.0 - mousepad_size) / 2.0
        width, height = pag.size()
        self.params = {
            'mousepad_min': blank,
            'mousepad_max': 1.0 - blank,
            #0~1 to 0~0.1
            'gestures_se': gestures_se / 10.0,
            #0~1 to 0~10
            'scroll_se': scroll_se * 10,
            'click_interval': click_interval,
            'click_interval_cnt': click_interval,
            'width': width,
            'height': height
        }
        return self.params

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

    def th_check(self, value):
        if value < self.params['mousepad_min']:
            return -1
        if value > self.params['mousepad_max']:
            return 1
        return 0

    def landmark_to_location(self, finger):
        finger_x = self.fingers[finger].x
        finger_y = self.fingers[finger].y
        width = self.params['width']
        height = self.params['height']
        mousepad_range = self.params['mousepad_max'] - self.params['mousepad_min']
        x_out_of_range = self.th_check(finger_x)
        y_out_of_range = self.th_check(finger_y)

        if x_out_of_range == 1:
            finger_x = 1
        elif x_out_of_range == -1:
            finger_x = 0
        if y_out_of_range == 1:
            finger_y = 1
        elif y_out_of_range == -1:
            finger_y = 0

        aligned_x = width - ((finger_x - self.params['mousepad_min']) / mousepad_range) * width
        aligned_y = (finger_y - self.params['mousepad_min']) / mousepad_range * height
        location = {'x': aligned_x, 'y': aligned_y, 'z': self.fingers[finger].z}
        return location

    def landmark_to_distance(self, finger_a, finger_b):
        distance_x = (self.fingers[finger_a].x - self.fingers[finger_b].x) ** 2
        distance_y = (self.fingers[finger_a].y - self.fingers[finger_b].y) ** 2
        distance = math.sqrt(distance_x + distance_y)
        return distance

    def move_mouse(self, location):
        if not location is None:
            try:
                pag.moveTo(location['x'], location['y'])
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
                    continue

                image.flags.writeable = False
                #image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
                results = hands.process(image)

                #image.flags.writeable = True
                #image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
                if results.multi_hand_landmarks:
                    hand_landmarks = self.get_hand_landmarks(results)
                    if hand_landmarks:
                        for i, k in zip(range(4, 17, 4), self.fingers):
                            self.fingers[k] = hand_landmarks.landmark[i]

                        thumb_middle_distance = self.landmark_to_distance('thumb', 'middle')
                        index_middle_distance = self.landmark_to_distance('index', 'middle')
                        thumb_ring_distance = self.landmark_to_distance('thumb', 'ring')

                        if thumb_middle_distance < self.params['gestures_se']:
                            if self.params['click_interval'] == self.params['click_interval_cnt']:
                                pag.click()
                                print('clicked')
                                self.params['click_interval_cnt'] = 0
                            else:
                                self.params['click_interval_cnt'] += 1
                        elif index_middle_distance < self.params['gestures_se'] and thumb_ring_distance < self.params['gestures_se']:
                            if self.gestures['scroll']:
                                scroll_range = self.prev_fingers['index'].y - self.fingers['index'].y
                                print('scrolled', scroll_range)
                                pag.scroll(-scroll_range * self.params['scroll_se'])
                            else:
                                self.gestures['scroll'] = True
                        else:
                            for k in self.gestures:
                                self.gestures[k] = False
                            location = self.landmark_to_location('index')
                            self.move_mouse(location)
                            self.prev_fingers = self.fingers.copy()
                            print(location)

                if self.stop_flag:
                    break
        cap.release()
