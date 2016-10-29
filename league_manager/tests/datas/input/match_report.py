from datetime import datetime

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
        {"team": 3},
        {"team": 4},
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
