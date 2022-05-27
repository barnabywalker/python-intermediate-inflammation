"""Module containing code for serialising inflammation data"""

import json
import csv
from abc import ABC
from inflammation import models
from collections import defaultdict


class Serializer(ABC):
    @classmethod
    def serialize(cls, instances):
        raise NotImplementedError

    @classmethod
    def save(cls, instances, path):
        raise NotImplementedError

    @classmethod
    def deserialize(cls, data):
        raise NotImplementedError

    @classmethod
    def load(cls, path):
        raise NotImplementedError


class ObservationSerializer(Serializer):
    model = models.Observation

    @classmethod
    def serialize(cls, instances):
        return [{
            "day": instance.day,
            "value": instance.value
        } for instance in instances]

    @classmethod
    def deserialize(cls, data):
        return [cls.model(**d) for d in data]


class PatientSerializer(Serializer):
    model = models.Patient

    @classmethod
    def serialize(cls, instances):
        return [{
            "name": instance.name,
            "observations": ObservationSerializer.serialize(instance.observations)
        } for instance in instances]

    @classmethod
    def deserialize(cls, data):
        instances = []

        for item in data:
            item["observations"] = ObservationSerializer.deserialize(item.pop("observations"))
            instances.append(cls.model(**item))

        return instances


class PatientJSONSerializer(PatientSerializer):
    @classmethod
    def save(cls, instances, path):
        with open(path, "w") as jsonfile:
            json.dump(cls.serialize(instances), jsonfile)

    @classmethod
    def load(cls, path):
        with open(path, "r") as jsonfile:
            data = json.load(jsonfile)

        return cls.deserialize(data)


class PatientCSVSerializer(PatientSerializer):
    @classmethod
    def save(cls, instances, path):
        with open(path, "w") as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=["name", "day", "observation"])
            writer.writeheader()
            for patient in cls.serialize(instances):
                for row in patient["observations"]:
                    writer.writerow({"name": patient["name"], "day": row["day"], "observation": row["value"]})
                

    @classmethod
    def load(cls, path):
        data = defaultdict(list)
        with open(path, "r") as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                data[row["name"]].append({"day": int(row["day"]), "value": float(row["observation"])})

        patients = [{"name": name, "observations": obs} for name, obs in data.items()]
        return cls.deserialize(patients)