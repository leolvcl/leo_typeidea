import cProfile
def loop(count):
    result = []
    for i in range(count):
        result.append(i)

cProfile.run('loop(10000)')        