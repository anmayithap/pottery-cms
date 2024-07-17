from django.db.models import TextChoices


class Status(TextChoices):
    NEW = 'NEW', 'Новый'
    IN_PROGRESS = 'IN_PROGRESS', 'В работе'
    READY = 'READY', 'Готово'
    GIVEN = 'GIVEN', 'Отдано'
    OVERDUE = 'OVERDUE', 'Просрочено'
    BROKEN = 'BROKEN', 'Брак'
    REPEAT_VISIT = 'REPEAT_VISIT', 'Повторный визит'
