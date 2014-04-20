
def is_number(a):
    if a<='9' and a>= '0':
        return True
    return False


def get_number( string ):
    found_number = False
    number = 0
    for i in range(len(string)):

        if is_number(string[i]):
            number *= 10
            number += int(string[i])
            if found_number == False:
                found_number = True

        else:
            if found_number:
                break

    return number

