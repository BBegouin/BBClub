
create_datas_incompatible_team_1={
        "match": 1,
        "team": 3,
    }


create_datas_incompatible_team_2 = {
    "match": 2,
    "team": 5,
    "supporters": 12,
    "fame": 1,
    "winnings": 50,
    "fan_factor": -1,
    "player_report": [
             {"id": 12, "nb_pass": 1, "nb_td": 1, "nb_int": 1, "nb_cas": 1, "nb_mvp": 1, "nb_foul": 1, "nb_blocks": 21, "is_wounded": False, "injury_type": None, "earned_xp": None, "team_report": 4, "player": 23},
             {"id": 13, "nb_pass": 1, "nb_td": 1, "nb_int": 1, "nb_cas": 1, "nb_mvp": 1, "nb_foul": 1, "nb_blocks": 21, "is_wounded": False, "injury_type": None, "earned_xp": None, "team_report": 4, "player": 24},
             {"id": 14, "nb_pass": 1, "nb_td": 1, "nb_int": 1, "nb_cas": 1, "nb_mvp": 1, "nb_foul": 1, "nb_blocks": 21, "is_wounded": False, "injury_type": None, "earned_xp": None, "team_report": 4, "player": 25},
    ],
}

create_datas_step_1_incompatible_team_3 = {
    "status": 0,
    "team_reports": [
        {"team": 2},
    ]
}

create_datas_team_not_related = {
    "match": 2,
    "team": 2,
    "supporters": 12,
    "fame": 1,
    "winnings": 50,
    "fan_factor": -1,
    "player_report": [
             {"id": 12, "nb_pass": 1, "nb_td": 1, "nb_int": 1, "nb_cas": 1, "nb_mvp": 1, "nb_foul": 1, "nb_blocks": 21, "is_wounded": False, "injury_type": None, "earned_xp": None, "team_report": 4, "player": 23},
             {"id": 13, "nb_pass": 1, "nb_td": 1, "nb_int": 1, "nb_cas": 1, "nb_mvp": 1, "nb_foul": 1, "nb_blocks": 21, "is_wounded": False, "injury_type": None, "earned_xp": None, "team_report": 4, "player": 24},
             {"id": 14, "nb_pass": 1, "nb_td": 1, "nb_int": 1, "nb_cas": 1, "nb_mvp": 1, "nb_foul": 1, "nb_blocks": 21, "is_wounded": False, "injury_type": None, "earned_xp": None, "team_report": 4, "player": 25},
    ],
}

create_datas_OK = {
    "match": 2,
    "team": 4,
}

update_datas_step_1_OK = {
    "match": 2,
    "team": 4,
    "supporters": 5,
    "fame": 0,
}

update_datas_step_2_OK = {
    "id":5,
    "match": 2,
    "team": 4,
    "winnings": 3,
    "fan_factor": -1,
}


update_datas_step_3_OK = {
    "id":5,
    "player_report": [
         {"id": 12, "nb_pass": 1, "nb_td": 1, "nb_int": 1, "nb_cas": 1, "mvp": True, "nb_foul": 1, "nb_blocks": 21, "is_wounded": False, "injury_type": None, "earned_xp": None, "team_report": 5, "player": 23},
         {"id": 13, "nb_pass": 2, "nb_td": 2, "nb_int": 2, "nb_cas": 2, "mvp": False, "nb_foul": 2, "nb_blocks": 21, "is_wounded": False, "injury_type": None, "earned_xp": None, "team_report": 5, "player": 24},
         {"id": 14, "nb_pass": 3, "nb_td": 3, "nb_int": 3, "nb_cas": 3, "mvp": False, "nb_foul": 3, "nb_blocks": 21, "is_wounded": True, "injury_type": 6, "earned_xp": None, "team_report": 5, "player": 25},
    ],
}