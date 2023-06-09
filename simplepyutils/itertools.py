def roundrobin(iterables, sizes):
    iterators = [iter(iterable) for iterable in iterables]
    for iterator, size in zip(itertools.cycle(iterators), itertools.cycle(sizes)):
        for _ in range(size):
            try:
                yield next(iterator)
            except StopIteration:
                return


def iterate_repeatedly(seq, shuffle_before_each_epoch=False, rng=None):
    """Iterates over and yields the elements of `iterable` over and over.
    If `shuffle_before_each_epoch` is True, the elements are put in a list and shuffled before
    every pass over the data, including the first."""

    if rng is None:
        rng = np.random.RandomState()

    # create a (shallow) copy so shuffling only applies to the copy.
    seq = list(seq)
    rng.shuffle(seq)
    yield from seq

    while True:
        if shuffle_before_each_epoch:
            rng.shuffle(seq)
        yield from seq


def roundrobin_iterate_repeatedly(
        seqs, roundrobin_sizes, shuffle_before_each_epoch=False, rng=None):
    iters = [iterate_repeatedly(seq, shuffle_before_each_epoch, util.new_rng(rng)) for seq in seqs]
    return roundrobin(iters, roundrobin_sizes)


def nested_spy_first(iterable, levels=1):
    it = iter(iterable)
    head = next(it)

    if levels == 1:
        return head, itertools.chain([head], it)

    deep_head, new_head = nested_spy_first(head, levels=levels - 1)
    return deep_head, itertools.chain([new_head], it)


def prefetch(seq, buffer_size):
    q = queue.Queue(buffer_size)
    end_of_sequence_marker = object()

    def producer():
        for elem in seq:
            q.put(elem)
        q.put(end_of_sequence_marker)

    producer_thread = threading.Thread(target=producer)
    producer_thread.start()

    try:
        while (elem := q.get()) is not end_of_sequence_marker:
            yield elem
    finally:
        producer_thread.join()
