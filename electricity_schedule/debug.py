def pretty(d):
    for key, value in d.items():
        if len(value) == 0:
            continue

        print(key, end=':\n')
        for i in value:
            print(f'[{i[0]} - {i[1]}]')
        print()