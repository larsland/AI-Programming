def read_2048_file(file_path):
    data = []
    with open(file_path) as mini:
        i = 0
        block = {}
        block['board'] = []
        for line in mini:
            if line.find('Move') == 0:
                i += 1
                if block != {'board': []}:
                    block['board'] = np.array(block['board']).flatten().tolist()
                    yield block
                    block = {}
                block['board'] = []
                block['score'] = line.split('=')[1].rstrip('\r\n')
            else:
                # print(line)
                row = line.split(' ')
                flat_board = []
                if len(row) > 1:
                    for item in row:
                        item = item.rstrip('\r\n')
                        if item != '':
                            item = int(item)
                            if item == 0:
                                flat_board.append(0)
                            else:
                                flat_board.append(int(math.log2(int(item))))
                    block['board'].append(flat_board)
                else:
                    item = row[0].rstrip('\r\n')
                    if item != '':
                        block['move'] = int(item)

        block['board'] = np.array(block['board']).flatten().tolist()
        yield block


def write_training_data(in_file, out_file):
    errors = 0
    with open(out_file, 'w') as testorama:
        for block in read_2048_file(in_file):
            try:
                line = '%s, %i, %s\n' % (block['board'], block['move'], block['score'])
                testorama.write(line)
            except KeyError:
                errors += 1
                pass

        print("experienced %s errors" % errors)
