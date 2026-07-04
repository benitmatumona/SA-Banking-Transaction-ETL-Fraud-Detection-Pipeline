from faker import Faker

faker = Faker()

for student_id in range(1, 6):
    print(
        f"{student_id}, {faker.name()}, Grade {faker.random_int(min=8, max=12)}"
    )