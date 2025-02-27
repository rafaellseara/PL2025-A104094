import sys

def on_off_sum(input_file : str) -> None:
    with open(input_file, "r") as file:
        content = file.read().lower()

    total = 0
    i = 0
    active = True

    while i < len(content):
        if content[i] == 'o':
            if content[i: i + 2] == 'on':  
                active = True
                i += 1
            elif content[i: i + 3] == 'off':  
                active = False
                i += 3
        elif content[i] == '=':
            print(total)
        elif active and content[i].isdigit():
            total += int(content[i])
        i += 1

if __name__ == "__main__":
    input_file = sys.argv[1]
    on_off_sum(input_file)