import cProfile
import pstats
from io import StringIO

pr = cProfile.Profile()

def loop(count):
    result = []
    for i in range(count):
        result.append(i)

pr.enable()
loop(100000)
pr.disable()
s = StringIO()
# sortby = 'cumulative'
sortby = 'tottime'
ps = pstats.Stats(pr, stream=s).sort_stats(sortby)
ps.print_stats()
print(s.getvalue())
