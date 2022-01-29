from password_strength import PasswordPolicy, PasswordStats




STRENGTH = 0.34

CAPITAL_LETTERS = 1

SPECIAL_LETTERS = 1

NUMBERS = 2

LENGTH = 8

NONLETTERS = 2

class PasswordUtil:
    def __init__(self, strength, upper_case, special_letters, numbers, length, noneletters):
        self.strength = strength
        self.upper_case_letters = upper_case
        self.special_letters = special_letters
        self.numbers = numbers
        self.length = length
        self.noneletters = noneletters


    @property
    def policy(self):
        _policy = PasswordPolicy.from_names(
            length=self.length,  # min length
            uppercase=self.upper_case_letters,  # need min.  uppercase letters
            numbers=self.numbers,  # need min. digits
            special=self.special_letters,  # need min. special characters
            nonletters=self.noneletters,  # need min. non-letter characters (digits, specials, anything)
            strength=self.strength
        )
        return _policy 

    def password_accepted(self, password):
        result = self.policy.test(password)
        if len(result) > 0:
            return False
        return True

    @staticmethod
    def password_strength(password):# 1(weak), 2(mediam), 3(strong)
        stats = PasswordStats(password)
        pass_strength = stats.strength()

        if pass_strength < 0.34:
            return 1
        elif pass_strength < 0.6:
            return 2
        return 3

        

main_password_policy = PasswordUtil(
    STRENGTH,
    CAPITAL_LETTERS,
    SPECIAL_LETTERS,
    NUMBERS,
    LENGTH,
    NONLETTERS
)




