#!/usr/bin/env python

import os
import argh
from argh import arg
import datetime

from settings import settings
from moviegif import Video, spg, get_size_mb, avg_time

'''

    DONE :: Add text overlays to images.
    DONE :: Add autosetting of FPS when creating gifs.
    TODO :: Add switches to set FPS when creating gifs.
    DONE :: Update while loop to grab last few seconds.
    TODO :: Add switch to use gifsicle.
    DONE :: Look into using averages for pull times
    TODO :: Add using averages for pull times as option.
    TODO :: Look into using more accurate get_spg function that makes a test gif instead of just a single image.
    TODO :: Add switch to do super fast.  Ignores checks on file size and sends jobs to workers to create the gifs.
    TODO :: Add deployment option.  Spins up and sends to Digital Ocean, AWS, etc. with web interface.
    TODO :: Add switches based on where it'll be stored (Imgur, Tumblr) to preset sizes and automatically upload.
    TODO :: Add dickbutt watermark flag.

'''

@arg('video_file', help='Path to video file.')
@arg('-p', '--preset', choices=['tumblr', 'imgur'], help='Preset settings type to use.')
@arg('-t', '--text', help='Text string to overlay on created gifs.')
@arg('-x', '--targetsize', help='Max size, in MB, to make the created gifs.', default=2)
@arg('-w', '--width', help='Width, in px, to resize the created gifs to.', default='350')
@arg('--fps', help='FPS to use when creating the gifs.', default=10)
def run(video_file, **kwargs):
    
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
                                   build_dir=settings['build_dir'],
                                   fps=settings['fps'],
                                   text=settings['overlay_text'])
        
        file_size = get_size_mb(gif_name)
        
        # Test gif's size and recreate until smaller than the target gif's size.
        # If this is the second attempt, use the seconds_per_gif setting - the average
        #   gif run time.  If it's the 3rd or greater pass, use the decrement stated in
        #   the settings.
        while file_size > settings['target_size']:
            
            attempt += 1

            # Decrement end time            
            if attempt == 2:
                decrement = float(seconds_per_gif - avg_time(settings['build_dir']))
                end_time = end_time - decrement
            if attempt > 2:
                end_time = end_time - settings['decrement']
            with open('log', 'a') as f:
                f.write(str(datetime.datetime.now()) + ' :: ' + 'REMOVED' + ' :: ' + gif_name + '\n')
            # Remove old gif.
            os.remove(gif_name)
            
            # Recreate gif.
            gif_name = video.build_gif(start_time, end_time,
                                       build_dir=settings['build_dir'],
                                       fps=settings['fps'],
                                       text=settings['overlay_text'])
            
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