from django.contrib.auth.models import User
from django.db import models
from django.conf import settings


# Create your models here.

# Default oolours for categoria.
defaultColourList = (
    ("FFFFFF", "White"),  # rgb(255, 255, 255)
    ("C0C0C0", "Silver"),  # rgb(192, 192, 192)
    ("808080", "Gray"),  # rgb(128, 128, 128)
    ("000000", "Black"),  # rgb(0, 0, 0)
    ("FF0000", "Red"),  # rgb(255, 0, 0)
    ("800000", "Maroon"),  # rgb(128, 0, 0)
    ("FFFF00", "Yellow"),  # rgb(255, 255, 0)
    ("808000", "Olive"),  # rgb(128, 128, 0)
    ("00FF00", "Lime"),  # rgb(0, 255, 0)
    ("008000", "Green"),  # rgb(0, 128, 0)
    ("00FFFF", "Aqua"),  # rgb(0, 255, 255)
    ("008080", "Teal"),  # rgb(0, 128, 128)
    ("0000FF", "Blue"),  # rgb(0, 0, 255)
    ("000080", "Navy"),  # rgb(0, 0, 128)
    ("FF00FF", "Fuchsia"),  # rgb(255, 0, 255)
    ("800080", "Purple"),  # rgb(128, 0, 128)
)
defaultColour = 5

class Categoria(models.Model):
    """
    categoria en la cual se puede encontrar una meta
    """

    name = models.CharField(null=False, max_length=15)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    colour = models.CharField(max_length=10, choices=defaultColourList, default=defaultColourList[defaultColour])

    def __str__(self):
        return self.name

class Goal(models.Model):
    """
    Meta Principal
    """

    name = models.CharField(null=False, max_length=100, blank=True)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, default=1)
    creationdate = models.DateTimeField(null=False)
    finishdate = models.DateTimeField(null=False, help_text="<em>yyyy-mm-dd hh:mm</em>.", blank=True)
    state = models.CharField(null=False, max_length=10, blank=True)
    category = models.ForeignKey(Categoria, on_delete=models.CASCADE,null=True)
    #date = models.DateField(null=True, help_text="<em>yyyy-mm-dd</em>.")
    #time = models.TimeField(null=True, help_text="<em>hh:mm</em>.")

    def __str__(self):
        return self.name


class Subgoal(models.Model):
    """
    Sub Metas
    """
    name = models.CharField(max_length=25)
    maingoal = models.ForeignKey(Goal, on_delete=models.CASCADE)
    state = models.BooleanField(default=False)

    def __str__(self):
        return self.name




    # def __init__(self):
    #     super(Categoria, self).__init__(name, user, colour)
    #     self._name = name
    #     self._owner = user
    #     self._colour = colour
    #
    # def __str__(self):  # __unicode__ on Python 2
    #     return self._name
    #
    # @property
    # def colour(self):
    #     """
    #     Return the hexadecimal colour of this object
    #     """
    #     return self._colour[1]
    #
    # @colour.setter
    # def colour(self, value):
    #     """
    #     set the tuple colour for this object
    #     :return
    #     """
    #     if value in defaultColourList:
    #         self._colour = value
    #     else:
    #         # TODO raise an error if colour is not permited
    #         pass
    # @property
    # def colourName(self):
    #     """
    #     Return the name colour of this object
    #     """
    #     return self._colour[0]
    #
    # @property
    # def name(self):
    #     """
    #     Return the name of this object
    #     """
    #     return self._name
    #
    # # default categories
    #     # TODO definir y crear los modelos de categorias predeterminados.
