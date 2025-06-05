import pytest
from src.models.metabolic import calculate_tmb, calculate_af, calculate_gb

def test_calculate_tmb_male():
    """Tests the calculate_tmb function for male."""
    # Using example values (adjust if needed based on realistic data)
    weight_kg = 70.0
    height_cm = 175.0
    age_years = 30
    expected_tmb = 88.362 + (13.397 * weight_kg) + (4.799 * height_cm) - (5.677 * age_years)
    assert calculate_tmb('Masculino', weight_kg, height_cm, age_years) == pytest.approx(expected_tmb)

def test_calculate_tmb_female():
    """Tests the calculate_tmb function for female."""
    # Using example values (adjust if needed based on realistic data)
    weight_kg = 60.0
    height_cm = 163.0
    age_years = 25
    expected_tmb = 447.593 + (9.247 * weight_kg) + (3.098 * height_cm) - (4.333 * age_years)
    assert calculate_tmb('Femenino', weight_kg, height_cm, age_years) == pytest.approx(expected_tmb)

def test_calculate_tmb_invalid_sex():
    """Tests the calculate_tmb function with invalid sex."""
    with pytest.raises(ValueError):
        calculate_tmb('Other', 70.0, 175.0, 30)

def test_calculate_af():
    """Tests the calculate_af function."""
    exercise_minutes = 30
    expected_af = 1.2 + 0.01 * exercise_minutes
    assert calculate_af(exercise_minutes) == pytest.approx(expected_af)

def test_calculate_gb():
    """Tests the calculate_gb function."""
    tmb = 1500.0
    af = 1.5
    expected_gb = tmb * af
    assert calculate_gb(tmb, af) == pytest.approx(expected_gb) 