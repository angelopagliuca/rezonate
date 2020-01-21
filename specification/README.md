
# REZONATE

## Project Description

### Music Platform

Our webapp integrates popular features from music applications such as Spotify, Genius, Shazam, etc.  The core features of our application includes but not limits to:

* User’s ability to annotate lyrics;
* Looking up songs by inputting part of lyrics;
* Recommending similar genre of music;
* Ability to rank Popular songs;
* Visualizer when music is playing (real time lyrics or waveforms)
* Create playlist

Our app provides a platform for music lovers to find the music they fell in love at the bar but don’t know what the name of the song is, or for die hard Beatles’ fans to comment on the history of Beatles’ albums. Right now, the applications on the market only do one or few of the features we mentioned, our application will combine all the good things so that users don’t have to, for example, listen to music on Spotify and looking up lyrics somewhere else.

The technologies we will be using are:
- Django
- Javascript, JQuery, AJAX
- AWS ?? AZURE ??
- Some kind of Machine Learning algorithm that analyzes users’ music preferences
- Music APIs: AudD, Spotify
- CSS libraries
- Javascript Libraries

## FUNCTIONALITIES

Our music platform, called Rezonate will be an app similar in functionality to Spotify--but with even more features. There will be a main page with our app name and logo where the user will have the option to log in. If a user is not logged in, they can play up to ten songs until they will be prompted to log in. There will also be a manager user that is allowed to add songs into the database.

In the Nav bar, there will be a Songs button. When the user clicks this button, a search bar will appear. Here the user can search by a substring of a song name, substring of an artist’s name, genre of music, a substring of album name, etc. After clicking a button, the results will show. Here the user can click a song and the song profile will appear showing the song name, artist name, album name, and song image. If the song is playing, a waveform of the song name will appear around the image, in tune with the song, and if a button on the right-hand side is clicked, the song lyrics will pop out from the right-hand side of the screen. The song profile page will have buttons that allow the user to add the song to the queue, skip to the next song, go to the previous song, add to a new or current playlist.

On the left-hand side, there will be a sidebar. Here there will be a search bar where the user can filter a search on a substring of a song name, substring of an artist’s name, genre of music, a substring of album name, or a playlist name.

In the Nav bar, there will be a Playlist button. When the user clicks this button, a search bar will appear. Here the user can search by a substring of a playlist name, substring of a playlist owner’s name, a substring of album name, etc. After clicking a button, the results will show. Here the user can click a playlist and the songs will begin to play and the song profile of the song currently playing will appear showing the song name, artist name, album name, and song image. The side-bar on the left hand song will show the playlist name and the songs in order on the queue. On the bottom of the page, the user can shuffle the playlist, turn shuffle off, skip to the next song, or go to the previous song.

Most of our views/templates will be created by Angelo. Aria and Mary will be working primarily on the backend and testing the code. Mary will be in charge of authentication and authorization for users and managers in addition to template inheritance. Aria will be in charge of deployment. Angelo will be in charge of adding JQuery and AJAX.

## DJANGO MODELS

sprint-backlogs/sprint-1/models.py

## WIREFRAME

sprint-backlogs/sprint-1/wireframe.pdf

## SPRINT 1 BACKLOG

sprint-backlogs/sprint-1/backlog.pdf
