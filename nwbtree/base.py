import h5py
from collections import defaultdict
from nwbinspector import inspect_nwbfile
from pynwb import NWBHDF5IO, validate
from colored import Fore, Style

short_gap = ' '*2
long_gap = ' '*4
T_branch = '├── '
L_branch = '└── '
I_branch = '│   '
blank = ' '*4

terminated = defaultdict(lambda: False)

def colorScheme(scheme):
    global group_color
    global error_color
    global attr_color
    global dataset_color

    if scheme == 'light':
        group_color = (0, 68, 136)
        error_color = (0, 0, 0)
        attr_color = (153, 68, 85)
        dataset_color = (153, 119, 0)
    else:
        group_color = (102, 153, 204)
        error_color = (255, 255, 255)
        attr_color = (238, 153, 170)
        dataset_color = (238, 204, 102)


def display_attributes(group, n):
    """ display the attribute on a single line """
    num_attrs = len(group.attrs)
    front = ""
    for i in range(n):
        if terminated[i]:
            front = front + blank
        else:
            front = front + I_branch

    if num_attrs > 0:
        for i,attr in enumerate(group.attrs):
            if i == num_attrs - 1 and (len(group.keys()) == 0):
                front_edit = front + L_branch
            else:
                front_edit = front + T_branch
            attr_output = front_edit + f"{Fore.rgb(*attr_color)}{attr}{Style.reset}"
            attr_output += short_gap + str(group.attrs[attr])
            print(attr_output)


def display(name, obj):
    """ display the group or dataset on a single line """
    global terminated

    depth = name.count('/')

    # reset terminated dict
    for d in terminated:
        if d > depth:
            terminated[d] = False

    # construct text at the front of line
    subname = name[name.rfind('/')+1:]
    front = ""
    for i in range(depth):
        if terminated[i]:
            front = front + blank
        else:
            front = front + I_branch

    if list(obj.parent.keys())[-1] == subname:
        front += L_branch
        terminated[depth] = True
    else:
        front += T_branch

    # is group
    if isinstance(obj, h5py.Group):
        output = front + f"{Fore.rgb(*group_color)}{subname}{Style.reset}" 
        print(output)
        out = []
        for item in results:
            if item.location == obj.name:
                out.append(item.message)
        for o in out:
            err = ' '*(len(front)+1) + f"{Fore.rgb(*error_color)}{Style.bold}{o}{Style.reset}"
            print(err, end = ' ')
            print()
        display_attributes(obj, depth + 1)

    # is dataset
    elif isinstance(obj, h5py.Dataset):
        output = front + f"{Fore.rgb(*dataset_color)}{subname}{Style.reset}" 
        output += short_gap + f'shape: {obj.shape}, dtype: {obj.dtype}'
        print(output)
        out = []
        for item in results:
            if item.location == obj.name:
                out.append(item.message)
        for o in out:
            err = ' '*(len(front)+1) + f"{Fore.rgb(*error_color)}{Style.bold}{o}{Style.reset}"
            print(err, end = ' ')
            print()

def makeTree(filepath, scheme='dark'):

    colorScheme(scheme)

    global results

    # open file and print tree
    with NWBHDF5IO(path=filepath, mode="r", load_namespaces=True) as read_io:
        nwbfile = read_io.read()
        results = list(inspect_nwbfile(nwbfile_path=filepath))

    # for item in results:
    #     if item.location == None:
    #         print(item)

    with h5py.File(filepath, 'r') as f:
        group = f['/']
        print(f"{Fore.rgb(*group_color)}{filepath}{Style.reset}")
        out = []
        for item in results:
            if item.location == '/':
                out.append(item.message)
        for o in out:
            err = ' ' + f"{Fore.rgb(*error_color)}{Style.bold}{o}{Style.reset}"
            print(err, end = ' ')
            print()

        display_attributes(group, 1)

        group.visititems(display)
