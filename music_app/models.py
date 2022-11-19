from django.db import models


class Artist(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField('',max_length=100, null=False)
    age = models.IntegerField('',null=True)
    nationality = models.CharField('',max_length=200)
    website = models.CharField('',max_length=100)
    label = models.CharField('',max_length=200)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Artist'
        verbose_name_plural = 'Artists'


class Song(models.Model):
    id = models.AutoField(primary_key=True)
    genre = models.CharField(max_length=60)
    title = models.CharField(max_length=100)
    release_year = models.IntegerField(null=True)
    album = models.CharField(max_length=80, null=True)
    artist = models.ForeignKey(Artist, on_delete=models.CASCADE)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Song"
        verbose_name_plural = "Songs"

    @property
    def artistName(self):
        return self.artist.name

    @property
    def artistId(self):
        return self.artist.id
