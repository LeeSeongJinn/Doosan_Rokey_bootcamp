# sub, service(operator 받아서 연산하고 결과 리턴), action( 임계값을 사용자가 전달->결과값이 임계값 될때까지 누적 -> 최대 누적값)

import rclpy

from rclpy.node import Node

from my_interfaces.msg import ArithmeticArgument

from my_interfaces.srv import ArithmeticOperator

from rclpy.action import ActionServer

from my_interfaces.action import ArithmeticChecker

import time

from rclpy.callback_groups import MutuallyExclusiveCallbackGroup, ReentrantCallbackGroup

from rclpy.executors import MultiThreadedExecutor



class Calculator(Node):

    def __init__(self):

        super().__init__("calculator")

        self.argument_a = 0.0

        self.argument_b = 0.0

        self.argument_result = 0.0

        group1 = ReentrantCallbackGroup()

        group2 = ReentrantCallbackGroup()



        self.create_subscription(ArithmeticArgument,"arithmetic_argument",self.on_argument,10)

        self.create_service(ArithmeticOperator,"arithmetic_operator", self.on_operator, callback_group=group1)

        ActionServer(self, ArithmeticChecker, "arithmetic_checker",self.on_check,callback_group=group2)

        self.get_logger().info("========= Calculator 서버 가동중 =================")





    # ros2 service call /arithmetic_operator my_interfaces/srv/ArithmeticOperator "{arithmetic_operator: 1}"

    # ros2 action send_goal /arithmetic_checker my_interfaces/action/ArithmeticChecker  "{goal_sum: 100.0}" --feedback

    def on_check(self, goal_handle):

        # goal_sum을 받고, argument_result 값을 확인해서, 누적값을 계산하며 피드백을 보내고, 최종 값을 리턴한다

        goal_sum = goal_handle.request.goal_sum

        argument_result = self.argument_result

        self.get_logger().info(f"누적값 연산 진행 : 목표 임계값 {goal_sum}")

        feedback = ArithmeticChecker.Feedback()

        total = 0.0

        while True:

            total += argument_result

            if total > goal_sum:

                total -= argument_result

                break

            feedback.current_num = total

            goal_handle.publish_feedback(feedback)

            time.sleep(1)

        goal_handle.succeed()

        result = ArithmeticChecker.Result()

        result.total_sum=total

        return result



    def on_argument(self, msg):

        self.argument_a = msg.argument_a

        self.argument_b = msg.argument_b

        self.get_logger().info(f"argument 수신 : {msg.argument_a} {msg.argument_b}")



    def on_operator(self, req, res): # operator를 받아서, 연산한다

        a, b = self.argument_a, self.argument_b

        if req.arithmetic_operator == ArithmeticOperator.Request.PLUS: # 이거 꼭 기억해야해.1은 +야!!!

            result = a + b

        res.arithmetic_result = result

        self.argument_result = result

        self.get_logger().info(f"연산 대상 숫자: {a} {b} ===== 연산 결과 : {self.argument_result} ")

        return res

            



def main():

    rclpy.init()

    node = Calculator()

    try:

        # rclpy.spin(node)

        ex = MultiThreadedExecutor()

        ex.add_node(node=node)

        ex.spin()

    except Exception:

        pass

    finally:

        node.destroy_node()

        rclpy.try_shutdown()

if __name__=="__main__":

    main()