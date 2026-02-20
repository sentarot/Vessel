## Vessel - Game Configuration Options

## Game title and version
define config.name = _("Vessel")
define config.version = "0.2 - Cycles One & Two"

## Window title
define config.window_title = _("Vessel - A Psychological Horror Simulator")

## Text display
define config.developer = True

## Build configuration
define build.name = "Vessel"

## Game saves
define config.save_directory = "Vessel-1234567890"

## Window configuration  
define config.window = "auto"

## Transitions
define config.enter_transition = dissolve
define config.exit_transition = dissolve
define config.intra_transition = dissolve

## Sound and Music
define config.has_sound = True
define config.has_music = True
define config.has_voice = False

## Skip settings
define config.allow_skipping = True
define config.fast_skipping = False

## Layers
define config.layers = [ 'master', 'transient', 'screens', 'overlay' ]

## Enable overlay screens
define config.overlay_screens = ["game_menu_buttons"]

## Thumbnails
define config.thumbnail_width = 256
define config.thumbnail_height = 144

## Console (for debugging)
define config.console = True

## GL settings
define config.gl2 = True

## History length
define config.history_length = 250

## Preference defaults
default preferences.text_cps = 50
default preferences.afm_time = 15
