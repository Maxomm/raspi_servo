import socket
import time

# from adafruit_servokit import ServoKit

PORT = 12345
HOST = "127.0.0.1"
STEPS = 10
# kit = ServoKit(channels=16)

"""
s_list = [
    [kit.servo[10], kit.servo[11]],
    [kit.servo[12], kit.servo[13]],
    [kit.servo[15], kit.servo[14]],
]
"""
s_list = [[0, 0], [0, 0], [0, 0]]

states = {
    "Neutral": [60, 60, 60],
    "Angry": [0, 60, 110],
    "Sad": [110, 110, 110],
    "Surprised": [0, 0, 0],
    "Disgusted": [110, 60, 0],
    "Happy": [10, 50, 100],
    "Fearful": [0, 30, 60],
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


def move_servos_slow(goal):
    range_list = [0, 0, 0]
    factor_list = [0, 0, 0]
    for i in range(3):
        range_list[i] = goal[i] - s_list[i][0]
        if range_list[i] != 0:
            factor_list[i] = STEPS / abs(range_list[i])
        else:
            factor_list[i] = 0

    for _ in range(STEPS):
        for i in range(3):
            if factor_list[i] != 0:
                s_list[i][0] += mysign(range_list[i]) / factor_list[i]
                s_list[i][1] = reverse(s_list[i][0])
        print(s_list)
        time.sleep(0.1)


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
