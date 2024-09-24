# Imports
import pandas as pd
from random import random
import sklearn
from sklearn.model_selection import train_test_split
from IPython.display import display


# Function to load data
def load_data(data_path):
    data_df = pd.read_csv(data_path)

    nr_classes = data_df['Survived'].unique()   # Nr of classes to predict
    
    # Shuffle data
    data_df = data_df.sample(frac=1)

    # Train test split 80/20
    train_df, test_df = train_test_split(data_df, test_size=0.2, random_state=42)

    # Sort training data by classification
    sorted_train_df = train_df.sort_values(by='Survived')     # Sort by Survived to get the rows for different classes

    # Split test data into x and y
    x_test = test_df.drop(columns='Survived')   # test data features
    y_test = test_df['Survived']                # test data classification

    
    # Training data survived
    training_data_survived = sorted_train_df[sorted_train_df['Survived'] == 1]
    print('training_data_survived')
    display(training_data_survived)

    # Training data not survived 
    training_data_not_survived = sorted_train_df[sorted_train_df['Survived'] == 0]
    print('training_data_not_survived')
    display(training_data_not_survived)

    # Split target from features
    x_train_survived = training_data_survived.drop(columns='Survived')              # Features data
    y_train_survived = training_data_survived['Survived']                           # Target data

    # Split target from features
    x_train_not_survived = training_data_not_survived.drop(columns='Survived')      # Features data
    y_train_not_survived = training_data_not_survived['Survived']                   # Target data
    
    
    return nr_classes, x_train_survived, x_train_not_survived, x_test, y_test



# Function to convert dataframe into list of dictionaries
def format_data_dictionaries(dataframe):
    data = []

    for _, row in dataframe.iterrows():
        dictionary = {}
        # loop over rows and create key-value pairs
        for col in dataframe.columns:
            dictionary[col] = bool(row[col])    # Convert binary to bool
        data.append(dictionary)

    # Returns list of dictionaries
    return data


# Create / Initiate rules
def initiate_rules(nr_rules, example_data_dict):
    # Turn example_data_dict into a dict with negated values as well
    dictionary_negated = {}
    for key, value in example_data_dict.items():
        dictionary_negated[key] = 5
        dictionary_negated[f'NOT {key}'] = 5

    rules = []
    for i in range(nr_rules):
        rule = Memory(0.8, 0.2, dictionary_negated)
        rules.append(rule)

    return rules

# Memory class used to store the values of rules
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
        if  self.memory[literal] < 10:
            self.memory[literal] += 1


# Evaluate condition
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


# Type i feedback to memorize true assesments and forget remaining literals
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


# Type ii feedback to momorize the false literals that are forgotten to increase the discrimination
def type_ii_feedback(observation, memory):
    if evaluate_condition(observation, memory.get_condition()) == True:
        for feature in observation:
            if observation[feature] == False:
                memory.memorize_always(feature)
            elif observation[feature] == True:
                memory.memorize_always('NOT ' + feature)



# Start of program
if __name__ == '__main__':
    print('Start program')

    data_path = 'titanic_binary_dataset.csv'

    nr_classes, x_train_survived, x_train_not_survived, x_test, y_test = load_data(data_path)

    survived_data = format_data_dictionaries(x_train_survived)
    not_survived_data = format_data_dictionaries(x_train_not_survived)

    print(survived_data[0])

    #rules = initiate_rules(Nr_rules_per_class)

    Nr_of_classes = 2
    Nr_rules_per_class = 5
    epochs = 100

    # Create n rules, and assign the rules to different classes to predict
    survived_rules = initiate_rules(Nr_rules_per_class, survived_data[0])   # Send in nr of rules and one row of data to create negated rules from
    not_survived_rules = initiate_rules(Nr_rules_per_class, not_survived_data[0])

    print(survived_rules[0].get_memory())

    # Train rules on data
    for i in range(epochs):
        # Loop the survived data over the survived-rules
        for survived_observation in survived_data:
            for survived_rule in survived_rules:
                evaluation = evaluate_condition(survived_observation, survived_rule.get_condition())
                if evaluation == True:  # Correctly classify entry
                    type_i_feedback(survived_observation, survived_rule)
                else:                   # Wrongly classified entry
                    type_ii_feedback(survived_observation, survived_rule)
        
        # Loop the survived data over the not survived-rules
        for survived_observation in survived_data:
            for not_survived_rule in not_survived_rules:
                evaluation = evaluate_condition(survived_observation, not_survived_rule.get_condition())
                if evaluation == True:  # Correctly classify entry
                    type_i_feedback(survived_observation, not_survived_rule)
                else:                   # Wrongly classified entry
                    type_ii_feedback(survived_observation, not_survived_rule)

        # Loop the not survived data over the survived rules
        for not_survived_observation in not_survived_data:
            for survived_rule in survived_rules:
                evaluation = evaluate_condition(not_survived_observation, survived_rule.get_condition())
                if evaluation == False:  # Correctly classify entry
                    type_i_feedback(not_survived_observation, survived_rule)
                else:                   # Wrongly classified entry
                    type_ii_feedback(not_survived_observation, survived_rule)

        # Loop the not survived data over the not-survived rules
        for not_survived_observation in not_survived_data:
            for not_survived_rule in not_survived_rules:
                evaluation = evaluate_condition(not_survived_observation, not_survived_rule.get_condition())
                if evaluation == False:  # Correctly classify entry
                    type_i_feedback(not_survived_observation, not_survived_rule)
                else:                   # Wrongly classified entry
                    type_ii_feedback(not_survived_observation, not_survived_rule)


    print('test regel etter trening?')
    print(survived_rules[0].get_memory())
    print(survived_rules[0].get_condition())
    print('------------------------------')
    print(survived_rules[1].get_memory())
    print(survived_rules[1].get_condition())
    print('------------------------------')
    print(not_survived_rules[0].get_memory())
    print(not_survived_rules[0].get_condition())
    print('------------------------------')
    print(not_survived_rules[1].get_memory())
    print(not_survived_rules[1].get_condition())


    # model inference
    x_test_data = format_data_dictionaries(x_test)

    #for i in range(len(x_test_data)):
