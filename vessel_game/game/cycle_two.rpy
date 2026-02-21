## Vessel - Cycle Two: The Knowing
## Now she understands. But understanding changes nothing.

## New Cycle Two Variables
default cycle = 2
default hope = 30  # Out of 100 - can she hold onto it?
default compliance = 50  # How obedient she's become
default weeks_pregnant_c2 = 6
default escape_clues = 0
default ally_trust = 0  # Trust level with potential ally
default met_elena = False
default found_phone = False
default found_map = False
default diary_entries = 0

## Updated physical status for early Cycle Two
default c2_status_feet = "Recovering from last pregnancy"
default c2_status_back = "Weakened core muscles"
default c2_status_hands = "Grip slowly returning"
default c2_status_abdomen = "Six weeks pregnant - barely showing"
default c2_status_mobility = "Weak but ambulatory"

## Characters
define elena = Character("Elena", color="#98d4a6")
define nurse = Character("Nurse Patton", color="#d4d4d4")
define voice = Character("Voice", color="#666666")


label cycle_two_start:

    scene bg bedroom morning

    "I know now."

    "I know what this place is. What they're doing. What I am to them."

    "A vessel."

    "Six weeks into my second forced pregnancy, and the morning sickness is already unbearable."

    "But this time is different. This time I'm awake."

    "Aria leans over me - all five-eleven of her, auburn waves tumbling forward, that generous, curving body in fresh scrubs that somehow look like designer loungewear. Her perfume settles over me like a net."

    "I'm so small in this bed. Curled on my side, knees drawn up around the new swell of my belly, my shoulder blades sharp enough to cut paper."

    aria "Good morning, mama! How's our tummy today?"

    menu:
        "How do I play this?"

        "Pretend everything is fine":
            $ compliance += 10
            $ hope += 5
            protag "Morning sickness, but I'm okay."
            aria "That's the spirit! It gets easier, you know that now."
            "She doesn't suspect I remember. Good."

        "Show my anger":
            $ resistance += 10
            $ compliance -= 10
            $ hope -= 5
            protag "How do you think I feel? You impregnated me while I was drugged."
            aria "Oh sweetie... those hormones are really doing a number on you. Let me get you some tea."
            "She dismisses it completely. Like I said the sky was green."
            sophie "She's been having those episodes again."
            aria "I'll let Dr. Marcus know. We may need to adjust her medication."
            "Medication. That's what they call it."

    "Aria helps me to the bathroom. Her hand on my lower back covers the entire width of my spine. I'm weaker than I should be - the back-to-back pregnancies have hollowed me out. My hip bones jut above the low curve of my belly. My legs are birdlike."

    "But I can walk. Aria shortens her long stride to match my shuffle, and I can feel her restraining herself from just picking me up."

    "That's more than I could do at the end of Cycle One."

    scene bg bathroom

    "The bath again. The same ritual."

    "But today I notice things I didn't before."

    "The lock on the bathroom door - removed. The window - sealed shut, painted over. The mirror - plastic, not glass."

    "Everything sharp has been taken away."

    "How did I not see this before?"

    sophie "Arms up, sweetie."

    "Sophie lifts my arms like they're made of pipe cleaners. She pulls my nightgown over my head with one fluid motion - her tall, toned body barely shifting with the effort."

    "I catch my reflection in the plastic mirror. Behind Sophie's broad, tan shoulders, I can see myself - all ribs and collarbones and hollow hips, except for the slight curve of my belly where the new pregnancy is just beginning to show. My breasts are still swollen from the last pregnancy, too large for my wasted frame, sitting heavy on my narrow chest."

    "I look like a doll that someone's been squeezing."

    "Dark circles under my eyes. Wrists I can close my own fingers around. My face still pretty - annoyingly, persistently pretty - with its big eyes and soft mouth. The kind of face people call 'sweet.' The kind of face no one takes seriously."

    "But my eyes. My eyes are clear for the first time in months."

    menu:
        "While they wash me..."

        "Study the room carefully":
            $ escape_clues += 1
            $ hope += 5
            "I catalogue everything while keeping my expression blank."
            "Vent in the ceiling - too small. Drain - bolted. Cabinet - locked."
            "But the cabinet key is on a ring clipped to Sophie's belt loop."
            "I file that away."

        "Try to engage Sophie":
            $ ally_trust += 5
            protag "Sophie... how long have you worked here?"
            sophie "Oh, about three years now! I love it. Taking care of our mothers is so rewarding."
            protag "Have any of them ever... left? Before their contract was done?"
            "Sophie's hands pause on my shoulders. Just for a second."
            sophie "Everyone completes their journey, Lily. It's what's best."
            "That pause. She knows something."

    scene bg dining room

    "Breakfast. But this time I'm wheeled past other residents and I actually look at them."

    "There's a woman I haven't seen before. She's tiny - maybe five feet, maybe less - with a thirty-week belly that looks grotesquely large on her small frame. Her neck is thin as a stem. Her caretaker, a towering blonde with a swimsuit model's body, holds a fork to the woman's lips."

    "The woman's eyes are glassy. Vacant. She chews when the fork enters. Swallows when a hand strokes her throat."

    "That was me. That's what I looked like."

    "Another woman - further along, enormous - is chatting brightly with her caretakers, laughing at something they said. She's taller than the others, nearly as tall as her staff, and her pregnancy looks almost natural on her long frame."

    "She looks happy. Genuinely happy."

    "That's worse."

    aria "Here we go, sweetheart. Lots of folic acid today - so important in the first trimester!"

    "She holds the fork out."

    menu:
        "What do I do?"

        "Feed myself":
            $ resistance += 5
            $ dignity += 10
            protag "I can do it."
            "I take the fork. My hand shakes slightly, but I bring the eggs to my mouth on my own."
            aria "Look at you! So independent today."
            "She says it like I'm a toddler who just used a spoon."
            "But I did it. I fed myself."

        "Let her feed me (conserve energy)":
            $ compliance += 10
            $ fatigue -= 5
            "I open my mouth. Let her feed me."
            "Not because I can't do it. Because fighting every battle will exhaust me before I can fight the one that matters."
            "Pick your battles, Lily."

    "Midway through breakfast, the haunted woman at the far table suddenly speaks."

    unknown "I want to go home."

    "Her voice is paper-thin. Her caretaker immediately begins soothing her."

    nurse "Shh, sweetie. You are home."

    unknown "No. No, I want to go HOME. I want my MOTHER."

    "Two more staff appear - both tall, both beautiful, one with the broad shoulders of a former athlete, the other willowy with perfect posture. They speak in calm, measured tones, their hands gentle but immovable on the small woman's shoulders. Within moments they're wheeling her away."

    "The dining room falls silent."

    "Then Vivian speaks."

    vivian "Poor thing. Some women just aren't suited for this."

    "She takes a delicate sip of tea."

    vivian "Not like us, right Lily?"

    menu:
        "How do I respond?"

        "Agree (stay under the radar)":
            $ compliance += 5
            protag "Right."
            "Vivian smiles. Aria beams."
            "I hate myself a little."

        "Say nothing":
            $ resistance += 5
            "I look at the empty chair where the woman was sitting."
            "Where did they take her?"

    jump c2_morning_activities


