from moviepy.editor import *
from moviepy.video.io.ffmpeg_reader import ffmpeg_parse_infos

import os
import glob


class Video(object):

    def __init__(self, video_file, width):
        '''
            Creates the video object.
        '''

        video_info = ffmpeg_parse_infos(video_file)

        # Full path the video.
        self.file = video_file

        # Moviepy VideoFileClip object.
        self.video = VideoFileClip(video_file).resize(width=width)

        # Length in seconds of the video.
        self.runtime = video_info['duration']

        # Get the video's file name.
        file_name, file_extension = os.path.splitext(video_file)
        self.video_name = file_name.split('/')[-1].replace(' ', '').translate(None, '[]')

        # The video's resized height and width.
        self.width = width
        self.height = float(video_info['video_size'][1]) / float(video_info['video_size'][0]) * width

    def overlay(self, video_clip, text, **kwargs):
        '''
            Creates and returns the text overlay for the video / gifs.
        '''

        if 'text_x' in kwargs:
            text_x = kwargs['text_x']
        else:
            text_x = 10

        if 'text_y' in kwargs:
            text_y = kwargs['text_y']
        else:
            text_y = self.height - 25

        if 'font_size' in kwargs:
            font_size = kwargs['font_size']
        else:
            font_size = 15

        # Build our text overlay.
        return TextClip(text, fontsize=font_size, color='white', font='Helvetica').\
                    set_pos((text_x,text_y)).set_duration(video_clip.duration)

    def build_gif(self, start_time, end_time, build_dir=None, fps=None, text=None):
        '''
            Creates a gif image.  Returns the new gif's file name.
        '''

        if fps is None:
            fps = self.video.fps

        # Build the gif's name.
        if build_dir is None:
            gif_name = self.video_name + '_' + str(start_time) + '_' + str(end_time) + '.gif'
        else:
            gif_name = build_dir + '/' + self.video_name
            gif_name = gif_name + '_' + str(start_time) + '_' + str(end_time) + '.gif'

        # Get the subclip.
        video_clip = self.video.subclip(start_time,end_time)

        if text is not None:
            # Create the overlay
            overlay = self.overlay(video_clip, text)

            # Compsite the video and overlay together.
            composite_clip = CompositeVideoClip([video_clip, overlay])

            # Create the gif.
            composite_clip.to_gif(gif_name, fps=fps, fuzz=2, verbose=False)
        else:
            # Create the gif.
            video_clip.to_gif(gif_name, fps=fps, fuzz=2, verbose=False)

        return gif_name


def get_size_mb(f):

    '''
        Gets the size in MB of a given file.
    '''

    file_size = os.path.getsize(f) / (1024*1024.0)  # Output in MB

    return file_size


def spg(video, target_size, fps=None):

    '''
    Get's the number of seconds per gif to match target file size.
    '''

    import math

    # Check if frames per second is preset, if not grab from the video file.
    if fps is None:
        # Get the video object's frames per second.
        fps = video.fps

    # Create our test frame.
    video.save_frame('test.gif', t=120)

    # Check test frame's size.
    frame_size = get_size_mb('test.gif')

    # Get frames per second.
    frames_per_gif = target_size / frame_size

    # Get seconds per gif.
    seconds_per_gif = math.trunc(frames_per_gif / fps)

    # Cleanup after ourselves.
    os.remove('test.gif')

    return seconds_per_gif


def get_avg(items):
    '''
        Function to get the average of a list.
    '''

    import decimal

    total=0
    for i in items:
        total = total + i

    decimal.getcontext().prec = 3

    return decimal.Decimal(total)/decimal.Decimal(len(items))


def avg_time(build_dir):
    '''
        Get's the average length in seconds of the gifs.
    '''

    times = list()

    for gif in glob.glob(build_dir + '/' + '*.gif'):
        times.append(float(gif.split('_')[-1].replace('.gif', '')) - float(gif.split('_')[-2]))

    return get_avg(times)


def avg_size(build_dir):
    '''
        Get's the average file size in MB of the gifs.
    '''

    sizes = list()

    for gif in glob.glob(build_dir + '/' + '*.gif'):
        sizes.append(get_size_mb(gif))

    return get_avg(sizes)