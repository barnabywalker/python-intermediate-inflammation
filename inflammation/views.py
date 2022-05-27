"""Module containing code for plotting inflammation data."""

from matplotlib import pyplot as plt
import numpy as np
from inflammation.serializers import PatientJSONSerializer

def display_patient_record(patient):
    """Display data for a single patient."""
    print(patient.name)
    for obs in patient.observations:
        print(obs.day, obs.value)


def save_patient_records(patients, path):
    """Save data for a set of patients as JSON.

    :param patients: A list of patient objects
    :param path: A str specifying the json file to save to
    :returns: the path that was provided
    """
    PatientJSONSerializer.save(patients, path)
    return path


def load_patient_records(path):
    """Load data for a set of patients from a JSON file
    : param path: A str specifying the path to a json file to load data from.
    : returns: A list of patient objects.
    """
    return PatientJSONSerializer.load(path)


def visualize(data_dict):
    """Display plots of basic statistical properties of the inflammation data.

    :param data_dict: Dictionary of name -> data to plot
    """
    # TODO(lesson-design) Extend to allow saving figure to file

    num_plots = len(data_dict)
    fig = plt.figure(figsize=((3 * num_plots) + 1, 3.0))

    for i, (name, data) in enumerate(data_dict.items()):
        axes = fig.add_subplot(1, num_plots, i + 1)

        axes.set_ylabel(name)
        axes.plot(data)

    fig.tight_layout()

    plt.show()
