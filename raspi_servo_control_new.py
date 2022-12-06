import socket
import time
from adafruit_servokit import ServoKit

PORT = 12345
# LOCAL
HOST = "192.168.0.183"
# HOST = "127.0.0.1"

STEPS = 10

kit = ServoKit(channels=16)


s_list = [
    [kit.servo[10], kit.servo[11]],
    [kit.servo[13], kit.servo[12]],
    [kit.servo[15], kit.servo[14]],
]


states = {
    "Neutral": [20, 20, 20],
    "Angry": [110, 60, 0],
    "Sad": [110, 110, 110],
    "Surprised": [0, 0, 0],
    "Disgusted": [0, 60, 110],
    "Happy": [60, 60, 60],
    "Fearful": [60, 30, 60],
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


def start():
    factor = [1] * 3
    position = [0] * 3
    pos_rng = 3
    cur_st = "Surprised"
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.connect((HOST, PORT))
    while True:
        try:
            msg = server.recv(64).decode("utf-8")
            print(f"Emotion received: {msg}")
            if msg in states:
                cur_st = msg
            for i in range(3):
                if factor[i] > 0 and position[i] >= states[cur_st][i] + pos_rng:
                    factor[i] = -factor[i]
                elif factor[i] < 0 and position[i] <= states[cur_st][i] - pos_rng:
                    factor[i] = -factor[i]
                position[i] += factor[i]
            move_servos(position)
        except socket.error:
            break
        except KeyboardInterrupt:
            break


if __name__ == "__main__":
    start()
