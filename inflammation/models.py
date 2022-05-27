"""Module containing models representing patients and their data.

The Model layer is responsible for the 'business logic' part of the software.

Patients' data is held in an inflammation table (2D array) where each row contains 
inflammation data for a single patient taken over a number of days 
and each column represents a single day across all patients.
"""

import numpy as np


def load_csv(filename):
    """Load a Numpy array from a CSV

    :param filename: Filename of CSV to load
    :returns: a loaded Numpy array
    """
    return np.loadtxt(fname=filename, delimiter=',')


def daily_mean(data):
    """Calculate the daily mean of a 2D inflammation data array.

    :param data: a 2D Numpy array with inflammation data
        (each row is a patient, each column is a day)
    :returns: an array of the mean values for measurements for each day.
    """
    return np.mean(data, axis=0)


def daily_max(data):
    """Calculate the daily max of a 2D inflammation data array.

    :param data: a 2D Numpy array with inflammation data
        (each row is a patient, each column is a day)
    :returns: an array of the maximum values for measurements for each day.
    """
    return np.max(data, axis=0)


def daily_min(data):
    """Calculate the daily min of a 2D inflammation data array.

    :param data: a 2D Numpy array with inflammation data
        (each row is a patient, each column is a day)
    :returns: an array of minimum values for measurements for each day.
    """
    return np.min(data, axis=0)


def patient_normalise(data):
    """Normalise patient data from a 2D inflammation data array.

    NaN values are ignored and normalised to 0.

    Negative values are rounded to 0.
    :param data: a 2D Numpy array with inflammation data
        (each row is a patient, each column is a day)
    :returns: the inflammation data array normalised by the max value of
        each day
    """
    if not isinstance(data, np.ndarray):
        msg = "Inflammation data must be a numpy array, "
        msg += f"you gave a {type(data)}."
        raise TypeError(msg)

    if data.ndim != 2:
        msg = f"Inflammation data must have 2 dimensions "
        msg += "(rows for patients, columns for days), "
        msg += f"yours has {data.ndim}."
        raise TypeError(msg)

    if np.any(data < 0):
        raise ValueError("Inflammation values should not be negative")

    max_data = np.nanmax(data, axis=1)
    with np.errstate(invalid="ignore", divide="ignore"):
        normalised = data / max_data[:, np.newaxis]

    normalised[np.isnan(normalised)] = 0
    normalised[normalised < 0] = 0
    return normalised


def attach_names(data, names):
    """Attach patient names to each row of inflammation data.

    :param data: a 2D Numpy array with inflammation data
        (each row is a patient, each column is a day)
    :param names: a list of names, the length of `names` must match
        the number of rows in `data`.
    :return: a list of dicts with entries for the name and inflammation
        measurements of each patient.
    """
    if not isinstance(names, list):
        msg = f"You must provide names as a list, you gave a {type(names)}"
        raise TypeError(msg)

    if len(names) != data.shape[0]:
        msg = "You must provide as many names as rows in the patient data"
        msg += f", you gave {len(names)} for {data.shape[0]} rows."
        raise ValueError(msg)

    return [{"name": name, "data": row} for name, row in zip(names, data)]



class Observation:
    def __init__(self, day, value):
        self.day = day
        self.value = value

    def __str__(self):
        return str(self.value)

    def __eq__(self, __o):
        return self.day == __o.day and self.value == __o.value


class Person:
    def __init__(self, name):
        self.name = name

    def __str__(self):
        return self.name

    def __eq__(self, __o):
        return self.name == __o.name


class Patient(Person):
    """A patient in the inflammation study."""
    def __init__(self, name, observations=None):
        super().__init__(name)
        self.observations = []
        if observations is not None:
            self.observations = observations

    def add_observation(self, value, day=None):
        if day is None:
            try:
                day = self.observations[-1]["day"] + 1

            except IndexError:
                day = 0

        new_observation = Observation(day, value)

        self.observations.append(new_observation)
        return new_observation

    @property
    def last_observation(self):
        return self.observations[-1]

    def __eq__(self, __o):
        same_person = super().__eq__(__o)
        same_obs = all([o == _o for o, _o in zip(self.observations, __o.observations)])
        return same_person and same_obs and len(self.observations) == len(__o.observations)


class Doctor(Person):
    def __init__(self, name):
        super().__init__(name)
        self.patients = PatientGroup(f"{name} patients")

    def add_patient(self, name):
        return self.patients.add_patient(name)


class Treatment:
    def __init__(self, name, amount, units=None):
        self.name = name
        self.amount = amount
        self.units = units

    def __str__(self):
        return f"{self.amount} {units} of {self.name}"


class PatientGroup:
    """A group of Patients"""
    def __init__(self, name, patients=None):
        self.name = name
        self.patients = []
        if patients is not None:
            self.patients = patients

    def add_patient(self, name):
        if name in [p.name for p in self.patients]:
            return

        new_patient = Patient(name=name)
        self.patients.append(new_patient)
        return new_patient

    def __getitem__(self, item):
        return self.patients[item]

    def __len__(self):
        return len(self.patients)

    def __str__(self):
        return f"A group of {len(self)} patients called {self.name}"


class TreatmentGroup(PatientGroup):
    def __init__(self, name, patients=None, treatment=None):
        super().__init__(name, patients)
        self.treatment = treatment

    def set_treatment(self, name, amount, units=None):
        if self.treatment is not None:
            raise ValueError(f"Treatment already set for group as '{self.treatment.__str__()}'")

        treatment = Treatment(name, amount, units)
        self.treatment = treatment
        return treatment

    def __str__(self):
        return f"A group of {len(self)} patients treated with {self.treatment.name}"