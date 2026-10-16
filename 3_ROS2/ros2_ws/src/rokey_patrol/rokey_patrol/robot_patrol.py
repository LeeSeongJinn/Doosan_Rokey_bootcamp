import rclpy
from rclpy.node import Node
from rclpy.action import ActionServer
from my_interfaces.action import PatrolAction
from std_msgs.msg import Float64
from std_srvs.srv import Trigger
import time
from rclpy.callback_groups import ReentrantCallbackGroup, MutuallyExclusiveCallbackGroup
from rclpy.executors import MultiThreadedExecutor
# 구조->액션콜백 작성/zone, map
class RobotPatrol(Node):
    def __init__(self):
        super().__init__("robot_patrol")
        self.zone = {"a":[1,1,2,2], "b":[2,1,2,1,2]}
        self.declare_parameter("limit", 50.0)
        self.group = ReentrantCallbackGroup()
        self.current_temp = 0.0
        ActionServer(self, PatrolAction,"robot/patrol", self.patrol, callback_group=self.group)
        self.create_subscription(Float64,"robot/temperature",self.on_temp,10, callback_group=self.group)
        self.create_service(Trigger, 'robot/report',self.report, callback_group=self.group)

    def report(self, req, res):# 순찰 횟수, 이슈 횟수
        content=f"""
        ======순찰 보고서======
        - 전체 순환 횟수 : {self.patrol_count}
        - 전체 이슈 횟수 : {self.issue_count}
        """



    def on_temp(self, msg):
        self.current_temp = msg.data
        self.get_logger().info(f"현재 로봇 감지 온도 : {msg.data}")

    def patrol(self, goal_handle):
        # zone을 받고, 지도를 가져오고, 지도를 순찰하고, 피드백 하고, 결과 리턴
        mission_zone = goal_handle.request.zone
        patrol_map = self.zone[mission_zone]
        fb = PatrolAction.Feedback()
        limit = self.get_parameter("limit").value
        is_issue = False
        for room_num, room_importance in enumerate(patrol_map):
            time.sleep(room_importance)
            self.get_logger().info(f"{room_num+1}번째 방에서 {room_importance} 초 동안 순찰함")
            # 온도를 체크해서 기준값 이상이면 화재라고 피드백과 내용 작성해서 보고 + 그러면 상황 끝나면 어떻게 일반 상태로 변경할까        
            if self.current_temp > limit:
                is_issue = True
                fb.is_issue = True 
                fb.zone = mission_zone
                fb.report = f"{room_num+1}번째 순찰구역에서 화재 발생!!!!!"
                goal_handle.publish_feedback(fb)
            else:
                fb.is_issue = False 
                fb.zone = mission_zone
                fb.report = "no issue"
                goal_handle.publish_feedback(fb)
        goal_handle.succeed()
        result = PatrolAction.Result()
        result.is_issue = True if is_issue else False
        result.zone = mission_zone
        result.report = f"{mission_zone} 지역 순찰 완료"
        return result

# 14:35까지 센서데이터와 패트롤 로봇 연결 및 보고서 작성 고민을 해보겠습니다!


def main():
    rclpy.init()
    node = RobotPatrol()
    try:
        ex = MultiThreadedExecutor()
        ex.add_node(node)
        ex.spin()
    except Exception:
        pass
    finally:
        node.destroy_node()
        rclpy.try_shutdown()

if __name__=="__main__":
    main()

        
