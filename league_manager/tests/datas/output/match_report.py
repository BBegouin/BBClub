from datetime import datetime

list_datas = [
    {
        "id": 1,
        "team_reports": [
            {"id":1,"match": 1,"team": 1,"supporters": 12,"fame": 1,"winnings": 50, "fan_factor": -1,"result":None,
            "player_report": [
                {"id": 1, "nb_pass": 0, "nb_td": 0, "nb_int": 0, "nb_cas": 0, "mvp": False, "nb_foul": 0, "nb_blocks": 21, "injury_type": None, "earned_xp": None, "team_report": 1, "player": 1},
                {"id": 2, "nb_pass": 0, "nb_td": 0, "nb_int": 0, "nb_cas": 0, "mvp": False, "nb_foul": 0, "nb_blocks": 21, "injury_type": None, "earned_xp": None, "team_report": 1, "player": 2},
                {"id": 3, "nb_pass": 0, "nb_td": 0, "nb_int": 0, "nb_cas": 0, "mvp": False, "nb_foul": 0, "nb_blocks": 21, "injury_type": None, "earned_xp": None, "team_report": 1, "player": 3},
                {"id": 4, "nb_pass": 0, "nb_td": 0, "nb_int": 0, "nb_cas": 0, "mvp": False, "nb_foul": 0, "nb_blocks": 21, "injury_type": None, "earned_xp": None, "team_report": 1, "player": 4}]},
            {"id":2,"match": 1, "team": 2, "supporters": 12, "fame": 1, "winnings": 50, "fan_factor": -1,"result":None,
             "player_report": [
                 {"id": 5, "nb_pass": 0, "nb_td": 0, "nb_int": 0, "nb_cas": 0, "mvp": False, "nb_foul": 0, "nb_blocks": 21, "injury_type": None, "earned_xp": None, "team_report": 2, "player": 12},
                 {"id": 6, "nb_pass": 0, "nb_td": 0, "nb_int": 0, "nb_cas": 0, "mvp": False, "nb_foul": 0, "nb_blocks": 21, "injury_type": None, "earned_xp": None, "team_report": 2, "player": 13},
                 {"id": 7, "nb_pass": 0, "nb_td": 0, "nb_int": 0, "nb_cas": 0, "mvp": False, "nb_foul": 0, "nb_blocks": 21, "injury_type": None, "earned_xp": None, "team_report": 2, "player": 14},
                 {"id": 8, "nb_pass": 0, "nb_td": 0, "nb_int": 0, "nb_cas": 0, "mvp": False, "nb_foul": 0, "nb_blocks": 21, "injury_type": None, "earned_xp": None, "team_report": 2, "player": 15}]}
        ],
        "date": datetime.today().strftime('%Y-%m-%d'),
        "weather": "2",
        "status": 0
    },
    {
        "id": 2,
        "team_reports": [
            {"id":3,"match": 2,"team": 1,"supporters": 12,"fame": 1,"winnings": 20, "fan_factor": -1,"result":None,
            "player_report": [
                {"id": 9,  "nb_pass": 0, "nb_td": 0, "nb_int": 0, "nb_cas": 0, "mvp": True, "nb_foul": 0, "nb_blocks": 21, "injury_type": 0, "earned_xp": None, "team_report": 3, "player": 3},
                {"id": 10, "nb_pass": 0, "nb_td": 0, "nb_int": 0, "nb_cas": 0, "mvp": False, "nb_foul": 0, "nb_blocks": 21, "injury_type": 2, "earned_xp": None, "team_report": 3, "player": 4},
                {"id": 11, "nb_pass": 0, "nb_td": 0, "nb_int": 0, "nb_cas": 0, "mvp": False, "nb_foul": 0, "nb_blocks": 21, "injury_type": 7, "earned_xp": None, "team_report": 3, "player": 5}]},
            {"id":4,"match": 2, "team": 4, "supporters": 12, "fame": 1, "winnings": 60, "fan_factor": 1,"result":None,
             "player_report": [
                 {"id": 12, "nb_pass": 0, "nb_td": 0, "nb_int": 0, "nb_cas": 0, "mvp": False, "nb_foul": 0, "nb_blocks": 21, "injury_type": None, "earned_xp": None, "team_report": 4, "player": 23},
                 {"id": 13, "nb_pass": 0, "nb_td": 0, "nb_int": 0, "nb_cas": 0, "mvp": False, "nb_foul": 0, "nb_blocks": 21, "injury_type": None, "earned_xp": None, "team_report": 4, "player": 24},
                 {"id": 14, "nb_pass": 0, "nb_td": 0, "nb_int": 0, "nb_cas": 0, "mvp": False, "nb_foul": 0, "nb_blocks": 21, "injury_type": None, "earned_xp": None, "team_report": 4, "player": 25},
                 {"id": 15, "nb_pass": 0, "nb_td": 0, "nb_int": 0, "nb_cas": 0, "mvp": False, "nb_foul": 0, "nb_blocks": 21, "injury_type": None, "earned_xp": None, "team_report": 4, "player": 26}]},
        ],
        "date": datetime.today().strftime('%Y-%m-%d'),
        "weather": "2",
        "status": 0
    },
]

