'''
Created on 08/11/2013

@author: mmpe
'''
class DualKeyDict(object):
    def __init__(self, unique_key_att, additional_key_att):
        self._unique_key_att = unique_key_att
        self._additional_key_att = additional_key_att
        self._dict = {}
        self._unique_keys = set()


    def __getitem__(self, key):
        obj = self._dict[key]
        if isinstance(obj, list):
            raise AttributeError("More objects associated by key, '%s'. Use 'get' function to get list of objects" % key)
        else:
            return obj



    def __contains__(self, key):
        return key in self._dict

    def __iter__(self):
        return (i for i in self._unique_keys)

    def __setitem__(self, key, obj):
        self.add(obj)

    def __len__(self):
        return len(self._unique_keys)

    def add(self, obj):
        unique_key = getattr(obj, self._unique_key_att)
        if unique_key in self._unique_keys:
            raise KeyError("Key '%s' already exists in dict" % unique_key)
        self._dict[unique_key] = obj
        self._unique_keys.add(unique_key)
        additional_key = getattr(obj, self._additional_key_att)
        if additional_key in self._dict:
            existing_obj = self._dict[additional_key]
            if isinstance(existing_obj, list):
                existing_obj.append(obj)
            else:
                self._dict[additional_key] = [existing_obj, obj]
        else:
            self._dict[additional_key] = obj

    def get(self, key, default=None, multiple_error=False):
        """
        Return <object> or <list of objects> associated by 'key'
        If key not exists, 'default' is returned
        If multiple_error is true, ValueError is raised if 'key' associates a <list of objects>
        """
        if key in self._dict:
            obj = self._dict[key]
            if multiple_error and isinstance(obj, list):
                raise AttributeError("More objects associated by key, '%s'" % key)
            return obj
        else:
            return default

    def keys(self):
        """Return list of unique keys"""
        return list(self._unique_keys)

    def values(self):
        return [self._dict[k] for k in self._unique_keys]

    def __str__(self):
        return "{%s}" % ",".join(["(%s,%s): %s" % (getattr(obj, self._unique_key_att), getattr(obj, self._additional_key_att), obj) for obj in self.values()])


    def remove(self, value):
        """
        Value may be:
        - unique key
        - additional key
        - object
        """
        obj = self._dict.get(value, value)

        unique_key = getattr(obj, self._unique_key_att)
        del self._dict[unique_key]
        self._unique_keys.remove(unique_key)
        additional_key = getattr(obj, self._additional_key_att)
        value = self._dict[additional_key]
        if isinstance(value, list):
            value = [v for v in value if v is not obj]
            #value.remove(obj)
            if len(value) == 1:
                self._dict[additional_key] = value[0]
            else:
                self._dict[additional_key] = value
        else:
            del self._dict[additional_key]
        return obj

    def clear(self):
        self._dict.clear()
        self._unique_keys.clear()

    def copy(self):
        copy = DualKeyDict(self._unique_key_att, self._additional_key_att)
        copy._unique_keys = self._unique_keys.copy()
        copy._dict = self._dict.copy()

        return copy




