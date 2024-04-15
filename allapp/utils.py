from geopy.distance import geodesic

def find_nearest_clinic(patient_latitude, patient_longitude, clinic_locations):
    """
    Finds the nearest clinic to the given patient coordinates.

    Args:
    - patient_latitude (float): Latitude of the patient's location.
    - patient_longitude (float): Longitude of the patient's location.
    - clinic_locations (list): List of tuples containing clinic names, latitude, and longitude.

    Returns:
    - nearest_clinic (tuple): Latitude and longitude of the nearest clinic.
    - min_distance (float): Minimum distance to the nearest clinic.
    - clinic_name (str): Name of the nearest clinic.
    """
    nearest_distance = float('inf')  # Initialize with infinity
    nearest_clinic = None
    clinic_name = None

    for clinic_name, clinic_latitude, clinic_longitude in clinic_locations:
        clinic_location = (clinic_latitude, clinic_longitude)
        patient_location = (patient_latitude, patient_longitude)
        distance = geodesic(patient_location, clinic_location).kilometers

        if distance < nearest_distance:
            nearest_distance = distance
            nearest_clinic = clinic_location
            clinic_name = clinic_name

    return nearest_clinic, nearest_distance, clinic_name