## DIY Hitster

Because Hitster will never release a set dedicated to 1990s gabber music.

### A toolkit to produce custom Hitster cards.

This collection of scripts is intended to complement[1] the Hitster game with more (and better) music cards. The idea is pretty simple. This toolkit helps you go from _I've got a better list of songs_ to _I've got a better list of Hitster Music Cards_.

### Why would you want to create your own cards?

Either you've played the game enough times to start to recognize that the 300 included songs simply isn't enough to challenge you. Or, you're upset that super mega hits such as 'Enjoy the Silence' by Depeche Mode and 'Thriller' by Michael Jackson[2] have been excluded somehow in the process of making the game.

One of the reasons I made this toolkit was because my family wanted to be able to play a _Eurovision Song Contest version_ of Hitster. You can find that PDF ready for printing in the `decks/ESC` folder. You probably have another idea on what would make for the most fun Hitster game ever.

### How do I do it?

You start by making your own curated list of the songs that you want include and save them in a `.csv` file. Use `;` to separate values.

You can use the `add_year_and_spotify_url.py` script to convert a `.csv` file containing `title` and `artist` to a file containing `year`, `title`, `artist` and `spotify-url`. Note! At the moment the script rewrites the contents of the file. Also, Spotify don't always give you the correct year of release of the track so make sure to double check your results before converting to `.pdf`.

Once you have a `.csv` file with `year`, `title`, `artist` and `spotify-url` you need to add a `title` in the first field in the first row. The rest of the fields on that row will be ignored. Just leave them empty. The title will be printed on the front of each card.

Run `python gen.py <filename>` and make sure to feed it your `.csv` file. Out comes a `.pdf` file meant for printing (2-sided portrait, fold on long side) and you can get your custom Hitster-game focused on dad rock, 1980s synthwave or just Taylor Swift. Whatever you want. 

If there are any cards where the text doesn't fit and is clipped it will warn you about that. Use `%` to add a newline where appropriate.

#### Here's a short example:

```
Shallow;Lady Gaga, Bradley Cooper
Pain;Boy Harsher
```

Running `python add_year_and_spotify_url.py <filename> <market>` will turn the above into (I used SE market here):

```
2018;Shallow;Lady Gaga, Bradley Cooper;https://open.spotify.com/track/2VxeLyX666F8uXCJ0dZF8B?si=
2014;Pain;Boy Harsher;https://open.spotify.com/track/13HYthybjhM3iyWcfl8VcN?si=
```

Manually adding a title on the first row. Note the use of `%` to turn a value into two lines of text.

```
The best%songs ever!;;;
2018;Shallow;Lady Gaga,%Bradley Cooper;https://open.spotify.com/track/2VxeLyX666F8uXCJ0dZF8B?si=
2014;Pain;Boy Harsher;https://open.spotify.com/track/13HYthybjhM3iyWcfl8VcN?si=
```

Running `python gen.py <filename>` will produce a `.pdf` with two cards.

The QR-codes don't work with the Hitster app, so don't try. Just use your phone's camera and you'll be fine. You still need a Spotify app and account to play.

### A quick note on credentials

In order to run the script that use Spotify's APIs you need to have a developer account and an app. Go to [Spotify for developers](https://developer.spotify.com/) to fix that. Once you've created an account and an app you make a copy of the `credentials/template_spotify.py` and save it as `credentials/spotify.py`. Then you copy-paste your Spotify app's client id and client secret into that file. You can find both values under Settings and Basic Information in the Spotify portal.

---

[1] When I say complement I mean that you can switch out the whole set of music cards. Your own 'cut-out from printed paper' version won't mix well with the laminated ones you get with the game box.

[2] You can of course switch these two bangers with whatever songs YOU feel are missing