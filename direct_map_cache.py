import pandas as pd
import numpy as np

class DMCache:
    def __init__(self, blksize:int, rows:int):
        self.blksize = blksize
        self.rows = rows
        self.cycles = 0
        self.miss_cycle_cost = 11 + 3*(self.blksize / 4)
        self.cache = {}
        self.hits = []
        self.cache["V"] = [0 for _ in range(self.rows)]
        self.cache["tag"] = [0 for _ in range(self.rows)]
    
    def update(self, i:int):
        for j in range(self.ways):
            if self.cache[f'V{j}'][i] == 1:
                self.cache[f'LRU{j}'][i] += 1

    def lookup(self, addr:int) -> None:
        block = int(addr / self.blksize)
        index = int(block % self.rows)
        tag = int(addr / self.rows)

        if self.cache["V"][index] != 0 or self.cache["tag"][index] == tag:
            self.hits.append(f'Hit: {addr}')
            self.cycles += 1
        else:
            self.hits.append(f'Miss: {addr}')
            self.cache["V"][index] = 1
            self.cache["tag"][index] = tag
            self.cycles += self.miss_cycle_cost

    def showhits(self) -> None:
        print("\n".join(self.hits))

    def showcache(self) -> None:
        print(pd.DataFrame(self.cache))

    def size(self) -> int:
        tagsize = (16 - np.log2(self.blksize)) - np.log2(self.rows)
        datasize = self.blksize * 8
        return (tagsize + datasize + 1) * self.rows