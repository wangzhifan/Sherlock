import sys


stepping = True
breakpoints = {9:True, 14:True}

def traceit(frame, event, arg):
    # frame.f_locals['tag'] = True
    global stepping
    global breakpoints

    if event == 'Line':
        if stepping or breakpoints.has_key(frame.f_lineno):
            print event, frame.f_lineno, frame.f_code.co_name, frame.f_locals
    return traceit

sys.settrace(traceit)
#todo
sys.settrace(None)
