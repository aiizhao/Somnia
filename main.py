########################################################################################
######################          Import packages      ###################################
########################################################################################
from flask import Blueprint, render_template, flash, request
from flask_login import login_required, current_user
import os
import csv  
import json
import plotly, plotly.graph_objects as go
import pandas as pd
from __init__ import create_app, db

########################################################################################
# our main blueprint
main = Blueprint('main', __name__)

@main.route('/') # home page that return 'index'
def index():
    return render_template('index.html')

def to_display_filename(fname, c=False):
    f = fname.split('_')
    if c:
        return 'COMMANDS: ' + f[1] + ' ' + f[2] + '-' + f[3] + '-' + f[4] + ' ' + f[5] + ':' + f[6] + ':' + f[7][:2]
    else:
        return f[0] + ' ' + f[1] + '-' + f[2] + '-' + f[3] + ' ' + f[4] + ':' + f[5] + ':' + f[6][:2] 

def to_filename(fdisplay, c=False):
    f = fdisplay.split(' ')
    if c:
        user = f[1]
        date = f[2].replace('-', '_')
        time = f[3].replace(':', '_')
        return 'c_' + user + '_' + date + '_' + time + '.csv'
    else:
        user = f[0]
        date = f[1].replace('-', '_')
        time = f[2].replace(':', '_')
        return user + '_' + date + '_' + time + '.csv'

def all_data(c=False):
    files = [f for f in os.listdir('.') if (os.path.isfile(f) and f.endswith(".csv"))]
    filenames = []
    for f in files:
        if c:
            if f.count('_') == 7:
                fname = to_display_filename(f, c)
                filenames.append(fname)
        else:
            if f.count('_') == 6:
                fname = to_display_filename(f)
                filenames.append(fname)
    return filenames

@main.route('/profile') # profile page that return 'profile'
@login_required
def profile():
    files = all_data()
    c_files = all_data(True)
    return render_template('profile.html', name=current_user.name, files=files, c_files = c_files)

@main.route('/data_api/', methods=['GET','POST'])
def data_api():
    
    if request.method == 'POST': 
        rows = request.json['data'] #data is in the form of a single string
        name = request.json['name']
        time = request.json['session']
        time1 = time.replace(' ', '_')
        time2 = time1.replace(':', '_')
        time3 = time2.replace('-', '_')
        filename = str(name) + '_' + time3 + '.csv'
        with open(filename, 'a') as myfile: #append to a csv file
            myfile.write(rows)
            
        return 'OK'
    
    if request.method == 'GET': 
        return 'GET test_api'
    
    
@main.route('/command_api/', methods=['GET','POST'])
def command_api():
    if request.method == 'GET':
        filename = request.json['file']
        with open(filename) as f:
            s = f.read() + '\n'
        return repr(s)
    else:
        rows = request.json['data'] #data is in the form of a single string
        name = request.json['name']
        time = request.json['session']
        time1 = time.replace(' ', '_')
        time2 = time1.replace(':', '_')
        time3 = time2.replace('-', '_')
        filename = 'c_' + str(name) + '_' + time3 + '.csv'
        with open(filename, 'a') as myfile: #append to a csv file
            myfile.write(rows)
            
        return 'OK'


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
    
def extract_data(file_name):
    """
    Takes in filename and loads the appropriate CSV file
    Returns two dicts containing seperate lists for the values under each category
    """
    LEFT = {
        'IND': [],
        'GEB': [],
        'GEL': [],
        'AEB': [],
        'AEL': [],
        'CURX': [],
        'CURY': [],
        'INTX': [],
        'INTY': []
    }
    RIGHT = {
        'IND': [],
        'GEB': [],
        'GEL': [],
        'AEB': [],
        'AEL': [],
        'CURX': [],
        'CURY': [],
        'INTX': [],
        'INTY': []
    }
    
    with open(file_name, 'r') as file:
        reader = csv.reader(file)
        for row in reader:
            category = row[2]
            LEFT[category].append(to_int(row[3]))
            RIGHT[category].append(to_int(row[4]))
  
    return((LEFT, RIGHT))
    
