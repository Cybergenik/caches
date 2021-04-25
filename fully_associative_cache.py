import pandas as pd
import numpy as np

class FACache:
    def __init__(self, blksize:int, rows:int):
        self.blksize = blksize
        self.rows = rows
        self.LRUsize = self.getint(int(np.ceil(np.log2(self.rows))))
        self.cycles = 0
        self.miss_cycle_cost = 11 + (3*(self.blksize / 4))
        self.hits = []
        self.cache = pd.DataFrame(np.arange(self.rows), columns=["V"])
        self.cache["tag"] = 0
        self.cache["V"] = 0
        self.cache["LRU"] = 0
    
    def getint(self, x:int) -> int:
        return int(''.join(["1" for _ in range(x)]), 2)

    def update(self):
        for i in range(self.rows):
            if self.cache.loc[i, "V"] == 1:
                self.cache.loc[i, "LRU"] += 1

    def lookup(self, addr:int) -> None:
        tag = int(addr / self.blksize)
        tags = self.cache["tag"]

        if tag in tags.values:
            if self.cache.loc[tags[tags == tag].index[0], "V"] == 1:
                self.hits.append(f'Hit: {addr}')
            else:
                self.hits.append(f'Miss: {addr}')
                valid = self.cache["V"]
                #find next unvalid block and set it
                index = valid[valid == 0].index[0]
                self.cache.loc[index, "V"] = 1
                self.cache.loc[index, "tag"] = tag
                self.update()
        else:
            self.hits.append(f'Miss: {addr}')
            valid = self.cache["V"]
            if 0 in valid.values:
                index = valid[valid == 0].index[0]
                self.cache.loc[index, "V"] = 1
                self.cache.loc[index, "tag"] = tag
                self.update()
            #update this
            else:
                LRU = self.cache["LRU"]
                index = LRU[LRU == self.rows].index[0]
                self.cache.loc[index, "LRU"] = 0
                self.cache.loc[index, "tag"] = tag
                self.update()

    def showhits(self) -> None:
        print("\n".join(self.hits))

    def showcache(self) -> None:
        print(self.cache)

    def size(self) -> int:
        tagsize = (16 - np.log2(self.blksize)) - np.log2(self.rows)
        datasize = self.blksize * 8
        return (tagsize + datasize + 1) * self.rows