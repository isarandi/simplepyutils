import datetime
import json
import os
import pickle


def load_pickle(file_path):
    with open(file_path, 'rb') as f:
        try:
            return pickle.load(f)
        except UnicodeDecodeError:
            return pickle.load(f, encoding='latin1')


def dump_pickle(data, file_path, protocol=pickle.DEFAULT_PROTOCOL):
    ensure_path_exists(file_path)
    with open(file_path, 'wb') as f:
        pickle.dump(data, f, protocol)


def dump_json(data, path, **kwargs):
    ensure_path_exists(path)
    with open(path, 'w') as file:
        return json.dump(data, file, **kwargs)


def load_yaml(path):
    import yaml
    with open(path) as file:
        return yaml.safe_load(file)


def write_file(content, path, is_binary=False):
    mode = 'wb' if is_binary else 'w'
    ensure_path_exists(path)
    with open(path, mode) as f:
        if not is_binary:
            content = str(content)
        f.write(content)
        f.flush()


def ensure_path_exists(filepath):
    os.makedirs(os.path.dirname(filepath), exist_ok=True)


def read_file(path, is_binary=False):
    mode = 'rb' if is_binary else 'r'
    with open(path, mode) as f:
        return f.read()


def read_lines(path):
    return read_file(path).splitlines()


def load_json(path):
    with open(path) as file:
        return json.load(file)


def is_pickle_readable(p):
    try:
        load_pickle(p)
        return True
    except BaseException:
        return False


def is_file_newer(path, min_time=None):
    if min_time is None:
        return os.path.exists(path)
    min_time = datetime.datetime.strptime(min_time, '%Y-%m-%dT%H:%M:%S').timestamp()
    return os.path.exists(path) and os.path.getmtime(path) >= min_time
