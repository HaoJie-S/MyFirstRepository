import re


def extract_log_lines(log_file_path, patterns=None, output_file=None):
    """
    提取日志文件中符合多个正则表达式模式的行，并输出到控制台或文件。

    :param log_file_path: 日志文件的路径
    :param patterns: 匹配的正则表达式列表（默认匹配以 [1033 开头的行）
    :param output_file: 输出文件路径（若不指定则输出到控制台）
    """
    # 设置默认的正则表达式模式（保持原功能）
    if patterns is None:
        patterns = [r'^\[1033']

    # 编译正则表达式列表
    compiled_patterns = [re.compile(p) for p in patterns]

    try:
        with open(log_file_path, 'r', encoding='utf-8') as infile:
            if output_file:
                # 将结果写入文件
                with open(output_file, 'w', encoding='utf-8') as outfile:
                    for line in infile:
                        for pattern in compiled_patterns:
                            if pattern.match(line):
                                # 写入处理后的行（保留换行符）
                                outfile.write(line)
                                break  # 匹配成功后跳出循环
            else:
                # 直接输出到控制台
                for line in infile:
                    for pattern in compiled_patterns:
                        if pattern.match(line):
                            print(line.strip())
                            break  # 匹配成功后跳出循环
    except FileNotFoundError as e:
        print(f"文件未找到: {e.filename}")
    except PermissionError as e:
        print(f"权限错误: {e.filename}")
    except Exception as e:
        print(f"发生错误: {str(e)}")


if __name__ == "__main__":
    log_file_path = 'in.txt'
    # log_file_path = 'kuawang.txt'


    # 示例1：输出到控制台（保持原功能）
    # extract_log_lines(log_file_path)

    # 示例2：自定义正则并保存到文件

    patterns = [
    # r'^\[1005',  # 匹配以 [1005 开头的行
    # r'^\[1033',  # 匹配以 [1033 开头的行
    # r'^\[1124:0',  # 匹配以 [1033 开头的行
    r'^C16'  # 匹配以 C10 开头后的行
    # '.*msgid:1006',  # 匹配以 1006 的行
    ]

    output_path = log_file_path + ".out"  # 输出文件路径
    extract_log_lines(log_file_path, patterns, output_path)
