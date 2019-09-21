class ASQL:
    """
    This class takes a single list. Each item in the list MUST be of the same datatype.
    This allows you to query the properties in a list quickly and easily.
    It is basicaly SQL, but for python lists/arrays

    GitHub:
    https://github.com/CPSuperstore-Inc/ASQL
    """
    # region List Behavior Items
    def __init__(self, iterable=None):
        """
        Initialize the object
        :param iterable: The iterable to base the object off
        """
        if iterable is None:
            iterable = []
        self.array = list(iterable)
        self.operation_mode = None
        self.selection_type = None

        self.current = 0

    def __iter__(self):
        return self

    def __next__(self):
        if self.current >= len(self.array):
            raise StopIteration
        else:
            self.current += 1
            return self.array[self.current - 1]

    def __len__(self):
        return len(self.array)

    def count(self, o):
        return self.array.count(o)

    def reset(self):
        self.array = []

    def remove(self, o):
        self.array.remove(o)

    def append(self, item):
        self.array.append(item)
    # endregion

    # region Special Selections
    def max(self, prop, where: str = ""):
        """
        Returns the largest value of a given property
        :param prop: the property to search
        :param where: the filter to apply to the result set
        :return: the largest value
        """
        return max(getattr(node, prop) for node in self.filter(where))

    def min(self, prop, where: str = ""):
        """
        Returns the smallest value of a given property
        :param prop: the property to search
        :param where: the filter to apply to the result set
        :return: the smallest value
        """
        return min(getattr(node, prop) for node in self.filter(where))

    def sum(self, prop, where: str = ""):
        """
        Returns the sum of a given property
        :param prop: the property to search
        :param where: the filter to apply to the result set
        :return: the sum
        """
        return sum(getattr(node, prop) for node in self.filter(where))

    def avg(self, prop, where: str = ""):
        """
        Returns the average of a given property
        :param prop: the property to search
        :param where: the filter to apply to the result set
        :return: the average
        """
        results = self.filter(where)
        return sum(getattr(node, prop) for node in results) / float(len(results))
    # endregion

    # region Generic Selection
    def select(self, what: str="", where: str = "", flat_list: bool = False, as_map: bool=False):
        """
        Allows the user to select values based off the criteria
        :param what: the space separated list of the items to select
        :param where: the criteria that each record should follow
        :param flat_list: return as a 2D array ([[1, 2, 3], [1, 2, 3]]) or 1D list ([1, 2, 3, 1, 2, 3])
        :param as_map: return as a dictionary ([{"a": 1, "b": 2, "c": 3}, {"a": 1, "b": 2, "c": 3}])
        :return: the selected items
        """

        # get the items which match the "where" criteria
        results = self.filter(where)

        result = []

        # if the user has not specified what to select, assume every property
        # so, get a list of each property of the saved object
        # if it is specified, split the string to a list at each space
        if what == "":
            what = list(results[0].__dict__.keys())
        else:
            what = what.split(" ")

        # iterate over each item which matches the "where" criteria
        for i in results:
            record = []
            record_map = {}

            # add each selected property to both the list and map
            for o in what:
                record_map[o] = getattr(i, o)
                record.append(getattr(i, o))

            # add the appropriate item to the master list of values to be returned
            if as_map:
                result.append(record_map)
            else:
                result.append(record)

        # flatten the list if the user has specified to have a flattened list
        if flat_list is True:
            return [item for sublist in result for item in sublist]

        # return the result
        return result

    def filter(self, query: str = "", sort: str = None, group_size: int = 0):
        """
        This function returns each record which matches specified criteria as a list
        :param query: the criteria each record must match (if not specified, select everything)
        :param sort: the property to sort each record by
        :param group_size: the amount of records to place in each group (if not specified, return a flat list)
        :return: the list of records which match the query
        """

        # make a copy of the master array
        results = self.array.copy()

        # if sort criteria is specified, split it into a list at every space
        if sort is not None:
            sort = sort.split(" ")

        if query != "":
            # if the query is specified, split it into a list at every space
            args = query.split(" ")

            # the list of possible comparison operators
            comparisons = ["<=", ">=", "<", ">", "==", "!=", "<>"]

            for a in args:
                for item in self.array:
                    for c in comparisons:
                        # check if the current query comparison operator is in the selected query
                        if c in a:

                            # evaluate the condition
                            prop, expected = a.split(c)
                            value = getattr(item, prop)
                            # noinspection PyUnusedLocal
                            expected = type(value)(expected)

                            # if the condition is false, remove from the list of possible results
                            if not eval("value {} expected".format(c)):
                                if item in results:
                                    results.remove(item)
                            break

        # sort the new list if specified
        if sort is not None:
            results = sorted(results, key=lambda x: getattr(x, sort[0]))

        # check if the size to group by is larger than 1
        if group_size > 0:
            total = []
            new = []
            index = 1

            # break the result into chunks of the specified size
            for r in results:
                new.append(r)
                if index % group_size == 0:
                    total.append(new)
                    new = []
                index += 1

            # if any remain, add it to the list
            if len(new) > 1:
                total.append(new)
            results = total

        # return the set
        return results
    # endregion

    # region Generic Modifications
    def delete(self, query: str = ""):
        """
        Deletes any items which match a specified query
        :param query: the query to delete by (leave blank for everything)
        :return: the items which were deleted
        """

        # get the items which match the query
        queued = self.filter(query)

        # delete each item
        for i in queued:
            self.array.remove(i)

        # return the deleted items
        return queued

    def update(self, change: str, where: str=""):
        """
        Updates each item which matches the 'where' clause
        :param change: the space separated list of changes (leave blank to apply to all)
        :param where: the condition each record must match to have the change apply
        :return: nothing
        """

        # get the list of items to change
        queued = self.filter(where)

        # iterate over each item
        for item in range(len(queued)):

            # iterate over each transaction
            for i in change.split(" "):

                # apply the change to each item
                prop, val = i.split("=")
                setattr(queued[item], prop, eval(val))
    # endregion

    # region Special Modifications
    def remove_duplicates(self, prop: str):
        """
        Removes duplicate values of a property
        :param prop: the property to remove duplicate values from
        :return: nothing
        """
        found = []

        # iterate over each item
        for item in self.array:

            # save the value of the property
            val = getattr(item, prop)

            if val in found:
                # if the value is already found, remove it from the array
                self.remove(item)
            else:
                # if not, add it to the list of found values
                found.append(val)

    def remove_duplicate_numbers(self, prop: str, buffer=0):
        """
        Removes duplicate values of a property within a specified buffer
        :param prop: the property to remove duplicate values from
        :param buffer: the tolerance for each removal
        :return: nothing
        """
        found = []

        # iterate over each item in the array
        for item in self.array:

            # get the attribute from the selected item
            val = float(getattr(item, prop))
            for f in found:

                # determine if the value is within the buffer
                if abs(f - val) <= buffer:

                    # if it is, remove it from the array
                    if item in self.array:
                        self.remove(item)

            # add the value to the list of located values, if it is not already in the list
            if val not in found:
                found.append(val)
    # endregion
