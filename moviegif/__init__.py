from moviepy.editor import *
from moviepy.video.io.ffmpeg_reader import ffmpeg_parse_infos

import os


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