from set_associative_cache import SACache
from fully_associative_cache import FACache
from direct_map_cache import DMCache

def sa_cache_test(lookups:list) -> None:
    cache = SACache(4, 4, 4)
    for j in lookups:
        cache.lookup(j)
    cache.reset()
    for j in lookups:
        cache.lookup(j)
    #cache.showhits()
    cache.showcache()
    print(cache.size())
    print(cache.cycles)
    print(cache.LRUsize)
    #print(cache.miss_cycle_cost)

def fa_cache_test(lookups:list) -> None:
    cache = FACache(12, 8)
    for j in lookups:
        cache.lookup(j)
    cache.reset()
    for j in lookups:
        cache.lookup(j)
    cache.showhits()
    cache.showcache()
    print(f'Cycles: {cache.cycles}')
    print(f'Cache size: {cache.size()}')
    print(f'Cache Miss Cost: {cache.miss_cycle_cost}')

def dm_cache_test(lookups:list) -> None:
    cache = DMCache(12, 8)
    for j in lookups:
        cache.lookup(j)
    cache.reset()
    for j in lookups:
        cache.lookup(j)
    cache.showhits()
    cache.showcache()
    print(f'Cycles: {cache.cycles}')
    print(f'Cache size: {cache.size()}')
    print(f'Cache Miss Cost: {cache.miss_cycle_cost}')

if __name__ == "__main__":
    test_lookups = [4, 8, 12, 16, 20, 36, 40, 44, 20, 36, 40, 44, 64, 68, 4, 8, 12, 92, 96, 100, 104, 108, 112, 100, 112, 116, 120, 128, 140, 144]
    print(len(test_lookups))
    sa_cache_test(test_lookups)
    fa_cache_test(test_lookups)
    dm_cache_test(test_lookups)