from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase, Client
from django.urls import reverse
from music_app.models import Artist, Song

# 1x1 transparent GIF
TINY_GIF = (
    b"\x47\x49\x46\x38\x39\x61\x01\x00\x01\x00\x00\x00\x00\x21\xf9\x04"
    b"\x01\x0a\x00\x01\x00\x2c\x00\x00\x00\x00\x01\x00\x01\x00\x00\x02"
    b"\x02\x4c\x01\x00\x3b"
)


class LandingPageViewTest(TestCase):

    def test_get_returns_200(self):
        response = self.client.get(reverse("home"))
        self.assertEqual(response.status_code, 200)

    def test_uses_correct_template(self):
        response = self.client.get(reverse("home"))
        self.assertTemplateUsed(response, "home.html")


class ArtistListViewTest(TestCase):

    def setUp(self):
        self.artist = Artist.objects.create(
            name="Listed Artist",
            age=30,
            nationality="American",
            website="",
            label="",
        )

    def test_get_returns_200(self):
        response = self.client.get(reverse("artists"))
        self.assertEqual(response.status_code, 200)

    def test_uses_correct_template(self):
        response = self.client.get(reverse("artists"))
        self.assertTemplateUsed(response, "list_artists.html")

    def test_context_contains_artists(self):
        response = self.client.get(reverse("artists"))
        self.assertIn("artists", response.context)
        self.assertEqual(list(response.context["artists"]), [self.artist])


class ArtistCreateViewTest(TestCase):

    def test_get_returns_200(self):
        response = self.client.get(reverse("add_artist"))
        self.assertEqual(response.status_code, 200)

    def test_uses_correct_template(self):
        response = self.client.get(reverse("add_artist"))
        self.assertTemplateUsed(response, "add_artist.html")

    def test_post_valid_data_creates_artist(self):
        data = {
            "name": "New Artist",
            "age": 25,
            "nationality": "British",
            "website": "https://new.com",
            "label": "New Label",
            "image": SimpleUploadedFile("test.gif", TINY_GIF, content_type="image/gif"),
        }
        response = self.client.post(reverse("add_artist"), data)
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Artist.objects.filter(name="New Artist").exists())

    def test_post_valid_data_redirects_to_artists(self):
        data = {
            "name": "Redirect Artist",
            "age": 25,
            "nationality": "British",
            "website": "https://redirect.com",
            "label": "Redirect Label",
            "image": SimpleUploadedFile("test.gif", TINY_GIF, content_type="image/gif"),
        }
        response = self.client.post(reverse("add_artist"), data)
        self.assertRedirects(response, reverse("artists"))

    def test_post_invalid_data_returns_200(self):
        data = {"name": ""}
        response = self.client.post(reverse("add_artist"), data)
        self.assertEqual(response.status_code, 200)

    def test_post_invalid_data_does_not_create(self):
        count_before = Artist.objects.count()
        self.client.post(reverse("add_artist"), {"name": ""})
        self.assertEqual(Artist.objects.count(), count_before)


