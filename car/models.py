from django.db import models

class Employee(models.Model):
    name = models.CharField(max_length=50)

    class Meta:
        ordering = ('name',)

    def __str__(self):
        return self.name


class Car(models.Model):
    reg_num = models.CharField(max_length=20)
    vin_num = models.CharField(max_length=20)
    brand = models.ForeignKey('Brand', on_delete=models.SET_NULL, related_name='brand', null=True)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('-created',)

    def __str__(self):
        return f'{self.reg_num} --- {self.vin_num} --- {self.brand.name}'

class Brand(models.Model):
    name = models.CharField(max_length=30)

    class Meta:
        ordering = ('name', )

    def __str__(self):
        return self.name




class StatusManager(models.Manager):

    def get_queryset(self):
        return super(StatusManager, self).get_queryset().filter(status='in_progress')




class Repair(models.Model):

    STATUS_CHOICES = (
        ('in_progress', 'InProgress'),
        ('finish', 'Finish')
    )
    body = models.TextField()
    created = models.DateField()
    updated = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=15, choices=STATUS_CHOICES, default='in_progress')
    car = models.ForeignKey('Car', on_delete=models.SET_NULL, related_name='repair', null=True)

    workman = models.ManyToManyField('Employee', blank=True)

    objects = models.Manager() # The default managere.
    progress = StatusManager() # My custom manager.
    
    class Meta:
        ordering = ('-created', )
    
    def __str__(self):
        return self.body[:30]



