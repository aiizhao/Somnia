from flask import Flask, render_template, request
import csv  
import json
import plotly
import plotly.graph_objects as go
import pandas as pd
#from flask_cors import CORS

 
app = Flask(__name__)
#CORS(app)


@app.route('/')
def loading():
    return 'Loading Page'


@app.route('/test_api/', methods=['GET','POST'])
def test_api():
    
    if request.method == 'POST': 
        rows = request.json['data'] #data is in the form of a single string
        with open('rows.csv', 'a') as myfile: #append to a csv file
            myfile.write(rows)
            
        return 'OK'
    
    if request.method == 'GET': 
        return


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
            LEFT[category].append(int(row[3]))
            RIGHT[category].append(int(row[4]))
  
    return((LEFT, RIGHT))
    
    
@app.route('/test_visualize', methods=['GET'])
def test_visualize():
    """
    Uses filename from GET request 'file' parameter
    Calls extract_data(filename) to parse data 
    Creates a plotly figure and renders it in a html page
    """
    file_name = request.args.get('file') + '.csv'
    data = extract_data(file_name)
    
    df_l = pd.DataFrame(data[0])
    df_r = pd.DataFrame(data[1])
    
    #create a plot for each category using the index values as the x variable
    fig = go.Figure(data=[
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
        ),
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
        ),
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
    ])
    
    graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
    
    return render_template('test_visualize.html', graphJSON = graphJSON)


if __name__ == '__main__':
    app.run(host='0.0.0.0')