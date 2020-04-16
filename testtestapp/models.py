from django.db import models

# Create your models here.

class Tipo_Pregunta(models.Model):
    id = models.AutoField(primary_key=True)
    nombre_tipo = models.CharField(max_length=200,null=False,unique=True)

    def save(self):
        super(Tipo_Pregunta,self).save()

    def __str__(self):
        return self.nombre_tipo

class Categoria(models.Model):
    nombre = models.CharField(max_length=200,primary_key=True)
    descripcion = models.CharField(max_length=400,null=True,unique=True)

    def save(self):
        super(Categoria,self).save()

    def __str__(self):
        return self.nombre

class Usuario(models.Model):
    nombre = models.CharField(max_length=200,primary_key=True)
    correo = models.EmailField(null=False,unique=True)
    test_creados = models.IntegerField(null=False,default=0)
    fecha_nacimiento = models.DateField(null=False)

    def save(self):
        super(Usuario,self).save()

    def __str__(self):
        return self.nombre

class Test(models.Model):
    nombre = models.CharField(max_length=200,unique=True)
    numero_preguntas = models.IntegerField(null=False,default=0)
    fecha_test = models.DateField(null=False)
    duracion = models.IntegerField(null=False)
    maxima_puntuacion = models.IntegerField(null=False)
    descripcion = models.CharField(max_length=4000,null=True)
    creador = models.ForeignKey(Usuario, on_delete = models.CASCADE)

    def save(self):
        super(Test,self).save()

    def __str__(self):
        return "{} {}".format(self.nombre, self.creador)

class Grupo(models.Model):
    numero_integrantes = models.IntegerField(null=False,default=0)
    nombre = models.CharField(max_length=200,unique=True)
    contrasena = models.CharField(max_length=200)
    descripcion = models.CharField(max_length=4000,null=True)
    tests = models.ManyToManyField(Test)
    usuarios = models.ManyToManyField(Usuario)

    def save(self):
        super(Grupo,self).save()

    def __str__(self):
        return self.nombre

class Resultado(models.Model):
    calificacion = models.DecimalField(max_digits=6,decimal_places=4)
    test = models.ForeignKey(Test, on_delete = models.CASCADE)
    usuario = models.ForeignKey(Usuario, on_delete = models.CASCADE)

    def save(self):
        super(Resultado,self).save()

    def __str__(self):
        return "{} {}".format(self.test, self.usuario)

class Pregunta(models.Model):
    enunciado =  models.CharField(max_length=4000)
    puntos = models.DecimalField(max_digits=6,decimal_places=4,default=0)
    test = models.ForeignKey(Test, on_delete = models.CASCADE)
    tipo = models.ForeignKey(Tipo_Pregunta, on_delete = models.CASCADE)

    def save(self):
        super(Pregunta,self).save()

    def __str__(self):
        return "{} {}".format(self.test, self.id)

class Opcion(models.Model):
    enunciado =  models.CharField(max_length=4000)
    puntos = models.DecimalField(max_digits=6,decimal_places=4,default=0)
    pregunta = models.ForeignKey(Pregunta, on_delete = models.CASCADE)

    def save(self):
        super(Pregunta,self).save()

    def __str__(self):
        return "{} {}".format(self.test, self.id)
