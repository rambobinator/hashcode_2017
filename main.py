import sys

def run(filename):
    with open(filename) as _file:
        for line in _file:
            print(line)

if __name__ == "__main__":
    if len(sys.argv) == 2:
        run(sys.argv[1])
    else:
        print("No given file !")
