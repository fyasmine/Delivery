import csv

# used to add or get an item from the dictionary
class HashTable:
    # O(1)
    # constructor initializes array
    def __init__(self):
        # sets array size to 100
        self.size = 100
        # sets array values to None
        self.map = [None] * self.size

    # O(1)
    # calculates index using key
    def _get_hash(self, key):
        # returns index
        return (int(key) % len(self.map) - 1)

    # O(1)
    # adds package to the array
    def add(self, key, value):
        # calls the _get_hash function to get the index to put the value in
        key_hash = self._get_hash(key)
        # creates list to pass into cell
        key_value = [key, value]
        # O(N)
        # checks if there is an exisiting value in the cell
        if self.map[key_hash] is None:
            # creates a list and adds value to it then returns true
            self.map[key_hash] = list([key_value])
            return True
        else:
            # checks for existing key in list and updates if found
            for pair in self.map[key_hash]:
                if pair[0] == key:
                    pair[1] = value
                    return True
            # adds new value to list if key not found
            self.map[key_hash].append(key_value)
            return True
        return None

    # O(1)
    # gets value from array
    def get(self, key):
        # calls _get_hash method to find index
        key_hash = self._get_hash(key)
        # returns value if key is found
        if self.map[key_hash] is not None:
            for pair in self.map[key_hash]:
                if pair[0] == key:
                    return pair[1]
        return None

    # O(1)
    # adds time package leaves hub
    def add_depart_status(self, key, status):
        # calls the _get_hash function to get the index to put the value in
        key_hash = self._get_hash(key)
        values = []
        # O(1)
        # finds existing key
        for pair in self.map[key_hash]:
            if pair[0] == key:
                # changes status to indicate time package left hub
                pair[1][7] = status
                # overwrites old values
                pair[1] = pair[1]
                return True

    # O(1)
    # adds delivery time to dictionary time_list
    def add_time(self, key, time):
        # calls the _get_hash function to get the index to put the value in
        key_hash = self._get_hash(key)
        values = []
        # O(1)
        # finds existing key
        for pair in self.map[key_hash]:
            if pair[0] == key:
                # changes status to indicate time package left hub
                pair[1][8] = time
                # overwrites old values
                pair[1] = pair[1]
                return True

# opens CSV files
data_file = csv.reader(open('WGUPS Package File CSV.csv'))
# instance
table = HashTable()

# O(N)
# reads CSV file and adds packages to dictionary
for row in data_file:
    key = row[0]
    value = row[1:]
    value.append('At hub')
    value.append(-1)
    table.add(key, value)
