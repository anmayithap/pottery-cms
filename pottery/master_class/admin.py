from django.contrib import admin

from pottery.master_class.models import Photo, Program, Visit, WorkPiece


@admin.register(Program)
class ProgramAdmin(admin.ModelAdmin):
    pass


@admin.register(Visit)
class VisitAdmin(admin.ModelAdmin):
    pass


@admin.register(WorkPiece)
class WorkPieceAdmin(admin.ModelAdmin):
    pass


@admin.register(Photo)
class PhotoAdmin(admin.ModelAdmin):
    pass
