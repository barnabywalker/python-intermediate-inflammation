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
            if args.json_path is not None:
                patient = views.load_patient_records(args.json_path)[args.patient]
            else:
                patient_data = inflammation_data[args.patient]
                observations = [models.Observation(day, value) for day, value in enumerate(patient_data)]
                patient = models.Patient("UNKNOWN", observations)

            views.display_patient_record(patient)

        elif args.view == "to-json":
            patients = []
            for i, item in enumerate(inflammation_data):
                observations = [models.Observation(day, value) for day, value in enumerate(item)]
                patients.append(models.Patient(f"patient{i:03d}", observations))

            views.save_patient_records(patients, args.json_path)


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
        choices=["visualise", "record", "to-json"],
        help="Which view should be used?"
    )

    parser.add_argument(
        '--patient',
        type=int,
        default=0,
        help="Which patient should be displayed?"
    )

    parser.add_argument(
        "--json-path",
        type=str,
        default=None,
        help="Where is the serialised patients JSON file?"
    )

    parser.add_argument(
        "--to-json",
        type=str,
        default=None,
        help="Where should the patient record be saved to?"
    )

    args = parser.parse_args()

    main(args)
