import time


def read_file():
    with open('retrievability.txt', 'r') as f:
        f.seek(0,2)
        while True:
            line = f.readline()
            if not line:
                time.sleep(0.1)
                continue
            yield line



def main():
    log_lines = read_file()
    for line in log_lines:
        print line

if __name__ == "__main__":
    main()