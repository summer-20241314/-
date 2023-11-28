def read_file(file_path, encoding):
    try:
        with open(file_path, 'r', encoding=encoding) as file:
            return file.read()
    except UnicodeDecodeError as e:
        print(f"Error reading file with encoding {encoding}: {e}")
        return None

file_path = 'P:\\01-question\\30-鬼频分析软件自主开发\\03-分析数据工作\\0304.mka'#'path_to_your_file.txt'  # 替换为您的文件路径

# 尝试使用 ISO-8859-1 编码读取文件
content = read_file(file_path, 'ISO-8859-1')
if content is None:
    # 如果 ISO-8859-1 失败，尝试使用 Windows-1252
    content = read_file(file_path, 'cp1252')

if content:
    print("File content read successfully")
    print("\n".join(content.split('\n')[:50])) 
    # 处理文件内容
else:
    print("Failed to read the file with the tried encodings")
