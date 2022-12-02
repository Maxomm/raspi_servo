import socket
import time
import random
from adafruit_servokit import ServoKit

PORT = 12345
# LOCAL
HOST = "192.168.1.1"
# HOST = "127.0.0.1"

STEPS = 10

kit = ServoKit(channels=16)


s_list = [
    [kit.servo[10], kit.servo[11]],
    [kit.servo[13], kit.servo[12]],
    [kit.servo[15], kit.servo[14]],
]


states = {
    "Neutral": [[20, 20, 20],10],
    "Angry": [[110, 60, 0],1],
    "Sad": [[110, 110, 110],15],
    "Surprised": [[0, 0, 0],1],
    "Disgusted": [[0, 60, 110],7],
    "Happy": [[60, 60, 60],10],
    "Fearful": [[60, 30, 60],7],
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


def clamp_value(angle):
    return 0 if angle < 0 else 120 if angle > 120 else angle


def upper(x):
    return x+5

def downer(x):
    return x-5


def groove(input_values):
    goal, STEPS = input_values
    move_servos_slow([list(map(upper,goal)),9])
    
    move_servos_slow([list(map(downer,goal)),9])
    

def move_servos_slow(input_values):
    goal, STEPS = input_values
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
                current_angle = clamp_value(current_angle)
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
            else:
                groove(states[msg])

        except socket.error:
            break
        except KeyboardInterrupt:
            break


if __name__ == "__main__":
    # start()
    print(map(upper,[1,1,1]))
    #for state in states:
    #    print(state, states[state][1])
    #    move_servos_slow(states[state])
    current_state = "Happy"
    while True:
        rnd_v = random.randrange(0,5)
        print(rnd_v)
        groove(states[current_state])
        if rnd_v == 3:
            rnd_st = random.choice(list(states))
            move_servos_slow(states[rnd_st])
            current_state = rnd_st