detail_datas = list_datas[0]

response_data_create_step_1 = {
    "id": 3,
    "team_reports": [
        {"id":5,"team": 1},
        {"id":6,"team": 2},
    ],
    "status": 0
}

response_data_step_2 = {
    "id": 4,
    "team_reports": [
        {"id":7,"match": 4,"team": 1,"supporters": 12,"fame": 1,"player_report": [],"winnings":None, "fan_factor":None,"result":None,},
        {"id":8,"match": 4,"team": 2, "supporters": 6,"fame": 0,"player_report": [],"winnings":None, "fan_factor":None,"result":None,},
    ],
    "date": "2016-10-21",
    "weather": 4,
    "status": 0
}

response_data_step_3 = {
    "id": 5,
    "team_reports": [
        {"id":8,"match": 4,"team": 1,"supporters": 12,"fame": 1,"winnings":None, "fan_factor":None,"result":None,
         "player_report": [
            {"nb_pass": 0,"nb_td": 0,"nb_int": 1,"nb_cas": 0,"mvp": True,"nb_foul": 0,"nb_blocks": 21,"is_wounded": False,"team_report": 1,"player": 1},
            {"nb_pass": 0,"nb_td": 1,"nb_int": 0,"nb_cas": 0,"mvp": False,"nb_foul": 0,"nb_blocks": 21,"is_wounded": False,"team_report": 1,"player": 2},
            {"nb_pass": 2, "nb_td": 0, "nb_int": 0, "nb_cas": 1, "mvp": False, "nb_foul": 0, "nb_blocks": 21, "team_report": 1,"player": 3},
            {"nb_pass": 0, "nb_td": 1, "nb_int": 0, "nb_cas": 2, "mvp": False, "nb_foul": 0, "nb_blocks": 21, "team_report": 1,"player": 4},
            {"nb_pass": 0, "nb_td": 0, "nb_int": 0, "nb_cas": 0, "mvp": False, "nb_foul": 0, "nb_blocks": 10, "is_wounded": True, "injury_type": 4, "team_report": 1, "player": 6},
        ],},
        {"id":9,"match": 4,"team": 2, "supporters": 6,"fame": 0,"winnings":None, "fan_factor":None,
         "player_report": [],},
    ],
    "date": "2016-10-21",
    "weather": 4,
    "status": 0
}

