import json
import random
import os
import mimetypes
import uuid
import time
from time import sleep
from datetime import datetime, timedelta, timezone

from bots.base.base import BaseFarmer
from bots.cats.configs import MIN_WAIT_TIME, MAX_WAIT_TIME, skip_ids
from bots.cats.strings import URL_GTASK, URL_CTASK, URL_USER
from bots.iceberg.strings import HEADERS, URL_INIT

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
        # Устанавливаем время начала на основе времени, оставшегося для загрузки аватара + 1-10 минут
        if hasattr(self, 'remaining_time_for_avatar'):
            additional_time = random.uniform(60, 300)  # От 1 до 5 минут
            self.start_time = time.time() + self.remaining_time_for_avatar + additional_time
        else:
            self.start_time = time.time() + random.uniform(MIN_WAIT_TIME, MAX_WAIT_TIME)

    def user(self):
        response = self.get(URL_USER, return_codes=(404,))
        if response.status_code == 404:
            self.reg()

    def tasks(self):
        self.log("Делаем таски")
        try:
            response = self.get(URL_GTASK).json()
            
            if response is None or 'tasks' not in response:
                self.log("Ошибка: получен некорректный ответ.")
                return
            
            tasks = response.get('tasks', [])

            for task in tasks:
                task_id = task['id']
                title = task['title']
                completed = task['completed']
                task_type = task['type']
                params = task.get('params', {})
                chat_url = params.get('channelUrl')

                if not completed and task_id not in skip_ids:
                    if task_type == "SUBSCRIBE_TO_CHANNEL" and chat_url:
                        self.initiator.connect()
                        try:
                            self.initiator.subscribe_channel(chat_url)
                            self.log(f"Успешно подписались на: {chat_url}")
                        except Exception as e:
                            self.log(f"Ошибка при подписке: {e}")
                            sleep(10)

                        self.log(f"Выполняем задачу: {title}")
                        result = self.post(f'{URL_CTASK}{task_id}/complete', return_codes=(500,)).json()
                        if result.get('success', False):
                            self.log(f"Задача завершена: {task_id} {title}")
                        else:
                            self.log(f"Ошибка при выполнении задачи: {task_id} {title}")

                    elif task_type == "OPEN_LINK":
                        link_url = params.get('linkUrl')
                        if link_url:
                            self.log(f"Открываем ссылку: {link_url}")
                            # Здесь можно добавить код для открытия ссылки, например, с использованием веб-браузера.

                        self.log(f"Выполняем задачу: {title}")
                        result = self.post(f'{URL_CTASK}{task_id}/complete', return_codes=(500,)).json()
                        if result.get('success', False):
                            self.log(f"Задача завершена: {task_id} {title}")
                        else:
                            self.log(f"Ошибка при выполнении задачи: {task_id} {title}")

                    sleep(4)  # Пауза перед выполнением следующего задания
                    
        except Exception as e:
            self.log(f"Ошибка при обработке задач: {e}")
            sleep(3)

    def reg(self):
        self.post(
            'https://api.catshouse.club/user/create?referral_code=VV1cmMGZf3dXibkVcHMMU'
        )
        
    def cats_avatar(self):
        try:
            avatar_info = self.get('https://api.catshouse.club/user/avatar').json()
            if avatar_info:
                attempt_time_str = avatar_info.get('attemptTime', None)
                current_time_utc = datetime.now(timezone.utc)

                if attempt_time_str is None:
                    self.log("Нет информации о последней попытке загрузки аватара.")
                    return None

                attempt_time = datetime.fromisoformat(attempt_time_str.replace('Z', '+00:00'))
                time_difference = (current_time_utc - attempt_time).total_seconds()

                if time_difference >= 24 * 3600:
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
                else:
                    remaining_time = timedelta(seconds=(24 * 3600 - time_difference))
                    self.remaining_time_for_avatar = remaining_time.total_seconds()

                    hours, remainder = divmod(remaining_time.total_seconds(), 3600)
                    minutes, seconds = divmod(remainder, 60)
                    self.log(f"Загрузить аватар можно через: {int(hours)} ч, {int(minutes)} мин и {int(seconds)} сек")
                    self.set_start_time()
                    return None

        except Exception as e:
            self.log(f"Неизвестная ошибка при отправке котейки | Error: {e}")
            sleep(3)

    def farm(self):
        self.user()
        self.tasks()
        self.cats_avatar()
