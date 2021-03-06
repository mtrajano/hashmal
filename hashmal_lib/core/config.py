import os
import json

# Singleton of config object
hashmal_config = None

def get_config():
    """Get the singleton Config instance."""
    return hashmal_config

def set_config(config):
    """Set the singleton Config instance."""
    global hashmal_config
    hashmal_config = config

class Config(object):
    """Configuration state."""
    def __init__(self):
        super(Config, self).__init__()
        self.options = {}
        set_config(self)

    def load(self, filename=None):
        if not filename:
            filename = os.path.abspath('hashmal.conf')
        if not os.path.exists(filename):
            open(filename, 'w').close()
            self.options = {'filename': filename}
            return
        try:
            with open(filename, 'r') as f:
                options = json.loads(f.read())
                self.options = byteify(options)
        except:
            self.options = {}
        if self.options is None:
            self.options = {}
        self.options['filename'] = filename

    def save(self):
        filename = self.options.get('filename')
        if not filename:
            filename = os.path.abspath('hashmal.conf')
        if not os.path.exists(filename):
            open(filename, 'w').close()
        with open(filename, 'w') as f:
            conf = json.dumps(self.options, indent=4, sort_keys=True)
            f.write(conf)

    def get_option(self, key, default=None):
        value = self.options.get(key, default)
        if isinstance(value, unicode): value = str(value)
        return value

    def set_option(self, key, value, do_save=True):
        self.options[key] = value
        if do_save:
            self.save()

# http://stackoverflow.com/questions/956867/how-to-get-string-objects-instead-of-unicode-ones-from-json-in-python
def byteify(input):
    if isinstance(input, dict):
        return {byteify(key):byteify(value) for key,value in input.iteritems()}
    elif isinstance(input, list):
        return [byteify(element) for element in input]
    elif isinstance(input, unicode):
        return input.encode('utf-8')
    else:
        return input
