import csv

def to_int(string, f = False):
    if type(string) == str:
        if f:
            if string[0] == "-":
                return (-1) * round(float(string[1:]), 1)
            else:
                return round(float(string), 1)
        else:
            if string[0] == "-":
                return (-1) * int(string[1:])
            else:
                return int(string)    
    return 0

def extract_commands(file_name):
    """
    Takes in filename and loads the appropriate CSV file
    Returns two dicts containing seperate lists for the values under each category
    """
    COMMANDS = {'TIME': []}
    RAW_COMMANDS = []
    
    with open(file_name, 'r') as file:
        reader = csv.reader(file)
        for row in reader:
            if not row[0][0].isdigit() and not row[0][0] == '-':
                continue
            if row[1] not in COMMANDS.keys():
                COMMANDS[row[1].upper()] = []
            RAW_COMMANDS.append([to_int(row[0], True), row[1].upper(), to_int(row[2], True), 
                                 to_int(row[3], True), to_int(row[4], True),]) 
                                 #starttime, category, str, freq, duration

    t = 0
    end_time = RAW_COMMANDS[-1][0] + RAW_COMMANDS[-1][4]
    while(t <= end_time + 0.01):
        for cat in COMMANDS:
            if cat == 'TIME':
                COMMANDS[cat].append(round(t, 2))
            else:
                COMMANDS[cat].append(0)
        t += 0.1
        
    print(RAW_COMMANDS)
    for com in RAW_COMMANDS:
        t = com[0] #starttime
        i = int(com[0]*10)
        while(t <= com[0] + com[4] + 0.01):
            COMMANDS[com[1]][i] = com[2]
            t += 0.1
            i += int(1)
    
    return COMMANDS

print(extract_commands('c_user_2022_11_10_00_00_00.csv'))