from django.test import TestCase
from django.urls import reverse, resolve
from music_app.views import (
    LandingPageView,
    ArtistListView,
    ArtistCreateView,
    ArtistUpdateView,
    deleteArtist,
    SongListView,
    SongCreateView,
    SongUpdateView,
    deleteSong,
)


class URLResolveTest(TestCase):

    def test_home_resolves(self):
        resolver = resolve("/")
        self.assertEqual(resolver.func.view_class, LandingPageView)

    def test_artists_resolves(self):
        resolver = resolve("/artists/")
        self.assertEqual(resolver.func.view_class, ArtistListView)

    def test_add_artist_resolves(self):
        resolver = resolve("/add_artist/")
        self.assertEqual(resolver.func.view_class, ArtistCreateView)

    def test_artist_details_resolves(self):
        resolver = resolve("/artist-details/1/")
        self.assertEqual(resolver.func.view_class, ArtistUpdateView)

    def test_delete_artist_resolves(self):
        resolver = resolve("/artist-delete/1/")
        self.assertEqual(resolver.func, deleteArtist)

    def test_songs_resolves(self):
        resolver = resolve("/songs/")
        self.assertEqual(resolver.func.view_class, SongListView)

    def test_add_song_resolves(self):
        resolver = resolve("/add_song/")
        self.assertEqual(resolver.func.view_class, SongCreateView)

    def test_song_details_resolves(self):
        resolver = resolve("/song-details/1/")
        self.assertEqual(resolver.func.view_class, SongUpdateView)

    def test_delete_song_resolves(self):
        resolver = resolve("/song-delete/1/")
        self.assertEqual(resolver.func, deleteSong)

    def test_admin_resolves(self):
        resolver = resolve("/admin/")
        self.assertEqual(resolver.app_name, "admin")


class URLReverseTest(TestCase):

    def test_home_reverse(self):
        self.assertEqual(reverse("home"), "/")

    def test_artists_reverse(self):
        self.assertEqual(reverse("artists"), "/artists/")

    def test_add_artist_reverse(self):
        self.assertEqual(reverse("add_artist"), "/add_artist/")

    def test_artist_details_reverse(self):
        self.assertEqual(
            reverse("artist_details", kwargs={"pk": 1}), "/artist-details/1/"
        )

    def test_delete_artist_reverse(self):
        self.assertEqual(
            reverse("delete_artist", kwargs={"pk": 1}), "/artist-delete/1/"
        )

    def test_songs_reverse(self):
        self.assertEqual(reverse("songs"), "/songs/")

    def test_add_song_reverse(self):
        self.assertEqual(reverse("add_song"), "/add_song/")

    def test_song_details_reverse(self):
        self.assertEqual(
            reverse("song_details", kwargs={"pk": 1}), "/song-details/1/"
        )

    def test_delete_song_reverse(self):
        self.assertEqual(
            reverse("delete_song", kwargs={"pk": 1}), "/song-delete/1/"
        )
