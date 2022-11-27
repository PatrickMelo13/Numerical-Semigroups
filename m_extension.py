import numpy as np
import math

class m_extension: # m-extension class, defined by it's pseudo characteristics relative to numerical semigroups

    def __init__(self, ns=[], ap=[], kunz=[], gapset=[], g:int=0, m:int=1, c:int=0):
        self.g: int = g # Genus
        self.m: int = m # Multiplicity
        self.c: int = c # Conductor
        self.q: int = int(math.ceil(c/m)) # Depth
        self.ns = np.array(ns) # Numerical Semigroup
        self.gapset = np.array(gapset) # Gapset
        self.ap = np.array(ap) # Apéry Set
        self.kunz = np.array(kunz) # Kunz Coordinates
        self.bitset = np.array([]) # Bitset vector (helps computational operations on ns)

        # Get invariants from Kunz coordinates
        if self.kunz.size != 0:
            self.m = len(self.kunz) + 1
            for i in range(len(self.kunz)):
                self.g += self.kunz[i]
                if self.kunz[i] >= self.q:
                    self.q = self.kunz[i]
                    self.c = i+2
            self.c += self.m * (self.q-1)

        # Get invariants from Apéry set
        elif self.ap.size != 0:
            self.m = len(self.ap)
            for i in range(len(self.ap)):
                self.g += int((self.ap[i]-i)/m)
                if self.ap[i] > self.c:
                    self.c = self.ap[i]
            self.q = math.ceil(self.c/self.m)

        # Get invariants from numerical semigroup
        elif self.ns.size != 0:
            self.g = self.ns[-1] - len(self.ns) + 1
            self.m = self.ns[1]
            self.c = self.ns[-1]
            self.q = math.ceil(self.c/self.m)

        # Get invariants from gapset
        elif self.gapset.size != 0:
            self.g = len(self.gapset)
            self.c = self.gapset[-1]+1
            if self.g == self.c-1:
                self.m = self.c
            else:
                for i in range(len(self.gapset)):
                    if self.gapset[i] != i+1:
                        self.m = i+1
                        break
            self.q = math.ceil(self.c/self.m)


    def Ap_to_Kunz(self):
        self.kunz = np.zeros((self.m-1,1))
        for i in range(self.ap.size):
            if i == 0:
                continue
            self.kunz[i-1] = int((self.ap-i)/self.m)

    def Ns_to_Ap(self):
        self.ap = np.zeros((self.m,1))
        for i in range(self.ns.size):
            congruence:int = self.ns[i]%self.m
            if self.ap[congruence] == 0:
                self.ap[congruence] = self.ns[i]
        for i in range(self.ap.size):
            if self.ap[i] == 0:
                self.ap[i] = self.q*self.m+i
        

    def Gapset_to_Kunz(self):
        pass

    def Kunz_to_Bitset(self):
        pass

    def Verify_element(self,i):
        pass

    def Verify_ns(self):

        # Create numerical semigroup if not existent
        if self.bitset.size == 0:
            if self.kunz.size == 0:
                if self.ns.size != 0:
                    self.Ns_to_Ap()
                    self.Ap_to_Kunz()
                elif self.ap.size != 0:
                    self.Ap_to_Kunz()
                elif self.gapset.size != 0:
                    self.Gapset_to_Kunz()
            self.Kunz_to_Bitset()

        # Verify if every element is a valid element, i.e., if the m-extension is a numerical semigroup
        for i in range(self.bitset.size):
            if self.bitset[i]:
                if self.Verify_element(i) == False:
                    return False
        return True
