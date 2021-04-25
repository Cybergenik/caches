import pandas as pd
import numpy as np

class SACache:
    def __init__(self, blksize:int, rows:int, ways:int):
        self.blksize = blksize
        self.rows = rows
        self.ways = ways
        self.LRUsize = self.getint(int(np.ceil(np.log2(self.ways))))
        self.cycles = 0
        self.miss_cycle_cost = 11 + 3*(self.blksize / 4)
        self.cache = {}
        self.hits = []
        for i in range(self.ways):
            self.cache[f'V{i}'] = [0 for _ in range(self.rows)]
            self.cache[f'tag{i}'] = [0 for _ in range(self.rows)]
            self.cache[f'lru{i}'] = [0 for _ in range(self.rows)]
            self.cache[f'add{i}'] = [None for _ in range(self.rows)]
    
    def getint(self, x:int) -> int:
        return int(''.join(["1" for _ in range(x)]), 2)

    def update(self, i:int):
        for j in range(self.ways):
            if self.cache[f'V{j}'][i] == 1:
                self.cache[f'lru{j}'][i] += 1

    def lookup(self, addr:int) -> None:
        block = int(addr / self.blksize)
        index = int(block % self.rows)
        tag = int(addr / self.rows / self.blksize)

        hit = False
        for i in range(self.ways):
            if self.cache[f'tag{i}'][index] == tag and self.cache[f'V{i}'][index] == 1:
                self.hits.append(f'Hit: {addr}')
                self.cycles += 1
                return

        #Miss
        self.hits.append(f'Miss: {addr}')
        self.cycles += self.miss_cycle_cost

        #if empty datablock add data
        for j in range(self.ways):
            if self.cache[f'V{j}'][index] == 0:
                self.cache[f'V{j}'][index] = 1
                self.cache[f'tag{j}'][index] = tag
                self.cache[f'add{j}'][index] = addr
                self.update(index)
                return

        for k in range(self.ways):
            if self.cache[f'lru{k}'][index] == self.LRUsize:
                self.cache[f'lru{k}'][index] = 0
                self.cache[f'tag{k}'][index] = tag
                self.update(index)

    def showhits(self) -> None:
        print(", ".join(self.hits))

    def showcache(self) -> None:
        print(pd.DataFrame(self.cache))

    def size(self) -> int:
        tagsize = (16 - np.log2(self.blksize)) - np.log2(self.rows)
        datasize = self.blksize * 8
        return (tagsize + datasize + 1) * self.ways * self.rows

    def reset(self) -> None:
        self.cycles = 0
        self.hits = []