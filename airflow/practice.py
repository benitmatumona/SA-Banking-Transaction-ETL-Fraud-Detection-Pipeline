from faker import Faker


f = Faker()

for i in range(1, 4):
    print(
        f"{i}, {f.name()} {f.last_name()}, Grade {f.random_int(1, 12)}"
        )