label c2_morning_activities:

    scene bg hallway

    aria "Today's schedule: gentle walk in the gardens, then crafting circle, then Dr. Marcus at two."

    "A walk. In the gardens. I haven't been outside in months."

    scene bg gardens

    "The gardens are beautiful and terrible."

    "Manicured lawns, flowering hedges, a koi pond. Like a luxury resort."

    "Surrounded by a twelve-foot stone wall with no visible gate."

    "I'm in a wheelchair - Aria insists, even though I can walk short distances now."

    "But being out here lets me see the layout."

    aria "Isn't this lovely? Fresh air is so good for baby."

    "Baby. Singular. They haven't told me how many this time."

    menu:
        "What catches my attention?"

        "Study the wall":
            $ escape_clues += 1
            $ hope += 5
            "I look at the wall while pretending to watch butterflies."
            "It's smooth stone. No handholds. But near the east corner, there's a section covered in ivy."
            "Ivy means rough stone underneath. Climbable, potentially."
            "If I were strong enough to climb. Which I'm not. Not yet."

        "Notice the other building":
            $ escape_clues += 1
            "Past the main house, there's a smaller building I've never been inside."
            "Staff go in and out. I see a delivery truck parked outside it."
            "A delivery truck means a road. A road means a way out."
            "If I could get to it."

        "Watch the staff patterns":
            $ escape_clues += 1
            "I count staff. Three per resident seems standard."
            "Shift change happens around... I need to pay more attention."
            "But I notice: between 2 and 3 PM, the gardens are nearly empty."
            "Everyone's at appointments."

    "We pass a bench where a woman is sitting alone. No caretaker in sight."

    "She's maybe forty, with short dark hair and an advanced pregnancy. She's small like me - five-three, maybe five-four - with the same narrow shoulders and delicate build that make pregnancy look like an act of structural engineering. Her belly is massive on her, low and heavy, but she sits upright without support."

    "She's reading. An actual book. Not a pregnancy manual."

    "She looks up as we pass and our eyes meet. Hers are dark, lined, unclouded."

    "There's something sharp in her gaze. Alert. Knowing. No gloss, no fog."

    $ met_elena = True

    "Aria wheels me past before I can react."

    aria "That's Elena. She's in her fourth cycle. Bit of an odd duck."

    "Fourth cycle."

    "Four pregnancies."

    "And she still looks... present. Aware."

    "How?"

    jump c2_crafting


