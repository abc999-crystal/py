import os
import ftplib

class FTPUtil:
    def __init__(self, ftp_server, ftp_username, ftp_password):
        self.ftp_server = ftp_server
        self.ftp_username = ftp_username
        self.ftp_password = ftp_password
        self.ftp = None

    def connect(self):
        """
        连接到FTP服务器
        """
        try:
            self.ftp = ftplib.FTP(self.ftp_server)
            self.ftp.login(self.ftp_username, self.ftp_password)
            print(f"连接到FTP服务器: {self.ftp_server}")
        except ftplib.all_errors as e:
            print(f"FTP连接错误: {e}")
            self.ftp = None

    def disconnect(self):
        """
        从FTP服务器断开连接
        """
        if self.ftp:
            self.ftp.quit()
            print("从FTP服务器断开连接")
            self.ftp = None

    def ftp_download_folder(self, remote_folder, local_folder):
        """
        下载远程目录下的所有文件到本地目录
        :param remote_folder: 远程目录
        :param local_folder: 本地目录
        """
        if not self.ftp:
            print("未连接到FTP服务器")
            return

        try:
            self.ftp.cwd(remote_folder)
            if not os.path.exists(local_folder):
                os.makedirs(local_folder)

            for filename in self.ftp.nlst():
                local_filepath = os.path.join(local_folder, filename)
                with open(local_filepath, 'wb') as local_file:
                    self.ftp.retrbinary(f'RETR {filename}', local_file.write)
                print(f"下载: {filename} 到 {local_filepath}")

        except ftplib.all_errors as e:
            print(f"FTP错误: {e}")

    def ftp_download(self, remote_path, local_path):
        """
        下载远程文件到本地路径
        :param remote_path: 远程文件路径
        :param local_path: 本地文件路径
        """
        if not self.ftp:
            print("未连接到FTP服务器")
            return

        try:
            remote_dir = os.path.dirname(remote_path)
            self.ftp.cwd(remote_dir)
            with open(local_path, 'wb') as local_file:
                self.ftp.retrbinary(f'RETR {os.path.basename(remote_path)}', local_file.write)
            print(f"下载: {remote_path} 到 {local_path}")

        except ftplib.all_errors as e:
            print(f"FTP错误: {e}")

    def upload_file_to_ftp(self, local_path, remote_dir=""):
        """
        上传本地文件到FTP服务器
        :param local_path: 本地文件路径
        :param remote_dir: 远程目录路径
        """
        if not self.ftp:
            print("未连接到FTP服务器")
            return "fail"

        try:
            self.create_ftp_directory(remote_dir)
            with open(local_path, 'rb') as file:
                self.ftp.storbinary(f'STOR {os.path.basename(local_path)}', file)
            remote_path = os.path.join(remote_dir, os.path.basename(local_path))
            print(f"成功上传 {local_path} 到 {remote_path}")
            return remote_path
        except ftplib.all_errors as e:
            print(f"FTP错误: {e}")
            return "fail"

    def create_ftp_directory(self, remote_dir):
        """
        在FTP服务器上创建目录
        :param remote_dir: 远程目录路径
        """
        dirs = remote_dir.split('/')
        for dir in dirs:
            if dir:
                try:
                    self.ftp.mkd(dir)
                    print(f"创建目录: {dir}")
                except ftplib.error_perm as e:
                    if not str(e).startswith('550'):  # 550 表示目录已经存在
                        print(f"创建目录 {dir} 错误: {e}")
                        raise
                self.ftp.cwd(dir)
                print(f"切换到目录: {self.ftp.pwd()}")


if __name__ == '__main__':
    # 初始化FTP连接信息
    ftp_server = "xxx"
    ftp_username = "xxx"
    ftp_password = "xxx"

    # 创建FTPUtility对象
    ftp_util = FTPUtil(ftp_server, ftp_username, ftp_password)

    # 连接到FTP服务器
    ftp_util.connect()

    # 下载远程目录下的所有文件到本地目录
    remote_folder = "/remote/path/to/folder"
    local_folder = "D:/local/path/to/folder"
    ftp_util.ftp_download_folder(remote_folder, local_folder)

    # 下载单个文件
    remote_file_path = "/remote/path/to/file.txt"
    local_file_path = "D:/local/path/to/file.txt"
    ftp_util.ftp_download(remote_file_path, local_file_path)

    # 上传文件到FTP服务器
    local_file_path_to_upload = "D:/local/path/to/upload.txt"
    remote_upload_dir = "/remote/path/to/upload/folder"
    ftp_util.upload_file_to_ftp(local_file_path_to_upload, remote_upload_dir)

    # 断开与FTP服务器的连接
    ftp_util.disconnect()