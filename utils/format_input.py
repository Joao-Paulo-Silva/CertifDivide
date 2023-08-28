def validate_input(new_value):
    if new_value == "":
        return True 
    try:
        float(new_value)
        return True
    except ValueError:
        return False