label c2_crafting:

    scene bg common room

    "Crafting circle is held in the common room. Eight pregnant women knitting baby blankets."

    "The irony is suffocating."

    "I'm given chunky yarn and enormous needles - 'easy for swollen fingers!'"

    "I'm placed next to Elena."

    "She doesn't look at me. She knits with practiced efficiency, her needles clicking rhythmically."

    "Then, without looking up, she speaks."

    elena "You're new to the knowing."

    "Her voice is barely audible over the chatter."

    menu:
        "What?"

        "What do you mean?":
            protag "I don't..."
            elena "Keep knitting. Don't look at me. Smile if a caretaker looks over."
            "I fumble with my yarn, trying to appear focused."
            elena "Most women never wake up. The drugs keep them compliant. Happy, even."

        "You can tell?":
            protag "How did you..."
            elena "Your eyes. They did the thing mine did, three cycles ago. Like someone turned the lights on."
            "She holds up her knitting, examining it casually."
            elena "Keep your voice down. Always keep your voice down."

    elena "They'll notice eventually. They always do. And then they increase the medication."

    protag "The warm milk."

    elena "Among other things. The food. The vitamins. The bath products. Everything is a delivery system."

    $ hope -= 10

    protag "Then how are you still..."

    elena "I learned to fake it. Cheek the pills. Vomit the milk when they're not looking. It took me two cycles to figure it out."

    "She pauses her knitting to stretch her fingers."

    elena "You have one advantage I didn't. You know early. I didn't figure it out until my third cycle."

    menu:
        "I need to know..."

        "Is there a way out?":
            $ hope += 10
            $ ally_trust += 10
            protag "Can we leave?"
            elena "Not 'we.' One, maybe. On the right night, with the right preparation."
            elena "I've been planning for eight months. I'm due in six weeks. If I'm going, it has to be before then."
            protag "After birth they'll..."
            elena "Drug me. Impregnate me. Again. Cycle five."
            "Her knitting needles never stop."
            elena "I won't let there be a cycle five."

        "What do they want?":
            $ ally_trust += 5
            protag "Why? Why are they doing this?"
            elena "Money. Each baby is worth mid-six figures to the right buyer. Healthy, genetically screened, carried to term in luxury conditions."
            elena "We're not patients. We're product."
            protag "That's..."
            elena "Keep smiling, sweetheart. Sophie's looking."
            "I force a smile. It feels like a crack in my face."

    "The crafting session continues. Elena teaches me a simple stitch. To anyone watching, we're just two pregnant women bonding over yarn."

    $ diary_entries += 1

    aria "Oh how sweet! You two are getting along!"

    elena "She reminds me of my daughter."

    "Elena says it smoothly, warmly. Perfect performance."

    aria "That's so nice. Lily could use a friend."

    "If only she knew."

    jump c2_doctor


