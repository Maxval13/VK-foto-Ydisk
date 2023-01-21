import requests


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
        if 'error' in res:
            return 'error'
        else:
            return res['response']['items']
