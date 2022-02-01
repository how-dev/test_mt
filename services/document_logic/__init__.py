import random


class BrazilianDocumentLogics:
    document = None

    @staticmethod
    def format_cpf(cpf):
        return f"{cpf[:3]}.{cpf[3:6]}.{cpf[6:9]}-{cpf[9:]}"

    @staticmethod
    def get_digit_algorithm(cpf):
        cpf_verify = list(cpf)
        cpf_verify.reverse()

        sum_char = 0
        count = 2
        for char in cpf_verify:
            sum_char += int(char) * count
            count += 1

        cpf_verify.reverse()
        cpf_verify = "".join(cpf_verify)

        rest = sum_char % 11

        if rest < 2:
            return cpf_verify + "0"

        digit = str(11 - rest)

        return cpf_verify + digit

    def random_eleven_digits(self):
        cpf = ""

        for _ in range(11):
            cpf += str(random.randrange(0, 10))

        cpf_verify = cpf[:9]
        for _ in range(2):
            cpf_verify = self.get_digit_algorithm(cpf_verify)

        if cpf == cpf_verify:
            return cpf
        else:
            return False

    def force_valid_cpf(self):
        cpf = self.random_eleven_digits()
        if cpf is not False:
            return cpf
        else:
            return self.force_valid_cpf()

    def validate_cpf(self, cpf):
        cpf_verify = cpf[:9]
        for _ in range(2):
            cpf_verify = self.get_digit_algorithm(cpf_verify)

        return cpf == cpf_verify

    def is_valid_document(self):
        return self.validate_cpf(self.document)
