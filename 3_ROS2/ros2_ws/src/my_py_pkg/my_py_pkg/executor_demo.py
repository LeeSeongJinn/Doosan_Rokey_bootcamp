import rclpy
from rclpy.node import Node
from rclpy.executors import MultiThreadedExecutor, ExternalShutdownException
from rclpy.callback_groups import MutuallyExclusiveCallbackGroup, ReentrantCallbackGroup
import time

# 설정에 따라 실행 방식을 바꿀 수 있는 플래그
USE_MULTI = True     # True면 MultiThreadedExecutor 사용, False면 단일 스레드
SPLITGROUP = True     # True면 서로 다른 콜백 그룹으로 분리

class ExecutorDemo(Node):
    def __init__(self):
        super().__init__("executor_demo")
        self.n = 0
        
        # SPLITGROUP이 True일 때만 slow_cb를 별도의 MutuallyExclusiveCallbackGroup으로 할당
        slow_group = MutuallyExclusiveCallbackGroup() if SPLITGROUP else None
        
        # 타이머 생성 (fast_cb는 0.5초 주기, slow_cb는 2.0초 주기)
        self.create_timer(0.5, self.fast_cb)
        self.create_timer(2.0, self.slow_cb, callback_group=slow_group)

    def fast_cb(self):
        self.get_logger().info(f"fast_cb: {self.n}")
        self.n += 1

    def slow_cb(self):
        self.get_logger().error(f"slow_cb 시작: {self.n}")
        time.sleep(2)  # 2초 동안 블로킹 발생
        self.get_logger().error(f"slow_cb 끝: {self.n}")
        self.n += 1

def main():
    rclpy.init()
    node = ExecutorDemo()
    
    try:
        # USE_MULTI가 True이면 멀티스레드 Executor 사용
        if USE_MULTI:
            # 멀티스레드 실행기 생성 (기본 CPU 코어 수만큼 스레드 할당)
            executor = MultiThreadedExecutor()
            executor.add_node(node)
            executor.spin()
        else:
            # 기본 싱글스레드 스핀
            rclpy.spin(node)
            
    except (KeyboardInterrupt, ExternalShutdownException):
        pass
    finally:
        node.destroy_node()
        rclpy.try_shutdown()

if __name__ == '__main__':
    main()