label c2_doctor:

    scene bg medical office

    "Dr. Marcus's office. Same soft lighting. Same abstract art."

    "But now I notice the door locks from the outside."

    marcus "Lily! How are we adjusting to the new pregnancy?"

    "He says it so casually. Like asking about the weather."

    menu:
        "How do I play this?"

        "Compliant (safer)":
            $ compliance += 15
            protag "The morning sickness is rough, but I'm managing."
            marcus "That's what I like to hear. You're one of our best, Lily."
            "Best. Best vessel."

        "Defiant":
            $ resistance += 15
            $ compliance -= 10
            protag "You impregnated me without my consent while I was sedated."
            marcus "Lily, we've discussed this. You signed the forms."
            protag "Under duress. While drugged."
            "He makes a note on his clipboard."
            marcus "I'm going to increase your evening supplement. You seem agitated."
            "Evening supplement. More drugs."
            $ hope -= 10

    "The ultrasound reveals the new pregnancy."

    marcus "Triplets this time. Three healthy embryos."

    "Three."

    marcus "We've refined the protocol. Triplets are easier on the body than quadruplets. You should have a smoother experience."

    "'Smoother experience.' Like I'm reviewing a hotel."

    marcus "Any questions?"

    menu:
        "What do I ask?"

        "About my first babies":
            protag "My babies from the first pregnancy. Where are they?"
            marcus "With their families, Lily. Happy and healthy. You gave them a wonderful gift."
            protag "Can I see them?"
            marcus "That's not part of the arrangement. You understand."
            "I don't understand. I'll never understand."

        "About the other woman (the one removed at breakfast)":
            protag "The woman who was upset at breakfast this morning. Is she okay?"
            marcus "She's being well cared for. Sometimes the hormonal shifts cause distress."
            protag "Where did they take her?"
            marcus "To the quiet wing. For rest."
            "The quiet wing. I've never seen a quiet wing."
            $ escape_clues += 1

        "Nothing (don't raise suspicion)":
            $ compliance += 5
            protag "No. I'm fine."
            marcus "Perfect. Keep up your exercises and nutrition. I'll see you next week."

    scene bg hallway

    "After the appointment, Aria wheels me back to my room."

    "We pass a corridor I've never been down. A sign reads 'EAST WING - STAFF ONLY.'"

    "I catch a glimpse through a briefly opened door. Medical equipment. A row of beds."

    "And the woman from breakfast, lying motionless."

    "The door closes."

    aria "Almost home, sweetheart! I thought we could watch a movie tonight. Your choice!"

    "My choice. How generous."

    jump c2_evening


label c2_evening:

    scene bg bedroom evening

    "Evening. Sophie brings the warm milk."

    "I know what's in it now."

    sophie "Here you go, sweetie. Your favorite."

    menu:
        "The milk..."

        "Drink it (they're watching closely tonight)":
            $ compliance += 10
            $ hope -= 10
            "I drink. I hate myself for it. But Sophie is watching me intently tonight."
            "The fog starts to creep in within minutes."
            "No. I have to fight it. I have to stay..."
            "..."
            "I wake up the next morning with no memory of falling asleep."

        "Fake drinking it":
            $ resistance += 10
            $ hope += 10
            "I bring the cup to my lips, pretend to swallow. Let some dribble back."
            "I moan softly. 'Mmm. Thank you.'"
            sophie "Drink it all, hon. Every drop."
            "I take another fake sip. Then I pretend to doze off."
            "Sophie gently takes the cup. I keep my eyes closed, breathing slowly."
            sophie "She's out."
            "I hear her leave. The click of the lock."
            "I'm locked in. But I'm awake."
            "This is the first night I've been conscious after lights out in... I don't know how long."

    "The night stretches out."

    "Whether foggy or alert, I lie in the dark and think about what Elena said."

    "Eight months of planning."

    "She's going to try to escape."

    "And maybe... maybe she could take me with her."

    scene bg black

    centered "WEEKS PASS"

    centered "THE PREGNANCY GROWS"

    centered "BUT THIS TIME, YOU'RE WATCHING"

    centered "LEARNING"

    centered "WAITING"

    jump c2_midpoint


