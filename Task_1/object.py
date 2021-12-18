# import packages
import imutil as imutil
import numpy as np
import argparse
import cv2

# construct the argument parse and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-c", "--confidence", type=float, default=0.2,
                help="minimum probability to filter weak detections")
args = vars(ap.parse_args())
for i in range(1, 7):
    img = "images/image"+str(i)+".jpg"
    # initialize the list of class labels MobileNet SSD was trained to
    # detect, then generate a set of bounding box colors for each class
    CLASSES = ["background", "aeroplane", "bicycle", "bird", "boat",
               "bottle", "bus", "car", "cat", "chair", "cow", "diningtable",
               "dog", "horse", "motorbike", "person", "pottedplant", "sheep",
               "sofa", "train", "tvmonitor","house"]
    COLORS = np.random.uniform(0, 255, size=(len(CLASSES), 3))

    # loading serialized model from disk
    print("[INFO] loading model...")
    net = cv2.dnn.readNetFromCaffe("L:\Spark foundation\Object-detection-in-python-using-opencv2-main\Task_1\MobileNetSSD_deploy.prototxt.txt",
                                   "L:\Spark foundation\Object-detection-in-python-using-opencv2-main\Task_1\MobileNetSSD_deploy.caffemodel")

    # load the input image and construct an input blob for the image and resizing to a fixed 300x300 pixels and then normalizing it
    image = cv2.imread(img)
    image=cv2.resize(image,(1000,600))
    (h, w) = image.shape[:2]
    blob = cv2.dnn.blobFromImage(cv2.resize(
        image, (300, 300)), 0.007843, (300, 300), 127.5)

    # pass the blob through the network and obtain the detections and predictions
    print("[INFO] computing object detections...")
    net.setInput(blob)
    detections = net.forward()

    # loop over the detections
    for i in np.arange(0, detections.shape[2]):
        # extract the confidence (i.e., probability) associated with the prediction
        confidence = detections[0, 0, i, 2]

        # filter out weak detections by ensuring the `confidence` is
        # greater than the minimum confidence
        if confidence > args["confidence"]:
            # extract the index of the class label from the `detections`,
            # then compute the (x, y)-coordinates of the bounding box for
            # the object
            idx = int(detections[0, 0, i, 1])
            box = detections[0, 0, i, 3:7] * np.array([w, h, w, h])
            (startX, startY, endX, endY) = box.astype("int")

            # display the prediction
            label = "{}: {:.2f}%".format(CLASSES[idx], confidence * 100)
            print("[INFO] {}".format(label))
            cv2.rectangle(image, (startX, startY),
                          (endX, endY), COLORS[idx], 2)
            y = startY - 15 if startY - 15 > 15 else startY + 15
            cv2.putText(image, label, (startX, y),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, COLORS[idx], 2)

    # show the output image
    cv2.imshow("Output", image)
    cv2.waitKey(5000)
    # Destroying present windows on screen
    cv2.destroyAllWindows()
