from data import db
import main
import login
import getopt, sys
import os

cdict = {
    'S': "Safad",
    't':"Tulkarm",
    'j':"jaffa",
    'R':"Ramallah",
    'A':"Acre",
    'H':"Haifa",
    'T':"Tiberias",
    'N':"Nazareth",
    'B':"Baysan",
    'J':"Jinin",
    'al':"al-Ramla",
    'Al':"Al-Quds",
    'h':"Hebron",
    'b':"Beersheba",
    'G':"Gaza",
    'n':"Nablus"
}

NAMES_TO_HEX = {
    "aliceblue": "#f0f8ff",
    "antiquewhite": "#faebd7",
    "aqua": "#00ffff",
    "aquamarine": "#7fffd4",
    "azure": "#f0ffff",
    "beige": "#f5f5dc",
    "bisque": "#ffe4c4",
    "black": "#000000",
    "blanchedalmond": "#ffebcd",
    "blue": "#0000ff",
    "blueviolet": "#8a2be2",
    "brown": "#a52a2a",
    "burlywood": "#deb887",
    "cadetblue": "#5f9ea0",
    "chartreuse": "#7fff00",
    "chocolate": "#d2691e",
    "coral": "#ff7f50",
    "cornflowerblue": "#6495ed",
    "cornsilk": "#fff8dc",
    "crimson": "#dc143c",
    "cyan": "#00ffff",
    "darkblue": "#00008b",
    "darkcyan": "#008b8b",
    "darkgoldenrod": "#b8860b",
    "darkgray": "#a9a9a9",
    "darkgrey": "#a9a9a9",
    "darkgreen": "#006400",
    "darkkhaki": "#bdb76b",
    "darkmagenta": "#8b008b",
    "darkolivegreen": "#556b2f",
    "darkorange": "#ff8c00",
    "darkorchid": "#9932cc",
    "darkred": "#8b0000",
    "darksalmon": "#e9967a",
    "darkseagreen": "#8fbc8f",
    "darkslateblue": "#483d8b",
    "darkslategray": "#2f4f4f",
    "darkslategrey": "#2f4f4f",
    "darkturquoise": "#00ced1",
    "darkviolet": "#9400d3",
    "deeppink": "#ff1493",
    "deepskyblue": "#00bfff",
    "dimgray": "#696969",
    "dimgrey": "#696969",
    "dodgerblue": "#1e90ff",
    "firebrick": "#b22222",
    "floralwhite": "#fffaf0",
    "forestgreen": "#228b22",
    "fuchsia": "#ff00ff",
    "gainsboro": "#dcdcdc",
    "ghostwhite": "#f8f8ff",
    "gold": "#ffd700",
    "goldenrod": "#daa520",
    "gray": "#808080",
    "grey": "#808080",
    "green": "#008000",
    "greenyellow": "#adff2f",
    "honeydew": "#f0fff0",
    "hotpink": "#ff69b4",
    "indianred": "#cd5c5c",
    "indigo": "#4b0082",
    "ivory": "#fffff0",
    "khaki": "#f0e68c",
    "lavender": "#e6e6fa",
    "lavenderblush": "#fff0f5",
    "lawngreen": "#7cfc00",
    "lemonchiffon": "#fffacd",
    "lightblue": "#add8e6",
    "lightcoral": "#f08080",
    "lightcyan": "#e0ffff",
    "lightgoldenrodyellow": "#fafad2",
    "lightgray": "#d3d3d3",
    "lightgrey": "#d3d3d3",
    "lightgreen": "#90ee90",
    "lightpink": "#ffb6c1",
    "lightsalmon": "#ffa07a",
    "lightseagreen": "#20b2aa",
    "lightskyblue": "#87cefa",
    "lightslategray": "#778899",
    "lightslategrey": "#778899",
    "lightsteelblue": "#b0c4de",
    "lightyellow": "#ffffe0",
    "lime": "#00ff00",
    "limegreen": "#32cd32",
    "linen": "#faf0e6",
    "magenta": "#ff00ff",
    "maroon": "#800000",
    "mediumaquamarine": "#66cdaa",
    "mediumblue": "#0000cd",
    "mediumorchid": "#ba55d3",
    "mediumpurple": "#9370db",
    "mediumseagreen": "#3cb371",
    "mediumslateblue": "#7b68ee",
    "mediumspringgreen": "#00fa9a",
    "mediumturquoise": "#48d1cc",
    "mediumvioletred": "#c71585",
    "midnightblue": "#191970",
    "mintcream": "#f5fffa",
    "mistyrose": "#ffe4e1",
    "moccasin": "#ffe4b5",
    "navajowhite": "#ffdead",
    "navy": "#000080",
    "oldlace": "#fdf5e6",
    "olive": "#808000",
    "olivedrab": "#6b8e23",
    "orange": "#ffa500",
    "orangered": "#ff4500",
    "orchid": "#da70d6",
    "palegoldenrod": "#eee8aa",
    "palegreen": "#98fb98",
    "paleturquoise": "#afeeee",
    "palevioletred": "#db7093",
    "papayawhip": "#ffefd5",
    "peachpuff": "#ffdab9",
    "peru": "#cd853f",
    "pink": "#ffc0cb",
    "plum": "#dda0dd",
    "powderblue": "#b0e0e6",
    "purple": "#800080",
    "red": "#ff0000",
    "rosybrown": "#bc8f8f",
    "royalblue": "#4169e1",
    "saddlebrown": "#8b4513",
    "salmon": "#fa8072",
    "sandybrown": "#f4a460",
    "seagreen": "#2e8b57",
    "seashell": "#fff5ee",
    "sienna": "#a0522d",
    "silver": "#c0c0c0",
    "skyblue": "#87ceeb",
    "slateblue": "#6a5acd",
    "slategray": "#708090",
    "slategrey": "#708090",
    "snow": "#fffafa",
    "springgreen": "#00ff7f",
    "steelblue": "#4682b4",
    "tan": "#d2b48c",
    "teal": "#008080",
    "thistle": "#d8bfd8",
    "tomato": "#ff6347",
    "turquoise": "#40e0d0",
    "violet": "#ee82ee",
    "wheat": "#f5deb3",
    "white": "#ffffff",
    "whitesmoke": "#f5f5f5",
    "yellow": "#ffff00",
    "yellowgreen": "#9acd32",
}

