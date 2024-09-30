import requests
import json
import random
import os
import mimetypes
import uuid
import time
from time import sleep
from datetime import datetime, timedelta, timezone
import cfscrape

from bots.base.base import BaseFarmer
from .configs import MIN_WAIT_TIME, MAX_WAIT_TIME, skip_ids
from .strings import URL_GTASK, URL_CTASK, URL_USER, HEADERS, URL_INIT

scraper = cfscrape.create_scraper(delay=10)

class BotFarmer(BaseFarmer):
    name = 'catsgang_bot'
    extra_code = "VV1cmMGZf3dXibkVcHMMU"
    initialization_data = dict(peer=name, bot=name, url=URL_INIT, start_param=extra_code)

    def set_headers(self, *args, **kwargs):
        self.headers = HEADERS.copy()

    def authenticate(self, *args, **kwargs):
        auth_data = self.initiator.get_auth_data(**self.initialization_data)["authData"]
        self.headers['authorization'] = f"tma {auth_data}"

    def refresh_token(self):
        print()

    def set_start_time(self):
        if hasattr(self, 'remaining_time_for_avatar'):
            additional_time = random.uniform(60, 300)  # время входа после конца таймера, для загрузки аватарки
            self.start_time = time.time() + self.remaining_time_for_avatar + additional_time
        else:
            self.start_time = time.time() + random.uniform(MIN_WAIT_TIME, MAX_WAIT_TIME)

    def user(self):
        response = scraper.get(URL_USER)
        if response.status_code == 404:
            self.reg()

    def tasks(self):
        self.log("Делаем таски")
        try:

            url = URL_GTASK
            payload = {
            'group': 'cats'
        }
            response = requests.get(url, headers=self.headers, json=payload)
            data = response.json()
            if data is None or 'tasks' not in data:
                self.log("Ошибка: получен некорректный ответ.")
                return
            
            tasks = data.get('tasks', [])

            for task in tasks:
                task_id = task['id']
                title = task['title']
                completed = task['completed']

                if not completed and task_id not in skip_ids:
                    task_type = task['type']
                    if task_type not in skip_ids:
                        self.log(f"Выполняем задачу: {title}")
                        result = scraper.post(f'{URL_CTASK}{task_id}/complete').json()
                        if result.get('success', False):
                            self.log(f"Задача завершена: {task_id} {title}")
                        else:
                            self.log(f"Ошибка при выполнении задачи: {task_id} {title}")  
                    sleep(5)
                    
        except Exception as e:
            self.log(f"Ошибка при обработке задач: {e}")
            sleep(3)

    def reg(self):
        scraper.post(
            'https://api.catshouse.club/user/create?referral_code=VV1cmMGZf3dXibkVcHMMU'
        )
        
    def upload_avatar(self):
        img_folder = 'bots/cats/img'
        image_files = [f for f in os.listdir(img_folder) if f.lower().endswith(('.png', '.jpg', '.jpeg'))]

        if not image_files:
            self.log("По пути 'bots/cats/img' не найдено изображений")
            return None

        random_image = random.choice(image_files)
        image_path = os.path.join(img_folder, random_image)

        mime_type, _ = mimetypes.guess_type(image_path)
        if not mime_type:
            mime_type = 'application/octet-stream'

        boundary = f"----WebKitFormBoundary{uuid.uuid4().hex}"
        form_data = (
            f'--{boundary}\r\n'
            f'Content-Disposition: form-data; name="photo"; filename="{random_image}"\r\n'
            f'Content-Type: {mime_type}\r\n\r\n'
        ).encode('utf-8')

        with open(image_path, 'rb') as file:
            file_content = file.read()
            form_data += file_content

        form_data += f'\r\n--{boundary}--\r\n'.encode('utf-8')
        headers = self.headers.copy()
        headers['Content-Type'] = f'multipart/form-data; boundary={boundary}'
        response = self.post('https://api.catshouse.club/user/avatar/upgrade', data=form_data, headers=headers).json()

        reward = response.get('rewards', 0)
        self.log(f"Награда за Аватарку: {reward}")
        return reward

    def check_avatar_upload_time(self):
        url = 'https://api.catshouse.club/user/avatar'
        avatar_info_response = requests.get(url, headers=self.headers)
        avatar_info = avatar_info_response.json()

        if avatar_info:
            attempt_time_str = avatar_info.get('attemptTime', None)
            current_time_utc = datetime.now(timezone.utc)

            if attempt_time_str is None:
                self.log("Нет информации о последней попытке загрузки аватара.")
                # Если информация отсутствует, считаем, что можно загрузить аватар прямо сейчас
                self.upload_avatar()
                return

            attempt_time = datetime.fromisoformat(attempt_time_str.replace('Z', '+00:00'))
            time_difference = (current_time_utc - attempt_time).total_seconds()

            if time_difference >= 24 * 3600:
                self.upload_avatar()
            else:
                remaining_time = timedelta(seconds=(24 * 3600 - time_difference))
                self.remaining_time_for_avatar = remaining_time.total_seconds()

                hours, remainder = divmod(remaining_time.total_seconds(), 3600)
                minutes, seconds = divmod(remainder, 60)
                self.log(f"Загрузить аватар можно через: {int(hours)} ч, {int(minutes)} мин и {int(seconds)} сек")
                self.set_start_time()

    def cats_avatar(self):
        try:
            self.check_avatar_upload_time()
        except Exception as e:
            self.log(f"Неизвестная ошибка при отправке котейки | Error: {e}")
            sleep(3)

    def farm(self):
        self.user()
        self.tasks()
        self.cats_avatar()