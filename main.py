from vk_user import VkUser
from RenameCountLike import Rename_likes
from ya_disk import YaUploader
import PySimpleGUI as sg
import time

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
            if vk_client.get_photo_profile(user_id) == 'error':
                user_id = input(f'Введите id пользователя для скачивания фото: ')
            else:
                run = False
                break

    # создали папку для скачивания фото на основании id_user.
    ya_disk.get_create_folder(f'{user_id}')
    ya_disk.get_create_folder(f'{user_id}/{"Profile"}')
    rename_like = Rename_likes(token_vk, user_id)
    rename_like_list = rename_like.like_rename_list()

    # Загружаем фото с профиля на ядиск, имя кол-во лайков + прогресс бар
    for url_ in range(len(rename_like_list)):
        sg.one_line_progress_meter('Загрузка данных на диск', url_ + 1, len(rename_like_list))
        time.sleep(1)
        ya_disk.upload_file_internet(f'{user_id}/{"Profile"}/{rename_like_list[url_][0]}.jpg',
                                     rename_like_list[url_][2])
