import SteamDataCrawler
import pandas as pd


# 1
game_list = SteamDataCrawler.get_df_game_list()
game_list = game_list.loc[game_list['review_count'] >= 100]
game_list.to_csv("./data/game_list.csv", encoding = 'utf-8', index = False)
game_id_list = game_list['game_id'].tolist()

# 2
game_tag = SteamDataCrawler.get_df_game_tag(game_id_list)
game_tag.to_csv("./data/game_tag.csv", encoding = 'utf-8', index = False)

# 3
game_user = SteamDataCrawler.get_df_game_user(game_id_list, num = 100, language = 'all', num_per_page = 100)
# game_user.to_csv("./data/game_user.csv", encoding = 'utf-8', index = False)

# 4
user_list = SteamDataCrawler.get_df_game_user(game_user)
user_list.to_csv("./data/user_list.csv", encoding = 'utf-8', index = False)