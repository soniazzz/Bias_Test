from django.db import models


class BiasTestQuestion(models.Model):
    question_text = models.TextField()
    option_A = models.TextField()
    point_for_optionA = models.IntegerField()
    option_B = models.TextField()
    point_for_optionB = models.IntegerField()
    option_C = models.TextField()
    point_for_optionC = models.IntegerField()
    option_D = models.TextField()
    point_for_optionD = models.IntegerField()
    test_for_bias_index = models.IntegerField()




class User(models.Model):
    user_name = models.CharField(max_length=255)
    user_id = models.IntegerField()
    phone_number = models.CharField(max_length=20)
    team = models.CharField(max_length=20)
    possibility_biases_1 = models.FloatField(default=0, null=True, blank=True)
    possibility_biases_2 = models.FloatField(default=0, null=True, blank=True)
    possibility_biases_3 = models.FloatField(default=0, null=True, blank=True)
    possibility_biases_4 = models.FloatField(default=0, null=True, blank=True)
    possibility_biases_5 = models.FloatField(default=0, null=True, blank=True)

    def update_possibility_biases(self, result_dict):
        for bias_index, possibility in result_dict.items():
            field_name = f"possibility_biases_{bias_index}"
            setattr(self, field_name, possibility)
        self.save()

'''
# Create a new question instance
question1 = BiasTestQuestion(
    question_text="How strongly do you associate science with males and females?",
    option_A=["Strongly for male"],
    point_for_optionA=1,
    option_B=["Strongly for female"],
    point_for_optionB=-1,
    option_C=["Neither male or female"],
    point_for_optionC=0,
    option_D=["Don't want to answer"],
    point_for_optionD=0,
    test_for_bias_index=1
)

# Save the question instance to the database
question1.save()

# Create a new question instance
question2 = BiasTestQuestion(
    question_text="How strongly do you associate liberal arts with males and females?",
    option_A=["Strongly for male"],
    point_for_optionA=1,
    option_B=["Strongly for female"],
    point_for_optionB=-1,
    option_C=["Neither male or female"],
    point_for_optionC=0,
    option_D=["Don't want to answer"],
    point_for_optionD=0,
    test_for_bias_index=2
)

# Save the question instance to the database
question2.save()

# Create a new user instance
user = User(
    user_name="Tom",
    user_id=30351234567,
    phone_number="12345678",
    team="Marketing",
    possibility_biases_1=0.04,
    possibility_biases_2=0.02,
    possibility_biases_3=0.1,
    possibility_biases_4=0.03,
    possibility_biases_5=0.00
)

# Save the user instance to the database
user.save()
'''