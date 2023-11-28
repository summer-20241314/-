import re

def parse_line(line):
    # 使用正则表达式匹配行中的描述和数值
    match = re.match(r'\s*\d+\s*:(.*?)(?::|\.)\s*(.*)', line)
    if match:
        # 提取描述和数值
        description, value = match.groups()
        return description.strip(), value.strip()
    return None

def parse_text(text):
    lines = text.split('\n')
    parsed_data = {}
    for line in lines:
        result = parse_line(line)
        if result:
            desc, value = result
            parsed_data[desc] = value
    return parsed_data



# 解析文本
parsed_data = parse_text(text)

# 打印结果
for desc, value in parsed_data.items():
    print(f"{desc}: {value}")
