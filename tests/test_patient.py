"""Tests for the Patient model."""

# Patients
def test_create_patient():
    from inflammation.models import Patient

    name = 'Alice'
    p = Patient(name=name)

    assert p.name == name


def test_patient_is_person():
    from inflammation.models import Patient, Person

    name = "Geoff"
    p = Patient(name=name)

    assert isinstance(p, Person)

# Groups
def test_group_duplicate_patient():
    from inflammation.models import PatientGroup

    name = "ward A"
    g = PatientGroup(name=name)

    patients = ["Geoff", "Geoff"]
    for p in patients:
        g.add_patient(p)

    assert len(g) == 1

def test_group_iterable():
    from inflammation.models import PatientGroup

    name = "ward A"
    g = PatientGroup(name=name)

    patients = ["Geoff", "Jane"]
    for p in patients:
        g.add_patient(p)

    iter(g)

# Doctors
def test_create_doctor():
    from inflammation.models import Doctor

    name = "House"
    d = Doctor(name=name)

    assert d.name == name


def test_doctor_is_person():
    from inflammation.models import Doctor, Person

    name = "House"
    d = Doctor(name=name)

    assert isinstance(d, Person)


def test_doctor_has_patient_group():
    from inflammation.models import Doctor, PatientGroup

    name = "House"
    d = Doctor(name=name)

    assert isinstance(d.patients, PatientGroup)


def test_doctor_patients_added_correctly():
    from inflammation.models import Doctor, Patient
    patients = ["Gregg", "Jane", "Geoff"]

    name = "House"
    d = Doctor(name=name)
    for p in patients:
        d.add_patient(p)

    assert all([isinstance(p, Patient) for p in d.patients])
    assert [p.name for p in d.patients] == patients


# Treatments
def test_create_treatment():
    from inflammation.models import Treatment
    name = "sugar"
    amount = 1
    units = "g"
    t = Treatment(name=name, amount=amount, units=units)

    assert t.name == name
    assert t.amount == amount
    assert t.units == units


# TreatmentGroups
def test_add_treatment():
    from inflammation.models import TreatmentGroup, Treatment
    g = TreatmentGroup(name="Placebo")

    name = "sugar"
    amount = 1
    units = "g"
    g.set_treatment(name, amount, units)

    assert isinstance(g.treatment, Treatment)


def test_treatment_group_is_group():
    from inflammation.models import TreatmentGroup, PatientGroup
    g = TreatmentGroup(name="Placebo")

    assert isinstance(g, PatientGroup)
