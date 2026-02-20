## Enhanced Custom Screens for Vessel

screen status_screen():
    
    modal True
    
    frame:
        xalign 0.5
        yalign 0.5
        xsize 900
        ysize 650
        background "#1c1e26"
        padding (50, 50)
        
        vbox:
            spacing 25
            
            text "PHYSICAL STATUS — WEEK [weeks_pregnant]" size 32 color "#ffebb4" xalign 0.5 bold True
            
            text "All body systems compromised due to pregnancy burden" size 18 color "#ff8888" xalign 0.5 italic True
            
            null height 25
            
            hbox:
                spacing 50
                
                vbox:
                    spacing 18
                    text "LOWER BODY" size 24 color "#ffebb4" underline True
                    
                    null height 5
                    
                    text "• Feet: [status_feet]" size 17 color "#ff8888"
                    text "• Ankles: Severe edema" size 17 color "#ff8888"
                    text "• Legs: Weakened, cramping" size 17 color "#ff8888"
                    text "• Pelvis: Constant pressure" size 17 color "#ff8888"
                    text "• Mobility: [status_mobility]" size 17 color "#ff8888"
                
                vbox:
                    spacing 18
                    text "UPPER BODY" size 24 color "#ffebb4" underline True
                    
                    null height 5
                    
                    text "• Hands: [status_hands]" size 17 color "#ff8888"
                    text "• Back: [status_back]" size 17 color "#ff8888"
                    text "• Breasts: Tender, engorged" size 17 color "#ff8888"
                    text "• Abdomen: [status_abdomen]" size 17 color "#ff8888"
                    text "• Breathing: Restricted by size" size 17 color "#ff8888"
            
            null height 25
            
            hbox:
                spacing 60
                xalign 0.5
                
                vbox:
                    spacing 8
                    text "FATIGUE" size 20 color "#b4c8ff" bold True
                    bar value fatigue range 100 xsize 280 ysize 35 left_bar "#ff6666" right_bar "#333344"
                    text "[fatigue]/100" size 16 xalign 0.5 color "#c8c8dc"
                
                vbox:
                    spacing 8
                    text "DIGNITY" size 20 color "#b4c8ff" bold True
                    bar value dignity range 100 xsize 280 ysize 35 left_bar "#6699ff" right_bar "#333344"
                    text "[dignity]/100" size 16 xalign 0.5 color "#c8c8dc"
            
            null height 25
            
            textbutton "Close" action Hide("status_screen") xalign 0.5:
                xsize 180
                ysize 50
                background Frame("gui/button/choice_idle_background.png", 10, 10)
                hover_background Frame("gui/button/choice_hover_background.png", 10, 10)
                text_size 22
                text_color "#b4b4c8"
                text_hover_color "#ffebb4"


screen inventory_screen():
    
    modal True
    
    frame:
        xalign 0.5
        yalign 0.5
        xsize 1000
        ysize 650
        background "#1c1e26"
        padding (50, 50)
        
        vbox:
            spacing 35
            
            text "INVENTORY MANAGEMENT" size 32 color "#ffebb4" xalign 0.5 bold True
            
            null height 15
            
            hbox:
                spacing 80
                xalign 0.5
                
                # Player's extremely limited inventory
                vbox:
                    spacing 18
                    
                    text "YOUR POCKETS" size 24 color "#ffebb4" xalign 0.5
                    text "(Dress has no pockets)" size 15 color "#888899" xalign 0.5 italic True
                    
                    null height 15
                    
                    frame:
                        xsize 380
                        ysize 320
                        background "#0f1117"
                        padding (25, 25)
                        
                        if len(player_inventory) == 0:
                            text "EMPTY" size 24 color "#4d4d5c" xalign 0.5 yalign 0.5 italic True
                        else:
                            vbox:
                                spacing 12
                                for item in player_inventory:
                                    text "• [item]" size 17 color "#ffffff"
                
                # Caretaker's tote - everything she needs but can't access alone
                vbox:
                    spacing 18
                    
                    text "ARIA'S TOTE BAG" size 24 color "#ffebb4" xalign 0.5
                    text "(Must ask permission to access)" size 15 color "#888899" xalign 0.5 italic True
                    
                    null height 15
                    
                    frame:
                        xsize 380
                        ysize 320
                        background "#0f1117"
                        padding (25, 25)
                        
                        viewport:
                            scrollbars "vertical"
                            mousewheel True
                            
                            vbox:
                                spacing 10
                                for item in caretaker_tote:
                                    text "• [item]" size 17 color "#aaaaaa"
            
            null height 25
            
            text "You must ask Aria or Sophie whenever you need something from the tote." size 17 color "#ff8888" xalign 0.5 italic True
            
            null height 15
            
            textbutton "Close" action Hide("inventory_screen") xalign 0.5:
                xsize 180
                ysize 50
                background Frame("gui/button/choice_idle_background.png", 10, 10)
                hover_background Frame("gui/button/choice_hover_background.png", 10, 10)
                text_size 22
                text_color "#b4b4c8"
                text_hover_color "#ffebb4"


