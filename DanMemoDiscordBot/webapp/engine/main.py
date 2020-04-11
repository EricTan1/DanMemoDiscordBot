from calculator import helper,calculator,oracle
import random
import time

if __name__ == '__main__':
    start = time.time()
    random.seed(1337)
    oracle.main()
    end = time.time()
    print("Time elapsed:",end-start,"s")