import cv2
import threading
import logging
from flask import Flask , Response

app = Flask(__name__)

class VideoStreamer:
    def __init__(self):
        self.camera = cv2.VideoCapture(0)
        self.running = True
        
    def generate_frames(self):
        """Continuously capture frames and yield as MJPEG stream."""
        while self.running:
            success, frame = self.camera.read()
            if not success:
                break
            _, buffer = cv2.imencode('.jpg', frame)
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + buffer.tobytes() + b'\r\n')
            
    def stop(self):
        self.running = False
        self.camera.release()


streamer = VideoStreamer()

@app.route("/video")
def video_feed():
    return Response(streamer.generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001, debug=False, threaded=True)