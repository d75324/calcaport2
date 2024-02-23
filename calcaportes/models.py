from django.db import models
from django.utils import timezone
from datetime import datetime

COMISIONES_AFAP = {
    'INTEGRA': 0.12,
    'SURACAP': 0.114,
    'UNIONCP': 0.12,
    'REPUBLI': 0.114,
}

class CalculoAportes(models.Model):

    AFAPUY_CHOICES = [
        ('INTEGRA', 'Integración AFAP'),
        ('SURACAP', 'Sura Capitales'),
        ('UNIONCP', 'Unión Capital'),
        ('REPUBLI', 'República AFAP'),
    ]

    created_at = models.DateTimeField(auto_now_add=True)
    nombre_empleado = models.CharField(max_length=50)
    apellido_empleado = models.CharField(max_length=50)
    salario_base = models.IntegerField()
    afap = models.CharField(max_length=7, choices=AFAPUY_CHOICES)
    fecha_ingreso = models.DateTimeField()
    cantidad_de_hijos = models.IntegerField()

    class Meta:
        app_label = 'calcaportes'

    def __str__(self):
        return (f'{self.nombre_empleado} {self.apellido_empleado}')
    
    def calcular_antiguedad_en_meses(self, fecha_ingreso):
        fecha_actual = datetime.now()
        fecha_actual_aware = timezone.make_aware(fecha_actual, timezone.get_current_timezone())
        diferencia_en_dias = (fecha_actual_aware - self.fecha_ingreso).days
        antiguedad_en_meses = diferencia_en_dias // 30
        return antiguedad_en_meses
    
    def bonifica(self):
        cantidad_meses_trabajados = self.calcular_antiguedad_en_meses(self.fecha_ingreso)
        uno_porciento_del_salario_base = self.salario_base / 100
        calculo_bonificacion = cantidad_meses_trabajados * uno_porciento_del_salario_base
        return calculo_bonificacion
    
    def asigna(self):
        factor_asignacion = 0.05
        total_asignacion = (self.salario_base * factor_asignacion) * self.cantidad_de_hijos
        return total_asignacion

    def pago_fonasa(self):
        pago_fonasa = self.salario_base * 0.07
        return pago_fonasa
    
    def pago_afap(self):
        comision_afap = COMISIONES_AFAP[self.afap]
        return self.salario_base * comision_afap
    
    def base_imponible(self):
        a = self.bonifica()
        b = self.asigna()
        base_impo = self.salario_base + a + b
        return base_impo