label c2_midpoint:

    scene bg bedroom morning

    $ weeks_pregnant_c2 = 20
    $ c2_status_abdomen = "Noticeably pregnant with triplets"
    $ c2_status_mobility = "Slowing down, assisted walking"
    $ c2_status_feet = "Beginning to swell"
    $ c2_status_back = "Increasing lower back pain"

    "Week twenty. Halfway through."

    "I'm bigger now. Not as massive as with the quadruplets, but the triplets are making themselves known. My belly is round and taut again, pulling my small frame forward. My lower back has started that deep, familiar ache. My breasts are heavy and sore, straining against the soft cotton they dress me in."

    "In the mirror this morning, I looked like a lowercase 'b' - thin everywhere except the one place that matters to them."

    "My window of mobility is closing."

    "If I'm going to act, it has to be soon."

    aria "Good morning! Big day today - we have your twenty-week scan!"

    "I smile. I've gotten good at smiling."

    protag "Can't wait."

    "Aria beams. She thinks I've accepted it."

    "Good."

    scene bg gardens

    "I find Elena in the gardens during the afternoon free period."

    "She's enormous now. Thirty-six weeks on her small frame - her belly is a planet, distorting her entire silhouette, forcing her to sit with her legs spread wide for balance. Her thin arms rest on top of it like they're draped over a boulder. Due any day."

    "We sit on the bench by the koi pond, two small women with grotesquely large bellies, looking like caricatures of motherhood. Her caretaker - a gorgeous, leggy redhead - is fifteen feet away, scrolling on a tablet."

    elena "Tonight."

    "One word. My heart stops."

    protag "What?"

    elena "Staff changeover at midnight. Three-minute gap in the east corridor cameras."

    protag "How do you know about cameras?"

    elena "Eight months, Lily. I've watched everything."

    menu:
        "What do I say?"

        "I'm coming with you":
            $ hope += 20
            $ resistance += 15
            protag "Take me with you."
            elena "You're twenty weeks pregnant. Can you run?"
            protag "I can try."
            elena "Trying isn't enough. If they catch us, there is no fifth chance for me."
            protag "Please."
            "She's quiet for a long time."
            elena "Supply building. Back door. Midnight exactly. If you're not there, I go alone."

        "I can't. Not yet.":
            $ compliance += 5
            $ hope -= 10
            protag "I'm not ready. I can barely walk fast."
            elena "I know. I didn't expect you to come."
            protag "But you..."
            elena "I'll send help. If I make it out, I'll send someone."
            protag "Promise me."
            elena "I promise."
            "She squeezes my hand once. Brief and fierce."

        "It's too dangerous":
            $ compliance += 10
            $ hope -= 15
            protag "Elena, if they catch you..."
            elena "Then it'll be cycle five and I'll never stop. I'd rather die in that wall than birth another child for these people."
            "There's nothing I can say to that."
            "She's made her choice."

    "That evening, I can barely eat."

    "Aria notices."

    aria "Not hungry? I hope you're not getting sick!"

    protag "Just tired."

    aria "Well, drink your milk and get a good night's rest."

    "She watches me drink. Every drop."

    "Tonight, of all nights."

    jump c2_the_night


label c2_the_night:

    scene bg bedroom night

    "11:47 PM."

    "The milk is heavy in my system. The fog is there, pressing at the edges."

    "But I forced myself to eat bread before drinking it. Elena told me that helps absorb some of it."

    "I'm fighting to stay conscious."

    "The hall is quiet. The night shift nurse passed by twenty minutes ago."

    menu:
        "What do I do?"

        "Try to get up":
            $ resistance += 20
            $ fatigue += 25
            "I swing my skinny legs off the bed. The room tilts."
            "My belly pulls me forward - twenty weeks of triplets on a hundred-pound frame. I grip the nightstand with fingers that can barely close."
            "Stand. You have to stand."
            "I stand. My knees shake. My belly hangs in front of me, stretching my nightgown taut. Barely."
            "The door. Is it locked?"
            "I try the handle. It turns."
            "They don't lock it on nights they give me the milk. They don't think they need to."
            "The hallway is dark. Emergency lighting only."
            "I take one step. Then another."
            $ hope += 15
            jump c2_hallway

        "Stay in bed":
            $ compliance += 10
            $ hope -= 20
            "I can't. I'm too drugged. Too pregnant. Too scared."
            "I lie there and listen to the silence."
            "At 12:04 AM, I hear running footsteps. Distant."
            "At 12:06, an alarm."
            "At 12:11, shouting."
            "Then silence again."
            jump c2_morning_after

        "Listen and wait":
            "I sit on the edge of the bed. Listening."
            "At midnight exactly, I hear a door somewhere far away open and close."
            "Then nothing for six minutes."
            "Then the alarm."
            jump c2_morning_after


