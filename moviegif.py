#!/usr/bin/env python

import os
import sys
import argh
from argh import arg
import datetime

from moviegif import Video
from moviegif.helpers import spg, get_size_mb, avg_time, load_presets, run_gifsicle

'''

    TODO :: Update while loop to grab last few seconds.
    TODO :: Add switch to use gifsicle.
    TODO :: Look into using averages for pull times / different methods for creating the gifs
    TODO :: Add using averages for pull times as option.
    TODO :: Look into using more accurate get_spg function that makes a test gif instead of just a single image.
    TODO :: Add switch to do super fast.  Ignores checks on file size and sends jobs to workers to create the gifs.
    TODO :: Add deployment option.  Spins up and sends to Digital Ocean, AWS, etc. with web interface.
    TODO :: Add switches based on where it'll be stored (Imgur, Tumblr) to preset sizes and automatically upload.
    TODO :: Add dickbutt watermark flag.

'''


@arg('video_file',
     help='Path to video file.')
@arg('-p', '--preset',
     choices=['tumblr', 'imgur', 'imgurfree'],
     help='Preset settings type to use.')
@arg('-t', '--text',
     help='Text string to overlay on created gifs.')
@arg('-x', '--targetsize',
     help='Max size, in MB, to make the created gifs.',
     default=2)
@arg('-w', '--width',
     help='Width, in px, to resize the created gifs to.',
     default=350)
@arg('--fps',
     help='FPS to use when creating the gifs.',
     default=10)
@arg('--build',
     help='Directory to build and output the gifs to.',
     default='./build')
@arg('--decrement',
     help='Time, in seconds, to decrement from gif length when retrying gif creation',
     default=0.3)
@arg('--gifsicle',
     help='Significantly faster, but may produce some odd coloring.',
     default=False,
     action='store_true')
def run(video_file, **kwargs):

    if kwargs['preset'] is not None:
        kwargs = load_presets(kwargs, kwargs['preset'])
    
    # Create our video object to work with.
    video = Video(video_file, kwargs['width'])
    
    # Get the number of seconds per gif to match target file size.
    seconds_per_gif = spg(video.video, kwargs['targetsize'], fps=kwargs['fps'])

    # Get the video's runtime.
    video_runtime = video.runtime
    
    # Build our gifs.
    start_time = 0
    end_time = seconds_per_gif
    
    while end_time <= video_runtime and start_time < video_runtime:
        attempt = 1

        # Create gif.  Returns gif_name for checking later.
        gif_name = video.build_gif(start_time, end_time,
                                   build_dir=kwargs['build'],
                                   fps=kwargs['fps'],
                                   text=kwargs['text'])

        if kwargs['gifsicle'] is True:
            if run_gifsicle(gif_name) is False:
                print 'Gifsicle failed. - %s' % gif_name
                sys.exit(0)

        
        file_size = get_size_mb(gif_name)
        
        # Test gif's size and recreate until smaller than the target gif's size.
        # If this is the second attempt, use the seconds_per_gif setting - the average
        #   gif run time.  If it's the 3rd or greater pass, use the decrement stated in
        #   the settings.
        while file_size > kwargs['targetsize']:
            
            attempt += 1

            # Decrement end time            
            if attempt == 2:
                decrement = float(seconds_per_gif - avg_time(kwargs['build']))
                end_time = end_time - decrement
            if attempt > 2:
                end_time = end_time - kwargs['decrement']
            with open('log', 'a') as f:
                f.write(str(datetime.datetime.now()) + ' :: ' + 'REMOVED' + ' :: ' + gif_name + '\n')
            # Remove old gif.
            os.remove(gif_name)
            
            # Recreate gif.
            gif_name = video.build_gif(start_time, end_time,
                                       build_dir=kwargs['build'],
                                       fps=kwargs['fps'],
                                       text=kwargs['text'])

            if kwargs['gifsicle'] is True:
                if run_gifsicle(gif_name) is False:
                    print 'Gifsicle failed. - %s' % gif_name
                    sys.exit(0)

            
            # Test gif's size again.
            file_size = get_size_mb(gif_name)
        
        # Increment values.
        start_time = end_time
        end_time = end_time + seconds_per_gif
        
        with open('log', 'a') as f:
            f.write(str(datetime.datetime.now()) + ' :: ' + 'FINISHED' + ' :: ' + gif_name + '\n')

parser = argh.ArghParser()
parser.add_commands([run])


if __name__ == '__main__':
    parser.dispatch()