def webqq_hash(i, a):
    if isinstance(i, (str, unicode)):
        i = int(i)
    class b:
        def __init__(self, _b, i):
            self.s = _b or 0
            self.e = i or 0

    r = [i >> 24 & 255, i >> 16 & 255, i >> 8 & 255, i & 255]

    j = [ord(_a) for _a in a]

    e = [b(0, len(j) - 1)]
    while len(e) > 0:
        c = e.pop()
        if not (c.s >= c.e or c.s < 0 or c.e > len(j)):
            if c.s+1 == c.e:
                if (j[c.s] > j[c.e]) :
                    l = j[c.s]
                    j[c.s] = j[c.e]
                    j[c.e] = l
            else:
                l = c.s
                J = c.e
                f=j[c.s]
                while c.s < c.e:
                    while c.s < c.e and j[c.e]>=f:
                        c.e -= 1
                        r[0] = r[0] + 3&255

                    if c.s < c.e:
                        j[c.s] = j[c.e]
                        c.s += 1
                        r[1] = r[1] * 13 + 43 & 255

                    while c.s < c.e and j[c.s] <= f:
                        c.s += 1
                        r[2] = r[2] - 3 & 255

                    if c.s < c.e:
                        j[c.e] = j[c.s]
                        c.e -= 1
                        r[3] = (r[0] ^ r[1]^r[2]^r[3]+1) & 255
                j[c.s] = f
                e.append(b(l, c.s-1))
                e.append(b(c.s + 1, J))
    j = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "A",
         "B", "C", "D", "E", "F"]
    e = ""
    for c in range(len(r)):
        e += j[r[c]>>4&15]
        e += j[r[c]&15]

    return e


def newhash(b,j):
    a=j+"password error"
    i=""
    E=[]
    while True:
        if len(i)<=len(a):
            i+=b
            if len(i)==len(a):
                break
        else:
            i=i[0:len(a)]
            break
    for c in range(len(i)):
        E.append(ord(str(i[c]))^ord(str(a[c])))
    print E
    a = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "A", "B", "C", "D", "E", "F"]
    i = ""
    for c in range(len(E)):
        i+=a[E[c] >> 4 & 15]
        i+= a[E[c] & 15]
    return i
#print newhash("578395917","02af31f48cc9211c51f6d9619f744f410f0055c3ab3d2cfe6b5182a5b0b98920")