published_data = {
    "id": 2,
    "team_reports": [
        {"id":3,
        "match": 2,
        "team": 1,
        "supporters": 12,
        "fame": 1,
        "winnings": 20,
        "fan_factor": -1,
        "result" : 1,
        "player_report": [
            {"id": 9,  "nb_pass": 0, "nb_td": 0, "nb_int": 0, "nb_cas": 0, "mvp": True, "nb_foul": 0, "nb_blocks": 21, "injury_type": 0, "earned_xp": 5, "team_report": 3, "player": 3},
            {"id": 10, "nb_pass": 0, "nb_td": 0, "nb_int": 0, "nb_cas": 0, "mvp": False, "nb_foul": 0, "nb_blocks": 21, "injury_type": 2, "earned_xp": 0, "team_report": 3, "player": 4},
            {"id": 11, "nb_pass": 0, "nb_td": 0, "nb_int": 0, "nb_cas": 0, "mvp": False, "nb_foul": 0, "nb_blocks": 21, "injury_type": 7, "earned_xp": 0, "team_report": 3, "player": None}]},
        {"id":4,
        "match": 2,
        "team": 4,
        "supporters": 12,
        "fame": 1,
        "winnings": 60,
        "fan_factor": 1,
        "result" : 1,
         "player_report": [
             {"id": 12, "nb_pass": 0, "nb_td": 0, "nb_int": 0, "nb_cas": 0, "mvp": False, "nb_foul": 0, "nb_blocks": 21, "injury_type": None, "earned_xp": 0, "team_report": 4, "player": 23},
             {"id": 13, "nb_pass": 0, "nb_td": 0, "nb_int": 0, "nb_cas": 0, "mvp": False, "nb_foul": 0, "nb_blocks": 21, "injury_type": None, "earned_xp": 0, "team_report": 4, "player": 24},
             {"id": 14, "nb_pass": 0, "nb_td": 0, "nb_int": 0, "nb_cas": 0, "mvp": False, "nb_foul": 0, "nb_blocks": 21, "injury_type": None, "earned_xp": 0, "team_report": 4, "player": 25},
             {"id": 15, "nb_pass": 0, "nb_td": 0, "nb_int": 0, "nb_cas": 0, "mvp": False, "nb_foul": 0, "nb_blocks": 21, "injury_type": None, "earned_xp": 0, "team_report": 4, "player": 26}]},
    ],
    "date": datetime.today().strftime('%Y-%m-%d'),
    "weather": "2",
    "status": 0
}

team_1_after_match={
    'players': [
        {'id':1,  'ref_roster_line': 13, 'skills':[], 'name':'django', 'miss_next_game':False, 'num':2, 'total_xp': 0, 'need_upgrade':False,'is_journeyman':False,'M':6,'F':3,'Ag':4,'Ar':7},
        {'id':2,  'ref_roster_line': 13, 'skills':[], 'name':'django', 'miss_next_game':False, 'num':2, 'total_xp': 0, 'need_upgrade':False,'is_journeyman':False,'M':6,'F':3,'Ag':4,'Ar':7},
        {'id':3,  'ref_roster_line': 13, 'skills':[], 'name':'django', 'miss_next_game':False, 'num':2, 'total_xp': 5, 'need_upgrade':False,'is_journeyman':False,'M':6,'F':3,'Ag':4,'Ar':7},
        {'id':4,  'ref_roster_line': 16, 'name':'django', 'miss_next_game':True, 'num':2, 'total_xp': 0, 'need_upgrade':False,'is_journeyman':False,'M':7,'F':3,'Ag':4,'Ar':8,
        'skills':[
            {'id':3, 'name':'Blocage'},
            {'id':18, 'name':'Glissade contrôlée'}]
        },
        {'id':6,  'ref_roster_line': 13, 'skills':[], 'name':'django', 'miss_next_game':False, 'num':2, 'total_xp': 0, 'need_upgrade':False,'is_journeyman':False,'M':6,'F':3,'Ag':4,'Ar':7},
        {'id':7,  'ref_roster_line': 13, 'skills':[], 'name':'django', 'miss_next_game':False, 'num':2, 'total_xp': 0, 'need_upgrade':False,'is_journeyman':False,'M':6,'F':3,'Ag':4,'Ar':7},
        {'id':8,  'ref_roster_line': 13, 'skills':[], 'name':'django', 'miss_next_game':False, 'num':2, 'total_xp': 0, 'need_upgrade':False,'is_journeyman':False,'M':6,'F':3,'Ag':4,'Ar':7},
        {'id':9,  'ref_roster_line': 13, 'skills':[], 'name':'django', 'miss_next_game':False, 'num':2, 'total_xp': 0, 'need_upgrade':False,'is_journeyman':False,'M':6,'F':3,'Ag':4,'Ar':7},
        {'id':10, 'ref_roster_line': 13, 'skills':[], 'name':'django', 'miss_next_game':False, 'num':2, 'total_xp': 0, 'need_upgrade':False,'is_journeyman':False,'M':6,'F':3,'Ag':4,'Ar':7},
        {'id':11, 'ref_roster_line': 13, 'skills':[], 'name':'django', 'miss_next_game':False, 'num':2, 'total_xp': 0, 'need_upgrade':False,'is_journeyman':False,'M':6,'F':3,'Ag':4,'Ar':7},
        {'id':34, 'ref_roster_line': 13, 'name':'journalier_3', 'miss_next_game':False, 'num':3, 'total_xp': 0, 'need_upgrade':False,'is_journeyman':True,'M':6,'F':3,'Ag':4,'Ar':7,
            'skills':[{'id':66, 'name':'Solitaire'}],},
        {'id':35, 'ref_roster_line': 13, 'name':'journalier_4', 'miss_next_game':False, 'num':4, 'total_xp': 0, 'need_upgrade':False,'is_journeyman':True, 'M':6,'F':3,'Ag':4,'Ar':7,
            'skills':[{'id':66, 'name':'Solitaire'}],},
        ],
    'icon_file_path': 'icon file path',
    'status': 1,
    'cheerleaders': 0,
    'assistants': 0,
    'TV': 780,
    'user': 2,
    'league': 1,
    'apo': False,
    'DungeonBowl': False,
    'ranking_points': 2,
    'pop': 2,
    'ref_roster': 4,
    'name': 'les boeufs crevés',
    'id': 1,
    'treasury': 30,
    'nb_rerolls': 2,
    'bonus_point': 0,
}


