from asyncio.windows_events import NULL
from flask import Flask, render_template, Response
import cv2
import logging

app = Flask(__name__)

def find_camera(id):
    cameras = ['rtsp://wowzaec2demo.streamlock.net/vod/mp4:BigBuckBunny_115k.mp4','rtsp://wowzaec2demo.streamlock.net/vod/mp4:BigBuckBunny_115k.mp4',
    'rtsp://wowzaec2demo.streamlock.net/vod/mp4:BigBuckBunny_115k.mp4','rtsp://wowzaec2demo.streamlock.net/vod/mp4:BigBuckBunny_115k.mp4',
    'rtsp://wowzaec2demo.streamlock.net/vod/mp4:BigBuckBunny_115k.mp4','rtsp://wowzaec2demo.streamlock.net/vod/mp4:BigBuckBunny_115k.mp4'
    ,'rtsp://wowzaec2demo.streamlock.net/vod/mp4:BigBuckBunny_115k.mp4','rtsp://wowzaec2demo.streamlock.net/vod/mp4:BigBuckBunny_115k.mp4'
     ,'rtsp://wowzaec2demo.streamlock.net/vod/mp4:BigBuckBunny_115k.mp4','rtsp://wowzaec2demo.streamlock.net/vod/mp4:BigBuckBunny_115k.mp4'
      ,'rtsp://wowzaec2demo.streamlock.net/vod/mp4:BigBuckBunny_115k.mp4','rtsp://wowzaec2demo.streamlock.net/vod/mp4:BigBuckBunny_115k.mp4'
       ,'rtsp://wowzaec2demo.streamlock.net/vod/mp4:BigBuckBunny_115k.mp4','rtsp://wowzaec2demo.streamlock.net/vod/mp4:BigBuckBunny_115k.mp4']
    return cameras[int(id)]
#  for cctv camera use rtsp://username:password@ip_address:554/user=username_password='password'_channel=channel_number_stream=0.sdp' instead of camera
#  for webcam use zero(0)
 

def gen_frames(camera_id):
     
    cam = find_camera(camera_id)
    logging.info('Cam',cam)
    cap=  cv2.VideoCapture(cam)
    
    while True:
        # for cap in caps:
        # # Capture frame-by-frame
        cap.set(3, 144)
        cap.set(4, 120)
        success, frame = cap.read()  # read the camera frame
        if not success:
            break
        else:
            ret, buffer = cv2.imencode('.jpg', frame)
            frame = buffer.tobytes()
            yield (b'--frame\r\n'
                b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')  # concat frame one by one and show result


@app.route('/video_feed/<string:id>/', methods=["GET"])
def video_feed(id):
    print(id)
    """Video streaming route. Put this in the src attribute of an img tag."""
    # return('Query String Example')
    return Response(gen_frames(id),
                    mimetype='multipart/x-mixed-replace; boundary=frame')


@app.route('/', methods=["GET"])
def index():
    return render_template('index.html')


if __name__ == '__main__':
    app.run()
