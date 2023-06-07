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

    def __str__(self):
        return self.question_text




class User(models.Model):
    user_name = models.CharField(max_length=255)
    user_id = models.AutoField(primary_key=True)
    password = models.CharField(max_length=50, default=0, null=True, blank=True)
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