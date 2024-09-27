## DIY Hitster

Because Hitster will never release a set dedicated to 1990s gabber music.

### A toolkit to produce custom Hitster cards.

This collection of scripts is intended to complement[1] the Hitster game with more (and better) music cards. The idea is pretty simple. This toolkit helps you go from _I've got a better list of songs_ to _I've got a better list of Hitster Music Cards_.

### Why would you want to create your own cards?

Either you've played the game enough times to start to recognize that the 300 included songs simply isn't enough to challenge you. Or, you're upset that super mega hits such as 'Enjoy the Silence' by Depeche Mode and 'Thriller' by Michael Jackson[2] have been excluded somehow in the process of making the game.

One of the reasons I made this toolkit was because my family wanted to be able to play a _Eurovision Song Contest version_ of Hitster. You can find that PDF ready for printing in the `decks/ESC` folder. You probably have another idea on what would make for the most fun Hitster game ever.

### How do I do it?

You start by making your own curated list of the songs that you want include and save them in a `.csv` file.

The QR-codes don't work with the Hitster app, so don't try. Just use your phone's camera and you'll be fine. You still need a Spotify app and account to play.

### The tools

There is one main script: `gen.py`. It takes a `.csv` file and produces a `.pdf` ready for printing (print two-sided; portrait orientation; make sure it folds on long side).

### Usage instructions

#### `gen.py`

Run `python gen.py <filename>` and make sure to feed it a CSV-file with Year, Artist, Song title and Spotify-URL. Out comes a PDF-file meant for printing (2-sided portrait, fold on long side) and you can get your custom Hitster-game focused on dad rock, 1980s synthwave or just Taylor Swift. Whatever you want. The first row should only contain the title of the collection of songs. It will be printed on the front of each card. Use `%` to add a newline and a `;` to separate values.

Here's a short example:

```
The best%songs ever!;;;
2018;Shallow;Lady Gaga, Bradley Cooper;https://open.spotify.com/track/2VxeLyX666F8uXCJ0dZF8B?si=
2014;Pain;Boy Harsher;https://open.spotify.com/track/13HYthybjhM3iyWcfl8VcN?si=
```

---

[1] When I say complement I mean that you can switch out the whole set of music cards. Your own 'cut-out from printed paper' version won't mix well with the laminated ones you get with the game box.

[2] You can of course switch these two bangers with whatever songs YOU feel are missing