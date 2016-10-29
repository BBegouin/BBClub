from datetime import datetime

list_datas = {
    0:{
        "id": 1,
        "team_reports": [
            {"match": 1,"team": 1,"supporters": 12,"fame": 1,"winnings": 50, "fan_factor": -1,
            "player_report": [
                {"id": 1, "nb_pass": 1, "nb_td": 1, "nb_int": 1, "nb_cas": 1, "nb_mvp": 1, "nb_foul": 1, "nb_blocks": 21, "is_wounded": False, "injury_type": None, "earned_xp": None, "team_report": 1, "player": 1},
                {"id": 2, "nb_pass": 1, "nb_td": 1, "nb_int": 1, "nb_cas": 1, "nb_mvp": 1, "nb_foul": 1, "nb_blocks": 21, "is_wounded": False, "injury_type": None, "earned_xp": None, "team_report": 1, "player": 2},
                {"id": 3, "nb_pass": 1, "nb_td": 1, "nb_int": 1, "nb_cas": 1, "nb_mvp": 1, "nb_foul": 1, "nb_blocks": 21, "is_wounded": False, "injury_type": None, "earned_xp": None, "team_report": 1, "player": 3},
                {"id": 4, "nb_pass": 1, "nb_td": 1, "nb_int": 1, "nb_cas": 1, "nb_mvp": 1, "nb_foul": 1, "nb_blocks": 21, "is_wounded": False, "injury_type": None, "earned_xp": None, "team_report": 1, "player": 4}]},
            {"match": 1, "team": 2, "supporters": 12, "fame": 1, "winnings": 50, "fan_factor": -1,
             "player_report": [
                 {"id": 5, "nb_pass": 1, "nb_td": 1, "nb_int": 1, "nb_cas": 1, "nb_mvp": 1, "nb_foul": 1, "nb_blocks": 21, "is_wounded": False, "injury_type": None, "earned_xp": None, "team_report": 2, "player": 12},
                 {"id": 6, "nb_pass": 1, "nb_td": 1, "nb_int": 1, "nb_cas": 1, "nb_mvp": 1, "nb_foul": 1, "nb_blocks": 21, "is_wounded": False, "injury_type": None, "earned_xp": None, "team_report": 2, "player": 13},
                 {"id": 7, "nb_pass": 1, "nb_td": 1, "nb_int": 1, "nb_cas": 1, "nb_mvp": 1, "nb_foul": 1, "nb_blocks": 21, "is_wounded": False, "injury_type": None, "earned_xp": None, "team_report": 2, "player": 14},
                 {"id": 8, "nb_pass": 1, "nb_td": 1, "nb_int": 1, "nb_cas": 1, "nb_mvp": 1, "nb_foul": 1, "nb_blocks": 21, "is_wounded": False, "injury_type": None, "earned_xp": None, "team_report": 2, "player": 15}]}
        ],
        "date": datetime.today().strftime('%Y-%m-%d'),
        "weather": "2",
        "status": 0
    },
    1:{
        "id": 2,
        "team_reports": [
            {"match": 2,"team": 1,"supporters": 12,"fame": 1,"winnings": 50, "fan_factor": -1,
            "player_report": [
                {"id": 9, "nb_pass": 1, "nb_td": 1, "nb_int": 1, "nb_cas": 1, "nb_mvp": 1, "nb_foul": 1, "nb_blocks": 21, "is_wounded": False, "injury_type": None, "earned_xp": None, "team_report": 3, "player": 3},
                {"id": 10, "nb_pass": 1, "nb_td": 1, "nb_int": 1, "nb_cas": 1, "nb_mvp": 1, "nb_foul": 1, "nb_blocks": 21, "is_wounded": False, "injury_type": None, "earned_xp": None, "team_report": 3, "player": 4},
                {"id": 11, "nb_pass": 1, "nb_td": 1, "nb_int": 1, "nb_cas": 1, "nb_mvp": 1, "nb_foul": 1, "nb_blocks": 21, "is_wounded": False, "injury_type": None, "earned_xp": None, "team_report": 3, "player": 5}]},
            {"match": 2, "team": 4, "supporters": 12, "fame": 1, "winnings": 50, "fan_factor": -1,
             "player_report": [
                 {"id": 12, "nb_pass": 1, "nb_td": 1, "nb_int": 1, "nb_cas": 1, "nb_mvp": 1, "nb_foul": 1, "nb_blocks": 21, "is_wounded": False, "injury_type": None, "earned_xp": None, "team_report": 4, "player": 23},
                 {"id": 13, "nb_pass": 1, "nb_td": 1, "nb_int": 1, "nb_cas": 1, "nb_mvp": 1, "nb_foul": 1, "nb_blocks": 21, "is_wounded": False, "injury_type": None, "earned_xp": None, "team_report": 4, "player": 24},
                 {"id": 14, "nb_pass": 1, "nb_td": 1, "nb_int": 1, "nb_cas": 1, "nb_mvp": 1, "nb_foul": 1, "nb_blocks": 21, "is_wounded": False, "injury_type": None, "earned_xp": None, "team_report": 4, "player": 25}]},
        ],
        "date": datetime.today().strftime('%Y-%m-%d'),
        "weather": "2",
        "status": 0
    },
}

detail_datas = list_datas[0]

create_datas_step_1_incompatible_team_1 = {
    "status": 0,
    "team_reports": [
        {"team": 1},
        {"team": 3},
    ]
}

create_datas_step_1_incompatible_team_2 = {
    "status": 0,
    "team_reports": [
        {"team": 5},
        {"team": 2},
    ]
}

create_datas_step_1_incompatible_team_3 = {
    "status": 0,
    "team_reports": [
        {"team": 2},
    ]
}

