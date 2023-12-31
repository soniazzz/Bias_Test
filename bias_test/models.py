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

class UserSession(models.Model):
    session_token = models.CharField(max_length=32, primary_key=True)
    creation_timestamp = models.DateTimeField(auto_now_add=True)

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
    avatar = models.TextField(default='https://th.bing.com/th/id/R.945f33b643f2ceffcdae90fb57c61854?rik=ZbauAhRVa2agEw&riu=http%3a%2f%2fgetdrawings.com%2ffree-icon-bw%2fgeneric-avatar-icon-3.png&ehk=MEKRKETvvufVVLoShHum%2baEfkHOctyKClaf6qCu3Msg%3d&risl=&pid=ImgRaw&r=0')

    def update_possibility_biases(self, result_dict):
        for bias_index, possibility in result_dict.items():
            field_name = f"possibility_biases_{bias_index}"
            setattr(self, field_name, possibility)
        self.save()


class Article(models.Model):
    bias_index=models.IntegerField()
    head= models.TextField()
    brief= models.TextField()
    img= models.TextField()
    link= models.TextField()


class Post(models.Model):
    post_id = models.AutoField(primary_key=True)
    bias_index=models.IntegerField()
    poster_id=models.IntegerField()
    post_title=models.TextField()
    post_details = models.TextField()
    post_time=models.DateTimeField(auto_now_add=True)


class Reply(models.Model):
    reply_index = models.AutoField(primary_key=True)
    post_id=models.IntegerField(default=0)
    title = models.TextField()
    poster_id=models.IntegerField()
    post_date = models.DateTimeField(auto_now_add=True)
    details = models.TextField()
    parent_reply = models.ForeignKey('self', null=True, blank=True, on_delete=models.CASCADE, related_name='child_replies')

    def __str__(self):
        return self.title

    def replies(self):
        return Reply.objects.filter(parent_reply=self)



