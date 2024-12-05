from dynamic_leds.dynamic_leds import init


cam = init.init_local_camera()
cam.save_photo('test.jpg')

cam.release()