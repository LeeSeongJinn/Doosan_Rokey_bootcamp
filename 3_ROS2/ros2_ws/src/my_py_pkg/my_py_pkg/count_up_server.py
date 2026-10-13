import rclpy
from rclpy.node import Node
from rclpy.action import ActionServer
from rclpy.executors import ExternalShutdownException
from my_interface.action import CountUp
import time

class CountUpServer(Node):
    def __init__(self):
        super().__init__("count_up_server")
        ActionServer(self, CountUp, "count_up",self.execute)
        self.get_logger().info("CountUp Server 가동 중")
    #cf.service_callback(self,req,res)
    #cf.subscribtion(self,msg)
    def execute(self, goal_handler): #goal 확인-> 동작 수행(피드백)-> 완료(응답)
        target=goal_handler.request.target
        seq=[]
        fb=CountUp.Feedback()
        for i in range(1,target+1):
            seq.append(i)
            fb.current = i
            goal_handler.publish_feedback(fb)
            self.get_logger().info(f"현재 Count Num: {i}")
            time.sleep(1)
        goal_handler.succeed()
        result = CountUp.Result()
        result.sequence=seq
        return result


def main():
    rclpy.init()
    node=CountUpServer()
    try:
        rclpy.spin(node)
    except (KeyboardInterrupt,ExternalShutdownException):
        pass
    finally:
        node.destroy_node()
        rclpy.try_shutdown()

if __name__=="__main__":
    main()