import os

def to_display_filename(fname):
    f = fname.split('_')
    fdisplay = f[0] + ' ' + f[1] + '-' + f[2] + '-' + f[3] + ' ' + f[4] + ':' + f[5] + ':' + f[6][:2] 
    return fdisplay

def to_filename(fdisplay):
    f = fdisplay.split(' ')
    user = f[0]
    date = f[1].replace('-', '_')
    time = f[2].replace(':', '_')
    fname = user + '_' + date + '_' + time + '.csv'
    return fname

def all_data():
    files = [f for f in os.listdir('.') if (os.path.isfile(f) and f.endswith(".csv"))]
    filenames = []
    for f in files:
        name = to_display_filename(f)
        filenames.append(name)
    return filenames
        
print(all_data())
print(to_filename('user1 2022-11-03 15:42:14'))