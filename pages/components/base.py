class Component(object):
    def __init__(self, name, block):
        self.name = name
        self.block = block

    def as_tuple(self):
        return (self.name, self.block)
