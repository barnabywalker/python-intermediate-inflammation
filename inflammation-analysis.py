#!/usr/bin/env python3
"""Software for managing and analysing patients' inflammation data in
our imaginary hospital."""

import argparse

from inflammation import models, views


def main(args):
    """The MVC Controller of the patient inflammation data system.

    The Controller is responsible for:
    - selecting the necessary models and views for the current task
    - passing data between models and views
    """
    infiles = args.infiles
    if not isinstance(infiles, list):
        infiles = [args.infiles]

    for filename in infiles:
        inflammation_data = models.load_csv(filename)

        if args.view == "visualise":
            view_data = {
                'average': models.daily_mean(inflammation_data),
                'max': models.daily_max(inflammation_data),
                'min': models.daily_min(inflammation_data)
            }

            views.visualize(view_data)

        elif args.view == "record":
            if args.serial_path is not None:
                patient = views.load_patient_records(args.serial_path)[args.patient]
            else:
                patient_data = inflammation_data[args.patient]
                observations = [models.Observation(day, value) for day, value in enumerate(patient_data)]
                patient = models.Patient("UNKNOWN", observations)

            views.display_patient_record(patient)

        elif args.view == "serialise":
            patients = []
            for i, item in enumerate(inflammation_data):
                observations = [models.Observation(day, value) for day, value in enumerate(item)]
                patients.append(models.Patient(f"patient{i:03d}", observations))

            views.save_patient_records(patients, args.serial_path)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='A basic patient inflammation data management system')

    parser.add_argument(
        'infiles',
        nargs='+',
        help='Input CSV(s) containing inflammation series for each patient')

    parser.add_argument(
        '--view',
        type=str,
        default="visualise",
        choices=["visualise", "record", "serialise"],
        help="Which view should be used?"
    )

    parser.add_argument(
        '--patient',
        type=int,
        default=0,
        help="Which patient should be displayed?"
    )

    parser.add_argument(
        "--serial-path",
        type=str,
        default=None,
        help="Where is the serialised patients file?"
    )

    args = parser.parse_args()

    main(args)
