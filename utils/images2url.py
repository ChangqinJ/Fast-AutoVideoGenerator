import os
import random
import string
import requests
import base64
import json
import hashlib

class images2url():
    def __init__(self,LOCAL_FOLDER):
        self.GITEE_USERNAME = "ChangqinJ"
        self.REPO_NAME = "images2url"
        self.GITEE_ACCESS_TOKEN = "6bc32cab5fa397da3db836dd109d6555"
        self.BRANCH_NAME = "main"
        self.LOCAL_FOLDER = LOCAL_FOLDER
        self.UPLOAD_PATH = "uploads"
        self.HASH_RECORD_FILE = "uploaded_hashes.json"
    # 配置信息
    # self.GITEE_USERNAME = "ChangqinJ"  # 替换为你的 Gitee 用户名
    # self.REPO_NAME = "images2url"  # 替换为你的 Gitee 仓库名
    # self.GITEE_ACCESS_TOKEN = "6bc32cab5fa397da3db836dd109d6555"  # 替换为你的 Gitee 个人访问令牌
    # BRANCH_NAME = "main"  # 仓库的分支名（通常是 main 或 master）
    # self.LOCAL_FOLDER = "科幻/战锤8-redo/images"  # 本地存放图片的文件夹路径
    # self.UPLOAD_PATH = "uploads"  # 在 Gitee 仓库中存放图片的文件夹路径
    # self.HASH_RECORD_FILE = "uploaded_hashes.json"  # 本地保存已上传哈希值的文件
    # 加载已上传哈希值列表
    def load_uploaded_hashes(self):
        if os.path.exists(self.HASH_RECORD_FILE):
            with open(self.HASH_RECORD_FILE, "r") as f:
                return json.load(f)
        return {}

    # 保存已上传哈希值列表
    def save_uploaded_hashes(self,uploaded_hashes):
        with open(self.HASH_RECORD_FILE, "w") as f:
            json.dump(uploaded_hashes, f)

    # 计算图片文件的哈希值（MD5）
    def calculate_file_hash(self,file_path):
        hasher = hashlib.md5()
        with open(file_path, "rb") as f:
            while chunk := f.read(8192):
                hasher.update(chunk)
        return hasher.hexdigest()


    # 上传图片到 Gitee
    def upload_to_gitee(self,file_path, file_name):
        url = f"https://gitee.com/api/v5/repos/{self.GITEE_USERNAME}/{self.REPO_NAME}/contents/{self.UPLOAD_PATH}/{file_name}"
        headers = {"Content-Type": "application/json"}
        with open(file_path, "rb") as f:
            content = f.read()
        b64content = base64.b64encode(content).decode("utf-8")
        data = {
            "access_token": self.GITEE_ACCESS_TOKEN,
            "content": b64content,  # 将文件内容转换为 Base64
            "message": f"Upload {file_name}"
        }
        response = requests.post(url, json=data, headers=headers)
        if response.status_code == 201:
            download_url = response.json().get("content", {}).get("download_url")
            return download_url
        else:
            print(f"Failed to upload {file_name}: {response.text}")
            return None

    # 生成随机 ID
    def generate_random_id(self,length=8):
        return ''.join(random.choices(string.ascii_letters + string.digits, k=length))

    # 主函数
    def get_url(self):
        # 加载已上传的哈希值
        uploaded_hashes = self.load_uploaded_hashes()

        if not os.path.exists(self.LOCAL_FOLDER):
            print(f"Local folder '{self.LOCAL_FOLDER}' does not exist!")
            return
        
        # 遍历本地文件夹中的所有图片文件
        for file_name in os.listdir(self.LOCAL_FOLDER):
            file_path = os.path.join(self.LOCAL_FOLDER, file_name)
            if not os.path.isfile(file_path):
                continue
            # 过滤仅允许的图片格式
            if not (file_name.lower().startswith("first_frame") and file_name.lower().endswith(('.png', '.jpg', '.jpeg', '.gif'))):
                print(f"Skipping non-image file: {file_name}")
                continue

            # 计算图片的哈希值
            file_hash = self.calculate_file_hash(file_path)
            print(f"File: {file_name}, Hash: {file_hash}")

            # 检查是否已上传
            if file_hash in uploaded_hashes:
                print(f"Skipping already uploaded file: {file_name}")
                existing_url = uploaded_hashes[file_hash]
                return existing_url
                

            # 上传图片到 Gitee
            print(f"Uploading {file_name}...")
            new_file_name = f"{file_hash}_{file_name}"  # 使用哈希值作为文件名的一部分
            download_url = self.upload_to_gitee(file_path, new_file_name)
            
            if download_url:
                print(f"Uploaded successfully! File URL: {download_url}")
                # 记录上传的哈希值
                uploaded_hashes[file_hash] = download_url
                self.save_uploaded_hashes(uploaded_hashes)
                return download_url
            else:
                print(f"Failed to upload {file_name}.")
                return None

