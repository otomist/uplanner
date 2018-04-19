import django
django.setup()

from schedule.models import Section

sections = Section.objects.all()

for section in sections:
    days = []
    day_set = section.days
    for i in range(0, len(day_set), 2):
        days.append(day_set[i:i+2])
    if "Mo" in days:
        section.mon = True
    if "Tu" in days:
        section.tue = True
    if "We" in days:
        section.wed = True
    if "Th" in days:
        section.thu = True
    if "Fr" in days:
        section.fri = True
    section.save()