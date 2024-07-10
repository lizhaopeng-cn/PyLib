import os
import shutil
import hashlib


def file_checksum(file_path):
    """计算文件的SHA-256校验和"""
    sha256 = hashlib.sha256()
    with open(file_path, 'rb') as f:
        for block in iter(lambda: f.read(4096), b''):
            sha256.update(block)
    return sha256.hexdigest()


def find_files(directory, suffixes, excluded_keywords):
    """查找特定后缀且不包含排除关键字的文件"""
    file_paths = {}
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith(tuple(suffixes)) and all(keyword not in file for keyword in excluded_keywords):
                file_path = os.path.join(root, file)
                checksum = file_checksum(file_path)
                file_paths[checksum] = file_path
    return file_paths


def clear_and_create_directory(directory):
    """清空目录，如果目录不存在则创建"""
    if os.path.exists(directory):
        shutil.rmtree(directory)
    os.makedirs(directory)


def compare_and_copy_files(new_files, old_files, add_dir, delete_dir):
    """比较文件并复制到相应的目录"""
    # 清空或创建目标目录
    clear_and_create_directory(add_dir)
    clear_and_create_directory(delete_dir)

    # folder_new 有但是 folder_old 没有的文件
    for checksum, file_path in new_files.items():
        if checksum not in old_files:
            dst_file_path = os.path.join(add_dir, os.path.basename(file_path))
            shutil.copy2(file_path, dst_file_path)
            print(f"Copied to addLib: {file_path}")

    # folder_old 有但是 folder_new 没有的文件
    for checksum, file_path in old_files.items():
        if checksum not in new_files:
            dst_file_path = os.path.join(delete_dir, os.path.basename(file_path))
            shutil.copy2(file_path, dst_file_path)
            print(f"Copied to deleteLib: {file_path}")


if __name__ == '__main__':
    # 使用示例
    folder_new = 'C:\\Users\\lizhaopeng\\.gradle\\caches\\modules-2\\files-2.1'  # 将此路径替换为你的新文件夹路径
    folder_old = 'C:\\Lzp\\Project\\Yostar\\AiriSDK\\yostar_sdk_unity\\UnityMainLine\\UnityProject\\AiriSDK\\Assets\\Plugins\\Android\\libs'  # 将此路径替换为你的旧文件夹路径
    add_directory = './addLib'  # folder_new 有但是 folder_old 没有的文件复制到这里
    delete_directory = './deleteLib'  # folder_old 有但是 folder_new 没有的文件复制到这里
    file_suffixes = ['.jar', '.aar']  # 文件后缀列表
    excluded_keywords = ['-sources', '-javadoc']  # 排除关键字列表

    # 查找文件
    new_files = find_files(folder_new, file_suffixes, excluded_keywords)
    old_files = find_files(folder_old, file_suffixes, excluded_keywords)

    # 比较并复制文件
    compare_and_copy_files(new_files, old_files, add_directory, delete_directory)
