import rosbag2_py
from rclpy.serialization import serialize_message
from std_msgs.msg import String

# 1) Writer 객체 생성
writer = rosbag2_py.SequentialWriter()

# 2) 저장 위치와 형식을 정해 열기
storage_options = rosbag2_py.StorageOptions(uri='code_bag', storage_id='mcap')
converter_options = rosbag2_py.ConverterOptions(
    input_serialization_format='cdr',
    output_serialization_format='cdr')
writer.open(storage_options, converter_options)

# 3) 어떤 토픽을 담을지 미리 등록
topic_info = rosbag2_py.TopicMetadata(
    id=0,
    name='/chatter',
    type='std_msgs/msg/String',
    serialization_format='cdr')
writer.create_topic(topic_info)

# 4) 메시지를 직렬화해 타임스탬프와 함께 기록
for i in range(10):
    msg = String()
    msg.data = f'hi from code {i}'
    timestamp_ns = i * 1_000_000_000          # 1초 간격(나노초 단위)
    writer.write('/chatter', serialize_message(msg), timestamp_ns)

# 5) (선택) 명시적으로 닫기 — 객체가 사라질 때 자동으로 닫히기도 함
del writer
print('녹화 완료: code_bag')