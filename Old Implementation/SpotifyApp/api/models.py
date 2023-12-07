from django.db import models


class Token(models.Model):
    user = models.CharField(unique=True, max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)
    access_token = models.CharField(max_length=500)
    refresh_token = models.CharField(max_length=500)
    expires_in = models.DateTimeField()
    token_type = models.CharField(max_length=50)

class Song(models.Model):
    title = models.CharField(max_length=100, default='No song title')
    query = models.CharField(max_length=100, default='No query')
    album = models.CharField(max_length=100, default='No album')
    songId = models.CharField(max_length=100, primary_key=True)
    preview = models.CharField(max_length=400, default='None', blank=True, null=True)
    external = models.CharField(max_length=100, default='No external URL')
    uri = models.CharField(max_length=100, default='No URI')
    duration = models.CharField(max_length=10, default='No duration')
    mainArtist = models.CharField(max_length=100, default='No artist')
    artists = models.CharField(max_length=100, default='No artists')
    popularity = models.FloatField(max_length=101, default=0)
    image = models.CharField(max_length=200, default='None', null=True, blank=True)
    theType = models.CharField(max_length=10, default='No type')
    albumId = models.CharField(max_length=100, default='None')
    artistId = models.CharField(max_length=100, default='None')


class Album(models.Model):
    title = models.CharField(max_length=100, default='No album title')
    query = models.CharField(max_length=100, default='No query')
    image = models.CharField(max_length=500, default='No image')
    albumId = models.CharField(max_length=500, primary_key=True)
    external = models.CharField(max_length=100, default='No external URL')
    uri = models.CharField(max_length=100, default='No URI')
    mainArtist = models.CharField(max_length=600, default='No artist')
    artists = models.CharField(max_length=500, default='No artists')
    releaseDate = models.CharField(max_length=20, default='No release date', null=True, blank=True)
    popularity = models.FloatField(max_length=11, default=0)
    theType = models.CharField(max_length=10, default='No type')
    artistId = models.CharField(max_length=500, default='None')
    year = models.CharField(max_length=10, default='No release year')


class Artist(models.Model):
    genres = models.CharField(max_length=500, default='No genres')
    query = models.CharField(max_length=100, default='No query')
    name = models.CharField(max_length=500, default='No name')
    artistId = models.CharField(max_length=500, primary_key=True)
    external = models.CharField(max_length=500, default='No external URL')
    uri = models.CharField(max_length=500, default='No URI')
    image = models.CharField(max_length=500, default='No image')
    popularity = models.FloatField(max_length=501, default=0)
    numOfFollowers = models.CharField(max_length=500, default="0")
    songId = models.CharField(max_length=100, default="None", null=True, blank=True)
    albumId = models.CharField(max_length=100, default="None", null=True, blank=True)
