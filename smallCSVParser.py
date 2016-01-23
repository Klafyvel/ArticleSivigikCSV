def csv_to_cell(s, converter=str):
    c = ""
    for x,i in enumerate(s):
        if i is ",":
            yield (converter(c),'END_CELL')
            c=""
        elif i is "\n":
            yield (converter(c),'END_LINE')
            c=""
        else:
            c+=i
    try:
        yield (converter(c),'END_LINE')
    except ValueError:
        pass

def build_table(s, converter=str):
    table = []
    row = []
    for i in csv_to_cell(s,converter):
        row.append(i[0])
        if i[1] == "END_LINE":
            table.append(row[:])
            row = []
    return table

def table_from_file(filename,converter=str):
    r=None
    with open(filename, "r") as f:
        r = build_table(f.read())
    return r

def csv_to_line(lines, converter=str):
    for l in lines:
        yield [c[0] for c in csv_to_cell(l, converter)]


def create_dict_from_columns(table):
    d = {}
    eq = {}
    for x,cell in enumerate(table[0]):
        d[cell] = []
        eq[cell] = x
    for key in d:
        for row in table[1:]:
            d[key].append(row[eq[key]])
    return d

def dict_from_file(filename, converter=float):
    r=None
    with open(filename, "r") as f:
        r = f.read()
    assert r

    table = []
    row = []
    r = r.split('\n')
    for c in csv_to_cell(r[0],str):
        row.append(c[0])
    table.append(row[:])
    row = []
    for c in csv_to_cell('\n'.join(r[1:]), converter):
        row.append(c[0])
        if c[1] == "END_LINE":
            table.append(row[:])
            row = []
    return  create_dict_from_columns(table)

def reader():
    while True:
        yield input("> ")

def printer(it):
    for i in it:
        print(i)

if __name__ == '__main__':
    print(dict_from_file("ValeursBidon.csv"))