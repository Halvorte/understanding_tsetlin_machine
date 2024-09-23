from random import random
from random import choice



# Memory class
class Memory:
    def __init__(self, forget_value, memorize_value, memory):
        self.memory = memory
        self.forget_value = forget_value
        self.memorize_value = memorize_value

    def get_memory(self):
        return self.memory

    def get_literals(self):
        return list(self.memory.keys())

    def get_condition(self):
        condition = []
        for literal in self.memory:
            if self.memory[literal] >= 6:
                condition.append(literal)
        return condition

    def memorize(self, literal):
        if random() <= self.memorize_value and self.memory[literal] < 10:
            self.memory[literal] += 1

    def forget(self, literal):
        if random() <= self.forget_value and self.memory[literal] > 1:
            self.memory[literal] -= 1

    def memorize_always(self, literal):
        if self.memory[literal] < 10:
            self.memory[literal] += 1


# Function to evaluate condition
def evaluate_condition(observation, condition):
    truth_value_of_condition = True
    for feature in observation:
        if feature in condition and observation[feature] == False:
            truth_value_of_condition = False
            break
        if 'NOT ' + feature in condition and observation[feature] == True:
            truth_value_of_condition = False
            break
    return truth_value_of_condition


# Function for type 1 feedback
def type_i_feedback(observation, memory):
    remaining_literals = memory.get_literals()
    if evaluate_condition(observation, memory.get_condition()) == True:
        for feature in observation:
            if observation[feature] == True:
                memory.memorize(feature)
                remaining_literals.remove(feature)
            elif observation[feature] == False:
                memory.memorize('NOT ' + feature)
                remaining_literals.remove('NOT ' + feature)
    for literal in remaining_literals:
        memory.forget(literal)


# Funciton for type 2 feedback
def type_ii_feedback(observation, memory):
    if evaluate_condition(observation, memory.get_condition()) == True:
        for feature in observation:
            if observation[feature] == False:
                memory.memorize_always(feature)
            elif observation[feature] == True:
                memory.memorize_always('NOT ' + feature)


# Classification function
def classify(observation, car_rules, plane_rules):
    vote_sum = 0
    for car_rule in car_rules:
        if evaluate_condition(observation, car_rule.get_condition()) == True:
            vote_sum += 1
    for plane_rule in plane_rules:
        if evaluate_condition(observation, plane_rule.get_condition()) == True:
            vote_sum -= 1
    if vote_sum >= 0:
        return "Recurrence"
    else:
        return "Non-Recurrence"


#
if __name__ == '__main__':
    # The dataset according to slide in presentation
    data = [
        {'lt40': False, 'ge40': True, 'premeno': False, '0-2': False, '3-5': True, '6-8': False,
         '1': False, '2': False, '3': True, 'Recurrence': True},
        {'lt40': True, 'ge40': False, 'premeno': False, '0-2': True, '3-5': True, '6-8': False,
         '1': False, '2': False, '3': True, 'Recurrence': False},
        {'lt40': False, 'ge40': True, 'premeno': False, '0-2': False, '3-5': False, '6-8': True,
         '1': False, '2': False, '3': True, 'Recurrence': True},
        {'lt40': False, 'ge40': True, 'premeno': False, '0-2': True, '3-5': False, '6-8': False,
         '1': False, '2': True, '3': False, 'Recurrence': False},
        {'lt40': False, 'ge40': False, 'premeno': True, '0-2': True, '3-5': False, '6-8': False,
         '1': False, '2': False, '3': True, 'Recurrence': True},
        {'lt40': False, 'ge40': False, 'premeno': True, '0-2': True, '3-5': False, '6-8': False,
         '1': True, '2': False, '3': False, 'Recurrence': False},
    ]

    recurrence = [
        {'lt40': False, 'ge40': True, 'premeno': False, '0-2': False, '3-5': True, '6-8': False,
         '1': False, '2': False, '3': True},
        {'lt40': False, 'ge40': True, 'premeno': False, '0-2': False, '3-5': False, '6-8': True,
         '1': False, '2': False, '3': True},
        {'lt40': False, 'ge40': False, 'premeno': True, '0-2': True, '3-5': False, '6-8': False,
         '1': False, '2': False, '3': True}
    ]

    nonRecurrence = [
        {'lt40': True, 'ge40': False, 'premeno': False, '0-2': True, '3-5': True, '6-8': False,
         '1': False, '2': False, '3': True},
        {'lt40': False, 'ge40': True, 'premeno': False, '0-2': True, '3-5': False, '6-8': False,
         '1': False, '2': True, '3': False},
        {'lt40': False, 'ge40': False, 'premeno': True, '0-2': True, '3-5': False, '6-8': False,
         '1': True, '2': False, '3': False}
    ]

    recurrence_r = Memory(0.8, 0.2, {'lt40': 5, 'NOT lt40': 5, 'ge40': 5, 'NOT ge40': 5, 'premeno': 5, 'NOT premeno': 5,
                           '0-2': 5, 'NOT 0-2': 5, '3-5': 5, 'NOT 3-5': 5, '6-8': 5, 'NOT 6-8': 5, '1': 5, 'NOT 1': 5,
                           '2': 5, 'NOT 2': 5, '3': 5, 'NOT 3': 5})

    non_recurrence = Memory(0.8, 0.2, {'lt40': 11, 'NOT lt40': 10, 'ge40': 1, 'NOT ge40': 1, 'premeno': 1, 'NOT premeno': 1,
                           '0-2': 1, 'NOT 0-2': 1, '3-5': 1, 'NOT 3-5': 1, '6-8': 1, 'NOT 6-8': 1, '1': 1, 'NOT 1': 1,
                           '2': 1, 'NOT 2': 1, '3': 10, 'NOT 3': 1})

    # Test rules
    R1 = ['3', 'NOT lt40']
    R2 = ['3', 'NOT lt40']
    R3 = ['0-2']

    # test the output of the test-rules on some of the data
    print(evaluate_condition(data[1], R1))
    print(evaluate_condition(data[1],R2))
    print(evaluate_condition(data[1], R3))


    # train the rule recurrence_r
    for i in range(100):
        observation_id = choice([0,1,2])
        rec = choice([0,1])     # Randomly select if the rule is correct or not/ randomly select what type of feedback to give
        if rec == 1:
            type_i_feedback(recurrence[observation_id], recurrence_r)
        else:
            type_ii_feedback(nonRecurrence[observation_id], recurrence_r)

    print('yo')
    print(recurrence_r.get_memory())
    print(recurrence_r.get_condition())