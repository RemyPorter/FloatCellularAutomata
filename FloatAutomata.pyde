#Rule should be an array of 8 floating point values between 0 and 1.
#NB: there's no error checking, so you might get unpredictable results if you violate that rule
#change rule to other values. The output will be saved to a .TIF file with a name based on the rule

#rule is also expressed with the least-significant float, first.
#if you use only the values 0 and 1, this is your basic elementary automata
rule = [0.81, 1, 0.08, 0.001, 0.65, 0.000513, 0, 0.99999999]

########################################    
current_row = None
rowcount = 0

def apply_rule(rule, trio):
    """
    So, I did build this so that it can *theoretically* work with values outside of the range
    0-1. I'm not really sure WHY I did that, but it does work.
    But basically, the whole idea here is that this takes the average of the weighted average
    of the floor and ceiling, and uses that to determine the next cell state.
    """
    l,c,r = trio
    raw = (l * 4 + c  * 2 + r) - 1.0
    bottom = floor(raw)
    top = ceil(raw)
    ratio = top - raw
    a = rule[bottom]
    b = rule[top]
    return ((a * (1 - ratio)) + (b * ratio) / 2.0)
    
def float_to_color(fl):
    return color(255*fl, 255*fl, 255*fl, fl)

def draw_row(row, offset=0, rowwidth=640):
    loadPixels()
    start_index = rowwidth * offset
    for i,col in enumerate(row):
        pixels[start_index + i] = float_to_color(col)
    updatePixels()
    
def iter_in_groups(l, groupsize = 3):
    res = l[0:groupsize]
    yield res
    for i in l[groupsize:]:
        res = res[1:] + [i]
        yield res
    
def seed(rowwidth=640):
    return [1.0 if 1 == i else 0.0 for i in range(rowwidth)]
    
def saveImage(ruleArray):
    stringed = [str(i) for i in reversed(ruleArray)]
    file = "-".join(stringed) + ".tif"
    save(file)

def setup():
    global current_row, rowcount
    size(640, 640, P3D)
    background(color(0x000000))
    first_row = seed()
    draw_row(first_row)
    current_row = first_row
    rowcount += 1
    randomSeed(0)
    
def draw():
    global current_row, rowcount
    if rowcount >= height:
        saveImage(rule)
        return
    next_row = [current_row[0]]
    for trio in iter_in_groups(current_row):
        center = apply_rule(rule, trio)
        next_row.append(center)
    next_row.append(current_row[-1])
    draw_row(next_row, rowcount)
    rowcount+=1
    current_row = next_row