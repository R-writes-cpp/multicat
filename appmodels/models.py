from django.db import models
from datetime import date

# user
class User(models.Model):
    def profile_picture_path(user, filename):
        return "users/{}.jpg".format(user.username)

    username = models.CharField(max_length=20)
    location = models.CharField(max_length=20)
    join_date = models.DateField(default=date.today)
    profile_picture = models.ImageField(upload_to=profile_picture_path, default="placeholder.jpg")

    def __str__(self):
        return self.username

# release and creator database
class Creator(models.Model):
    name = models.CharField()

    def __str__(self):
        return self.name

class Release(models.Model):
    def release_art_path(release, filename):
        return "releases/{}.jpg".format(self.__str__())

    class Medium(models.IntegerChoices):
        ALBUM = 0
        BOOK = 1
        FILM = 2

    medium = models.IntegerField(choices=Medium)

    title = models.CharField()
    release_date = models.DateField(default=date.today)
    creator_primary = models.ForeignKey(Creator, on_delete=models.CASCADE, related_name="creator1")
    creator_secondary = models.ForeignKey(Creator, on_delete=models.CASCADE, related_name="creator2")
    length = models.IntegerField(default=0)
    language = models.CharField(default="English")

    art = models.ImageField(upload_to=release_art_path, default="placeholder.jpg")

    def __str__(self):
        return "{} - {}".format(self.creator_primary.name, self.title)

# ratings
class Rating(models.Model):
    release = models.ForeignKey(Release, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    score = models.IntegerField(default=0)
    date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return "{}: {}".format(self.user, self.release)

class DescriptorVote(models.Model):
    class Descriptor(models.IntegerChoices):
        HAPPY = 0
        SAD = 1
        BITTERSWEET = 2

        MELLOW = 3
        ENERGETIC = 4

        LIGHTHEARTED = 5
        HUMOROUS = 6
        SERIOUS = 7

        SURREAL = 8
        SOBER = 9

        WARM = 10
        COLD = 11

        LUSH = 12
        HARSH = 13

        BRIGHT = 14
        DARK = 15

        SOOTHING = 16
        ANXIOUS = 17

    release = models.ForeignKey(Release, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    descriptor = models.IntegerField(choices=Descriptor)
    score = models.IntegerField(default=0)

# connections
class Connection(models.Model):
    follower = models.ForeignKey(User, on_delete=models.CASCADE, related_name="follower")
    followee = models.ForeignKey(User, on_delete=models.CASCADE, related_name="followee")

    def __str__(self):
        return "{} following {}".format(follower, followee)

"""
class Artist(models.Model):
    artist_name = models.CharField()

class Album(models.Model):
    title = models.CharField()
    release_date = models.DateField()
    artist = models.ForeignKey(Artist, on_delete=models.CASCADE)
    producer = models.CharField()
    duration = models.DurationField()
    language = models.CharField()

class AlbumRating(models.Model):
    album = models.ForeignKey(Album, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    rating = models.IntegerField()



# film
class Director(models.Model):
    name = models.CharField()

class Film(models.Model):
    title = models.CharField()
    release_date = models.DateField()
    director = models.ForeignKey(Director, on_delete=models.CASCADE)
    producer = models.CharField()
    duration = models.DurationField()
    language = models.CharField()

# books
class Author(models.Model):
    name = models.CharField()

class Book(models.Model):
    title = models.CharField()
    release_date = models.DateField()
    author = models.ForeignKey(Director, on_delete=models.CASCADE)
    publisher = models.CharField()
    page_count = models.IntegerField()
    language = models.CharField()
"""