@main.route('/test_visualize', methods=['GET'])
@login_required
def test_visualize():
    """
    Uses filename from GET request 'file' parameter
    Calls extract_data() to parse data 
    Creates a plotly figure and renders it in a html page
    """
    f = request.args.get('file')
    fname = to_filename(f)
    files = all_data()
    files.remove(f)
    
    data = extract_data(fname)
    df_l = pd.DataFrame(data[0])
    df_r = pd.DataFrame(data[1])
    
    #SET RANGES
    x_min = min(data[0]['IND'])
    x_max = max(data[0]['IND'])
    
    x_low = request.args.get('x_low', default = str(x_min))
    x_high = request.args.get('x_high', default = str(x_max))
    
    #CREATE PLOT for each category using the index values as the x variable
    fig = plotly.tools.make_subplots(rows=3, cols=1, subplot_titles=('', 'CUR', 'INT'), 
                                     shared_xaxes = True)
    
    g_traces=[
        go.Scatter(
            name = 'GEB (L)',
            x = df_l.IND,
            y = df_l.GEB,
        ),
        go.Scatter(
            name = 'GEB (R)',
            x = df_r.IND,
            y = df_r.GEB
        ),
        go.Scatter(
            name = 'GEL (L)',
            x = df_l.IND,
            y = df_l.GEL
        ),
        go.Scatter(
            name = 'GEL (R)',
            x = df_r.IND,
            y = df_r.GEL
        ),
        go.Scatter(
            name = 'AEB (L)',
            x = df_l.IND,
            y = df_l.AEB
        ),
        go.Scatter(
            name = 'AEB (R)',
            x = df_r.IND,
            y = df_r.AEB
        ),
        go.Scatter(
            name = 'AEL (L)',
            x = df_l.IND,
            y = df_l.AEL
        ),
        go.Scatter(
            name = 'AEL (R)',
            x = df_r.IND,
            y = df_r.AEL
        )
    ]
    
    c_traces=[
        go.Scatter(
            name = 'CURX (L)',
            x = df_l.IND,
            y = df_l.CURX
        ),
        go.Scatter(
            name = 'CURX (R)',
            x = df_r.IND,
            y = df_r.CURX
        ),
        go.Scatter(
            name = 'CURY (L)',
            x = df_l.IND,
            y = df_l.CURY
        ),
        go.Scatter(
            name = 'CURY (R)',
            x = df_r.IND,
            y = df_r.CURY
        )
    ]
    i_traces=[
        go.Scatter(
            name = 'INTX (L)',
            x = df_l.IND,
            y = df_l.INTX
        ),
        go.Scatter(
            name = 'INTX (R)',
            x = df_r.IND,
            y = df_r.INTX
        ),
        go.Scatter(
            name = 'INTY (L)',
            x = df_l.IND,
            y = df_l.INTY
        ),
        go.Scatter(
            name = 'INTY (R)',
            x = df_r.IND,
            y = df_r.INTY
        )
    ]
    
    for trace in g_traces:
        fig.append_trace(trace, 1, 1)
    for trace in c_traces:
        fig.append_trace(trace, 2, 1)
    for trace in i_traces:
        fig.append_trace(trace, 3, 1)
    
    
    title = 'SESSION: ' + str(x_min) + ' to ' + str(x_max)
    
    fig.update_layout(
        title_text = title,
        xaxis3_rangeslider_visible = True
    )
    fig.update_xaxes(range = [x_low, x_high])
    
    
    graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
    
    return render_template('test_visualize.html', graphJSON=graphJSON, f=f, files=files, l=x_low, h=x_high)