class ArtistUpdateViewTest(TestCase):

    def setUp(self):
        self.artist = Artist.objects.create(
            name="Edit Artist",
            age=40,
            nationality="French",
            website="https://edit.com",
            label="Edit Label",
        )
        self.song = Song.objects.create(
            genre="Jazz",
            title="Artist Song",
            release_year=2020,
            album="Album",
            artist=self.artist,
        )

    def test_get_returns_200(self):
        response = self.client.get(
            reverse("artist_details", kwargs={"pk": self.artist.pk})
        )
        self.assertEqual(response.status_code, 200)

    def test_uses_correct_template(self):
        response = self.client.get(
            reverse("artist_details", kwargs={"pk": self.artist.pk})
        )
        self.assertTemplateUsed(response, "edit_artist.html")

    def test_context_contains_songs(self):
        response = self.client.get(
            reverse("artist_details", kwargs={"pk": self.artist.pk})
        )
        self.assertIn("songs", response.context)
        self.assertEqual(list(response.context["songs"]), [self.song])

    def test_post_valid_data_updates_artist(self):
        data = {
            "name": "Updated Artist",
            "age": 41,
            "nationality": "French",
            "website": "https://updated.com",
            "label": "Updated Label",
            "image": SimpleUploadedFile("test.gif", TINY_GIF, content_type="image/gif"),
        }
        self.client.post(
            reverse("artist_details", kwargs={"pk": self.artist.pk}), data
        )
        self.artist.refresh_from_db()
        self.assertEqual(self.artist.name, "Updated Artist")
        self.assertEqual(self.artist.age, 41)

    def test_post_valid_data_redirects(self):
        data = {
            "name": "Updated",
            "age": 41,
            "nationality": "French",
            "website": "https://updated.com",
            "label": "Updated Label",
            "image": SimpleUploadedFile("test.gif", TINY_GIF, content_type="image/gif"),
        }
        response = self.client.post(
            reverse("artist_details", kwargs={"pk": self.artist.pk}), data
        )
        self.assertRedirects(response, reverse("artists"))

    def test_post_invalid_data_returns_200(self):
        data = {"name": ""}
        response = self.client.post(
            reverse("artist_details", kwargs={"pk": self.artist.pk}), data
        )
        self.assertEqual(response.status_code, 200)

    def test_get_nonexistent_returns_404(self):
        response = self.client.get(
            reverse("artist_details", kwargs={"pk": 99999})
        )
        self.assertEqual(response.status_code, 404)


class DeleteArtistViewTest(TestCase):

    def setUp(self):
        self.artist = Artist.objects.create(
            name="Delete Me",
            age=35,
            nationality="German",
            website="",
            label="",
        )

    def test_delete_removes_artist(self):
        pk = self.artist.pk
        self.client.get(reverse("delete_artist", kwargs={"pk": pk}))
        self.assertFalse(Artist.objects.filter(pk=pk).exists())

    def test_delete_redirects_to_artists(self):
        response = self.client.get(
            reverse("delete_artist", kwargs={"pk": self.artist.pk})
        )
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, "/artists/")

    def test_delete_nonexistent_returns_404(self):
        response = self.client.get(
            reverse("delete_artist", kwargs={"pk": 99999})
        )
        self.assertEqual(response.status_code, 404)

    def test_cascade_deletes_songs(self):
        Song.objects.create(
            genre="Rock",
            title="Cascade Song",
            artist=self.artist,
        )
        self.client.get(
            reverse("delete_artist", kwargs={"pk": self.artist.pk})
        )
        self.assertEqual(Song.objects.filter(artist_id=self.artist.pk).count(), 0)


class SongListViewTest(TestCase):

    def setUp(self):
        self.artist = Artist.objects.create(
            name="Song List Artist",
            nationality="",
            website="",
            label="",
        )
        self.song = Song.objects.create(
            genre="Pop",
            title="Listed Song",
            artist=self.artist,
        )

    def test_get_returns_200(self):
        response = self.client.get(reverse("songs"))
        self.assertEqual(response.status_code, 200)

    def test_uses_correct_template(self):
        response = self.client.get(reverse("songs"))
        self.assertTemplateUsed(response, "list_songs.html")

    def test_context_contains_songs(self):
        response = self.client.get(reverse("songs"))
        self.assertIn("songs", response.context)
        self.assertEqual(list(response.context["songs"]), [self.song])


