def make_w(right,pred,pos):
    final = ''
    count = 0
    counter = 0
    for i in pred:
        if count == pos[counter]:
            final += right[pos[counter]]
            if counter + 1 != len(pos):
                counter += 1
        else:
            final += '_'
        count += 1
    return final
pred = '_______'
right = 'present'
pos = [2,4]
result = make_w(right,pred,pos)
print(result)
