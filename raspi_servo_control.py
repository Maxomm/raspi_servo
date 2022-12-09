import socket

from adafruit_servokit import ServoKit

PORT = 12345
HOST = "192.168.0.183"

kit = ServoKit(channels=16)

s_list = [
    [kit.servo[10], kit.servo[11]],
    [kit.servo[13], kit.servo[12]],
    [kit.servo[15], kit.servo[14]],
]

states = {
    "Neutral": [60, 60, 60],
    "Angry": [110, 60, 0],
    "Sad": [110, 110, 110],
    "Surprised": [0, 0, 0],
    "Disgusted": [0, 60, 110],
    "Happy": [100, 50, 10],
    "Fearful": [0, 30, 60],
}


def reverse(degree):
    return 180 - degree


def move_servo(pos):
    print(f"moving motors to {pos}")
    for index, s_pair in enumerate(s_list):
        s_pair[0].angle = pos[index]
        s_pair[1].angle = reverse(pos[index])


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
                    move_servo(states[msg])
                    last_emo = msg

        except socket.error:
            break
        except KeyboardInterrupt:
            break


if __name__ == "__main__":
    start()