label c2_hallway:

    scene bg hallway night

    "The corridor stretches ahead of me, dimly lit and silent."

    "Every step is a negotiation with my body. My bare feet are cold and swollen on the tile. The triplets shift with each movement, redistributing weight my narrow hips were never built to carry."

    "I pass doors. Other residents, sleeping their drugged sleep."

    "How many of us are there? Twelve? Fifteen?"

    "All vessels."

    "I reach the east corridor. The sign reads STAFF ONLY."

    "Elena said three minutes. The camera gap."

    "I don't have a watch. I have to guess."

    "I push through the door."

    scene bg east corridor

    "This part of the facility is different. Institutional. No pretty wallpaper or soft lighting."

    "Just concrete and fluorescent tubes."

    "I pass the medical wing. Through the window, I see beds. IV drips. Monitors."

    "The quiet wing."

    "There are women in those beds. Three of them. Motionless."

    "The breakfast woman is there. An IV in her arm. Her eyes closed."

    "'Resting.'"

    $ escape_clues += 1

    "I keep moving. The supply building should be at the end of this corridor."

    "My back screams. My feet ache. The babies kick in protest."

    "Almost there."

    "Then I hear a sound behind me."

    menu:
        "React..."

        "Hide":
            "I press myself into a doorway alcove. My belly juts out obscenely - I can't flatten against the wall, can't suck it in, can't make my body small enough to hide even though the rest of me is barely there."
            "Footsteps approach. Pass. Recede."
            "A night guard. Not looking in my direction."
            "I wait thirty seconds, then keep moving."
            $ hope += 5

        "Keep going (don't stop)":
            $ fatigue += 15
            "I don't look back. I move as fast as I can, which is barely faster than a shuffle."
            "The footsteps don't follow. Maybe they didn't see me."
            "Maybe."

    "I reach the back door. It's propped open with a folded towel."

    "Elena."

    scene bg outside night

    "The night air hits me and I almost collapse. I haven't been outside at night in... I can't remember."

    "Stars. I can see stars."

    "But Elena isn't here."

    "I wait. One minute. Two."

    "Then I hear the alarm."

    "It splits the silence - a shrieking electronic wail."

    "Lights snap on across the compound. The garden floods with light."

    "I'm standing in the open - five-foot-two, a hundred and thirty pounds of baby weight on a frame built for ninety-eight, in a white nightgown stretched transparent over my belly. I must look like a ghost."

    "Then a hand grabs my arm."

    elena "RUN."

    "She's there. Wild-eyed, breathing hard, her massive belly heaving under her own straining nightgown. Two small women, absurdly pregnant, lit up by floodlights."

    "We don't run. We can't run. Our legs are too thin, our bellies too heavy. Two vessels shuffling desperately toward the wall."

    "Elena leads me to the ivy-covered section. She pulls the vines aside."

    "There's a gap. Not in the wall - under it. A drainage channel, half-covered by vegetation."

    elena "I found it during garden walks. I've been widening it for months."

    "It's narrow. Terrifyingly narrow."

    protag "I can't fit through that."

    elena "You can. I did a practice run at thirty-two weeks."

    "Behind us, doors are slamming. Voices shouting."

    menu:
        "Do I..."

        "Go through the gap":
            $ hope += 25
            $ resistance += 20
            "I get on my hands and knees. My belly drops toward the ground, grazing the mud. My thin arms tremble."
            "I crawl. Mud and roots and stone scraping my taut, stretched skin. My belly drags through the drainage channel."
            "Halfway through, I get stuck. My belly - the only big part of me - wedged against stone. My shoulders fit. My hips fit. But the babies won't."
            "I can't breathe. I can't move forward or back."
            protag "Elena-"
            elena "Breathe out. Flatten yourself. Push with your legs."
            "I exhale everything. Dig my toes into the mud. Push."
            "Something tears - my nightgown, or my skin, I can't tell."
            "But I'm through."
            jump c2_outside_wall

        "Tell Elena to go without me":
            $ hope -= 20
            $ dignity += 15
            protag "Go. I'll slow you down."
            elena "Lily-"
            protag "GO. Send help. You promised."
            "She looks at me. In the floodlights, her face is a mask of anguish."
            elena "I promise."
            "She drops and crawls through the gap with practiced efficiency."
            "And then she's gone."
            "I stand there in my muddy nightgown, belly hanging low and heavy off my little frame, and wait for them to find me."
            jump c2_caught


