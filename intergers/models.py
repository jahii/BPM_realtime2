from django.db import models


# Create your models here.
class Serial_data(models.Model):
    class Meta:
        db_table = "serial"

    data = models.IntegerField(default=0)


#
class NewTable(models.Model):
    bpm = models.IntegerField()
    ibi = models.IntegerField()
    mysignal = models.IntegerField()

    class Meta:
        db_table = 'new_table'
# class new_table(models.Model):
#     class Meta:
#         db_table = "new_table"
#
