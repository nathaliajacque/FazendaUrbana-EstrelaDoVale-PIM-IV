import re
from django.core.exceptions import ValidationError


def validate_cnpj(value):
    cnpj = re.sub(r"\D", "", value)  # Remove non-numeric characters
    if len(cnpj) != 14:
        raise ValidationError("CNPJ deve ter exatamente 14 dígitos.")

    # Validação do CNPJ
    def calculate_digit(digits, weights):
        sum = 0
        for i in range(len(digits)):
            sum += int(digits[i]) * weights[i]
        remainder = sum % 11
        return "0" if remainder < 2 else str(11 - remainder)

    if cnpj in (c * 14 for c in "1234567890"):
        raise ValidationError("CNPJ inválido.")

    weights1 = [5, 4, 3, 2, 9, 8, 7, 6, 5, 4, 3, 2]
    weights2 = [6] + weights1

    calculated_digit1 = calculate_digit(cnpj[:12], weights1)
    calculated_digit2 = calculate_digit(cnpj[:13], weights2)

    if cnpj[-2:] != calculated_digit1 + calculated_digit2:
        raise ValidationError("CNPJ inválido.")
