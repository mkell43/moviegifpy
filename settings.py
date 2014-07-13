# Predefineds.
video_file = ''
v = True

# Presets for Tumblr.
tumblr_presets = dict()
tumblr_presets['width'] = 350
tumblr_presets['fps'] = 10
tumblr_presets['text_x'] = 10
tumblr_presets['text_y'] = 225
tumblr_presets['font_size'] = 15
tumblr_presets['target_size'] = 2  # In MB

# Doing this for testing.
settings = tumblr_presets

if settings['target_size'] is None:
    settings['target_size'] = 2

settings['decrement'] = 0.3
settings['overlay_text'] = ''
settings['build_dir'] = 'build'