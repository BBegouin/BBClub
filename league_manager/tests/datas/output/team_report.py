from datetime import datetime

list_datas = {
    0:{ "id":1,
        "match": 1,
        "team": 1,
        "supporters": 12,
        "fame": 1,
        "winnings": 50,
        "fan_factor": -1,
        "result":None,
        "player_report": [
                {"id": 1, "nb_pass": 0, "nb_td": 0, "nb_int": 0, "nb_cas": 0, "mvp": False, "nb_foul": 0, "nb_blocks": 21, "injury_type": None, "earned_xp": None, "team_report": 1, "player": 1},
                {"id": 2, "nb_pass": 0, "nb_td": 0, "nb_int": 0, "nb_cas": 0, "mvp": False, "nb_foul": 0, "nb_blocks": 21, "injury_type": None, "earned_xp": None, "team_report": 1, "player": 2},
                {"id": 3, "nb_pass": 0, "nb_td": 0, "nb_int": 0, "nb_cas": 0, "mvp": False, "nb_foul": 0, "nb_blocks": 21, "injury_type": None, "earned_xp": None, "team_report": 1, "player": 3},
                {"id": 4, "nb_pass": 0, "nb_td": 0, "nb_int": 0, "nb_cas": 0, "mvp": False, "nb_foul": 0, "nb_blocks": 21, "injury_type": None, "earned_xp": None, "team_report": 1, "player": 4}
        ]
    },
    1:{ "id":2,
        "match":1,
        "team": 2,
        "supporters": 12,
        "fame": 1,
        "winnings": 50,
        "fan_factor": -1,
        "result":None,
        "player_report": [
             {"id": 5, "nb_pass": 0, "nb_td": 0, "nb_int": 0, "nb_cas": 0, "mvp": False, "nb_foul": 0, "nb_blocks": 21, "injury_type": None, "earned_xp": None, "team_report": 2, "player": 12},
             {"id": 6, "nb_pass": 0, "nb_td": 0, "nb_int": 0, "nb_cas": 0, "mvp": False, "nb_foul": 0, "nb_blocks": 21, "injury_type": None, "earned_xp": None, "team_report": 2, "player": 13},
             {"id": 7, "nb_pass": 0, "nb_td": 0, "nb_int": 0, "nb_cas": 0, "mvp": False, "nb_foul": 0, "nb_blocks": 21, "injury_type": None, "earned_xp": None, "team_report": 2, "player": 14},
        ]
    },
    2:{ "id":3,
        "match": 2,
        "team": 1,
        "supporters": 12,
        "fame": 1,
        "winnings": 50,
        "fan_factor": -1,
        "result":None,
        "player_report": [
                {"id": 8, "nb_pass": 0, "nb_td": 0, "nb_int": 0, "nb_cas": 0, "mvp": False, "nb_foul": 0, "nb_blocks": 21, "injury_type": None, "earned_xp": None, "team_report": 3, "player": 3},
                {"id": 9, "nb_pass": 0, "nb_td": 0, "nb_int": 0, "nb_cas": 0, "mvp": False, "nb_foul": 0, "nb_blocks": 21, "injury_type": None, "earned_xp": None, "team_report": 3, "player": 4},
                {"id": 10, "nb_pass": 0, "nb_td": 0, "nb_int": 0, "nb_cas": 0, "mvp": False, "nb_foul": 0, "nb_blocks": 21, "injury_type": None, "earned_xp": None, "team_report": 3, "player": 5},
        ]
    },
}

detail_datas = list_datas[0]

response_create_datas_OK = {
    "id":4,
    "match": 2,
    "team": 4,
}

reponse_update_data_step_1_OK = {
    "id":5,
    "match": 2,
    "team": 4,
    "supporters": 5,
    "fame": 0,
    "winnings": None,
    "fan_factor": None,
    "player_report": [
    ],
    "result":None
}

reponse_update_datas_step_2_OK = {
    "id":5,
    "match": 2,
    "team": 4,
    "supporters": 5,
    "fame": 0,
    "winnings": 3,
    "fan_factor": -1,
    "player_report": [
    ],
    "result":None
}

reponse_update_datas_step_3_OK = {
    "id":5,
    "match": 2,
    "team": 4,
    "supporters": 5,
    "fame": 0,
    "winnings": 3,
    "fan_factor": -1,
    "player_report": [
             {"id": 11, "nb_pass": 1, "nb_td": 1, "nb_int": 1, "nb_cas": 1, "mvp": True,  "nb_foul": 1, "nb_blocks": 21, "injury_type": None, "earned_xp": None, "team_report": 5, "player": 23},
             {"id": 12, "nb_pass": 2, "nb_td": 2, "nb_int": 2, "nb_cas": 2, "mvp": False, "nb_foul": 2, "nb_blocks": 21, "injury_type": None, "earned_xp": None, "team_report": 5, "player": 24},
             {"id": 13, "nb_pass": 3, "nb_td": 3, "nb_int": 3, "nb_cas": 3, "mvp": False, "nb_foul": 3, "nb_blocks": 21, "injury_type": 6,    "earned_xp": None, "team_report": 5, "player": 25},
    ],
    "result":None
}
