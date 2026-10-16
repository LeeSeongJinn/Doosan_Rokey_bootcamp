import rclpy
from rclpy.node import Node
from std_msgs.msg import Float64
import random
class RobotSensor(Node):
    def __init__(self):
        super().__init__("robot_sensor")
        # 온도를 pub / 기준온도는 25도로 정하고, 이상온도는 50도 나오도록 동적으로 구성
        # self.threshold = 0.1        
        # self.base_temp = 25.0
        self.declare_parameter("threshold", 0.1)
        # self.threshold = self.get_parameter("threshold")
        self.declare_parameter("base_temp", 25.0)
        self.pub = self.create_publisher(Float64,"robot/temperature",10)
        self.create_timer(1, self.measure)
        self.get_logger().info("SensorNode 준비완료")
    def measure(self):
        # msg 만들고 pub하기
        msg = Float64()
        threshold = self.get_parameter("threshold").value
        base_temp = self.get_parameter("base_temp").value
        # 임의의 온도 생성
        if random.random() < threshold:
            temp = random.uniform(50,60)
        else:
            temp = base_temp + random.uniform(-1,1)
        msg.data = temp
        self.pub.publish(msg)
        self.get_logger().info(f"현재 온도 : {temp}")

def main():
    rclpy.init()
    node = RobotSensor()
    try:
        rclpy.spin(node)
    except Exception:
        pass
    finally:
        node.destroy_node()
        rclpy.try_shutdown()

if __name__=="__main__":
    main()

        
