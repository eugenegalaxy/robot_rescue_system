from pydarknet import Detector, Image
import cv2
import pyrealsense2 as rs
import numpy as np


# cfg_path = 'hex-train-cfgV1.cfg'
# weights_path = 'yolov3-trainv1_16000.weights'
# dataFile_path = 'obj.data'

### Run original yoloV3 
cfg_path = 'yolov3.cfg'
weights_path = 'yolov3.weights'
dataFile_path = 'testv1.data'
# StartImage_path = 'dog.jpg'


def initCameraStreamRS():
    p = rs.pipeline()
    config = rs.config()
    config.enable_stream(rs.stream.depth, 640, 480, rs.format.z16, 30)
    config.enable_stream(rs.stream.color, 640, 480, rs.format.bgr8, 30)
    profile = p.start(config)
    depth_sensor = profile.get_device().first_depth_sensor()
    # depth_sensor.set_option(rs.option.depth_units, 0.01)
    depth_scale = depth_sensor.get_depth_scale()
    return p, depth_scale

def LogFile(data_input1,data_input2,data_input3):
    file1 = open("log.txt","a")#append mode 
    file1.writelines(data_input1 + '-')
    file1.writelines(data_input2 + '-')
    file1.writelines(data_input3 + '\n')   
    file1.close() 



def ObjectDetection():
    net = Detector(bytes(cfg_path, encoding="utf-8"), bytes(weights_path, encoding="utf-8"), 0, bytes(dataFile_path,encoding="utf-8"))
    pipeline, depth_scale = initCameraStreamRS()
    try: 
        while True:
            frames = pipeline.wait_for_frames()
            color_frame = frames.get_color_frame()
            depth_frame = frames.get_depth_frame()
            depth_intrin = depth_frame.profile.as_video_stream_profile().intrinsics
            color_image = np.asanyarray(color_frame.get_data())
            img_darknet = Image(color_image)
            img = color_image
            results = net.detect(img_darknet)
            for cat, score, bounds in results:
                x, y, w, h = bounds
                cv2.rectangle(img, (int(x - w / 2), int(y - h / 2)), (int(x + w / 2), int(y + h / 2)), (255, 0, 0), thickness=2)
                cv2.putText(img,str(cat.decode("utf-8")),(int(x),int(y)),cv2.FONT_HERSHEY_COMPLEX,1,(255,255,0))
                #d = rs.rs2_deproject_pixel_to_point(depth_intrin, [x,y], depth_scale)
                x1 = int(x)
                y1 = int(y)
                depthPoint = depth_frame.get_distance(x1, y1)
                print("test->", depthPoint)
                d = rs.rs2_deproject_pixel_to_point(depth_intrin, [x,y], depthPoint)
                print("VectorD: ",d)
                dis = np.linalg.norm(d)
                print("Distance in meters:",dis)
                print("Detected: ", str(cat.decode("utf-8")), " Score:", score)
                LogFile(str(cat.decode("utf-8")),str(d),str(dis))
            cv2.imshow("output", img)
            cv2.waitKey(1)
    except KeyboardInterrupt:
        print("Detection terminated!!")
        pipeline.stop()

def main():
    ObjectDetection()

if __name__ == "__main__":
    main()