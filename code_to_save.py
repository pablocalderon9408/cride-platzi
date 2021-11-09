import csv

from cride.circles.models import Circle


def load_circles(filename):
    with open(filename, 'r') as csvfile:
        reader = csv.reader(csvfile)
        rows = list(reader)[1:]
        for row in rows:
            c = Circle.objects.create(
                name=row[0],
                slug_name=row[1],
                is_public=row[2] == '1',
                verified=row[3] == '1',
                is_limited=row[4] != '0',
                members_limit=0 if row[4] == '0' else int(
                                row[4])
            )
            print(c)


load_circles('circles.csv')
