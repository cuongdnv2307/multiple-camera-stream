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


def write_video(camera_id):
    # Create an object to read
    # from camera
    cam = find_camera(camera_id)
    video = cv2.VideoCapture(cam)

    # We need to check if camera
    # is opened previously or not
    if (video.isOpened() == False):
        print("Error reading video file")

    # We need to set resolutions.
    # so, convert them from float to integer.
    frame_width = int(video.get(3))
    frame_height = int(video.get(4))

    size = (frame_width, frame_height)

    # Below VideoWriter object will create
    # a frame of above defined The output
    # is stored in 'filename.avi' file.
    result = cv2.VideoWriter('filename.avi',
                            cv2.VideoWriter_fourcc(*'MJPG'),
                            10, size)
        
    while(True):
        ret, frame = video.read()

        if ret == True:

            # Write the frame into the
            # file 'filename.avi'
            result.write(frame)

            # Display the frame
            # saved in the file
            cv2.imshow('Frame', frame)

            # Press S on keyboard
            # to stop the process
            if cv2.waitKey(1) & 0xFF == ord('s'):
                break

        # Break the loop
        else:
            break

    # When everything done, release
    # the video capture and video
    # write objects
    video.release()
    result.release()
        
    # Closes all the frames
    cv2.destroyAllWindows()

    print("The video was successfully saved")
 


@app.route('/video_feed/<string:id>/', methods=["GET"])
def video_feed(id):
    print(id)
    """Video streaming route. Put this in the src attribute of an img tag."""
    # return('Query String Example')
    return Response(gen_frames(id),
                    mimetype='multipart/x-mixed-replace; boundary=frame')
@app.route('/write_video/<string:id>/', methods=["GET"])
def write_feed(id):
    write_video(id)
    return Response('Query String Example')    


@app.route('/', methods=["GET"])
def index():
    return render_template('index.html')


if __name__ == '__main__':
    app.run()
