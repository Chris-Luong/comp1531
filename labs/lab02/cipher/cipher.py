def cipher(key, m):
    kl = len(key)

    m = ''.join([ char for char in m if char.isalpha() ])
    cipher = [list(key)]
    t = len(m) // kl

    if len(m) % kl != 0:
      t += 1

    mt = 0
    alpha = 'abcdefghijklmnopqrstuvwxyz'
    alph = 0
    for x in range(1, t+1):
      cipher.append([])
      for y in range(kl):
        try:
          cipher[x].append(m[mt])
        except IndexError:
          if alph > 25:
            alph = 0
          cipher[x].append(alpha[alph])
          alph += 1
        mt += 1

    colcipher = []
    for a in range(kl):
      colcipher.append([])
      for b in range(len(cipher)):
        colcipher[a].append(cipher[b][a])
    def sorta(lst):
      return lst[0]
    colcipher.sort(key=sorta)

    for c in range(len(colcipher)):
      del colcipher[c][0]
    return ''.join([ ''.join(lst) for lst in colcipher ])
