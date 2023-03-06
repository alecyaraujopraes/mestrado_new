import argparse

argParser = argparse.ArgumentParser()
argParser.add_argument("-n", "--name", help="your name")
argParser.add_argument("-s", "--second", help="your second name")

args = argParser.parse_args()

print(args.name, args.second)