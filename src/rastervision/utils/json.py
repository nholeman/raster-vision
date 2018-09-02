def set_nested_keys(target, mods, ignore_missing_keys):
    """Sets dictionary keys based on modifications stated
       in a dictionary. TODO: Explain.
       Only overrides values, does not replace dicts.
       TODO: Errors will be user facing, so provide good feedback.
    """
    searched_keys, found_keys = [], []

    def f(_target, _mods):
        for key in _target:
            if key in _mods.keys():
                found_keys.append(key)
                if type(_target[key]) is dict:
                    if type(_mods[key]) is dict:
                        f(_target[key], _mods[key])
                    else:
                        raise Exception("Error: cannot modify dict with value")
                else:
                    _target[key] = _mods[key]
            else:
                if type(_target[key]) is dict:
                    f(_target[key], _mods)
        searched_keys.extend(list(_mods.keys()))

    f(target, mods)
    if not ignore_missing_keys:
        d = set(searched_keys) - set(found_keys)
        if d:
            raise Exception("Mod keys not found in target dict: {}".format(d))