label c2_outside_wall:

    scene bg road night

    "The other side of the wall."

    "A slope of rough grass leading down to a country road."

    "Elena is already sliding down, one hand under her belly."

    "I follow. Half sliding, half tumbling."

    "My body is screaming. Every ligament, every muscle."

    "But I'm outside. Outside the wall."

    elena "The road goes east to a village. Maybe two miles."

    "Two miles. In the dark. Twenty and thirty-six weeks pregnant."

    "Behind the wall, the shouting gets louder."

    elena "Move. Now."

    "We walk. Shuffle. Stagger."

    "Elena is having contractions. I can see her gripping her belly every few minutes."

    protag "Elena..."

    elena "I know. Stress-induced. I'll deal with it later."

    "We make it maybe half a mile before headlights appear on the road behind us."

    "A vehicle. Moving fast."

    elena "Into the trees."

    "We scramble off the road into a thicket. Branches scratch my face and arms."

    "The vehicle passes. A van with the facility logo on the side."

    "They're looking for us."

    elena "We need to keep going. Off-road."

    "She's bent double now, breathing through a contraction."

    protag "You're in labor."

    elena "I'm aware."

    "We keep moving. Through trees, over uneven ground."

    "Everything hurts."

    "But for the first time in a year, I'm making my own choices."

    scene bg black

    centered "..."

    centered "YOU WALK THROUGH THE NIGHT"

    centered "TWO VESSELS, REFUSING TO BE CONTAINED"

    centered "THE ROAD IS LONG"

    centered "YOUR BODY IS FAILING"

    centered "BUT YOU ARE FREE"

    centered "FOR NOW"

    jump c2_ending_free


label c2_caught:

    scene bg medical room

    "They find me in under two minutes."

    "Aria. Sophie. Two security staff I've never seen - both over six feet, thick-armed, with the quiet competence of people trained to handle things that try to escape."

    "I'm five-two in a muddy nightgown. My belly is caked with dirt. I look up at all four of them, and I am so, so small."

    "Aria's face is not warm anymore. Not honey-sweet."

    aria "Oh, Lily."

    "Disappointment. Like I'm a child who broke a vase."

    "They bring a wheelchair. Strap me in."

    "Back through the east corridor. Past the quiet wing."

    "Into a room I've never seen. White walls. A single bed with restraints."

    "They put me on the bed."

    marcus "This is very disappointing, Lily."

    "Dr. Marcus, in a bathrobe, dark circles under his eyes."

    marcus "We're going to need to adjust your care plan significantly."

    protag "Where's Elena?"

    marcus "Elena is none of your concern."

    "He nods to a nurse - tall, placid-faced, with strong hands and a beauty queen's jawline - who approaches with an IV."

    protag "No. No, don't-"

    aria "Shh, sweetheart. This is for the babies. You don't want to hurt the babies, do you?"

    "The needle slides in."

    "The fog comes. Heavy and absolute."

    "The last thing I hear is Aria's voice."

    aria "We'll take such good care of you, sweet girl. You don't need to worry about anything ever again."

    "And then..."

    "Nothing."

    scene bg black

    centered "..."

    centered "THE FOG TAKES YOU"

    centered "WHEN YOU WAKE, WEEKS HAVE PASSED"

    centered "YOU DON'T REMEMBER THE ESCAPE ATTEMPT"

    centered "YOU DON'T REMEMBER ELENA"

    centered "YOU DON'T REMEMBER KNOWING"

    centered "YOU ARE A VESSEL"

    centered "AND VESSELS DON'T NEED TO THINK"

    jump c2_ending_caught


