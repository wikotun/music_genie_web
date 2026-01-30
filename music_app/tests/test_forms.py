from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase
from music_app.forms import ArtistForm, SongForm
from music_app.models import Artist

# 1x1 transparent GIF
TINY_GIF = (
    b"\x47\x49\x46\x38\x39\x61\x01\x00\x01\x00\x00\x00\x00\x21\xf9\x04"
    b"\x01\x0a\x00\x01\x00\x2c\x00\x00\x00\x00\x01\x00\x01\x00\x00\x02"
    b"\x02\x4c\x01\x00\x3b"
)


class ArtistFormTest(TestCase):

    def test_valid_form(self):
        data = {
            "name": "Valid Artist",
            "age": 28,
            "nationality": "Canadian",
            "website": "https://valid.com",
            "label": "Valid Label",
        }
        image = SimpleUploadedFile("test.gif", TINY_GIF, content_type="image/gif")
        form = ArtistForm(data=data, files={"image": image})
        self.assertTrue(form.is_valid())

    def test_missing_name_is_invalid(self):
        data = {
            "name": "",
            "age": 28,
            "nationality": "Canadian",
            "website": "https://valid.com",
            "label": "Valid Label",
        }
        form = ArtistForm(data=data)
        self.assertFalse(form.is_valid())
        self.assertIn("name", form.errors)

    def test_fields_set_to_all(self):
        self.assertEqual(ArtistForm.Meta.fields, "__all__")

    def test_name_widget_has_form_control_class(self):
        form = ArtistForm()
        self.assertIn('class="form-control"', str(form["name"]))

    def test_name_widget_placeholder(self):
        form = ArtistForm()
        self.assertIn('placeholder="Artist Name"', str(form["name"]))

    def test_age_widget_has_form_control_class(self):
        form = ArtistForm()
        self.assertIn('class="form-control"', str(form["age"]))

    def test_age_widget_placeholder(self):
        form = ArtistForm()
        self.assertIn('placeholder="Age"', str(form["age"]))

    def test_nationality_widget_placeholder(self):
        form = ArtistForm()
        self.assertIn('placeholder="Nationality"', str(form["nationality"]))

    def test_website_widget_placeholder(self):
        form = ArtistForm()
        self.assertIn('placeholder="Website"', str(form["website"]))

    def test_label_widget_placeholder(self):
        form = ArtistForm()
        self.assertIn('placeholder="Record Label"', str(form["label"]))

    def test_image_widget_has_img_thumbnail_class(self):
        form = ArtistForm()
        self.assertIn('class="img-thumbnail"', str(form["image"]))

    def test_crispy_helper_exists(self):
        form = ArtistForm()
        self.assertTrue(hasattr(form, "helper"))

    def test_crispy_helper_form_tag_false(self):
        form = ArtistForm()
        self.assertFalse(form.helper.form_tag)

    def test_crispy_helper_layout_fields(self):
        form = ArtistForm()
        layout_fields = [f for f in form.helper.layout.fields if isinstance(f, str)]
        self.assertEqual(layout_fields, ["name", "age", "nationality", "website", "label", "image"])


class SongFormTest(TestCase):

    def setUp(self):
        self.artist = Artist.objects.create(
            name="Form Artist",
            age=30,
            nationality="British",
            website="",
            label="",
        )

    def test_valid_form(self):
        data = {
            "genre": "Pop",
            "title": "Valid Song",
            "release_year": 2023,
            "album": "Valid Album",
            "artist": self.artist.id,
        }
        form = SongForm(data=data)
        self.assertTrue(form.is_valid())

    def test_missing_title_is_invalid(self):
        data = {
            "genre": "Pop",
            "title": "",
            "release_year": 2023,
            "album": "Album",
            "artist": self.artist.id,
        }
        form = SongForm(data=data)
        self.assertFalse(form.is_valid())
        self.assertIn("title", form.errors)

    def test_missing_genre_is_invalid(self):
        data = {
            "genre": "",
            "title": "Song",
            "release_year": 2023,
            "album": "Album",
            "artist": self.artist.id,
        }
        form = SongForm(data=data)
        self.assertFalse(form.is_valid())
        self.assertIn("genre", form.errors)

    def test_missing_artist_is_invalid(self):
        data = {
            "genre": "Pop",
            "title": "Song",
            "release_year": 2023,
            "album": "Album",
        }
        form = SongForm(data=data)
        self.assertFalse(form.is_valid())
        self.assertIn("artist", form.errors)

    def test_invalid_genre_choice(self):
        data = {
            "genre": "NotAGenre",
            "title": "Song",
            "release_year": 2023,
            "album": "Album",
            "artist": self.artist.id,
        }
        form = SongForm(data=data)
        self.assertFalse(form.is_valid())
        self.assertIn("genre", form.errors)

    def test_fields_set_to_all(self):
        self.assertEqual(SongForm.Meta.fields, "__all__")

    def test_crispy_helper_exists(self):
        form = SongForm()
        self.assertTrue(hasattr(form, "helper"))

    def test_valid_genre_choices(self):
        for genre_value, _ in [
            ("Afrobeats", "Afrobeats"),
            ("Pop", "Pop"),
            ("Jazz", "Jazz"),
            ("Hip Hop", "Hip Hop"),
            ("R&B", "R&B"),
        ]:
            data = {
                "genre": genre_value,
                "title": f"Song {genre_value}",
                "release_year": 2023,
                "album": "Test Album",
                "artist": self.artist.id,
            }
            form = SongForm(data=data)
            self.assertTrue(form.is_valid(), f"Genre '{genre_value}' should be valid")
