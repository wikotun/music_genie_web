from django.test import TestCase
from music_app.models import Artist, Song


class ArtistModelTest(TestCase):

    def setUp(self):
        self.artist = Artist.objects.create(
            name="Test Artist",
            age=30,
            nationality="American",
            website="https://example.com",
            label="Test Label",
        )

    def test_create_artist_with_all_fields(self):
        self.assertEqual(self.artist.name, "Test Artist")
        self.assertEqual(self.artist.age, 30)
        self.assertEqual(self.artist.nationality, "American")
        self.assertEqual(self.artist.website, "https://example.com")
        self.assertEqual(self.artist.label, "Test Label")

    def test_create_artist_with_null_age(self):
        artist = Artist.objects.create(
            name="No Age",
            nationality="British",
            website="",
            label="",
        )
        self.assertIsNone(artist.age)

    def test_str_returns_name(self):
        self.assertEqual(str(self.artist), "Test Artist")

    def test_name_max_length(self):
        field = Artist._meta.get_field("name")
        self.assertEqual(field.max_length, 100)

    def test_nationality_max_length(self):
        field = Artist._meta.get_field("nationality")
        self.assertEqual(field.max_length, 200)

    def test_website_max_length(self):
        field = Artist._meta.get_field("website")
        self.assertEqual(field.max_length, 100)

    def test_label_max_length(self):
        field = Artist._meta.get_field("label")
        self.assertEqual(field.max_length, 200)

    def test_verbose_name(self):
        self.assertEqual(Artist._meta.verbose_name, "Artist")

    def test_verbose_name_plural(self):
        self.assertEqual(Artist._meta.verbose_name_plural, "Artists")

    def test_image_field_upload_to(self):
        field = Artist._meta.get_field("image")
        self.assertEqual(field.upload_to, "images/")

    def test_image_field_nullable(self):
        field = Artist._meta.get_field("image")
        self.assertTrue(field.null)


class SongModelTest(TestCase):

    def setUp(self):
        self.artist = Artist.objects.create(
            name="Song Artist",
            age=25,
            nationality="Nigerian",
            website="https://songartist.com",
            label="Music Label",
        )
        self.song = Song.objects.create(
            genre="Pop",
            title="Test Song",
            release_year=2023,
            album="Test Album",
            artist=self.artist,
        )

    def test_create_song_with_all_fields(self):
        self.assertEqual(self.song.genre, "Pop")
        self.assertEqual(self.song.title, "Test Song")
        self.assertEqual(self.song.release_year, 2023)
        self.assertEqual(self.song.album, "Test Album")
        self.assertEqual(self.song.artist, self.artist)

    def test_create_song_with_null_optional_fields(self):
        song = Song.objects.create(
            genre="Jazz",
            title="Minimal Song",
            artist=self.artist,
        )
        self.assertIsNone(song.release_year)
        self.assertIsNone(song.album)

    def test_str_returns_title(self):
        self.assertEqual(str(self.song), "Test Song")

    def test_genre_max_length(self):
        field = Song._meta.get_field("genre")
        self.assertEqual(field.max_length, 60)

    def test_title_max_length(self):
        field = Song._meta.get_field("title")
        self.assertEqual(field.max_length, 100)

    def test_album_max_length(self):
        field = Song._meta.get_field("album")
        self.assertEqual(field.max_length, 80)

    def test_verbose_name(self):
        self.assertEqual(Song._meta.verbose_name, "Song")

    def test_verbose_name_plural(self):
        self.assertEqual(Song._meta.verbose_name_plural, "Songs")

    def test_foreign_key_cascade_delete(self):
        artist_id = self.artist.id
        song_id = self.song.id
        self.artist.delete()
        self.assertFalse(Song.objects.filter(id=song_id).exists())
        self.assertFalse(Artist.objects.filter(id=artist_id).exists())

    def test_artist_name_property(self):
        self.assertEqual(self.song.artistName, "Song Artist")

    def test_artist_id_property(self):
        self.assertEqual(self.song.artistId, self.artist.id)

    def test_genre_choices(self):
        field = Song._meta.get_field("genre")
        expected_genres = [
            "Afrobeats", "Pop", "Jazz", "Hip Hop", "Gospel", "R&B",
            "Classical", "Techno", "Rock", "Country", "Indie Rock",
            "Electro", "House", "Instrumental", "Soul", "Garage",
        ]
        actual_genres = [choice[0] for choice in field.choices]
        self.assertEqual(actual_genres, expected_genres)

    def test_genre_choices_count(self):
        field = Song._meta.get_field("genre")
        self.assertEqual(len(field.choices), 16)