class SongCreateViewTest(TestCase):

    def setUp(self):
        self.artist = Artist.objects.create(
            name="Song Create Artist",
            nationality="",
            website="",
            label="",
        )

    def test_get_returns_200(self):
        response = self.client.get(reverse("add_song"))
        self.assertEqual(response.status_code, 200)

    def test_uses_correct_template(self):
        response = self.client.get(reverse("add_song"))
        self.assertTemplateUsed(response, "add_song.html")

    def test_post_valid_data_creates_song(self):
        data = {
            "genre": "Pop",
            "title": "New Song",
            "release_year": 2024,
            "album": "New Album",
            "artist": self.artist.id,
        }
        response = self.client.post(reverse("add_song"), data)
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Song.objects.filter(title="New Song").exists())

    def test_post_valid_data_redirects_to_songs(self):
        data = {
            "genre": "Jazz",
            "title": "Redirect Song",
            "release_year": 2024,
            "album": "Redirect Album",
            "artist": self.artist.id,
        }
        response = self.client.post(reverse("add_song"), data)
        self.assertRedirects(response, reverse("songs"))

    def test_post_invalid_data_returns_200(self):
        data = {"title": "", "genre": ""}
        response = self.client.post(reverse("add_song"), data)
        self.assertEqual(response.status_code, 200)

    def test_post_invalid_data_does_not_create(self):
        count_before = Song.objects.count()
        self.client.post(reverse("add_song"), {"title": ""})
        self.assertEqual(Song.objects.count(), count_before)


class SongUpdateViewTest(TestCase):

    def setUp(self):
        self.artist = Artist.objects.create(
            name="Song Update Artist",
            nationality="",
            website="",
            label="",
        )
        self.song = Song.objects.create(
            genre="Rock",
            title="Edit Song",
            release_year=2022,
            album="Edit Album",
            artist=self.artist,
        )

    def test_get_returns_200(self):
        response = self.client.get(
            reverse("song_details", kwargs={"pk": self.song.pk})
        )
        self.assertEqual(response.status_code, 200)

    def test_uses_correct_template(self):
        response = self.client.get(
            reverse("song_details", kwargs={"pk": self.song.pk})
        )
        self.assertTemplateUsed(response, "edit_song.html")

    def test_post_valid_data_updates_song(self):
        data = {
            "genre": "Jazz",
            "title": "Updated Song",
            "release_year": 2025,
            "album": "Updated Album",
            "artist": self.artist.id,
        }
        self.client.post(
            reverse("song_details", kwargs={"pk": self.song.pk}), data
        )
        self.song.refresh_from_db()
        self.assertEqual(self.song.title, "Updated Song")
        self.assertEqual(self.song.genre, "Jazz")

    def test_post_valid_data_redirects(self):
        data = {
            "genre": "Pop",
            "title": "Redirected Song",
            "release_year": 2025,
            "album": "Redirected Album",
            "artist": self.artist.id,
        }
        response = self.client.post(
            reverse("song_details", kwargs={"pk": self.song.pk}), data
        )
        self.assertRedirects(response, reverse("songs"))

    def test_post_invalid_data_returns_200(self):
        data = {"title": "", "genre": ""}
        response = self.client.post(
            reverse("song_details", kwargs={"pk": self.song.pk}), data
        )
        self.assertEqual(response.status_code, 200)

    def test_get_nonexistent_returns_404(self):
        response = self.client.get(
            reverse("song_details", kwargs={"pk": 99999})
        )
        self.assertEqual(response.status_code, 404)


class DeleteSongViewTest(TestCase):

    def setUp(self):
        self.artist = Artist.objects.create(
            name="Delete Song Artist",
            nationality="",
            website="",
            label="",
        )
        self.song = Song.objects.create(
            genre="Hip Hop",
            title="Delete Me Song",
            artist=self.artist,
        )

    def test_delete_removes_song(self):
        pk = self.song.pk
        self.client.get(reverse("delete_song", kwargs={"pk": pk}))
        self.assertFalse(Song.objects.filter(pk=pk).exists())

    def test_delete_redirects_to_songs(self):
        response = self.client.get(
            reverse("delete_song", kwargs={"pk": self.song.pk})
        )
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, "/songs/")

    def test_delete_nonexistent_returns_404(self):
        response = self.client.get(
            reverse("delete_song", kwargs={"pk": 99999})
        )
        self.assertEqual(response.status_code, 404)

    def test_delete_song_does_not_delete_artist(self):
        artist_pk = self.artist.pk
        self.client.get(
            reverse("delete_song", kwargs={"pk": self.song.pk})
        )
        self.assertTrue(Artist.objects.filter(pk=artist_pk).exists())
