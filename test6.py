
def merge_count(state):
    mergable = [0, 0, 0, 0, 0, 0, 0, 0]
    i = 0
    for merge in range(len(mergable)):
        temp = state[i:i+4]
        if temp:
            prev = temp[0]
            for tile in temp[1::]:
                if tile == prev:
                    mergable[merge] = 1
                    break
                prev = tile
            i+=4
            print(temp)

    print(state)
    print(mergable)
    print('-.-.-.-.-.-.-')


if __name__ == '__main__':
    state = [1, 1, 0, 0, 1]