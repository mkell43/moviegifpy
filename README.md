# MovieGifPy

Tool to convert video files to sets of gifs with a very unoriginal name.

## Installing

First get the files from github.

`git clone git@github.com:mkell43/moviegifpy.git`

Then install the requirements.

`pip install -r requirements.txt`


## Using

For basic help run with `-h`.

`python moviegif -h`

`python moviegif run -h`

### Note About Gifsicle

[Gifsicle](http://www.lcdf.org/gifsicle/) is a mighty fine tool for reducing gif image sizes.  However,
[MoviePy](https://github.com/Zulko/moviepy) which I use for generating the gifs already does a fantastic job in
creating gifs relatively small in file size.

Because of this in order to have Gifsicle to have any profound effect I have it changing the color palette of the gifs
to 256.  What this means is that sometimes colors come out looking a little funky in the gifs it creates.
  
On the upside though the process to create gifs from a video file goes much faster.  In one test a file that took 36
minutes to create without the `--gifsicle` flag, took only 12 minutes with it.