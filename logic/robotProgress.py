

mech1 = 75
mech2 = 50
mech3 = 60
mech4 = 35

robot_Progress = (mech1 + mech2 + mech3 + mech4) // 4

def get_robot_progress():
    progress_data = {
        'robot_progress': robot_Progress,  
        'mech1': mech1,
        'mech2': mech2,
        'mech3': mech3,
        'mech4': mech4
    }
    return progress_data
