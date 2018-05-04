# TODO Info about download: Part of installer - Full size of file - Downloaded (file) - Percentage (file) - Speed
#                       or: Full size (all parts) - Downloaded - Percentage - Speed
# TODO Download dlcs
# TODO Download language specific installers in separate directory

import os
import sys
import hashlib
from gogapi.base import GogObject
from gogapi import GogApi, Token, get_auth_url
import gogapi.api
from gogapi.download import Download
from urllib.request import Request as urllib_request
from urllib.request import urlopen as urllib_urlopen

from modules.gamesdb import GamesDB

CONFIG_PATH = os.getenv('HOME') + '/.config/games_nebula/'

class Pygogdownloader:

    def __init__(self):

        self.gamesdb = GamesDB(CONFIG_PATH)

    def activate_gogapi(self):

        token = Token.from_file(CONFIG_PATH + 'token.json')
        if token.expired():
            token.refresh()
            token.save(CONFIG_PATH + 'token.json')
        self.api = GogApi(token)

    def get_games_data(self):

        if not os.path.exists(CONFIG_PATH + '/games.db'):
            self.request_games_data()

        games_data = self.gamesdb.get_games_data()

        return games_data

    def get_ids_list(self):

        if not os.path.exists(CONFIG_PATH + '/games.db'):
            ids_list = self.request_ids_list()
        else:
            ids_list = self.gamesdb.get_ids()

        return ids_list

    def request_ids_list(self):

        temp_dict = self.api.web_user_games()
        ids_list = temp_dict['owned']

        return ids_list

    def request_games_data(self):

        ids_list = self.get_ids_list()

        games_list = []

        for game_id in ids_list:
            prod = self.api.product(game_id)
            prod.update_galaxy(expand=True)

            # Second condition to filter movies and some other non-game content
            if (prod.type == 'game') and (len(prod.installers) > 0):

                name = prod.slug
                title = prod.title
                banner = 'https:' + ''.join(prod.image_logo.split('_glx_logo'))
                icon = 'https:' + prod.image_icon
                dlcs = prod.dlcs

                print(title)

                dlcs_str = ''
                if len(dlcs) > 0:
                    for i in range(len(dlcs)):
                        if i != (len(dlcs) - 1):
                            dlcs_str += str(dlcs[i].id) + '; '
                        else:
                            dlcs_str += str(dlcs[i].id)

                games_list.append((name, game_id, title, banner, icon, dlcs_str))

        self.gamesdb.write(games_list)
