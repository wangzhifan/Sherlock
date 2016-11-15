import sys
import readline


def is_int(s):
    try:
        int(s)
        return True
    except ValueError:
        return False

stepping = False
breakpoints = {r'D:\work\Sherlock\otherfile2.py':{9:True, 14:True}}
watchpoints = {r'D:\work\Sherlock\otherfile2.py':{'c': True}}
watchfiles = (r'D:\work\Sherlock\otherfile.py',r'D:\work\Sherlock\otherfile2.py')

def debug(command, arg, my_locals):
    global stepping
    global breakpoints
    global watchpoints

    for wp in watchpoints:
        if watchpoints[wp] is True:
            if my_locals.has_key(wp):
                print wp, " = ", repr(my_locals[wp])

    if command.find(' ') > 0:
        arg = command.split(' ')[1]
    else:
        arg = None

    if command.startswith('s'):
        stepping = True
        return True
    elif command.startswith('c'):
        stepping = False
        return True
    elif command.startswith('q'):
        sys.exit(0)
    elif command.startswith('p'):
        if arg is None:
            print my_locals
        elif my_locals.has_key(arg):
            print arg, " = ", repr(my_locals[arg])
        else:
            print "No such variable: ", arg
            return False
        return True
    elif command.startswith('b'):
        if is_int(arg):
            breakpoints[int(arg)] = True
        else:
            print "You must supply a line number"
            return False
        return True
    elif command.startswith('w'):
        if arg is not None:
            watchpoints[arg] = True
        else:
            print "You must supply a variable name"
        return True
    else:
        print "No such command", repr(command)

    return False

def input_command():
    command = raw_input("(Sherlock) ")
    return command

def traceit(frame, event, arg):
    # frame.f_locals['tag'] = True
    global stepping
    global breakpoints

    if event == 'line':
        if frame.f_code.co_filename in watchfiles:
            isBP = False
            if breakpoints.has_key(frame.f_code.co_filename):
                if frame.f_lineno in breakpoints[frame.f_code.co_filename]:
                    if breakpoints[frame.f_code.co_filename][frame.f_lineno]:
                        isBP = True
            if stepping or isBP:
                resume = False
                while not resume:
                    print event, frame.f_lineno, frame.f_code.co_name, frame.f_locals,frame.f_code.co_filename
                    command = input_command()
                    resume = debug(command, arg, frame.f_locals)
    return traceit

