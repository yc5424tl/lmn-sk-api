import multiprocessing

def power(x):
    return x*x

if __name__ == '__main__':
    pool = multiprocessing.Pool(processes=5)
    result = pool.apply_async(power, (10,))
    print(result.get(timeout=1))
    print(pool.map(power, range(10)))

    it = pool.imap(power, range(10))
    print(next(it))
    print(next(it))
    print(it.next(timeout=1))

    import time
    result = pool.apply_async(time.sleep, (10,))
    print(result.get(timeout=1))