"""Un module qui gère les opérations sur les polynômes"""

class Polynome():
    def __init__(self, chaine, liste=None):
        if liste != None:
            self.corps = liste
        else:
            liste = chaine.split('+')
            deg = int(chaine.split('x')[-1])
            self.corps = [0] * (deg+1)
            for elt in liste:
                tmp = elt.split('x')
                if len(tmp) < 2:
                    self.corps[0] += int(tmp[0])
                elif len(tmp[1]) < 1 or tmp[1] == ' ':
                    self.corps[1] += int(tmp[0]) if tmp[0] != ' ' else 1
                else:
                    self.corps[int(tmp[1])] += int(tmp[0]) if tmp[0] != ' ' else 1

    def __str__(self):
        res = ''
        for k, elt in enumerate(self.corps):
            if k == 0:
                res += str(elt) + ' + ' if elt != 0 else ''
            elif elt != 0:
                str_k = str(k) if k != 1 else ''
                res += str(elt) + f'x{str_k} + '
        return res[:-3] if res[:-3] != '' else '0'

    def __add__(self, pol2):
        res = [0] * max(len(self.corps), len(pol2.corps))

        for k in range(len(self.corps)):
            res[k] += self.corps[k]

        for k in range(len(pol2.corps)):
            res[k] += pol2.corps[k]

        while res[-1] == 0:
            res.pop()

        return Polynome('', res)

    def __sub__(self, pol2):
        res = [0] * max(len(self.corps), len(pol2.corps))

        for k in range(len(self.corps)):
            res[k] += self.corps[k]

        for k in range(len(pol2.corps)):
            res[k] -= pol2.corps[k]

        while res[-1] == 0:
            res.pop()

        return Polynome('', res)

    def __mul__(self, pol2):
        if str(type(pol2)) == "<class '__main__.Polynome'>":
            res = [0] * (len(self.corps) + len(pol2.corps))

            for k in range(len(self.corps) + len(pol2.corps)):
                for i in range(len(self.corps)):
                    if k-i > -1:
                        try:
                            res[k] += self.corps[i] * pol2.corps[k-i]
                        except:
                            None

            while res[-1] == 0:
                res.pop()

            return Polynome('', res)

        if str(type(pol2)) in ["<class 'int'>", "<class 'float'>"]:
            res = [pol2 * k for k in self.corps]
            return Polynome('', res)

    def __eq__(self, pol2):
        if len(self.corps) != len(pol2.corps):
            return False

        for k in range(len(self.corps)):
            if self.corps[k] != pol2.corps[k]:
                return False

        return True

    def eval(self, val):
        res = 0
        puiss = 1

        for elt in self.corps:
            res += puiss * elt
            puiss *= val
        return res