team_4_after_match={
    'players': [
        {'id':23,  'ref_roster_line': 13, 'skills':[], 'name':'django', 'miss_next_game':False, 'num':2, 'total_xp': 0, 'need_upgrade':False,'is_journeyman':False,'M':6,'F':3,'Ag':4,'Ar':7},
        {'id':24,  'ref_roster_line': 13, 'skills':[], 'name':'django', 'miss_next_game':False, 'num':2, 'total_xp': 0, 'need_upgrade':False,'is_journeyman':False,'M':6,'F':3,'Ag':4,'Ar':7},
        {'id':25,  'ref_roster_line': 13, 'skills':[], 'name':'django', 'miss_next_game':False, 'num':2, 'total_xp': 0, 'need_upgrade':False,'is_journeyman':False,'M':6,'F':3,'Ag':4,'Ar':7},
        {'id':26,  'ref_roster_line': 13, 'skills':[], 'name':'django', 'miss_next_game':False, 'num':2, 'total_xp': 0, 'need_upgrade':False,'is_journeyman':False,'M':6,'F':3,'Ag':4,'Ar':7},
        {'id':27,  'ref_roster_line': 13, 'skills':[], 'name':'django', 'miss_next_game':False, 'num':2, 'total_xp': 0, 'need_upgrade':False,'is_journeyman':False,'M':6,'F':3,'Ag':4,'Ar':7},
        {'id':28,  'ref_roster_line': 13, 'skills':[], 'name':'django', 'miss_next_game':False, 'num':2, 'total_xp': 0, 'need_upgrade':False,'is_journeyman':False,'M':6,'F':3,'Ag':4,'Ar':7},
        {'id':29,  'ref_roster_line': 13, 'skills':[], 'name':'django', 'miss_next_game':False, 'num':2, 'total_xp': 0, 'need_upgrade':False,'is_journeyman':False,'M':6,'F':3,'Ag':4,'Ar':7},
        {'id':30,  'ref_roster_line': 13, 'skills':[], 'name':'django', 'miss_next_game':False, 'num':2, 'total_xp': 0, 'need_upgrade':False,'is_journeyman':False,'M':6,'F':3,'Ag':4,'Ar':7},
        {'id':31,  'ref_roster_line': 13, 'skills':[], 'name':'django', 'miss_next_game':False, 'num':2, 'total_xp': 0, 'need_upgrade':False,'is_journeyman':False,'M':6,'F':3,'Ag':4,'Ar':7},
        {'id':32,  'ref_roster_line': 13, 'skills':[], 'name':'django', 'miss_next_game':False, 'num':2, 'total_xp': 0, 'need_upgrade':False,'is_journeyman':False,'M':6,'F':3,'Ag':4,'Ar':7},
        {'id':33,  'ref_roster_line': 13, 'skills':[], 'name':'django', 'miss_next_game':False, 'num':2, 'total_xp': 0, 'need_upgrade':False,'is_journeyman':False,'M':6,'F':3,'Ag':4,'Ar':7},],
    'icon_file_path': 'icon file path',
    'status': 1,
    'cheerleaders': 0,
    'assistants': 0,
    'TV': 800,
    'user': 3,
    'league': 1,
    'apo': False,
    'DungeonBowl': False,
    'ranking_points': 2,
    'pop': 4,
    'ref_roster': 4,
    'name': 'les boeufs crevés',
    'id': 4,
    'treasury': 70,
    'nb_rerolls': 2,
    'bonus_point': 0,
}