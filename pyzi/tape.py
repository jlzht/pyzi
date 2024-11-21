class Tape:
    THRESHOLD = 1
    def __init__(self):
        self.data = {}
        self.cursor = None

    def load(self, data, cursor):
        self.data = data
        self.cursor = cursor
        # checks if level was reseted
        if self.cursor and sum(self.data.values()) == 0:
            self.cursor[0] = 0
 
    def current(self):
        key = list(self.data.keys())[self.cursor[0]]
        return key, self.data[key]

    def next(self):
        cursor = self.cursor[0]
        while True:
            self.cursor[0] = (self.cursor[0] + 1) % len(self.data)
            key, value = self.current()
            
            if value < self.THRESHOLD:
                return key, value
            
            if self.cursor[0] == cursor:
                return None, None

    def verify(self, increment: bool):
        key = list(self.data.keys())[self.cursor[0]]
        if increment:
            self.data[key] += 1
        else:
            if self.data[key] > 0:
                self.data[key] -= 1

            value = self.data.pop(key)
            keys = list(self.data.keys())

            keys = list(self.data.keys())

            insertion_index = self.cursor[0] % (len(keys) + 1)

            self.data = {
                **{k: self.data[k] for k in keys[:insertion_index]},
                key: value,
                **{k: self.data[k] for k in keys[insertion_index:]},
            }

            self.cursor[0] = insertion_index
        
    def get_progress(self):
        return sum(self.data.values()) / (len(self.data) * Tape.THRESHOLD)

