import decimal

def Round0(value, sf):
	
    if value == 0.0:
        return "0"

    # Convert the value to a decimal
    decimal_value = decimal.Decimal(str(value))

    # Round the decimal to the desired number of significant figures
    rounded_decimal = decimal_value.quantize(
        decimal.Decimal('0.' + '0' * (sf - 1)),
        rounding=decimal.ROUND_HALF_UP
    )

    # Convert the rounded decimal back to a string
    rounded_str = str(rounded_decimal).rstrip('0').rstrip('.')

    return rounded_str

def Round1(value, sf):
    if value == 0.0:
        return "0"

    # Convert the value to a decimal
    decimal_value = decimal.Decimal(str(value))

    # Calculate the magnitude of the first significant digit
    magnitude = decimal_value.adjusted() - sf + 1

    # Calculate the rounding factor based on the first significant digit
    rounding_factor = decimal.Decimal('1') / decimal.Decimal(10 ** magnitude)

    # Round the decimal to the desired number of significant figures
    rounded_decimal = (decimal_value * rounding_factor).quantize(decimal.Decimal('0.00'))

    # Convert the rounded decimal back to a string
    rounded_str = str(rounded_decimal)

    return rounded_str

def Round3(value, sf):
    if value == 0.0:
        return "0"

    # Convert the value to a decimal
    decimal_value = decimal.Decimal(str(value))

    # Calculate the magnitude of the first significant digit
    magnitude = decimal_value.adjusted()

    # Calculate the rounding factor based on the first significant digit
    rounding_factor = decimal.Decimal(10) ** (sf - magnitude - 1)

    # Round the decimal to the desired number of significant figures
    rounded_decimal = (decimal_value * rounding_factor).quantize(decimal.Decimal('0.00'))

    # Convert the rounded decimal back to a string
    rounded_str = str(rounded_decimal)

    return rounded_str


def Round4(value, sf):
    if value == 0.0:
        return "0"

    # Determine the absolute value of the float
    abs_value = abs(value)

    # Check if scientific notation should be used
    use_scientific = abs_value >= 10 ** 6 # arbitrary rule, adjust accordingly

    # Format the float accordingly
    formatted_str = "{:.{}f}".format(value, sf - 1)

    # if/ use_scientific==False: 

        # Get the exponent 

        # Get value 

        # Add appropriate number of zeros to formatted string

    return formatted_str


from decimal import Decimal

def Round6(value, sf):
    if value == 0.0:
        return "0"

    # Determine the absolute value of the float
    abs_value = abs(value)

    # Check if scientific notation should be used
    use_scientific = abs_value >= 10 ** 6  # Arbitrary rule, adjust accordingly

    # Format the float accordingly
    formatted_str = "{:.{}f}".format(value, sf - 1)

    if not use_scientific:
        # Check if the value is an integer
        if int(value) == value:
            return "{:.0f}".format(value)

        # Convert the value to a Decimal object
        decimal_value = Decimal(str(value))

        # Get the exponent
        exponent = decimal_value.as_tuple().exponent

        # Get value
        value_str = "{:.{}f}".format(value, sf - 1 - exponent)

        # Add appropriate number of zeros to formatted string
        formatted_str = value_str + "0" * (sf - 1 - len(value_str))

    return formatted_str

import math

def Round(value, sf):
    if value == 0.0:
        return "0"

    # Determine the order of magnitude
    magnitude = math.floor(math.log10(abs(value))) + 1

    # Calculate the scale factor
    scale_factor = sf - magnitude

    # Truncate the float to the desired number of significant figures
    truncated_value = math.trunc(value * 10 ** scale_factor) / 10 ** scale_factor

    # Convert the truncated value to a string
    truncated_str = str(truncated_value).rstrip('0').rstrip('.')

    return truncated_str

print(Round(12.250995295734228, 1))  # Output: 10


# print(Round(12.250995295734228, 1))

print(Round(134.2723, 1)) # returns 134, should return 100
print(Round(134.2723, 2)) # returns 134.3, should return 130
print(Round(134.2723, 3)) # returns 134.27, should return 134
print(Round(134.2723, 4)) # returns 134.272, should return 134.3
print(Round(134.2723, 5)) # returns 134.2723, should return 134.272