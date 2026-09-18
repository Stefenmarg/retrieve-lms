import re

email_regex = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")


def has_valid_format(v):
    return bool(email_regex.match(v))


def has_no_spaces(v):
    return " " not in v


def has_single_at(v):
    return v.count("@") == 1


def has_valid_domain(v):
    if "@" not in v:
        return False
    domain = v.split("@")[-1]
    return "." in domain and not domain.startswith(".") and not domain.endswith(".")


def has_reasonable_length(v):
    return len(v) <= 254  # RFC 5321 max length


email_validation_rules = {
    "Email is required": lambda v: len(v.strip()) > 0,
    "No spaces allowed": has_no_spaces,
    "Must contain exactly one @": has_single_at,
    "Enter a valid email address": has_valid_format,
    "Email is too long": has_reasonable_length,
}


password_validation_rules = {
    "Too short (min 8 characters)": lambda v: len(v) >= 8,
    "Too long (max 64 characters)": lambda v: len(v) <= 64,
    "Needs an uppercase letter": lambda v: any(c.isupper() for c in v),
    "Needs a lowercase letter": lambda v: any(c.islower() for c in v),
    "Needs a digit": lambda v: any(c.isdigit() for c in v),
    "Needs a special character": lambda v: any(not c.isalnum() for c in v),
}

full_name_validation_rules = {
    "Too short (min 3 characterss)": lambda v: len(v) >= 3,
    "Too long (max 255 characterss)": lambda v: len(v) <= 255,
}
