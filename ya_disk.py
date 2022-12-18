import requests
from pprint import pprint

class YaUploader:
    host = 'https://cloud-api.yandex.net'

    # принимаем токен
    def __init__(self, token):
        self.token = token

    # формируем заголовки
    def get_headers(self):
        return {
            'Content-Type': 'application/json',
            'Authorization': f'OAuth {self.token}'
        }

    # функция создания папки
    def get_create_folder(self, path):
        url = f'{self.host}/v1/disk/resources/'
        headers = self.get_headers()
        params = {'path': path}
        response = requests.put(url, headers=headers, params=params)
        return response

    # Функция проверки наличия файла по его имени
    def get_check_folder(self, path):
        url = f'{self.host}/v1/disk/resources/'
        headers = self.get_headers()
        params = {'path': path}
        rez = requests.get(url, headers=headers, params=params).json()
        return rez["_embedded"]['items'][0]


    # метод для получения данных
    def get_files_list(self):
        url = f'{self.host}/v1/disk/resources/files/'
        headers = self.get_headers()
        response = requests.get(url, headers=headers)
        pprint(response.json())

    # функция получения ссылки для загрузки
    def _get_upload_link(self, path):
        url_link = f'{self.host}/v1/disk/resources/upload/'
        headers = self.get_headers()
        params = {'path': path, 'overwrite': 'false'}
        response = requests.get(url_link, params=params, headers=headers)
        print(response.json().get('href'))
        return response.json().get('href')

    # Функция загрузки из интернета на яндекс.диск
    def upload_file_internet(self, path, url):
        uurll = f'{self.host}/v1/disk/resources/upload/'
        headers = self.get_headers()
        params = {'path': path, 'url': url}
        response = requests.post(uurll, params=params, headers=headers)
        response.raise_for_status()
        # if response.status_code == 202:
        #     print('Файл загружен')



    # функция загрузки с диска
    def upload_file(self, path, file_name):
        upload_link = self._get_upload_link(path)
        headers = self.get_headers()
        response = requests.put(upload_link, data=open(file_name, 'rb'), headers=headers)
        response.raise_for_status()
        if response.status_code == 201:
            print('Файл успешно загружен')




