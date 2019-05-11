#!/usr/bin/python
# -*- coding: utf-8 -*-

# Rodar como python 2

def get_message(variable, alphabet, rules, initial_variable, commands):
    word = initial_variable
    for command in commands:
        command -= 1
        key = rules[command].keys()[0]
        word = word.replace(key, rules[command][key], 1)
    return word


def is_validated(word):
    print("Resulado:")
    for value in result:
        if value not in alphabet:
            print("Palavra não valida")
            return

    print(result)
    print("Palavra valida")


if __name__ == "__main__":

    variable = raw_input("Escreva as variaveis separadas por espaço:").split()
    alphabet = raw_input("Escreva as letras do alfabeto por espaço:").split()

    rules = []
    rules_noformat = raw_input(
        "Escreva as regras separadas por (ex: X:Y,X:XaA)   :").split(',')

    for rule in rules_noformat:
        rule = rule.split(':')
        dict1 = {rule[0]: rule[1]} if rule[1] else {rule[0]: ""}
        rules.append(dict1)

    initial_variable = raw_input("Escreva a palavra inicial:")

    commands = [int(x) for x in raw_input(
        "Escreva os comandos por espaço:").split()]

    result = get_message(variable, alphabet, rules, initial_variable, commands)
    is_validated(result)
