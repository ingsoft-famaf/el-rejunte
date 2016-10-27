from django.contrib.auth.models import User
from django.db import models
from django.conf import settings

# Create your models here.

# Default oolours for categoria.
defaultColourList = (
    ("White", "FFFFFF"),  # rgb(255, 255, 255)
    ("Silver", "C0C0C0"),  # rgb(192, 192, 192)
    ("Gray", "808080"),  # rgb(128, 128, 128)
    ("Black", "000000"),  # rgb(0, 0, 0)
    ("Red", "FF0000"),  # rgb(255, 0, 0)
    ("Maroon", "800000"),  # rgb(128, 0, 0)
    ("Yellow", "FFFF00"),  # rgb(255, 255, 0)
    ("Olive", "808000"),  # rgb(128, 128, 0)
    ("Lime", "00FF00"),  # rgb(0, 255, 0)
    ("Green", "008000"),  # rgb(0, 128, 0)
    ("Aqua", "00FFFF"),  # rgb(0, 255, 255)
    ("Teal", "008080"),  # rgb(0, 128, 128)
    ("Blue", "0000FF"),  # rgb(0, 0, 255)
    ("Navy", "000080"),  # rgb(0, 0, 128)
    ("Fuchsia", "FF00FF"),  # rgb(255, 0, 255)
    ("Purple", "800080"),  # rgb(128, 0, 128)
)
defaultColour = 0


class Goal(models.Model):
    """
    Meta Principal
    """

    id = models.AutoField(primary_key=True)
    name = models.CharField(null=False, max_length=100, blank=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE,null=True)
    creationdate = models.DateTimeField(null=False)
    finishdate = models.DateTimeField(null=False, help_text="<em>yyyy-mm-dd hh:mm</em>.", blank=True)
    state = models.CharField(null=False, max_length=10, blank=True)
    #date = models.DateField(null=True, help_text="<em>yyyy-mm-dd</em>.")
    #time = models.TimeField(null=True, help_text="<em>hh:mm</em>.")




class Subgoal(models.Model):
    """
    Sub Metas
    """
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=25)
    maingoal = models.ForeignKey(Goal, on_delete=models.CASCADE)


class Categoria(models.Model):
    """
    categoria en la cual se puede encontrar una meta
    """

    id = models.AutoField(primary_key=True)
    _name = models.CharField(max_length=15)
    _owner = models.ForeignKey(User, on_delete=models.CASCADE)
    _colour = models.CharField(max_length=10, choices=defaultColourList, default=defaultColourList[defaultColour])

    def __init__(self, name, user, colour=defaultColourList[defaultColour]):
        super(Categoria, self).__init__(name, user, colour)
        self._name = name
        self._owner = user
        self._colour = colour

    def __str__(self):  # __unicode__ on Python 2
        return self._name

    @property
    def colour(self):
        """
        Return the hexadecimal colour of this object
        """
        return self._colour[1]

    @colour.setter
    def colour(self, value):
        """
        set the tuple colour for this object
        :return
        """
        if value in defaultColourList:
            self._colour = value
        else:
            # TODO raise an error if colour is not permited
            pass
    @property
    def colourName(self):
        """
        Return the name colour of this object
        """
        return self._colour[0]

    @property
    def name(self):
        """
        Return the name of this object
        """
        return self._name

    # default categories
        # TODO definir y crear los modelos de categorias predeterminados.
