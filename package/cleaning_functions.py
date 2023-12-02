import re


def elapsed_time(time_list):
    time_list = time_list.tolist()
    elapsed_times = []
    length = len(time_list)
    # print(length)
    for i in range(0,length-1):
        # print('in for loop')
        # print(i)
        time1 = time_list[i]
        # print(time1)
        time2 = time_list[i+1]
        # print(time2)
        # print(f'time1: {time1}, time2: {time2}')
        if time1 > time2:
            elapsed = time1 - time2
            # print(elapsed)
            elapsed_times.append(elapsed)
        elif time1 == time2:
            elapsed = 0
            elapsed_times.append(elapsed)
        else:
            elapsed = (time1) + (15-time2)
            # print(elapsed)
            elapsed_times.append(elapsed)
    elapsed_times.append(time_list[length-1])
    return elapsed_times


def game_time(elapsed_time):
    elapsed_time = elapsed_time.tolist()
    real_game_time = []
    real_game_time.append(0)
    # print(real_game_time)
    for i in range(0,len(elapsed_time)-1):
        time = real_game_time[i] + elapsed_time[i]
        real_game_time.append(time)
    # real_game_time = real_game_time[1:len(real_game_time)]
    return real_game_time


def play_type(play_description):
        if 'pass' in play_description.lower() or 'scrambles' in play_description.lower():
            return 'Pass'
        elif 'kicks' in play_description.lower() or 'punts' in play_description.lower():
            return "Special Teams"
        else: 
             return "Run"
        

def determine_possession(play_start, drives):
    closest_drive_team = None
    for drive_start, drive_team in zip(drives['drive_start_time'], drives['team']):
            if drive_start <= play_start:
                closest_drive_team = drive_team
            else:
                break
    return closest_drive_team


def yardage_by_play(play_detail, play_type):
    yardage = 0
    
    if play_type in ['Run', 'Pass']:
        # Define a regular expression pattern to find yardage in play_detail
        pattern = r'(-?\d+\.\d+|-?\d+)'
        # Use re.findall to find all yardage values that match the pattern
        yards = re.findall(pattern, play_detail)
        # If we found yardage values, sum them up
        if yards:
            yardage = sum(map(float, yards))
    return yardage