label c2_morning_after:

    scene bg bedroom morning

    "Morning."

    "Aria is there. Smiling. But tighter than usual."

    aria "Good morning, sweetheart. Sleep well?"

    "I nod. My head feels like concrete."

    aria "We had a little excitement last night. One of the residents had a... wandering episode."

    protag "Elena?"

    "The name slips out before I can stop it."

    "Aria's smile doesn't waver."

    aria "Elena's being taken care of. You don't need to worry about her."

    "Being taken care of."

    protag "Is she okay?"

    aria "She's where she needs to be."

    "That's not an answer."

    scene bg gardens

    "During garden time, Elena's bench is empty."

    "It stays empty the next day. And the next."

    "I never see her again."

    scene bg black

    centered "ELENA IS GONE"

    centered "WHETHER SHE ESCAPED OR WAS TAKEN"

    centered "YOU NEVER LEARN"

    centered "AND THE PREGNANCY CONTINUES"

    centered "AS IT ALWAYS DOES"

    jump c2_ending_stayed


label c2_ending_free:

    scene bg dawn

    "Dawn breaks over the tree line."

    "Elena is leaning against a tree, breathing through contractions that are now minutes apart."

    "In the distance, I can see rooftops. A village."

    elena "Go. Find a phone. Call the police. Tell them everything."

    protag "I'm not leaving you."

    elena "You have to. I can't walk anymore."

    "She grips my hand."

    elena "I got out. That's enough. Now get help."

    "I look at the village. Half a mile, maybe."

    "I look at Elena, in labor under a tree."

    "I look at my own belly. The three lives inside me that I didn't choose."

    "But I chose this. I chose to run."

    "I chose."

    "I start walking toward the village."

    "My feet are bleeding. My nightgown is torn, barely covering my body - thin limbs, sharp bones, and this impossible belly leading the way. I'm covered in mud."

    "I'm five-foot-two. I weigh a hundred and thirty pounds, most of it babies. My legs are scratched and trembling. My arms are streaked with dirt."

    "I'm twenty weeks pregnant with triplets I didn't consent to carry."

    "And I'm free."

    scene bg black

    centered "CYCLE TWO — COMPLETE"

    centered "STATUS: ESCAPED"

    centered "But the facility still stands."
    centered "Other women still sleep in drugged silence."
    centered "And your body still carries their product."

    centered "The escape is not the end."
    centered "It's the beginning of a different kind of horror."

    centered "VESSEL will continue in Cycle Three..."

    return


label c2_ending_caught:

    scene bg bedroom morning

    "Weeks later. Months later. You don't know."

    "You're enormous again. The triplets growing on schedule. Your small body distorted beyond recognition, belly round and hard and massive, your thin arms resting on top of it because there's nowhere else for them to go."

    "Aria brushes your hair - her long, elegant fingers working through the tangles. Sophie brings your milk, bending her tall frame to hold the cup to your lips."

    "You drink it."

    "You don't remember why you wouldn't."

    aria "Such a good girl."

    "You smile."

    "You don't remember why you wouldn't."

    scene bg black

    centered "CYCLE TWO — COMPLETE"

    centered "STATUS: RECAPTURED"

    centered "The knowing is gone."
    centered "The fog has returned."
    centered "You are compliant."
    centered "You are cared for."
    centered "You are loved."
    centered "You are empty."

    centered "VESSEL will continue in Cycle Three..."

    return


label c2_ending_stayed:

    scene bg bedroom evening

    "Weeks pass. You grow larger."

    "The triplets move inside you. You've started talking to them."

    "Not because you love them. Not because you don't."

    "Because they're the only ones who are truly trapped with you."

    protag "We're going to get out of here. Not today. Not soon. But someday."

    "You don't know if that's true."

    "But Elena tried."

    "And next time, you'll be ready."

    scene bg black

    centered "CYCLE TWO — COMPLETE"

    centered "STATUS: ENDURING"

    centered "Elena showed you the gap in the wall."
    centered "Elena showed you that escape is possible."
    centered "Elena may have made it. You choose to believe she did."

    centered "Cycle Three will come."
    centered "You will be pregnant again."
    centered "But you will also be planning."

    centered "VESSEL will continue in Cycle Three..."

    return
