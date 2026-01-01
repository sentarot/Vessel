## Enhanced GUI Configuration for Vessel

## Colors - Muted, sophisticated palette
define gui.accent_color = '#ffebb4'
define gui.idle_color = '#b4b4c8'
define gui.idle_small_color = '#888899'
define gui.hover_color = '#ffebb4'
define gui.selected_color = '#ffffff'
define gui.insensitive_color = '#4d4d5c'
define gui.muted_color = '#646478'
define gui.hover_muted_color = '#8a8a9e'

define gui.text_color = '#ffffff'
define gui.interface_text_color = '#c8c8dc'
define gui.button_text_idle_color = '#b4b4c8'
define gui.button_text_hover_color = '#ffebb4'
define gui.button_text_selected_color = '#ffffff'
define gui.button_text_insensitive_color = '#4d4d5c'

## Fonts
define gui.text_font = "DejaVuSans.ttf"
define gui.name_text_font = "DejaVuSans-Bold.ttf"
define gui.interface_text_font = "DejaVuSans.ttf"
define gui.button_text_font = "DejaVuSans.ttf"

## Font sizes
define gui.text_size = 24
define gui.name_text_size = 32
define gui.interface_text_size = 22
define gui.button_text_size = 22
define gui.label_text_size = 28
define gui.notify_text_size = 20
define gui.title_text_size = 48

## Main and game menus
define gui.main_menu_background = "gui/main_menu.png"
define gui.game_menu_background = "gui/game_menu.png"

## Dialogue
define gui.textbox_height = 240
define gui.textbox_yalign = 1.0

define gui.name_xpos = 300
define gui.name_ypos = 0
define gui.name_xalign = 0.0

define gui.namebox_width = None
define gui.namebox_height = None
define gui.namebox_borders = Borders(5, 5, 5, 5)
define gui.namebox_tile = False

define gui.dialogue_xpos = 320
define gui.dialogue_ypos = 62
define gui.dialogue_width = 900
define gui.dialogue_text_xalign = 0.0

## Buttons
define gui.button_width = None
define gui.button_height = 40
define gui.button_borders = Borders(6, 6, 6, 6)
define gui.button_tile = False
define gui.button_text_font = gui.button_text_font
define gui.button_text_size = gui.button_text_size
define gui.button_text_xalign = 0.5
define gui.button_text_idle_color = gui.button_text_idle_color
define gui.button_text_hover_color = gui.button_text_hover_color
define gui.button_text_selected_color = gui.button_text_selected_color
define gui.button_text_insensitive_color = gui.button_text_insensitive_color

## Choice buttons
define gui.choice_button_width = 800
define gui.choice_button_height = 60
define gui.choice_button_tile = False
define gui.choice_button_borders = Borders(120, 8, 120, 8)
define gui.choice_button_text_font = gui.button_text_font
define gui.choice_button_text_size = gui.button_text_size
define gui.choice_button_text_xalign = 0.5
define gui.choice_button_text_idle_color = "#c8c8dc"
define gui.choice_button_text_hover_color = "#ffebb4"
define gui.choice_button_text_insensitive_color = "#4d4d5c"

## File slot buttons
define gui.slot_button_width = 276
define gui.slot_button_height = 206
define gui.slot_button_borders = Borders(10, 10, 10, 10)
define gui.slot_button_text_size = 20
define gui.slot_button_text_xalign = 0.5
define gui.slot_button_text_idle_color = gui.idle_small_color
define gui.slot_button_text_hover_color = gui.hover_color
define gui.slot_button_text_selected_idle_color = gui.selected_color
define gui.slot_button_text_selected_hover_color = gui.hover_color

## Page buttons
define gui.page_button_width = 100
define gui.page_button_height = 40

## Navigation buttons
define gui.navigation_button_width = 200
define gui.navigation_button_height = 40

## Quick buttons
define gui.quick_button_borders = Borders(10, 6, 10, 6)
define gui.quick_button_text_size = 18
define gui.quick_button_text_idle_color = gui.idle_small_color
define gui.quick_button_text_hover_color = gui.hover_color

## Positioning
define gui.navigation_xpos = 60
define gui.skip_ypos = 15
define gui.notify_ypos = 68
define gui.choice_spacing = 26
define gui.navigation_spacing = 6
define gui.pref_spacing = 15
define gui.pref_button_spacing = 0
define gui.page_spacing = 0
define gui.slot_spacing = 15
define gui.main_menu_text_xalign = 0.5

## Frames
define gui.frame_borders = Borders(6, 6, 6, 6)
define gui.confirm_frame_borders = Borders(60, 60, 60, 60)
define gui.skip_frame_borders = Borders(24, 8, 75, 8)
define gui.notify_frame_borders = Borders(24, 8, 60, 8)
define gui.frame_tile = False

## Bars, Scrollbars, and Sliders
define gui.bar_size = 32
define gui.scrollbar_size = 16
define gui.slider_size = 32
define gui.bar_tile = False
define gui.scrollbar_tile = False
define gui.slider_tile = False
define gui.bar_borders = Borders(6, 6, 6, 6)
define gui.scrollbar_borders = Borders(6, 6, 6, 6)
define gui.slider_borders = Borders(6, 6, 6, 6)
define gui.vbar_borders = Borders(6, 6, 6, 6)
define gui.vscrollbar_borders = Borders(6, 6, 6, 6)
define gui.vslider_borders = Borders(6, 6, 6, 6)
define gui.unscrollable = "hide"

## History
define gui.history_height = 180
define gui.history_name_xpos = 180
define gui.history_name_ypos = 0
define gui.history_name_width = 180
define gui.history_name_xalign = 1.0
define gui.history_text_xpos = 200
define gui.history_text_ypos = 5
define gui.history_text_width = 900
define gui.history_text_xalign = 0.0

## NVL-Mode
define gui.nvl_borders = Borders(0, 15, 0, 30)
define gui.nvl_list_length = 6
define gui.nvl_height = 173
define gui.nvl_spacing = 15
define gui.nvl_name_xpos = 645
define gui.nvl_name_ypos = 0
define gui.nvl_name_width = 225
define gui.nvl_name_xalign = 1.0
define gui.nvl_text_xpos = 675
define gui.nvl_text_ypos = 12
define gui.nvl_text_width = 885
define gui.nvl_text_xalign = 0.0
define gui.nvl_thought_xpos = 360
define gui.nvl_thought_ypos = 0
define gui.nvl_thought_width = 1170
define gui.nvl_thought_xalign = 0.0
define gui.nvl_button_xpos = 675
define gui.nvl_button_xalign = 0.0

## Localization
define gui.language = "unicode"
