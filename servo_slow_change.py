import socket
import time
from adafruit_servokit import ServoKit

PORT = 12345
# LOCAL
HOST = "192.168.1.1"
# HOST = "127.0.0.1"
STEPS = 5
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
    if x >= 0:
        return 1
    return -1


def move_servo(pos):
    print(f"moving motors to {pos}")
    for index, s_pair in enumerate(s_list):
        s_pair[0] = pos[index]
        s_pair[1] = reverse(pos[index])


def correct_value(angle):
    return 0 if angle < 0 else 120 if angle > 120 else angle


def move_servos_slow(goal):
    range_list = [0, 0, 0]
    factor_list = [0, 0, 0]
    for i in range(3):
        range_list[i] = goal[i] - s_list[i][0].angle
        if range_list[i] != 0:
            factor_list[i] = STEPS / abs(range_list[i])
        else:
            factor_list[i] = 0

    for _ in range(STEPS):
        for i in range(3):
            if factor_list[i] != 0:
                current_angle = int(s_list[i][0].angle)
                current_angle += mysign(range_list[i]) / factor_list[i]
                current_angle = correct_value(current_angle)
                s_list[i][0].angle = current_angle
                s_list[i][1].angle = reverse(current_angle)
        # print(s_list)
        time.sleep(0.05)


def start():
    last_emo = "Nothing"
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.connect((HOST, PORT))
    while True:
        try:
            msg = server.recv(64).decode("utf-8")
            print(f"Emotion received: {msg}")
            if msg != last_emo:
                if msg in states:
                    move_servos_slow(states[msg])
                    last_emo = msg

        except socket.error:
            break
        except KeyboardInterrupt:
            break


if __name__ == "__main__":
    start()
    

