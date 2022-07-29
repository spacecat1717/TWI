from django.contrib import admin
from .models import Course, Action, Step

class CourseAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("title", )}

class ActionAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("title", )}

class StepAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("title", )}


admin.site.register(Course, CourseAdmin)
admin.site.register(Action, ActionAdmin)
admin.site.register(Step, StepAdmin)

