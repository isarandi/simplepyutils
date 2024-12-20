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


def progressbar(iterable=None, step=None, *args, **kwargs):
    # noinspection PyUnresolvedReferences
    import tqdm
    # noinspection PyUnresolvedReferences
    import tqdm.notebook
    import sys
    if is_running_in_jupyter_notebook():
        if step is None:
            return tqdm.notebook.tqdm(iterable, *args, **kwargs)
        else:
            pbar = tqdm.notebook.tqdm(None, *args, **kwargs)
            return StepProgress(pbar, iterable, step)
    elif sys.stdout.isatty():
        if step is None:
            return tqdm.tqdm(iterable, *args, dynamic_ncols=True, **kwargs)
        else:
            pbar = tqdm.tqdm(None, *args, dynamic_ncols=True, **kwargs)
            return StepProgress(pbar, iterable, step)
    elif iterable is None:
        class X:
            def update(self, *a, **kw):
                pass

        return X()
    else:
        return iterable


class StepProgress:
    def __init__(self, pbar, seq, step=0):
        self.pbar = pbar
        self.step = step
        self.seq = seq

    def __iter__(self):
        for i in self.seq:
            yield i
            self.update()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.pbar.close()

    def update(self, n=1):
        self.pbar.update(n * self.step)

    def set_description(self, desc):
        self.pbar.set_description(desc)

    def close(self):
        self.pbar.close()


def zip_progressbar(iterable=None, *args, **kwargs):
    pbar = progressbar(iterable, *args, **kwargs)
    if pbar is iterable:
        class X:
            def set_description(self, *a, **kw):
                pass

            def update(self, *a, **kw):
                pass

        return zip(itertools.repeat(X()), iterable)
    return zip(itertools.repeat(pbar), pbar)


def progressbar_items(dictionary, *args, **kwargs):
    return progressbar(dictionary.items(), total=len(dictionary), *args, **kwargs)


def parallel_map_with_progbar(fn, items, pool=None, desc=None):
    if pool is None:
        pool = multiprocessing.Pool()

    return list(progressbar(pool.imap(fn, items), total=len(items), desc=desc))


def groupby_map(items, key_and_value_fn):
    result = collections.defaultdict(list)
    for item in items:
        key, value = key_and_value_fn(item)
        result[key].append(value)
    return result


def groupby(items, key):
    return groupby_map(items, lambda item: (key(item), item))


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
