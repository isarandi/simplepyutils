import collections
import glob
import itertools
import multiprocessing


def all_disjoint(*seqs):
    union = set()
    for item in itertools.chain(*seqs):
        if item in union:
            return False
        union.add(item)
    return True


def is_running_in_jupyter_notebook():
    try:
        # noinspection PyUnresolvedReferences
        shell = get_ipython().__class__.__name__
        if shell == 'ZMQInteractiveShell':
            return True  # Jupyter notebook or qtconsole
        elif shell == 'TerminalInteractiveShell':
            return False  # Terminal running IPython
        else:
            return False  # Other type (?)
    except NameError:
        return False  # Probably standard Python interpreter


def progressbar(iterable=None, *args, **kwargs):
    # noinspection PyUnresolvedReferences
    import tqdm
    # noinspection PyUnresolvedReferences
    import tqdm.notebook
    import sys
    if is_running_in_jupyter_notebook():
        return tqdm.notebook.tqdm(iterable, *args, **kwargs)
    elif sys.stdout.isatty():
        return tqdm.tqdm(iterable, *args, dynamic_ncols=True, **kwargs)
    elif iterable is None:
        class X:
            def update(self, *a, **kw):
                pass

        return X()
    else:
        return iterable


def progressbar_items(dictionary, *args, **kwargs):
    return progressbar(dictionary.items(), total=len(dictionary), *args, **kwargs)


def parallel_map_with_progbar(fn, items, pool=None):
    if pool is None:
        pool = multiprocessing.Pool()

    for _ in progressbar(pool.imap(fn, items), total=len(items)):
        pass


def groupby(items, key):
    result = collections.defaultdict(list)
    for item in items:
        result[key(item)].append(item)
    return result


def groupby_map(items, key_and_value_fn):
    result = collections.defaultdict(list)
    for item in items:
        key, value = key_and_value_fn(item)
        result[key].append(value)
    return result


def itemsetter(seq, *indices):
    def setter(item):
        s = seq
        for i in indices[:-1]:
            s = s[i]

        s[indices[-1]] = item

    return setter


def sorted_recursive_glob(pattern):
    return sorted(glob.glob(pattern, recursive=True))


def rounded_int_tuple(p):
    return tuple([round(x) for x in p])
