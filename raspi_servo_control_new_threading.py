import socket
import threading
import time

from adafruit_servokit import ServoKit

PORT = 12345
# LOCAL
HOST = "192.168.0.183"
# HOST = "127.0.0.1"

STEPS = 10

kit = ServoKit(channels=16)


# fake_s_list = [[0, 0]] * 3
s_list = [
    [kit.servo[10], kit.servo[11]],
    [kit.servo[13], kit.servo[12]],
    [kit.servo[15], kit.servo[14]],
]


states = {
    "Neutral": [[20, 20, 20],1],
    "Angry": [[110, 60, 0],5],
    "Sad": [[110, 110, 110],1],
    "Surprised": [[0, 0, 0],3],
    "Disgusted": [[0, 60, 110],2],
    "Happy": [[60, 60, 60],2],
    "Fearful": [[60, 30, 60],2],
}


def reverse(degree):
    return 180 - degree


def mysign(x):
    return -1 if x > 0 else 1


def clamp_value(angle):
    return 0 if angle < 0 else 120 if angle > 120 else angle


def move_servos(input_values):
    for i in range(3):
        current_angle = clamp_value(input_values[i])
        s_list[i][0].angle = current_angle
        s_list[i][1].angle = reverse(current_angle)
    # print(s_list)
    time.sleep(0.1)


"""
def move_fake_servos(input_values):
    for i in range(3):
        current_angle = clamp_value(input_values[i])
        fake_s_list[i][0] = current_angle
        fake_s_list[i][1] = reverse(current_angle)
    # print(s_list)
    time.sleep(0.05)
"""


class EmotionTracker:
    def __init__(self):
        # define an instance variable
        self.cur_st = "Surprised"

    def start_server(self):
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.connect((HOST, PORT))
        global cur_st
        while True:
            try:
                msg = server.recv(64).decode("utf-8")
                print(f"Emotion received: {msg}")
                if msg in states:
                    self.cur_st = msg
            except socket.error:
                break
            except KeyboardInterrupt:
                break

    def get_emotion(self):
        return self.cur_st


def start():
    factor = [1] * 3
    position = [0] * 3
    pos_rng = 5
    cur_st = "Surprised"
    emotrack = EmotionTracker()
    thread = threading.Thread(target=emotrack.start_server)
    thread.daemon = True
    thread.start()
    while True:
        try:
            cur_st = emotrack.get_emotion()
            factor = [1*states[cur_st][1]] * 3
            for i, st_pos in enumerate(states[cur_st][0]):
                if factor[i] > 0 and position[i] >= st_pos + pos_rng:
                    factor[i] = -factor[i]
                elif factor[i] < 0 and position[i] <= st_pos - pos_rng:
                    factor[i] = -factor[i]
                position[i] += factor[i]
            move_servos(position)
        except socket.error:
            break
        except KeyboardInterrupt:
            break


if __name__ == "__main__":
    start()