def extract_commands(file_name):
    """
    Takes in filename and loads the appropriate CSV file
    Returns two dicts containing seperate lists for the values under each category
    """
    COMMANDS_S = {'TIME': []}
    COMMANDS_F = {}
    RAW_COMMANDS = []
    
    with open(file_name, 'r') as file:
        reader = csv.reader(file)
        for row in reader:
            if not row[0][0].isdigit() and not row[0][0] == '-':
                continue
            if row[1] not in COMMANDS_S.keys():
                COMMANDS_S[row[1].upper()] = []
                COMMANDS_F[row[1].upper()] = []
            RAW_COMMANDS.append([to_int(row[0], True), row[1].upper(), to_int(row[2], True), 
                                 to_int(row[3], True), to_int(row[4], True),]) 
                                 #starttime, category, str, freq, duration

    t = 0
    end_time = RAW_COMMANDS[-1][0] + RAW_COMMANDS[-1][4]
    while(t <= end_time + 0.01):
        for cat in COMMANDS_S:
            if cat == 'TIME':
                COMMANDS_S[cat].append(round(t, 2))
            else:
                COMMANDS_S[cat].append(0)
                COMMANDS_F[cat].append(0)
        t += 0.1
        
    print(RAW_COMMANDS)
    for com in RAW_COMMANDS:
        t = com[0] #starttime
        i = int(com[0]*10)
        while(t <= com[0] + com[4] + 0.01):
            COMMANDS_S[com[1]][i] = com[2]
            COMMANDS_F[com[1]][i] = com[3]
            t += 0.1
            i += int(1)
    
    return COMMANDS_S, COMMANDS_F

@main.route('/command_visualize', methods=['GET'])
@login_required
def command_visualize():
    """
    Uses filename from GET request 'file' parameter
    Calls extract_data() to parse data 
    Creates a plotly figure and renders it in a html page
    """
    f = request.args.get('c_file')
    fname = to_filename(f, True)
    files = all_data(True)
    files.remove(f)
    
    commands = extract_commands(fname)
    df_s = pd.DataFrame(commands[0])
    df_f = pd.DataFrame(commands[1])
    
    #SET RANGES
    x_min = min(commands[0]['TIME'])
    x_max = max(commands[0]['TIME'])
    
    x_low = request.args.get('x_low', default = str(x_min))
    x_high = request.args.get('x_high', default = str(x_max))
    
    #CREATE PLOT for each category using the index values as the x variable
    fig = plotly.tools.make_subplots(rows=2, cols=1, subplot_titles=('Strength', 'Frequency'), 
                                     shared_xaxes = True)
    
    s_traces=[
        go.Scatter(
            name = 'ROCK Strength',
            x = df_s.TIME,
            y = df_s.ROCK,
            fill='tozeroy',
            line=dict(color='#9467bd')
        ),
        go.Scatter(
            name = 'PUSH Strength',
            x = df_s.TIME,
            y = df_s.PUSH,
            fill='tozeroy',
            line=dict(color='#1f77b4')
        ),
        go.Scatter(
            name = 'WAKE Strength',
            x = df_s.TIME,
            y = df_s.WAKE,
            fill='tozeroy',
            line=dict(color='#17becf')
        ),
        go.Scatter(
            name = 'Z',
            x = df_s.TIME,
            y = df_s.TIME * 0,
            fill='tozeroy',
            line=dict(color='#ffffff'),
            showlegend = False
        )
    ]
    
    f_traces=[
        go.Scatter(
            name = 'ROCK Frequency',
            x = df_s.TIME,
            y = df_f.ROCK,
            fill='tozeroy',
            line=dict(color='#9467bd')
        ),
        go.Scatter(
            name = 'PUSH Frequency',
            x = df_s.TIME,
            y = df_f.PUSH,
            fill='tozeroy',
            line=dict(color='#1f77b4')
        ),
        go.Scatter(
            name = 'WAKE Frequency',
            x = df_s.TIME,
            y = df_f.WAKE,
            fill='tozeroy',
            line=dict(color='#17becf')
        ),
        go.Scatter(
            name = 'Z',
            x = df_s.TIME,
            y = df_s.TIME * 0,
            fill='tozeroy',
            line=dict(color='#ffffff'),
            showlegend = False
        )
    ]
    
    for trace in s_traces:
        fig.append_trace(trace, 1, 1)
    for trace in f_traces:
        fig.append_trace(trace, 2, 1)
    
    title = 'DURATION: ' + str(x_max) + ' min'
    
    fig.update_layout(
        title_text = title,
        xaxis2_rangeslider_visible = True
    )
    fig.update_xaxes(range = [x_low, x_high])
    
    graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
    
    return render_template('command_visualize.html', graphJSON=graphJSON, f=f, c_files=files, l=x_low, h=x_high)

app = create_app() # we initialize our flask app using the __init__.py function
if __name__ == '__main__':
    db.create_all(app=create_app()) # create the SQLite database
    app.run(host = '0.0.0.0') # run the flask app on debug mode