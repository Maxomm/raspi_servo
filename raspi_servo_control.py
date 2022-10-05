import time
import socket

from adafruit_servokit import ServoKit
kit = ServoKit(channels=16)

def reverse(degree):
    return 180 - degree

s_list = [[kit.servo[10], kit.servo[11]],[kit.servo[12], kit.servo[13]],[kit.servo[15],kit.servo[14]]]
last_angle = 0
new_angle = 0
happy_state = [0,60,120]
neutral_state = [0,0,0]
states = {"Neutral": [60,60,60],"Angry": [0,60,110], "Sad": [110, 110,110], "Surprised": [0,0,0], "Disgusted": [110,60,0], "Happy": [10,50,100], "Fearful": [0,30,60]}


PORT = 12345
HOST = "192.168.0.183"

def mysign(x):
    if x >= 0: 
        return 1
    else:
        return -1

def lerp_pos(start):
    global last_angle
    new_angle = start[0]
    dif = new_angle - last_angle
    for i in range(abs(dif)):
        last_angle += 10*mysign(dif)                
        move_servo([last_angle,last_angle,last_angle])
        time.sleep(0.1)

def move_servo(pos):
    print(f"moving motors to {pos}")
    for i in range(len(s_list)):
        s_list[i][0].angle = pos[i]
        s_list[i][1].angle = reverse(pos[i])
            
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
                #lerp_pos(states[msg])
                    last_emo = msg
        
        except socket.error:
            break
        except KeyboardInterrupt:
            break
        
if __name__ == "__main__":
    #move_servo([0,0,0])
    #for i in range(len(s_list)):
    #    for u in range(len(s_list[i])):
    #        print(s_list[i][u].angle)
    #start()
    move_servo(states["Happy"])
    #while True:
    #    move_servo(states["Happy"])
    #    time.sleep(1)
    #    move_servo(states["Angry"])
    #    time.sleep(1)
    #print(states["Happy"])

    #goal_degree = 10
    #current_degree = 90
    #while True:
    #    for i in state_list:
    #        move_servo(i)
    #        time.sleep(1)
        #move_servo([current_degree,current_degree])
        #for i in range(goal_degree):
        #    move_servo([current_degree + i, current_degree + i])
        #    time.sleep(0.3)
            