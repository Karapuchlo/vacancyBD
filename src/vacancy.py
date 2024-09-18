class Vacancy:
    def __init__(self, employer_name, name, salary, alternate_url):
        self.employer_name = employer_name
        self.name = name
        self.salary = salary
        self.alternate_url = alternate_url

    def __str__(self):
        return f"Вакансия {self.name} в {self.employer_name} с зарплатой {self.salary}"

    def __repr__(self):
        return f"Vacancy(employer_name='{self.employer_name}', name='{self.name}', salary='{self.salary}', alternate_url='{self.alternate_url}')"

    @property
    def dict(self):
        return {
            'employer_name': self.employer_name,
            'name': self.name,
            'salary': self.salary,
            'alternate_url': self.alternate_url
        }
