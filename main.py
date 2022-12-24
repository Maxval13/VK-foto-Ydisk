from datetime import date
import requests
import json
from ya_disk import YaUploader
import PySimpleGUI as sg
import time


class VkUser:
    url = 'https://api.vk.com/method/'

    def __init__(self, token, version):
        self.params = {
            'access_token': token,
            'v': version
        }

    # проверка акк в вк на доступ
    def user_verifid(self, user_id=None):
        user_verif = self.url + 'users.get'
        user_verif_params = {
            'user_ids': user_id
        }
        res = requests.get(user_verif, params={**self.params, **user_verif_params}).json()
        return res['response']

    # аватарка в максимальном разрешении
    def photo_max_orig_vk(self, user_id=None):
        photo_max_url = self.url + 'users.get'
        photo_max_params = {
            'user_ids': user_id,
            'fields': 'photo_max_orig'
        }
        res = requests.get(photo_max_url, params={**self.params, **photo_max_params}).json()
        return res['response']

    # функция для скачивания фото с профиля
    def get_photo_profile(self, user_id=None):
        photo_profile_url = self.url + 'photos.get'
        photo_profile_params = {
            'owner_id': user_id,
            'album_id': 'profile',
            'extended': 1,
            'photo_sizes': 0
        }
        res = requests.get(photo_profile_url, params={**self.params, **photo_profile_params}).json()
        return res['response']['items']


if __name__ == '__main__':

    with open('TOKEN_VK.txt', 'r') as file_vk:
        token_vk = file_vk.read().strip()

    with open('TOKEN_YA.txt', 'r') as file_ya:
        token_ya = file_ya.read().strip()

    # Пользователь вводит id
    user_id = input(f'Введите id пользователя для скачивания фото: ')
    vk_client = VkUser(token_vk, '5.131')
    ya_disk = YaUploader(token_ya)

    run = True
    # Проверка на пустой id
    while not user_id:
        user_id = input(f'Введите id пользователя для скачивания фото: ')
    else:
        while run:
            vk_client_ver = vk_client.user_verifid(user_id)
            for key_vk_client_ver, value_vk_client_ver in vk_client_ver[0].items():
                if key_vk_client_ver == 'is_closed' and value_vk_client_ver == False:
                    run = False
                    break
                else:
                    pass
            else:
                user_id = input(f'Введите id пользователя для скачивания фото: ')

    # создали папку для скачивания фото на основании id_user.
    ya_disk.get_create_folder(f'{user_id}')
    ya_disk.get_create_folder(f'{user_id}/{"Profile"}')

    vk_client_photo_prof = vk_client.get_photo_profile(user_id)
    count_like = []
    file_json = []
    for like_ in vk_client_photo_prof:
        count_like.append({dict(like_['likes'])['count']: [
            (dict(like_['sizes'][-1]))['type'], (dict(like_['sizes'][-1]))['url']]})

    len_clt = len(count_like)

    for i in range(len_clt - 1):
        for j in range(i + 1, len_clt):
            if count_like[i].keys() == count_like[j].keys():
                f_count_like = count_like[j].popitem()
                count_like[j].setdefault(f'{f_count_like[0]}_{date.today()}', f_count_like[1])
            else:
                continue

    for i_count_like in count_like:
        for key, value in i_count_like.items():
            file_json.append({'file_name': f"{str(key)}.jpg", 'size': str(value[0])})

    with open("my.json", 'w') as file:
        json.dump(file_json, file, indent=3)

    # Загружаем фото с профиля на ядиск, имя кол-во лайков + прогресс бар
    for url_ in range(len(count_like)):
        sg.one_line_progress_meter('Загрузка данных на диск', url_ + 1, len(count_like))
        time.sleep(1)
        for url_key, url_value in count_like[url_].items():
            ya_disk.upload_file_internet(f'{user_id}/{"Profile"}/{url_key}.jpg', url_value[1])
