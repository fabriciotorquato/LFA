def getStringSolution(solution):
    solution.sort(key=lambda x: x.name)
    string_solution = '|'.join(
        [str(item.name) for item in solution])
    return string_solution
