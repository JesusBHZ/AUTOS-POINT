from tortoise import fields, Model

class Autos(Model):
    id_auto = fields.IntField(pk=True)
    matricula = fields.CharField(max_length=100)
    modelo = fields.CharField(max_length=100)
    marca = fields.CharField(max_length=100)
    color = fields.CharField(max_length=100)
    motor = fields.CharField(max_length=100)

    class Meta:
        db = "default" 