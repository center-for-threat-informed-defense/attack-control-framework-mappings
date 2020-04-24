from collections import OrderedDict
from .base import StrictlyTyped, SerializableObject, StrictlyTypedList

class Characteristic(SerializableObject):
    """A control characteristic is a flexible way to encode additional data about a control. 
    Within a given control framework all controls *should* have the same characteristic types (names), but not necessarily the same characteristic values."""

    def __init__(self, initialValues=None):
        super().__init__()
        self._properties = OrderedDict({
            "name": StrictlyTyped(str),
            "value": StrictlyTypedList(str)
        })
        if initialValues:
            self.from_dict(initialValues)

    # name property
    @property
    def name(self): 
        return self._properties["name"].getter()
    @name.setter
    def name(self, newvalue):
        self._properties["name"].setter(newvalue)
        
    # value property
    @property
    def value(self): 
        return self._properties["value"].getter()
    @value.setter
    def value(self, newvalue):
        self._properties["value"].setter(newvalue)

class Control(SerializableObject):
    """A control object is an individual control from within a control framework."""

    def __init__(self, initialValues=None):
        super().__init__()
        self._properties = OrderedDict({
            "id": StrictlyTyped(str),
            "name": StrictlyTyped(str),
            "parent_id": StrictlyTyped(str),
            "description": StrictlyTyped(str),
            "characteristics": StrictlyTypedList(Characteristic)
        })
        if initialValues:
            self.from_dict(initialValues)

    
    # id property
    @property
    def id(self):
        return self._properties["id"].getter()
    @id.setter
    def id(self, value):
        self._properties["id"].setter(value)

    # name property
    @property
    def name(self):
        return self._properties["name"].getter()
    @name.setter
    def name(self, value):
        self._properties["name"].setter(value)

    # parent_id property
    @property
    def parent_id(self):
        return self._properties["parent_id"].getter()
    @parent_id.setter
    def parent_id(self, value):
        self._properties["parent_id"].setter(value)

    # description property
    @property
    def description(self):
        return self._properties["description"].getter()
    @description.setter
    def description(self, value):
        self._properties["description"].setter(value)

    # characteristics property
    @property
    def characteristics(self):
        return self._properties["characteristics"].getter()
    @characteristics.setter
    def characteristics(self, values):
        self._properties["characteristics"].setter(values)


class ControlBundle(SerializableObject):
    """A collection of individual controls. Typically used to represent an entire control framework."""

    def __init__(self, initialValues=None):
        super().__init__()
        self._properties = OrderedDict({
            "name": StrictlyTyped(str),
            "description": StrictlyTyped(str),
            "spec_version": StrictlyTyped(str),
            "source": StrictlyTyped(str),
            "controls": StrictlyTypedList(Control)
        })
        if initialValues:
            self.from_dict(initialValues)

    # name property
    @property
    def name(self):
        return self._properties["name"].getter()
    @name.setter
    def name(self, value):
        self._properties["name"].setter(value)

    # description property
    @property
    def description(self):
        return self._properties["description"].getter()
    @description.setter
    def description(self, value):
        self._properties["description"].setter(value)

    # spec_version property
    @property
    def spec_version(self):
        return self._properties["spec_version"].getter()
    @spec_version.setter
    def spec_version(self, value):
        self._properties["spec_version"].setter(value)
    
    # source property
    @property
    def source(self):
        return self._properties["source"].getter()
    @source.setter
    def source(self, value):
        self._properties["source"].setter(value)

    #controls property
    @property
    def controls(self):
        return self._properties["controls"]
    @controls.setter
    def controls(self, values):
        self._properties["controls"].setter(values)
