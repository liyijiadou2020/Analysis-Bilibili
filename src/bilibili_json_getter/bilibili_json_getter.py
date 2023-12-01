# ------*------ coding: utf-8 ------*------
# @Time    : 2023/11/30 14:01
# @Author  : 冰糖雪狸 (NekoSilverfox)
# @Project : Bilibili-dig
# @File    : bilibili_json_getter.py
# @Software: PyCharm
# @Github  ：https://github.com/NekoSilverFox
# -----------------------------------------

import requests
import time

cur_uid = 100072
# end_uid = 100005
end_uid = 100000000

json_file_path = './json_out'
csv_file_path = './csv_out'
sign_file_path = './sign_out'
url = 'https://api.bilibili.com/x/web-interface/card'  # 请求的URL
SLEEP_TIME = 1

if __name__ == '__main__':
    while cur_uid < end_uid:
        # 请求参数，可以根据需要修改
        params = {'mid': str(cur_uid),
                  'photo': 'false'}

        # 发送GET请求
        response = requests.get(url, params=params)
        time.sleep(SLEEP_TIME)

        # 检查请求是否成功
        if response.status_code == 200:
            # 解析JSON响应
            json_data = response.json()

            # JSON 响应码
            code = json_data.get("code")
            if code != 0:
                print(f'[ERROR] 请求错误 code: {code}, 等待重试中，最后尝试抓取的 uid: {cur_uid}')
                time.sleep(SLEEP_TIME)
                continue

            # 访问 "data" 字段
            data = json_data.get("data")

            # 输出 "data" 字段的内容
            # print(data)

            # -> card
            mid = data.get('card').get('mid')  # mid
            name = data.get('card').get('name')  # 昵称
            sex = data.get('card').get('sex')  # 性别
            face = data.get('card').get('face')  # 头像链接
            face_nft = data.get('card').get('face_nft')  # 是否为 NFT
            sign = data.get('card').get('sign')  # 签名
            fans = data.get('card').get('fans')  # 粉丝数
            friend = data.get('card').get('friend')  # 关注数
            attention = data.get('card').get('attention')  # 关注数

            # -> 主要信息
            archive_count = data.get('archive_count')  # 用户稿件数
            follower = data.get('follower')  # 粉丝数
            like_num = data.get('like_num')  # 获赞数

            # -> card -> level_info
            current_level = data.get('card').get('level_info').get('current_level')  # 等级

            # -> card -> Official
            official_role = data.get('card').get('Official').get('role')  # 见用户认证类型一览
            official_title = data.get('card').get('Official').get('title')  # 认证类型（名称）
            official_type = data.get('card').get('Official').get('type')  # 是否认证

            # -> card -> vip
            vip_type = data.get('card').get('vip').get('type')
            vip_status = data.get('card').get('vip').get('status')
            vip_due_date = data.get('card').get('vip').get('due_date')  # 会员过期时间	Unix时间戳(毫秒)
            vip_label_theme = data.get('card').get('vip').get('label').get('label_theme')  # 会员标签

            print(
                f'正在抓取 uid: {cur_uid}\tJSON 响应码: {code}\n\tname: {name}, sex: {sex}, archive_count: {archive_count}, follower: {follower}, like_num: {like_num} ...')

            print('\tJSON data 响应写入文件')
            # with 语句用于自动关闭文件
            with open(json_file_path, "a") as file:
                file.write(str(data) + "\n")

            print('\tCSV 写入文件')
            # with 语句用于自动关闭文件
            with open(csv_file_path, "a") as file:
                res_str = f'{mid}, {name}, {sex}, {face_nft}, {fans}, {friend}, {attention}, {archive_count}, {follower}, {like_num}, {current_level}, {official_role}, {official_title}, {official_type}, {vip_type}, {vip_status}, {vip_due_date}, {vip_label_theme}'
                file.write(res_str + "\n")

            print('\tSign 写入文件\n')
            # with 语句用于自动关闭文件
            with open(sign_file_path, "a") as file:
                sign = f'{mid}, {sign}'
                file.write(sign + "\n")

            cur_uid += 1

        else:
            # 输出错误信息
            print(f"Error: {response.status_code} - {response.text}")
            print(f'[ERROR] 请求错误, 等待重试中，最后尝试抓取的 uid: {cur_uid}')
            time.sleep(SLEEP_TIME)

