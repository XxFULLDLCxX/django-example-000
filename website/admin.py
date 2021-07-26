from django.contrib import admin

from .models import Contacto, Pregunta, Respuesta, PreguntasRespondidas, QuizUsuario
from .forms import ElegirInlineFormSet

# Register your models here.


class RespuestaInline(admin.TabularInline):
    model = Respuesta
    can_delete = False
    max_num = Respuesta.answer_number
    min_num = Respuesta.answer_number
    formset = ElegirInlineFormSet


class PreguntaAdmin(admin.ModelAdmin):
    model = Pregunta
    inlines = (RespuestaInline, )
    list_display = ['text']
    search_fields = ['text', 'preguntas__text']


class ContactoAdmin(admin.ModelAdmin):
    readonly_fields = ('created', 'updated')

admin.site.register(Contacto, ContactoAdmin)


class PreguntasRespondidasAdmin(admin.ModelAdmin):
    list_display = ['question', 'answer', 'correct']

    class Meta:
        model = PreguntasRespondidas



admin.site.register(Pregunta, PreguntaAdmin)
admin.site.register(Respuesta)
admin.site.register(PreguntasRespondidas)
admin.site.register(QuizUsuario)