import time
from vk_user import VkUser
import json


class Rename_likes:

    def __init__(self, token_vk, user_id):
        self.vk_client = VkUser(token_vk, '5.131')
        self.vk_client_photo_prof = self.vk_client.get_photo_profile(user_id)

    def data_pr(self, ttt):
        t = time.ctime(ttt)
        ts = time.strptime(t)
        return time.strftime("%Y_%b_%d", ts)

    def like_rename_list(self):
        count_like = []
        photo_like = []
        file_json = []
        for like_ in self.vk_client_photo_prof:
            if (dict(like_['likes'])['count']) in photo_like:
                count_like.append((f"{(dict(like_['likes'])['count'])}_{self.data_pr(like_['date'])}",
                                   (dict(like_['sizes'][-1]))['type'], (dict(like_['sizes'][-1]))['url']))
            else:
                count_like.append(((dict(like_['likes'])['count']),
                                   (dict(like_['sizes'][-1]))['type'], (dict(like_['sizes'][-1]))['url']))
                photo_like.append(dict(like_['likes'])['count'])

        for i_count_like in count_like:
            file_json.append({'file_name': f"{str(i_count_like[0])}.jpg", 'size': str(i_count_like[1])})

        with open("my.json", 'w') as file:
            json.dump(file_json, file, indent=3)

        return count_like
