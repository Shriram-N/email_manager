from datetime import datetime

class Condition:
    def __init__(self, field, operator, value):
        self.field = field
        self.operator = operator
        self.value = value

    def matches(self, email):
        pass

class ContainsCondition(Condition):
    def matches(self, email):
        return self.value.lower() in email[self.field].lower()

class DoesNotContainCondition(Condition):
    def matches(self, email):
        return self.value.lower() not in email[self.field].lower()

class EqualsCondition(Condition):
    def matches(self, email):
        return self.value.lower() == email[self.field].lower()

class DoesNotEqualCondition(Condition):
    def matches(self, email):
        return self.value.lower() != email[self.field].lower()

class LessThanCondition(Condition):
    def matches(self, email):
        return email[self.field] < datetime.strptime(self.value, '%Y-%m-%dT%H:%M:%S')

class GreaterThanCondition(Condition):
    def matches(self, email):
        return email[self.field] > datetime.strptime(self.value, '%Y-%m-%dT%H:%M:%S')
