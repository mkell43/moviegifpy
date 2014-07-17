import os
import glob


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


def load_presets(settings, preset):

    if preset == 'tumblr':
        from presets import tumblr_presets as kwargs
    elif preset == 'imgur':
        from presets import tumblr_presets as kwargs  # This is the same due to Imgur's file size requirements.
    elif preset == 'imgurfree':
        from presets import imgurfree_presets as kwargs
    else:
        kwargs = settings

    kwargs['text'] = settings['text']
    kwargs['build'] = settings['build']
    kwargs['gifsicle'] = settings['gifsicle']

    return kwargs


def prog_exists(prog):
    '''
    Returns true if the specified program is available.
    :param prog: a string, name of the program to locate.
    :returns: True/False depending on if the program is found and accessible by the current user.
    '''

    responses = list()
    for path in os.environ["PATH"].split(os.pathsep):
        path = path.strip('"')
        prog_path = os.path.join(path, prog)
        response = os.path.isfile(prog_path) and os.access(prog_path, os.X_OK)
        responses.append(response)

    if True in responses:
        return True
    else:
        return False


def run_gifsicle(filename):
    '''
    Runs gifsicle on the specified image file.
    :param filename: a string, the file to be processed
    :returns: True/False depending on if gifsicle is able to process the file appropriately.
    '''

    # --use-col=gray for gray scale

    import subprocess

    p = subprocess.Popen(['gifsicle', '--batch', '-O3', '--colors=256', filename],
                         stderr=subprocess.PIPE)
    error = p.communicate()[1]

    if 'No such file or directory' in error:
        return False
    else:
        return True