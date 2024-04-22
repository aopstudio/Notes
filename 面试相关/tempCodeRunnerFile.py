    start = time.time()
    single_thread()
    end = time.time()
    print('single thread, cost:',end-start,'seconds')

    start = time.time()
    multi_thread()
    end = time.time()
    print('multi thread, cost:',end-start,'seconds')

    start = time.time()
    multi_process()
    end = time.time()
    print('multi process, cost:',end-start,'seconds')