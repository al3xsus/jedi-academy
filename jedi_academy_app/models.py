from django.db import models


class Planet(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name

    class Meta:
        db_table = "planet"


class Jedi(models.Model):
    name = models.CharField(max_length=100, unique=True)
    planet = models.ForeignKey(Planet, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

    class Meta:
        db_table = "jedi"


class Candidate(models.Model):
    name = models.CharField(max_length=100, unique=True)
    planet = models.ForeignKey(Planet, on_delete=models.CASCADE)
    age = models.PositiveIntegerField()
    email = models.EmailField()

    def __str__(self):
        return self.name

    class Meta:
        db_table = "candidate"


class Trial(models.Model):
    unique_order_code = models.CharField(max_length=100, unique=True)
    question1 = models.CharField(max_length=256, default="")
    question2 = models.CharField(max_length=256, default="")
    question3 = models.CharField(max_length=256, default="")

    def __str__(self):
        return self.unique_order_code

    class Meta:
        db_table = "trial"


class Answers(models.Model):
    trial = models.ForeignKey(Trial, on_delete=models.CASCADE)
    candidate = models.ForeignKey(Candidate, on_delete=models.CASCADE)
    answer1 = models.BooleanField()
    answer2 = models.BooleanField()
    answer3 = models.BooleanField()

    class Meta:
        db_table = "answers"


class Students(models.Model):
    jedi = models.ForeignKey(Jedi, on_delete=models.CASCADE)
    padawans = models.ManyToManyField(Candidate)

    class Meta:
        db_table = "students"