create_datas_step_1_OK = {
    "status": 0,
    "team_reports": [
        {"team": 1},
        {"team": 2},
    ]
}

update_datas_step_2_OK = {
    "date": "2016-10-21",
    "weather": 4,
    "team_reports": [
        {"id":5,
        "team": 1,
        "supporters": 12,
        "fame": 1,},
        {"id":6,
         "team": 2,
        "supporters": 6,
        "fame": 0,},
    ]
}

response_data_step_2 = {
    "id": 4,
    "team_reports": [
        {"id":7,"match": 4,"team": 1,"supporters": 12,"fame": 1,"player_report": [],"winnings":None, "fan_factor":None,},
        {"id":8,"match": 4,"team": 2, "supporters": 6,"fame": 0,"player_report": [],"winnings":None, "fan_factor":None,},
    ],
    "date": "2016-10-21",
    "weather": 4,
    "status": 0
}

# mise à jour du rapport d"équipe de l"équipe 1

update_datas_step_3 = {
    "team_reports": [{
        "id": 7,
        "player_report": [
            {"nb_pass": 0,"nb_td": 0,"nb_int": 1,"nb_cas": 0,"nb_mvp": 1,"nb_foul": 1,"nb_blocks": 21,"is_wounded": False,"team_report": 1,"player": 1},
            {"nb_pass": 0,"nb_td": 1,"nb_int": 0,"nb_cas": 0,"nb_mvp": 0,"nb_foul": 1,"nb_blocks": 21,"is_wounded": False,"team_report": 1,"player": 2},
            {"nb_pass": 2, "nb_td": 0, "nb_int": 0, "nb_cas": 1, "nb_mvp": 0, "nb_foul": 1, "nb_blocks": 21, "is_wounded": False, "team_report": 1,"player": 3},
            {"nb_pass": 0, "nb_td": 1, "nb_int": 0, "nb_cas": 2, "nb_mvp": 0, "nb_foul": 1, "nb_blocks": 21, "is_wounded": False, "team_report": 1,"player": 4},
            {"nb_pass": 0, "nb_td": 0, "nb_int": 0, "nb_cas": 0, "nb_mvp": 0, "nb_foul": 1, "nb_blocks": 10, "is_wounded": True, "injury_type": 4, "team_report": 1, "player": 6},
        ]},
    ]
}

response_data_step_3 = {
    "id": 5,
    "team_reports": [
        {"id":8,"match": 4,"team": 1,"supporters": 12,"fame": 1,"winnings":None, "fan_factor":None,
         "player_report": [
            {"nb_pass": 0,"nb_td": 0,"nb_int": 1,"nb_cas": 0,"nb_mvp": 1,"nb_foul": 1,"nb_blocks": 21,"is_wounded": False,"team_report": 1,"player": 1},
            {"nb_pass": 0,"nb_td": 1,"nb_int": 0,"nb_cas": 0,"nb_mvp": 0,"nb_foul": 1,"nb_blocks": 21,"is_wounded": False,"team_report": 1,"player": 2},
            {"nb_pass": 2, "nb_td": 0, "nb_int": 0, "nb_cas": 1, "nb_mvp": 0, "nb_foul": 1, "nb_blocks": 21, "is_wounded": False, "team_report": 1,"player": 3},
            {"nb_pass": 0, "nb_td": 1, "nb_int": 0, "nb_cas": 2, "nb_mvp": 0, "nb_foul": 1, "nb_blocks": 21, "is_wounded": False, "team_report": 1,"player": 4},
            {"nb_pass": 0, "nb_td": 0, "nb_int": 0, "nb_cas": 0, "nb_mvp": 0, "nb_foul": 1, "nb_blocks": 10, "is_wounded": True, "injury_type": 4, "team_report": 1, "player": 6},
        ],},
        {"id":9,"match": 4,"team": 2, "supporters": 6,"fame": 0,"winnings":None, "fan_factor":None,
         "player_report": [],},
    ],
    "date": "2016-10-21",
    "weather": 4,
    "status": 0
}


# mise à jour du rapport d"équipe de l"équipe 2
update_datas_step_4 = {
    "id":3,
    "team_reports": [{
        "player_report": [
            {"nb_pass": 0,"nb_td": 0,"nb_int": 1,"nb_cas": 0,"nb_mvp": 1,"nb_foul": 1,"nb_blocks": 21,"is_wounded": False,"team_report": 1,"player": 17},
            {"nb_pass": 0,"nb_td": 1,"nb_int": 0,"nb_cas": 0,"nb_mvp": 0,"nb_foul": 1,"nb_blocks": 21,"is_wounded": False,"team_report": 1,"player": 13},
            {"nb_pass": 2, "nb_td": 0, "nb_int": 0, "nb_cas": 1, "nb_mvp": 0, "nb_foul": 1, "nb_blocks": 21, "is_wounded": False, "team_report": 1,"player": 14},
            {"nb_pass": 0, "nb_td": 1, "nb_int": 0, "nb_cas": 2, "nb_mvp": 0, "nb_foul": 1, "nb_blocks": 21, "is_wounded": False, "team_report": 1,"player": 15},
            {"nb_pass": 0, "nb_td": 0, "nb_int": 0, "nb_cas": 0, "nb_mvp": 0, "nb_foul": 1, "nb_blocks": 10, "is_wounded": True, "injury_type": 3, "team_report": 1, "player": 16},
        ]}
    ]
}

# mise à jour de la séquence d"après match
update_datas_step_5 = {
    "id": 1,
    "team_reports": [
        {"id":1,"winnings": 50,"fan_factor": -1,"other_casualties": 2,},
        {"id":2,"winnings": 20,"fan_factor": -1,"other_casualties": 2}
    ]
}
