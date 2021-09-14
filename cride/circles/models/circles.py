"""Circle model"""

# Django
from django.db import models
# Utilities
from cride.utils.models import CRideModel

class Circle(CRideModel):

    name = models.CharField('circle name', max_length=150)
    slug_name = models.SlugField(max_length=40,unique=True)

    about = models.CharField('circle description', max_length=255)
    picture = models.ImageField(upload_to='circles/pictures', blank=True)

    #Stats
    rides_taken = models.PositiveIntegerField(default=0)
    rides_offered = models.PositiveIntegerField(default=0)


    verified = models.BooleanField(
        'verified circle',
        default=True,
        help_text='Verified cricles are also known as official communities'
    )

    is_public = models.BooleanField(
        default=True,
        help_text='Public circles are listed in the main page so everyone know about their existence.'
    )

    is_limited = models.BooleanField(
        default=False,
        help_text='Limited circles can grow up to a fixed number of members.'
    )

    members_limit = models.PositiveIntegerField(
        default=0,
        help_text='If circle is limited, this wil be the limit of the number of members'
    )

    def __str__(self):
        return self.name

    class Meta(CRideModel.Meta):

        ordering = ['-rides_taken','-rides_offered']
