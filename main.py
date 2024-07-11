import os
import shutil
import hashlib


# C:\Users\lizhaopeng\.gradle2.x\caches\modules-2\files-2.1
folder_new = 'C:\\Users\\lizhaopeng\\.gradle2.x\\caches\\modules-2\\files-2.1'  # 将此路径替换为你的新文件夹路径
# C:\Lzp\Project\Yostar\AiriSDK\yostar_sdk_unity\UnityMainLine\UnityProject\AiriSDK\Assets\Plugins\Android\libs
folder_old = 'C:\\Lzp\\Project\\Yostar\\AiriSDK\\yostar_sdk_unity\\UnityMainLine\\UnityProject\\AiriSDK\\Assets\\Plugins\\Android\\libs'  # 将此路径替换为你的旧文件夹路径
file_suffixes = ['.jar', '.aar']  # 文件后缀列表
excluded_keywords = ['-sources', '-javadoc']  # 排除关键字列表
add_dir_all = './addLibAll'  # folder_new 有但是 folder_old 没有的文件复制到这里(包含文件夹)
add_dir = './addLib'  # folder_new 有但是 folder_old 没有的文件复制到这里
delete_dir = './deleteLib'  # folder_old 有但是 folder_new 没有的文件复制到这里
common_dir = './commonLib'  # 本地项目或三方本地文件
common_files = ['alml.jar',
                'IAP6Helper-release.aar',
                'iap_plugin_v17.02.00_20181012.jar',
                'in-app-purchasing-2.0.76.jar',
                'login-with-amazon-sdk.jar',
                'SdkHttpClient-release.aar',
                'twitter_android_core-release.aar']


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


def compare_and_copy_files(new_files, old_files):
    """比较文件并复制到相应的目录"""
    # 清空或创建目标目录
    clear_and_create_directory(add_dir_all)
    clear_and_create_directory(add_dir)
    clear_and_create_directory(delete_dir)
    clear_and_create_directory(common_dir)

    # folder_new 有但是 folder_old 没有的文件
    for checksum, file_path in new_files.items():
        if checksum not in old_files:
            # addLibAll
            dst_file_path_all = os.path.join(add_dir_all, os.path.relpath(file_path, folder_new))
            dst_dir_all = os.path.dirname(dst_file_path_all)
            if not os.path.exists(dst_dir_all):
                os.makedirs(dst_dir_all)
            shutil.copy2(file_path, dst_file_path_all)
            print(f"Copied to addLibAll: {file_path}")
            # addLib
            dst_file_path = os.path.join(add_dir, os.path.basename(file_path))
            shutil.copy2(file_path, dst_file_path)
            print(f"Copied to addLib: {file_path}")

    # folder_old 有但是 folder_new 没有的文件
    for checksum, file_path in old_files.items():
        if checksum not in new_files:
            basename = os.path.basename(file_path)
            # commonLib
            if basename in common_files:
                dst_file_path = os.path.join(common_dir, basename)
                shutil.copy2(file_path, dst_file_path)
                print(f"Copied to commonLib: {file_path}")
            # deleteLib
            else:
                dst_file_path = os.path.join(delete_dir, basename)
                shutil.copy2(file_path, dst_file_path)
                print(f"Copied to deleteLib: {file_path}")


if __name__ == '__main__':
    # 查找文件
    new_files = find_files(folder_new, file_suffixes, excluded_keywords)
    old_files = find_files(folder_old, file_suffixes, excluded_keywords)

    # 比较并复制文件
    compare_and_copy_files(new_files, old_files)
