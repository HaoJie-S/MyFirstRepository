import socket
import base64
import time
import logging
from threading import Thread, Event

# 设置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("ntrip_client.log"),
        logging.StreamHandler()
    ]
)


class NTRIPClient:
    def __init__(self, host, port, mountpoint, username, password):
        self.host = host
        self.port = port
        self.mountpoint = mountpoint
        self.username = username
        self.password = password
        self.socket = None
        self.is_connected = False
        self.stop_event = Event()

    def connect(self):
        """连接到NTRIP Caster服务器"""
        try:
            # 创建socket连接
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.socket.settimeout(10)  # 设置连接超时
            self.socket.connect((self.host, self.port))
            logging.info(f"已连接到NTRIP Caster: {self.host}:{self.port}")

            # 准备认证信息
            auth_str = f"{self.username}:{self.password}"
            auth_b64 = base64.b64encode(auth_str.encode()).decode()

            # 构建NTRIP请求
            request = (
                f"SOURCE {self.password} /{self.mountpoint}\r\n"
                f"\r\n"
            )

            # 发送认证请求
            self.socket.sendall(request.encode())
            logging.info("NTRIP认证请求已发送")

            # 接收服务器响应
            response = self.socket.recv(1024).decode()
            logging.info(f"服务器响应: {response.strip()}")

            # 检查响应是否成功
            if "ICY 200 OK" in response or "OK" in response:
                self.is_connected = True
                logging.info("NTRIP认证成功")
                return True
            else:
                logging.error("NTRIP认证失败")
                self.disconnect()
                return False

        except Exception as e:
            logging.error(f"连接NTRIP Caster失败: {str(e)}")
            self.disconnect()
            return False

    def send_data(self, data):
        """发送数据到NTRIP Caster"""
        if not self.is_connected:
            logging.error("未连接到NTRIP Caster，无法发送数据")
            return False

        try:
            self.socket.sendall(data.encode())
            return True
        except Exception as e:
            logging.error(f"发送数据失败: {str(e)}")
            self.is_connected = False
            return False

    def disconnect(self):
        """断开连接"""
        if self.socket:
            try:
                self.socket.close()
            except:
                pass
            self.socket = None
        self.is_connected = False
        logging.info("已断开与NTRIP Caster的连接")

    def start_data_stream(self, data_generator, interval=1):
        """启动数据流推送"""
        if not self.is_connected:
            logging.error("未连接到NTRIP Caster，无法启动数据流")
            return

        logging.info(f"开始推送数据，间隔: {interval}秒")

        def stream_data():
            while not self.stop_event.is_set() and self.is_connected:
                try:
                    # 从生成器获取数据
                    data = next(data_generator)

                    # 发送数据
                    if self.send_data(data):
                        logging.info(f"已发送数据: {data.strip()}")
                    else:
                        break

                    # 等待指定间隔
                    time.sleep(interval)

                except StopIteration:
                    logging.info("数据生成器已结束")
                    break
                except Exception as e:
                    logging.error(f"数据流错误: {str(e)}")
                    break

        # 启动数据流线程
        self.stream_thread = Thread(target=stream_data)
        self.stream_thread.daemon = True
        self.stream_thread.start()

    def stop_data_stream(self):
        """停止数据流推送"""
        self.stop_event.set()
        if hasattr(self, 'stream_thread'):
            self.stream_thread.join(timeout=5)
        logging.info("数据流已停止")


def generate_nmea_data():
    """生成NMEA数据示例"""
    base_time = time.time()
    nmea_template = "$GNGGA,{time},3035.8200,N,11419.5600,E,1,12,0.8,45.6,M,-25.3,M,,*65"

    count = 0
    while True:
        # 更新时间
        current_time = time.strftime("%H%M%S", time.gmtime(base_time + count))

        # 生成NMEA语句
        nmea_data = nmea_template.format(time=current_time)

        # 添加校验和（简化处理）
        checksum = 0
        for char in nmea_data[1:]:
            checksum ^= ord(char)
        nmea_data = f"{nmea_data}{checksum:02X}\r\n"

        yield nmea_data
        count += 1


def main():
    # NTRIP Caster配置
    HOST = "58.49.94.131"  # NTRIP Caster服务器地址
    PORT = 18336  # NTRIP Caster端口，默认2101
    MOUNTPOINT = "0000"  # 挂载点名称
    USERNAME = "0000"  # 用户名
    PASSWORD = "123"  # 密码

    # 创建NTRIP客户端
    client = NTRIPClient(HOST, PORT, MOUNTPOINT, USERNAME, PASSWORD)

    try:
        # 连接到NTRIP Caster
        if client.connect():
            # 创建数据生成器
            data_generator = generate_nmea_data()

            # 启动数据流，每秒发送一条数据
            client.start_data_stream(data_generator, interval=1)

            # 运行一段时间（例如60秒）
            time.sleep(60)

            # 停止数据流
            client.stop_data_stream()

    except KeyboardInterrupt:
        logging.info("用户中断程序")
    except Exception as e:
        logging.error(f"程序执行错误: {str(e)}")
    finally:
        # 断开连接
        client.disconnect()


if __name__ == "__main__":
    main()