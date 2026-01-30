# Music Genie Web

A Django web application for managing a catalogue of music artists and their songs.

## Features

- Browse, add, edit, and delete artists
- Browse, add, edit, and delete songs
- Artist profile images with upload support
- Songs linked to artists with genre classification (16 genres including Afrobeats, Pop, Jazz, Hip Hop, and more)
- Cascading delete — removing an artist removes all their songs
- Bootstrap 5 UI with crispy forms

## Tech Stack

- **Framework:** Django 4.1
- **Database:** SQLite
- **Frontend:** Bootstrap 5 via django-crispy-forms
- **Static files:** WhiteNoise
- **Image handling:** Pillow
- **Production server:** Gunicorn

## Project Structure

```
music_genie_web/
├── manage.py
├── requirements.txt
├── db.sqlite3
├── music_genie/          # Project settings & root URL config
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── music_app/            # Main application
│   ├── models.py         # Artist & Song models
│   ├── views.py          # List, Create, Update, Delete views
│   ├── forms.py          # ArtistForm & SongForm with crispy helpers
│   └── tests/            # Unit tests (106 tests)
│       ├── test_models.py
│       ├── test_forms.py
│       ├── test_views.py
│       └── test_urls.py
├── templates/            # HTML templates
│   ├── _base.html
│   ├── home.html
│   ├── list_artists.html
│   ├── add_artist.html
│   ├── edit_artist.html
│   ├── list_songs.html
│   ├── add_song.html
│   └── edit_song.html
├── static/               # Source static files
├── staticfiles/          # Collected static files (collectstatic output)
└── images/               # Uploaded media (artist images)
```

## Setup

1. **Clone the repository:**
   ```bash
   git clone <repository-url>
   cd music_genie_web
   ```

2. **Create and activate a virtual environment:**
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run migrations:**
   ```bash
   python manage.py migrate
   ```

5. **Start the development server:**
   ```bash
   python manage.py runserver
   ```

   The app will be available at `http://127.0.0.1:8000/`.

## Environment Variables

| Variable             | Description                          | Default                    |
|----------------------|--------------------------------------|----------------------------|
| `DJANGO_SECRET_KEY`  | Django secret key                    | Auto-generated random key  |
| `DEBUG`              | Enable debug mode (`True`/`False`)   | `False`                    |

## Running Tests

```bash
python manage.py test music_app.tests
```

This runs 106 unit tests covering models, forms, views, and URL routing.

## URL Routes

| Path                        | Name              | Description          |
|-----------------------------|-------------------|----------------------|
| `/`                         | `home`            | Landing page         |
| `/artists/`                 | `artists`         | List all artists     |
| `/add_artist/`              | `add_artist`      | Add a new artist     |
| `/artist-details/<id>/`     | `artist_details`  | Edit an artist       |
| `/artist-delete/<id>/`      | `delete_artist`   | Delete an artist     |
| `/songs/`                   | `songs`           | List all songs       |
| `/add_song/`                | `add_song`        | Add a new song       |
| `/song-details/<id>/`       | `song_details`    | Edit a song          |
| `/song-delete/<id>/`        | `delete_song`     | Delete a song        |
