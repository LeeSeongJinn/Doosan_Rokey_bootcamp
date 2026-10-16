# topic을 통해서 랜덤 숫자 두개를 송출

import rclpy

from rclpy.node import Node

from my_interfaces.msg import ArithmeticArgument

from rcl_interfaces.msg import SetParametersResult

import random

import time

class Argument(Node):

    def __init__(self):

        super().__init__("argument")

        # min, max 설정 -> 랜덤 값을 추출

        self.declare_parameter("min_random_num",1)

        self.declare_parameter("max_random_num",9)

        self.min_random_num=self.get_parameter("min_random_num").value

        self.max_random_num=self.get_parameter("max_random_num").value

        # timer 1초 마다

        # 콜백 -> 두 개의 숫자를 추출 -> pub

        self.create_timer(1.0, self.on_timer)

        self.pub = self.create_publisher(ArithmeticArgument, "arithmetic_argument", 10)

        self.add_on_set_parameters_callback(self.on_set)

    def on_timer(self): # 2개 숫자 만들기(random), msg 만들기, pub, logger

        msg = ArithmeticArgument()

        self.min_random_num=self.get_parameter("min_random_num").value

        self.max_random_num=self.get_parameter("max_random_num").value

        msg.argument_a = float(random.randint(self.min_random_num,self.max_random_num))

        msg.argument_b = float(random.randint(self.min_random_num,self.max_random_num))

        self.pub.publish(msg)

        self.get_logger().info(f"발행 : a={msg.argument_a}, b={msg.argument_b}")

    def on_set(self, params): # paramsetting cli : ros2 param set /argument max_random_num 19

        # 최대 최소 값이 서로 안맞는 부분 검증

        low, high = self.min_random_num, self.max_random_num

        for p in params:

            if p.name == "min_random_num" and p.value > high:

                return SetParametersResult(successful=False, reason = "잘못된 값")

            elif p.name == "max_random_num" and p.value < low:

                return SetParametersResult(successful=False, reason = "잘못된 값")

        return SetParametersResult(successful=True)



def main():

    rclpy.init()

    node = Argument()

    try:

        rclpy.spin(node)

    except Exception:

        pass

    finally:

        node.destroy_node()

        rclpy.try_shutdown()



if __name__=="__main__":

    main()

