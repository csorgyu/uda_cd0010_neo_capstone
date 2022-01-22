"""Represent models for near-Earth objects and their close approaches.

The `NearEarthObject` class represents a near-Earth object. Each has a unique
primary designation, an optional unique name, an optional diameter, and a flag
for whether the object is potentially hazardous.

The `CloseApproach` class represents a close approach to Earth by an NEO. Each
has an approach datetime, a nominal approach distance, and a relative approach
velocity.

A `NearEarthObject` maintains a collection of its close approaches, and a
`CloseApproach` maintains a reference to its NEO.

The functions that construct these objects use information extracted from the
data files from NASA, so these objects should be able to handle all of the
quirks of the data set, such as missing names and unknown diameters.

You'll edit this file in Task 1.
"""
from helpers import cd_to_datetime, datetime_to_str


class NearEarthObject:
    """A near-Earth object (NEO).

    An NEO encapsulates semantic and physical parameters about the object, such
    as its primary designation (required, unique), IAU name (optional), diameter
    in kilometers (optional - sometimes unknown), and whether it's marked as
    potentially hazardous to Earth.

    A `NearEarthObject` also maintains a collection of its close approaches -
    initialized to an empty collection, but eventually populated in the
    `NEODatabase` constructor.
    """
    # TODO: How can you, and should you, change the arguments to this constructor?
    # If you make changes, be sure to update the comments in this file.

    ## csgy Adding id, skpid and pdes as mandatory parameters,
    def __init__(self, pdes, **info):
        """Create a new `NearEarthObject`.

        :param pdes: unique identifier of the object, this cannot be None
        :param info: A dictionary of excess keyword arguments supplied to the constructor.
        """
        # TODO: Assign information from the arguments passed to the constructor
        # onto attributes named `designation`, `name`, `diameter`, and `hazardous`.
        # You should coerce these values to their appropriate data type and
        # handle any edge cases, such as a empty name being represented by `None`
        # and a missing diameter being represented by `float('nan')`.
        self._designation = pdes
        if 'name' in info.keys():
            self._name = info['name']
        else:
            self._name = 'Unknown'
        if 'diameter' in info.keys():
            self._diameter = float(info['diameter'])
        else:
            self._diameter = float('nan')
        if 'hazardous' in info.keys():
            self._hazardous = bool(info['hazardous'])
        else:
            self._hazardous = False
        # Create an empty initial collection of linked approaches.
        self._approaches = []

    @property
    def designation(self):
        return f'{self._designation}'
    @property
    def name(self):
        return f'{self._name}'
    @property
    def diameter(self):
        return self._diameter

    @property
    def diameter_str(self):
        if(self._diameter == float('nan')):
            return 'unknown'
        else:
            return f'{self._diameter:.3f}'

    @property
    def hazardous(self):
        return self._hazardous

    @property
    def approaches(self):
        return self._approaches

    @property
    def fullname(self):
        """Return a representation of the full name of this NEO."""
        # TODO: Use self.designation and self.name to build a fullname for this object.
        return f'{self._designation} {self._name}'

    def __str__(self):
        """Return `str(self)`."""
        # TODO: Use this object's attributes to return a human-readable string representation.
        # The project instructions include one possibility. Peek at the __repr__
        # method for examples of advanced string formatting.
        return f"A NearEarthObject {self.fullname} and with designation {self._designation}. "\
               f"Diameter is {self.diameter_str} km. "\
               f"It is potentially {'' if self._hazardous else 'NOT'} hazardous."

    def __repr__(self):
        """Return `repr(self)`, a computer-readable string representation of this object."""
        return f"NearEarthObject(designation={self._designation!r}, name={self._name!r}, " \
               f"diameter={self._diameter:.3f}, hazardous={self._hazardous!r})"


class CloseApproach:
    """A close approach to Earth by an NEO.

    A `CloseApproach` encapsulates information about the NEO's close approach to
    Earth, such as the date and time (in UTC) of closest approach, the nominal
    approach distance in astronomical units, and the relative approach velocity
    in kilometers per second.

    A `CloseApproach` also maintains a reference to its `NearEarthObject` -
    initially, this information (the NEO's primary designation) is saved in a
    private attribute, but the referenced NEO is eventually replaced in the
    `NEODatabase` constructor.
    """
    # TODO: How can you, and should you, change the arguments to this constructor?
    # If you make changes, be sure to update the comments in this file.
    def __init__(self, des, **info):
        """Create a new `CloseApproach`.

        :param des: The designation of the close approach. Cannot be None
        :param info: A dictionary of excess keyword arguments supplied to the constructor.
        """
        # TODO: Assign information from the arguments passed to the constructor
        # onto attributes named `_designation`, `time`, `distance`, and `velocity`.
        # You should coerce these values to their appropriate data type and handle any edge cases.
        # The `cd_to_datetime` function will be useful.
        self._designation = des
        # TODO: Use the cd_to_datetime function for this attribute.
        if 'time' in info.keys():
            self._time = cd_to_datetime(info['time'])
        else:
            self._time = None
        if 'distance' in info.keys():
            self._distance = float(info['distance'])
        else:
            self._distance = float('nan')
        if 'velocity' in info.keys():
            self._velocity = float(info['velocity'])
        else:
            self._velocity = float('nan')

        # Create an attribute for the referenced NEO, originally None.
        self._neo = None

    @property
    def time(self):
        return self._time

    @property
    def distance(self):
        return self._distance

    @property
    def velocity(self):
        return self._velocity

    @property
    def neo(self):
        return self._neo

    @property
    def time_str(self):
        """Return a formatted representation of this `CloseApproach`'s approach time.

        The value in `self.time` should be a Python `datetime` object. While a
        `datetime` object has a string representation, the default representation
        includes seconds - significant figures that don't exist in our input
        data set.

        The `datetime_to_str` method converts a `datetime` object to a
        formatted string that can be used in human-readable representations and
        in serialization to CSV and JSON files.
        """
        # TODO: Use this object's `.time` attribute and the `datetime_to_str` function to
        # build a formatted representation of the approach time
        # TODO: Use the cd_to_datetime function for this attribute.
        if self._time:
            return f"{datetime_to_str(self._time)}"
        else:
            return "unknown"

    def __str__(self):
        """Return `str(self)`."""
        # TODO: Use this object's attributes to return a human-readable string representation.
        # The project instructions include one possibility. Peek at the __repr__
        # method for examples of advanced string formatting.
        return f"On {self.time_str}, the '{self.neo.fullname}' approaches Earth at a distance of "\
               f"{self._distance} au and a velocity of {self._velocity} km/s."

    def __repr__(self):
        """Return `repr(self)`, a computer-readable string representation of this object."""
        return f"CloseApproach(time={self.time_str!r}, distance={self._distance:.2f}, " \
               f"velocity={self._velocity:.2f}, neo={self._neo!r})"
