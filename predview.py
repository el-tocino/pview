import array
import picamera
import time
import numpy
import uuid
import melopero_amg8833 as mp
import matplotlib.pyplot as plt

cam = picamera.PiCamera(resolution=(1280, 720), framerate=30)
cam.color_effects = (128,128)
cam.start_preview()
sensor = mp.AMGGridEye()
sensor.set_fps_mode(mp.AMGGridEye.FPS_10_MODE)
time.sleep(.5)

def mapper(thefn):
    fig = plt.figure(frameon=False)
    ax = fig.add_axes([0, 0, 1, 1])
    ax.axis('off')
    grid = sensor.get_pixel_temperature_matrix()
    boondoggle = []
    for hrow in grid:
        boondoggle.append(hrow)       
    colorarray = numpy.array(boondoggle)
    fig.imshow(colorarray, cmap='plasma')
    savefn = thefn + ".png"
    fig.savefig(savefn,  transparent=True)

while(True):
    newfn = uuid.uuid5
    sensor.update_pixel_temperature_matrix()
    camfn = newfn + ".png"
    mapper(newfn)
    img = Image.open(camfn)
    pad = Image.new('RGB', (
        ((img.size[0] + 31) // 32) * 32,
        ((img.size[1] + 15) // 16) * 16,
        ))
    pad.paste(img, (0, 0))
    o = cam.add_overlay(pad.tostring(), size=img.size)
    o.alpha = 128
    o.layer = 3        
    time.sleep(0.1)
