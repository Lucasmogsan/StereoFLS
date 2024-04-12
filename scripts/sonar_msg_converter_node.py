#!/usr/bin/env python

import rospy
from sensor_msgs.msg import Image, CompressedImage

import cv2

from stereo_sonar.msg import OculusPing


class SonarMsgConverter:
    
    def __init__(self):
        # Define sensor name
        sensor_name_1 = '/oculus_m750d'
        sensor_name_2 = '/blueview_p900'

        # PUBLISHER - publish to topic: /sonar_new
        pub_topic_name_1 = sensor_name_1 + '/sonar_new'
        self.pub1 = rospy.Publisher(pub_topic_name_1, OculusPing, queue_size=10)

        pub_topic_name_2 = sensor_name_2 + '/sonar_new'
        self.pub2 = rospy.Publisher(pub_topic_name_2, OculusPing, queue_size=10)

        # SUBSCRIBER - subscribe to topic: /blueview_p900/sonar_image OR /oculus_m750d/sonar_image
        sub_topic_name_1 = sensor_name_1 + '/sonar_image'
        self.sub1 = rospy.Subscriber(sub_topic_name_1, Image, self.callback_1)

        sub_topic_name_2 = sensor_name_2 + '/sonar_image'
        self.sub2 = rospy.Subscriber(sub_topic_name_2, Image, self.callback_2)

    def make_sonar_msg(self, data):
        shape = (data.height, data.width)
        rospy.loginfo(rospy.get_caller_id() + "I got image with shape %s", shape)

        # Convert the image to a compressed image
        img = data.data
        # convert the image to a compressed format
        #encode_param = [int(cv2.IMWRITE_JPEG_QUALITY), 90]
        #compressed_img, encimg = cv2.imencode('.jpg', img, encode_param)
        format = "jpeg"
        # Populate the compressed image message
        ping_img = CompressedImage()
        ping_img.format = format
        ping_img.data = img

        # Populate the sonar message
        sonar_msg = OculusPing()  # Create an instance of SonarMsg
        sonar_msg.header.stamp = rospy.Time.now()
        sonar_msg.header.frame_id = "sonar"
        sonar_msg.ping = ping_img

        return sonar_msg

    # Callback function for the subscriber
    def callback_1(self, data):
        sonar_msg = self.make_sonar_msg(data)
        self.pub1.publish(sonar_msg)  # Publish the sonar message
    
    def callback_2(self, data):
        sonar_msg = self.make_sonar_msg(data)
        self.pub2.publish(sonar_msg)  # Publish the sonar message


def main():
    rospy.init_node('sonar_msg_converter', anonymous=True)
    rospy.loginfo("sonar_msg_converter node started")

    SonarMsgConverter()

    try:
        # spin() simply keeps python from exiting until this node is stopped
        rospy.spin()
    except KeyboardInterrupt:
        print("Shutting down")


if __name__ == '__main__':
    main()