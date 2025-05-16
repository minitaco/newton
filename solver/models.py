from django.db import models

class Calculation(models.Model):
    function = models.CharField(max_length=100)
    initial_guess = models.FloatField()
    result = models.FloatField(null=True, blank=True)
    iterations = models.JSONField(default=list)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"f(x)={self.function}, x0={self.initial_guess}"
