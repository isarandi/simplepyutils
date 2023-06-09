
def split_path(path):
    return os.path.normpath(path).split(os.path.sep)


def str_range(string, sep, start, end):
    return sep.join(string.split(sep)[start:end])


def path_range(path, start, end):
    return str_range(os.path.normpath(path), os.path.sep, start, end)


def path_stem(path):
    return pathlib.PurePath(path).stem


def last_path_components(path, n_components):
    return path_range(path, -n_components, None)

def replace_extension(path, new_ext):
    return os.path.splitext(path)[0] + new_ext



def natural_sort_key_float(s, _pat=re.compile(r'([-+]?[0-9]*\.?[0-9]+(?:[eE][-+]?[0-9]+)?)')):
    return [float(t) if i % 2 == 1 else t for i, t in enumerate(re.split(_pat, s))]


def natural_sort_key(s):
    """Normal string sort puts '10' before '2'. Natural sort puts '2' before '10'."""
    return [float(t) if t.isdigit() else t for t in re.split('([0-9]+)', s)]


def natural_sorted(seq):
    return sorted(seq, key=natural_sort_key)