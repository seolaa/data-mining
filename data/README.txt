Raw data list

1. game_list : 게임 리스트 [game_id, game_title, review_count]
2. game_tag : 게임 태그 <리뷰 100개 이상인 8509 게임에 대해서, 그 중 95% 정도 크롤링 성공> [game_id, tag]
3. user_list : 리뷰 500개 초과인 게임에서 100명 추출 -> 29만명 [user_id]
4. playtime/user_playtime_000~099 : user_list의 playtime (대략 30% 정도 공개) [user_id, game_id, play_time]
5. user_list_playtime : user_list에서 playtime이 공개된 유저 약 9만명 [user_id]
6. vote/user_vote_000~099 : user_list_playtime 유저의 vote (대략 99%정도 공개) [user_id, game_id, vote]