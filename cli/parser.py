import argparse
from backend.dh import DevHelper

def parse():
    parser = argparse.ArgumentParser()
    parser.add_argument("cmd", 
        choices=DevHelper.commands,
        nargs="*"
    )
    parser.add_argument('-path', '-p', type=str, default='default')
    parser.add_argument('-filter', '-f', type=str)
    parser.add_argument('-project', '-pr', type=str, default=None)
    parser.add_argument('-description', '-d', type=str)
    parser.add_argument('-command', '-c', type=str, default=None)
    parser.add_argument('-ask', '-ask', type=str)
    parser.add_argument("-name", "-n", type=str, default=None)
    args = parser.parse_args()
    dh = DevHelper(args)
    dh.execute()


if __name__ == '__main__':
    parse()