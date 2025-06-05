import math

def calculate_tmb(sex: str, weight_kg: float, height_cm: float, age_years: int) -> float:
    """Calculates the Basal Metabolic Rate (TMB) based on sex, weight, height, and age.

    Args:
        sex: The sex of the individual ('Masculino' for male, 'Femenino' for female).
        weight_kg: Weight in kilograms.
        height_cm: Height in centimeters.
        age_years: Age in years.

    Returns:
        The calculated TMB in kcal.

    Raises:
        ValueError: If the sex is not 'Masculino' or 'Femenino'.
    """
    if sex == 'Masculino':
        tmb = 88.362 + (13.397 * weight_kg) + (4.799 * height_cm) - (5.677 * age_years)
    elif sex == 'Femenino':
        tmb = 447.593 + (9.247 * weight_kg) + (3.098 * height_cm) - (4.333 * age_years)
    else:
        raise ValueError("Sex must be 'Masculino' or 'Femenino'")
    return tmb

def calculate_af(exercise_minutes: float) -> float:
    """Calculates the Physical Activity Factor (AF) based on daily exercise minutes.

    Args:
        exercise_minutes: Minutes of exercise per day.

    Returns:
        The calculated AF.
    """
    af = 1.2 + 0.01 * exercise_minutes
    return af

def calculate_gb(tmb: float, af: float) -> float:
    """Calculates the Gross Daily Expenditure (GB) based on TMB and AF.

    Args:
        tmb: Basal Metabolic Rate (TMB).
        af: Physical Activity Factor (AF).

    Returns:
        The calculated GB in kcal.
    """
    gb = tmb * af
    return gb