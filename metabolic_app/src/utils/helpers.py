def validate_numeric_input(value: str, field_name: str) -> float:
    """Validates if a string value can be converted to a positive float.

    Args:
        value: The string value to validate.
        field_name: The name of the field being validated (for error messages).

    Returns:
        The validated value as a float.

    Raises:
        ValueError: If the value is not a valid positive number.
    """
    try:
        numeric_value = float(value)
        if numeric_value < 0:
            raise ValueError(f"{field_name} must be a positive number.")
        return numeric_value
    except ValueError:
        raise ValueError(f"Invalid input for {field_name}. Please enter a valid number.")

def validate_integer_input(value: str, field_name: str) -> int:
    """Validates if a string value can be converted to a positive integer.

    Args:
        value: The string value to validate.
        field_name: The name of the field being validated (for error messages).

    Returns:
        The validated value as an integer.

    Raises:
        ValueError: If the value is not a valid positive integer.
    """
    try:
        int_value = int(value)
        if int_value < 0:
            raise ValueError(f"{field_name} must be a positive integer.")
        return int_value
    except ValueError:
        raise ValueError(f"Invalid input for {field_name}. Please enter a valid integer.")

def validate_sex_input(value: str) -> str:
    """Validates if the sex input is either 'Masculino' or 'Femenino'.

    Args:
        value: The string value for sex.

    Returns:
        The validated sex string.

    Raises:
        ValueError: If the sex is not 'Masculino' or 'Femenino'.
    """
    if value not in ['Masculino', 'Femenino']:
        raise ValueError("Sex must be 'Masculino' or 'Femenino'.")
    return value 