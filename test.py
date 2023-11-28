import re
from datetime import datetime
def parse_float_value(value):
    # 使用正则表达式查找第一个浮点数
    match = re.search(r'[\d\.]+', value)
    if match:
        return float(match.group())
    else:
        raise ValueError(f"Invalid float format: {value}")
def parse_int_value(value):
    # 查找第一个整数
    match = re.search(r'\d+', value)
    if match:
        return int(match.group())
    else:
        raise ValueError(f"Invalid integer format: {value}")


def parse_value(line_no, value):
    if line_no == '2':  # 日期格式
        return datetime.strptime(value.strip(), '%d.%m.%y').date()
    elif line_no == '3':  # 时间格式
        # 提取时间部分，忽略额外内容
        time_match = re.match(r'(\d{2}:\d{2}:\d{2})', value.strip())
        if time_match:
            return datetime.strptime(time_match.group(1), '%H:%M:%S').time()
        else:
            raise ValueError(f"Invalid time format: {value}")
    elif line_no in ['4', '6', '7', '8']:  # 字符串
        return value.strip()
    elif line_no in ['21', '25', '26', '27', '272', '41', '42', '43', '44', '46', '47', '61', '62', '63', '64']:  # 双精度数值
        return parse_float_value(value)
    elif line_no in ['22']:  # 整数
        return parse_int_value(value)
    elif line_no in ['23', '24']:  # 螺旋角，度分秒格式
        match = re.match(r'(-?\d+)°(\d+)\'(\d+)"', value.strip())
        if match:
            degrees, minutes, seconds = map(int, match.groups())
            return degrees + minutes / 60 + seconds / 3600
        return float(value)
    else:
        return value.strip()

def parse_line(line):
    match = re.match(r'\s*(\d+)\s*:(.*?):\s*(.*)', line)
    if match:
        line_no, description, value = match.groups()
        return line_no, parse_value(line_no, value)
    return None

def parse_text1(text):
    data = {}
    for line in text.split('\n'):
        result = parse_line(line)
        if result:
            line_no, value = result
            # Assign to variable based on the line number
            if line_no == '2':
                data['date'] = value
            elif line_no == '3':
                data['time'] = value
            elif line_no == '4':
                data['operator'] = value
            elif line_no == '6':
                data['Drawing No'] = value
            elif line_no == '7':
                data['Order No'] = value
            elif line_no == '8':
                data['Type'] = value
            elif line_no == '21':
                data['mn'] = value
            elif line_no == '22':
                data['z'] = value
            elif line_no == '23':
                data['Beta'] = value
            elif line_no == '24':
                data['an'] = value
            elif line_no == '25':
                data['xn'] = value
            elif line_no == '26':
                data['b'] = value
            elif line_no == '27':
                data['da'] = value
            elif line_no == '272':
                data['df'] = value
            elif line_no == '41':
                data['d0'] = value
            elif line_no == '42':
                data['d1'] = value
            elif line_no == '43':
                data['d2'] = value
            elif line_no == '44':
                data['de'] = value
            elif line_no == '46':
                data['dinv'] = value
            elif line_no == '47':
                data['dLead'] = value
            elif line_no == '61':
                data['Ba'] = value
            elif line_no == '62':
                data['b1'] = value
            elif line_no == '63':
                data['b2'] = value
            elif line_no == '64':
                data['be'] = value
            # ... (and so on for other line numbers)
    return data
def read_file(file_path, encoding):
    try:
        with open(file_path, 'r', encoding=encoding) as file:
            return file.read()
    except UnicodeDecodeError as e:
        print(f"Error reading file with encoding {encoding}: {e}")
        return None

def parse_data_block(block_type, direction, text_block):
    # 初始化数组来存储数据点
    data_points = []
    # 对于每一行，提取所有浮点数
    for line in text_block:
        values = re.findall(r'-?\d+(\.\d+)?', line)
        data_points.extend(float(val) if '.' in val else int(val) for val in values)

        # 如果已经达到480个数据点，则停止
        if len(data_points) >= 480:
            break 

    return {
        'type': block_type,
        'direction': direction,
        'data': data_points
    }

def parse_text2(text):# 分三种情况进行标记和读取
    lines = text.split('\n')

    all_data_blocks = []
    current_block = []
    block_type = None
    direction = None
    lines_to_read=0


    for line in lines:
        if 'Profil:  Zahn-Nr.:' in line :
            lines_to_read=40
            continue
        if lines_to_read>0 :
            current_block.append(line)
            block_type="profil"
            direction="rechts" if 'rechts' in line else 'links'
            lines_to_read-=1

            if lines_to_read == 0:
                block_type="profil"
                direction="rechts" if 'rechts' in line else 'links'
                all_data_blocks.append(parse_data_block(block_type,direction,current_block))
                current_block = []

    return all_data_blocks

file_path = 'P:\\01-question\\30-鬼频分析软件自主开发\\03-分析数据工作\\B101.mka'#'path_to_your_file.txt'  # 替换为您的文件路径

# 尝试使用 ISO-8859-1 编码读取文件
content = read_file(file_path, 'ISO-8859-1')
# 示例文本
text =content #

# 解析文本
parsed_data1 = parse_text1(text)
parsed_data2= parse_text2(text)
# 打印结果
for key, value in parsed_data1.items():
    print(f"{key} = {value}")

for block in parsed_data2:
    print(block['type'], block['direction'], len(block['data']))
