from djitellopy import Tello

tello = Tello()

tello.connect()
tello.takeoff()
tello.land()

if(tello.takeoff()):
    print("It's flying")