## Quick access buttons during gameplay
screen game_menu_buttons():
    
    hbox:
        xalign 0.02
        yalign 0.02
        spacing 12
        
        textbutton "Status":
            action Show("status_screen")
            xsize 120
            ysize 40
            background Frame("gui/button/small_idle_background.png", 6, 6)
            hover_background Frame("gui/button/small_hover_background.png", 6, 6)
            text_size 18
            text_color "#b4b4c8"
            text_hover_color "#ffebb4"
            
        textbutton "Inventory":
            action Show("inventory_screen")
            xsize 120
            ysize 40
            background Frame("gui/button/small_idle_background.png", 6, 6)
            hover_background Frame("gui/button/small_hover_background.png", 6, 6)
            text_size 18
            text_color "#b4b4c8"
            text_hover_color "#ffebb4"


## Say screen
screen say(who, what):
    style_prefix "say"

    window:
        id "window"
        background Frame("gui/textbox.png", 0, 0)
        
        if who is not None:
            window:
                id "namebox"
                style "namebox"
                background Frame(Solid("#2d303a"), 10, 10)
                padding (20, 8, 20, 8)
                
                text who:
                    id "who"
                    color "#ffebb4"
                    size 30
                    bold True

        text what:
            id "what"
            color "#ffffff"
            size 24


## Choice screen  
screen choice(items):
    style_prefix "choice"

    vbox:
        xalign 0.5
        yalign 0.5
        spacing 26

        for i in items:
            textbutton i.caption:
                action i.action
                xsize 800
                ysize 60
                background Frame("gui/button/choice_idle_background.png", 10, 10)
                hover_background Frame("gui/button/choice_hover_background.png", 10, 10)
                text_size 22
                text_color "#c8c8dc"
                text_hover_color "#ffebb4"
                text_xalign 0.5


style window is default
style say_label is default
style say_dialogue is default
style say_thought is say_dialogue

style namebox is default
style namebox_label is say_label

style window:
    xalign 0.5
    xfill True
    yalign gui.textbox_yalign
    ysize gui.textbox_height
    background Image("gui/textbox.png", xalign=0.5, yalign=1.0)

style namebox:
    xpos gui.name_xpos
    xanchor gui.name_xalign
    xsize gui.namebox_width
    ypos gui.name_ypos
    ysize gui.namebox_height

style say_label:
    properties gui.text_properties("name", accent=True)
    xalign gui.name_xalign
    yalign 0.5

style say_dialogue:
    properties gui.text_properties("dialogue")
    xpos gui.dialogue_xpos
    xsize gui.dialogue_width
    ypos gui.dialogue_ypos
    adjust_spacing False


## Confirm screen - fixes yesno_prompt AttributeError
screen confirm(message, yes_action, no_action):

    modal True

    zorder 200

    style_prefix "confirm"

    add "gui/game_menu.png"

    frame:
        xalign 0.5
        yalign 0.5
        xsize 600
        ysize 300
        background "#1c1e26"
        padding (40, 40)

        vbox:
            xalign 0.5
            yalign 0.5
            spacing 30

            label _(message):
                style "confirm_prompt"
                xalign 0.5
                text_color "#ffebb4"
                text_size 24

            hbox:
                xalign 0.5
                spacing 100

                textbutton _("Yes") action yes_action:
                    xsize 140
                    ysize 50
                    background Frame("gui/button/choice_idle_background.png", 10, 10)
                    hover_background Frame("gui/button/choice_hover_background.png", 10, 10)
                    text_size 22
                    text_color "#b4b4c8"
                    text_hover_color "#ffebb4"

                textbutton _("No") action no_action:
                    xsize 140
                    ysize 50
                    background Frame("gui/button/choice_idle_background.png", 10, 10)
                    hover_background Frame("gui/button/choice_hover_background.png", 10, 10)
                    text_size 22
                    text_color "#b4b4c8"
                    text_hover_color "#ffebb4"

style confirm_prompt is gui_prompt:
    xalign 0.5
    text_align 0.5