INFO = {
    "github": "https://github.com/AnasMady22/jaffa",
    "whoareu": "Sigmas"
}

def hydra_check(passwd):
    with open("data\hydra_list.txt", 'r') as file:
        for x in file.readlines():
            if passwd == login.hash(x.strip()):
                return x
        else: return None

def getter(command: str, general_history, command_history, nodes:dict, graph: dict, uname):
    command = command.split()
    if command[0] == "show":
        _return = ""
        argumentList = command[1:]
        options = "hcAsgnt"
        long_options = ["help", "cities", "cities-ne", "command-history", "general-history", "nodes", "time"]
        try:
            arguments, values = getopt.getopt(argumentList, options, long_options)
            for currentArgument, currentValue in arguments:
                
                if currentArgument in ("-h", "--help"): _return += db.show_help_message 
                elif currentArgument in ("-c", "--cities"): _return += " \n".join(graph.keys()) + "\n"
                elif currentArgument in ("-A", "--cities-ne"):
                    list = ""
                    for x in graph: list += f"{x} {graph[x]}\n"
                    return list
                elif currentArgument in ("-s", "--command-history"): _return += " \n".join(command_history) + "\n"
                elif currentArgument in ("-g", "--general-history"): _return += " \n".join(general_history) + "\n"
                elif currentArgument in ("-t", "--time"): _return += main.Jaffa.get_time("") + "\n"
                elif currentArgument in ("-n", "--nodes"):
                    list = ""
                    for x in nodes: list += f"{x} {nodes[x]}\n"
                    _return += list
                _return += '\n'
        except getopt.error as err: return str(err)
        return _return[:-1]
    elif command[0] == "history":
        _return = ""
        argumentList = command[1:]
        options = "hcg"
        long_options = ["help", "command-history", "general-history"]

        try:
            arguments, values = getopt.getopt(argumentList, options, long_options)
            for currentArgument, currentValue in arguments:
                
                if currentArgument in ("-h", "--help"): _return += db.history_help_message 
                elif currentArgument in ("-c", "--command-history"): _return += " \n".join(command_history) + "\n"
                elif currentArgument in ("-g", "--general-history"): _return += " \n".join(general_history) + "\n"
                _return += '\n'
        except getopt.error as err: return str(err)
        return _return[:-1]
    elif command[0] == "go":
        _from = _to = read = wiki = 0
        _return = ""
        argumentList = command[1:]
        options = "hf:t:WR"
        long_options = ["help", "from=", "to=", "WIKI", "READ"]

        try:
            arguments, values = getopt.getopt(argumentList, options, long_options)
            for currentArgument, currentValue in arguments:
                
                if currentArgument in ("-h", "--help"): return ["go", db.go_help_message ]
                elif currentArgument in ("-f", "--from"):
                    _from = currentValue
                elif currentArgument in ("-t", "--to"):
                    _to = currentValue
                elif currentArgument in ("-W", "--WIKI"): wiki = 1
                elif currentArgument in ("-R", "--READ"): read = 1
            if _from and len(_from) < 3: _from = cdict[_from]
            if _to and len(_to) < 3: _to = cdict[_to]
            if _from and _to: return['go', _from, _to, wiki, read]
            if read or wiki or values: return['go', "you must enter -f {from} and -t {to}"]
            return['go', '']
        except getopt.error as err: return ["go", str(err)]
    elif command[0] == "chuname":
        passwd = new_username = ''
        argumentList = command[1:]
        options = "hp:n:"
        long_options = ["help", "passwd=", "new-username="]

        try:
            arguments, values = getopt.getopt(argumentList, options, long_options)
            for currentArgument, currentValue in arguments:
                
                if currentArgument in ("-h", "--help"): return ["go", db.go_help_message ]
                elif currentArgument in ("-p", "--passwd"):
                    passwd = currentValue
                    if not login.check(uname, login.hash(passwd)): return f"incorrect password." 
                elif currentArgument in ("-n", "--new-username"):
                    new_username = currentValue
            if passwd and new_username: return['chuname', new_username]
            if not passwd: return "you have to enter your password."
            if not new_username: return "you have to enter a new name."
            return ""
        except getopt.error as err: return str(err)
    elif command[0] == "music":
        song = 0
        volume = 0.2
        argumentList = command[1:]
        options = "hs:v:"
        long_options = ["help", "song=", "volume"]

        try:
            arguments, values = getopt.getopt(argumentList, options, long_options)
            if "stop" in values: return ["music", "stop"]
            for currentArgument, currentValue in arguments:
                if currentArgument in ("-h", "--help"): return ["music", db.music_help_message]
                elif currentArgument in ("-s", "--song"): song = currentValue
                elif currentArgument in ("-v", "--volume"): volume =  currentValue
            if song: return ["music", int(song)-1, float(volume)]
            elif values or volume: return ["music", "you have to Enter the song number by -s"]
            else: return ["music", ""]
        except getopt.error as err: return str(err)
    elif command[0] == "su":
        username = passwd = 0
        argumentList = command[1:]
        options = "hu:p:"
        long_options = ["help", "username=", "passwd="]

        try:
            arguments, values = getopt.getopt(argumentList, options, long_options)
            for currentArgument, currentValue in arguments:
                if currentArgument in ("-h", "--help"): return ["su", db.su_help_message]
                elif currentArgument in ("-u", "--username"): username = currentValue
                elif currentArgument in ("-p", "--passwd"): passwd =  currentValue
            if username and passwd: return ["su", username, passwd]
            elif username or passwd: return ["su", "you have to Enter the the username by -u and the password by -p."]
            else: return ["su", ""]
        except getopt.error as err: return ["su", str(err)]
    elif command[0] == "game":
        _return = ""
        argumentList = command[1:]
        options = "h"
        long_options = ["help"]

        try:
            arguments, values = getopt.getopt(argumentList, options, long_options)
            for currentArgument, currentValue in arguments:
                if currentArgument in ("-h", "--help"): return db.game_help_message
            for currentValue in values:
                if currentValue == "start": return ["game", "start"]
            return ""
        except getopt.error as err: return str(err)
    elif command[0] == "is":
        if len(command) != 3: return "is take two arguments! try again."
        try:
            if command[1] == command[2]: return "Yes"
            else : return "No"
        except:
            return "mmmmm.. you trying to make some thing bad right!"
    elif command[0] == "hash":
        _return = ""
        argumentList = command[1:]
        options = "h"
        long_options = ["help"]

        try:
            arguments, values = getopt.getopt(argumentList, options, long_options)
            for currentArgument, currentValue in arguments:
                if currentArgument in ("-h", "--help"): return db.hash_help_message
            for _pass in values:
                _return += _pass + ": " + login.hash(_pass) + "\n"
            return _return
        except getopt.error as err: return str(err)
    elif command[0] == "hydra":
        _return = ""
        argumentList = command[1:]
        options = "hp:"
        long_options = ["help","passwd="]

        try:
            arguments, values = getopt.getopt(argumentList, options, long_options)
            for currentArgument, currentValue in arguments:
                if currentArgument in ("-h", "--help"): return db.hydra_help_message
                elif currentArgument in ("-p", "--passwd"):
                    x = hydra_check(currentValue)
                    return f"the password is: {x}" if x else "There are no matches!"
            for currentValue in values:
                if currentValue.lower() == 'list': return ['hydra']
            return ''
        except getopt.error as err: return str(err)
    elif command[0] == "ls": return "\n".join(os.listdir())
    elif command[0] == "pwd": return os.getcwd()
    elif command[0] == "cd":
        try:
            os.chdir(command[1])
            return ""
        except:
            return "The system cannot find the path specified."
    elif command[0] == "mode":
        _return = ""
        argumentList = command[1:]
        options = ""

        try:
            arguments, values = getopt.getopt(argumentList, options)
            for currentValue in values:
                if currentValue == "dark": return ['mode', 'dark']
                elif currentValue == "light": return ['mode', 'light']
                elif currentValue == "cmd": return ['mode', 'cmd']
                
        except getopt.error as err: return ["mode",str(err)]
        return ["mode",'unknown parameter, you can use {dark, light, cmd}']
    elif command[0] == "newcity" or command[0] == "addcity":
        c, d = 0, 1
        if len(command) == 1 or command[1] == '-h' or command[1] == '--help':
            return db.newcity_help_message
        if "--silence" in command:
            command.remove("--silence")
            d = 0
        if command[1] == '-n' or command[1] == '--name':
            c += 1
            name = command[2]
        if command[3] == '-x' or command[3] == '--xaxis':
            c += 1
            x = command[4]
        if command[5] == '-y' or command[5] == '--yaxis':
            c += 1
            y = command[6]
        if command[7] == '-nb' or command[7] == '--neighbours':
            c += 1
            nb = command[8:]
        if c == 4:
            return ['newcity',name,int(x),int(y),nb,d]
        return 'not found parameter, try -h for help'
    elif command[0] == "adduser":
        name = new_passwd = 0
        passwd = ""
        if '-h' in command or '--help' in command or len(command) == 1: return db.adduser_help_message
        if '-n' in command or '--name' in command:
            try: 
                try: name = command[command.index('-n')+1]
                except: name = command[command.index('--name')+1]
            except: return 'You must enter username by -n or --name, try -h for help'
        if '-p' in command or '--passwd' in command:
            try:
                try: passwd = command[command.index('-p')+1]
                except: passwd = command[command.index('--passwd')+1]
            except: return 'You must enter a password by -p or --passwd, try -h for help'
        if name and passwd:
            return ['adduser',name,passwd]
        return 'unknown parameter! you must add -n and -p, try -h for help'
    elif command[0] == "chpasswd":
        name = new_passwd = 0
        passwd = ""
        if '-h' in command or '--help' in command or len(command) == 1: return db.chpasswd_help_message
        if '-u' in command or '--username' in command:
            try: 
                try: name = command[command.index('-u')+1]
                except: name = command[command.index('--username')+1]
            except: return 'You must enter username by -n or --name, try -h for help'
        if '-p' in command or '--passwd' in command:
            try:
                try: passwd = command[command.index('-p')+1]
                except: passwd = command[command.index('--passwd')+1]
            except: return 'You must enter a password by -p or --passwd, try -h for help'
        if '-n' in command or '--new' in command:
            try:
                try: new_passwd = command[command.index('-n')+1]
                except: new_passwd = command[command.index('--new')+1]
            except: return 'You must enter a new password by -n or --new, try -h for help'
        if name and new_passwd:
            return ['chpasswd',name, passwd, new_passwd]
        return 'unknown parameter! you must add -n and -p, try -h for help'
    elif command[0] == "color":
        if len(command) == 1 or command[1] == '-h' or command[1] == '--help': return db.color_help_message
        elif command[1] == '-r' or command[1] == "reset" : return ['color',"reset"]
        elif command[1][0] == '#' and len(command[1]) == 7: return ['color',command[1]]
        elif command[1][0] == '#' and len(command[1]) != 7: return f'you must Enter 6 HEX values not {len(command[1])-1}'
        elif command[1] in NAMES_TO_HEX.keys(): return ['color',NAMES_TO_HEX[command[1]]]
        else: return "unknown parameter!"
    elif command[0] == "back" or command[0] == 'ارجع': return ['back']
    elif command[0] == "cat":
        argumentList = command[1:]
        try:
            arguments, values = getopt.getopt(argumentList, "", "")
            for currentValue in values:
                if currentValue == "/etc/shadow" or currentValue == "/etc/passwd":
                    if uname == 'root' or uname == 'dev':
                        with open("data\db.csv", 'r') as file: return file.read()
                    else: return 'you have no permission to see this file.'
                try:
                    with open(currentValue, 'r') as file: return file.read()
                except: 
                    return f'No such file or directory: {currentValue}'
        except getopt.error as err: return str(err)
    
    elif command[0] in INFO.keys(): return INFO[command[0]]
    elif command[0] == "?" or command[0] == "مساعده":
        return db.main_help
    return "command not found!"