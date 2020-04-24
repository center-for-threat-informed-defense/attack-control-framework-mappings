from collections import OrderedDict

class StrictlyTyped:
    def __init__(self, thetype, initialValue=None):
        self._type = thetype
        self.setter(initialValue)

    def setter(self, value):
        if not isinstance(value, self._type) and value is not None :
            raise TypeError("expected " + str(self._type) + " got " + str(type(value)))
        else:
             self._value = value
    
    def getter(self):
        return self._value

class StrictlyTypedList:
    def __init__(self, thetype, initialValues=[]):
        self._type = thetype
        self.setter(initialValues)

    def setter(self, values):
        for value in values: # check each value in array
            if not isinstance(value, self._type):
                raise TypeError("expected " + str(self._type) + " got " + str(type(value)))
        self._values = values
    
    def getter(self):
        return self._values

class SerializableObject:
    def __init__(self):
        self._properties = OrderedDict({})

    def _parse_value(self, value):
        """helper method for parsing a value in _properties"""
        if isinstance(value, StrictlyTyped):
            return value.getter()
        elif isinstance(value, StrictlyTypedList):
            l = value.getter()
            if len(l) == 0:
                return None
            elif isinstance(l[0], SerializableObject):
                # recurse
                return list(map(lambda v: v.to_dict(), l))
            else: # probably a string[]
                return l
        else: return value

    def to_dict(self):
        """export this object into a dict"""
        output = {}
        for propertyname in self._properties:
            value = self._parse_value(self._properties[propertyname])
            if value is not None: output[propertyname] = value
            
        return output

    def from_dict(self, thedict):
        """import the data from a dict into this object"""
        for key in thedict:
            if key not in self._properties:
                raise ValueError(f"Unable to parse {type(self)} from dict: unexpected key '{key}'")
            self._properties[key].setter(thedict[key])

