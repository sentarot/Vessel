## Vessel - A Psychological Horror Simulator
## First Cycle

## Character Definitions
define protag = Character("Lily", color="#c8c8ff")
define aria = Character("Aria", color="#ffb6c1")
define sophie = Character("Sophie", color="#ffd4b8")
define marcus = Character("Dr. Marcus", color="#b8e6ff")
define vivian = Character("Vivian", color="#f0e68c")
define narrator = Character(None)
define luna = Character("Luna", color="#d4a6e8")
define unknown = Character("???", color="#999999")

## Game Variables
default day = 1
default trimester = 2  # Starting in second trimester when awareness returns
default weeks_pregnant = 18
default fatigue = 75  # Out of 100
default dignity = 60  # Out of 100
default resistance = 80  # Willingness to push back

## Physical Status Tracking
default status_feet = "Severely swollen, can't wear shoes"
default status_back = "Constant lordosis pain"
default status_hands = "Puffy, reduced grip strength"
default status_abdomen = "Massively distended - quadruplets"
default status_mobility = "Waddling gait, requires assistance"

## Inventory
default player_inventory = []
default caretaker_tote = ["Incontinence pads", "Antacids", "Pregnancy journal", "Snacks", "Water bottle", "Nipple cream", "Belly oil"]

## Story Flags
default knows_truth = False
default first_pool = False
default first_yoga = False
default met_vivian = False

## Opening
label start:
    
    scene bg bedroom morning
    
    "I wake to the sensation of hands in my hair."
    
    "It's become so routine I don't even startle anymore. Just... accept it."
    
    aria "Good morning, sweetheart. Did we sleep well?"
    
    "Aria's voice is warm honey. Her fingers - long, elegant, manicured in soft pink - continue their gentle combing through my hair, untangling knots I got from tossing in my sleep."

    "She's sitting on the edge of my bed, and even seated she seems to tower over me. Aria is nearly six feet tall, with the kind of body that makes maternity dresses look like evening gowns on everyone else. Full hips, a narrow waist, broad shoulders. Her auburn hair falls in glossy waves past her collarbone. She smells like jasmine and something expensive."

    "I'm five-foot-two. I weigh ninety-eight pounds when I'm not... like this. My wrists are the size of her thumbs. People have been carding me since I was twelve - not because I look older, but because they can't believe I'm as old as I am. At twenty-three, I still get asked if I need a parent's signature."

    "Or trying to toss. At this size, 'tossing' means rocking slightly and hoping."
    
    menu:
        "How do I respond?"
        
        "I slept fine.":
            $ dignity += 5
            protag "I slept okay."
            aria "That's wonderful! Your color looks much better today."
            
        "I'd sleep better without someone watching me.":
            $ resistance += 5
            $ dignity -= 5
            protag "I'd probably sleep better if I had some privacy."
            aria "Oh sweetie, you know we can't risk you trying to get up alone. What if you fell?"
            "She says it so gently, so reasonably. Like I'm being silly."
    
    aria "Let's get you freshened up! Sophie's drawing your bath now."
    
    "I don't remember agreeing to a bath."
    
    "But Aria's already pulling back the covers with one hand - effortless, like unwrapping a gift. My massive belly rises from the mattress like a hill under the soft nightgown. The fabric is stretched so thin across my abdomen I can see my navel poking through. The quadruplets are active this morning - I can see movement rippling across my taut, veiny skin."

    "My legs look wrong next to my belly. Thin, pale, the muscles wasted from months of limited movement. The belly doesn't look like it belongs to the body underneath it."
    
    aria "Oh! Look at them go! They're so lively today."
    
    "Her hand goes to my belly automatically. I used to flinch. Now I just... let it happen."
    
    scene bg bathroom
    
    "Sophie is testing the water temperature. She looks up and smiles when we enter - all cheekbones and full lips, her long dark hair pulled back in a neat bun that shows off her neck. She's almost as tall as Aria, five-ten at least, with the kind of curves that make scrubs look like athleisure. Her arms are toned and tan. She could pick me up like a child."

    "She has picked me up like a child."

    sophie "Perfect timing! The water's just right."

    "Between the two of them, they help me out of my nightgown. Two gorgeous Amazons undressing a pregnant pixie. I come up to their chests. My bare belly juts out almost comically between their long, capable bodies."

    sophie "She's so tiny. Every time I see her without the gown I forget how little she is."

    "Sophie says it to Aria like I'm not here. Or like I can't understand."

    aria "I know. She looks about fifteen, doesn't she? My niece is bigger than her."

    "I'm twenty-three. I have a degree. But naked and pregnant between these two women, I look like their underage charge."

    "I'm naked in front of them multiple times a day. You'd think I'd be used to it."

    "I'm not."
    
    $ dignity -= 5
    
    "They guide me to the enormous tub - custom-made to accommodate my size. The water is beautifully warm and smells like lavender."
    
    sophie "Easy does it, let us do the work..."
    
    "I have to. I literally cannot maneuver myself in and out of a bathtub anymore."
    
    "Once I'm settled, leaning back against the cushioned support, Sophie begins washing my hair while Aria soaps a soft cloth."
    
    protag "I can wash myself."
    
    "It comes out weaker than I intended."
    
    aria "Of course you could, sweetie. But what would you do if you dropped the soap? Your fingers are so puffy today."
    
    "She's right. My wedding ring - not that I'm married, it's just a ring I've worn since high school - had to be removed weeks ago. My hands look like inflated gloves. Tiny inflated gloves. My fingers were slender before all this - pianist's fingers, my mom used to say. Now they're swollen sausages on doll-sized palms."

    "Aria's hands, by contrast, are strong and sure, with long fingers that wrap completely around my forearm when she steadies me."
    
    menu:
        "What do I do?"
        
        "Insist on trying":
            $ resistance += 5
            $ fatigue += 10
            protag "I still want to try."
            aria "Alright, sweet girl. Here you go."
            "She hands me the cloth. I manage maybe three strokes across my arm before my grip fails and it plops into the water."
            sophie "It's okay, honey. We've got you."
            "The humiliation burns, but they're already back to washing me, cooing gentle reassurances."
            $ dignity -= 10
            
        "Give in":
            $ dignity -= 5
            $ fatigue -= 5
            "I don't say anything. Just let them wash me like a child."
            "It's easier this way. I'm so tired."
    
    "The bath continues in relative silence, punctuated by their gentle observations about my skin, my belly, how well I'm carrying."
    
    "Like I'm livestock. Prize livestock, sure. But still."
    
    scene bg bedroom morning
    
    "After the bath, they dress me. This takes twenty minutes."

    "A soft cotton dress in pale blue, custom-made to accommodate my belly. It's essentially a tent with a Peter Pan collar. No bra - my breasts are too tender and swollen to tolerate one, heavy and sore against the thin fabric. Comfortable underwear that Sophie slides up my legs while I grip Aria's shoulders for balance. Compression socks that Aria rolls up my swollen calves - her hands spanning nearly the full circumference of my leg."

    aria "There. You look lovely."

    "I catch my reflection in the mirror. Between them, in the glass, I look like their daughter. Their teenage daughter who got in trouble."

    "My face is the problem. Heart-shaped, with big dark eyes, long lashes, a small upturned nose, a dusting of freckles across the bridge. Rosebud mouth. I look fourteen. I've always looked absurdly young - got pulled aside at my own college graduation because security thought a high schooler had wandered in."

    "Now the baby face isn't just embarrassing. It's a weapon they use against me. Framed by my thin neck and narrow shoulders, above this enormous pregnant belly, I look like a child carrying a child. The kind of face you pity, not respect. The kind of face that makes people say 'oh, honey' before you've opened your mouth."

    "Aria and Sophie flank me like a matching set of runway models in pastel medical scrubs. They glow. They radiate health and beauty and competence. Next to them, I am small and round and helpless. Their bodies say 'adult.' Mine says 'please take care of me.'"

    "I'm twenty-three. I was valedictorian. I ran track. I had a full scholarship. I was a hundred and two pounds of fast-twitch muscle. I could have done anything."

    "Now I can't even put on my own socks."
    
    menu:
        "Check Status Screen":
            call screen status_screen
            
        "Check Inventory":
            call screen inventory_screen
            
        "Continue":
            pass
    
    scene bg dining room
    
    "Breakfast is in the sunroom. Aria wheels me there in the cushioned transport chair - too far for me to walk, apparently."
    
    "The room is beautiful. Floor-to-ceiling windows overlook manicured gardens. Other residents are already eating, attended by their own caretakers - all of them tall, all of them stunning. It's like a sorority house for supermodels who happen to work in maternal care."

    "The residents themselves are mostly tall too. Healthy, glowing, elegantly pregnant. Women whose bodies accommodate pregnancy like it's an accessory."

    "I'm twenty-two weeks. I look more pregnant than any of them. My belly rests on my thighs when I sit. I can feel it pulling on my spine, stretching the skin over my tiny ribcage."

    vivian "Lily! Good morning!"

    "Vivian waves from her table. She's six feet tall in bare feet, blonde, radiantly pregnant with her second child - long golden legs crossed at the ankle, pregnancy sitting high and tight on her athletic frame like a volleyball under a designer top. Her belly is perfectly round and proportional. She's wearing maternity activewear that costs more than my scholarship stipend."

    "I'm in a muumuu. My belly hangs low and wide. I look like I'm smuggling a bean bag chair."
    
    $ met_vivian = True
    
    protag "Morning."
    
    vivian "You look adorable today. That color is perfect on you. Honestly, you look about sixteen in that dress."

    "She laughs like it's a compliment."

    "Adorable. Sixteen. Not beautiful. Not elegant. Not an adult woman with a master's-level education."
    
    "Aria settles me at a table and immediately begins preparing my plate from the breakfast buffet. I didn't get to choose."
    
    aria "Lots of protein for our growing babies. And some fresh fruit. You need the fiber."
    
    "She returns with a plate piled high - scrambled eggs, turkey sausage, Greek yogurt with berries, whole grain toast."
    
    "Then she picks up the fork."
    
    menu:
        "How do I react?"
        
        "Object to being fed":
            $ resistance += 5
            protag "I can feed myself, Aria."
            aria "I know you think that, sweetheart, but remember what happened yesterday? You got so shaky by mid-meal."
            "Did I? I... don't remember clearly. The mornings blur together."
            aria "Let's not risk it. Open up."
            "She holds the fork to my lips with those long, graceful fingers, smiling down at me encouragingly. She has to lean down to reach my mouth. I feel like a baby bird."
            $ dignity -= 10
            
        "Accept it":
            $ dignity -= 5
            "I open my mouth. She feeds me like a toddler, making approving sounds after each bite."
            "It's humiliating. But I am shakier than I used to be. Maybe she's right."
    
    "Vivian watches from her table with an amused smile."
    
    vivian "Your girls are SO devoted. I keep telling my assistant I want that level of care!"
    
    "There's something in her tone. Not quite mockery, but... awareness. Like she knows exactly how this looks."
    
    protag "They're very... attentive."
    
    vivian "I'll say! Though honestly, at your size, you need it. How many are you carrying again?"
    
    protag "Four."
    
    vivian "Four! My god. And here I am complaining about one. You poor thing. How old are you, anyway?"

    protag "Twenty-three."

    vivian "No! Truly? I would have guessed... well. You wear it well."

    "She would have guessed seventeen. Maybe younger. Everyone does."

    "Poor thing."
    
    "The meal continues. Aria feeds me every bite, wipes my mouth with a napkin, gives me water through a straw."
    
    $ fatigue += 10
    
    scene bg hallway
    
    "After breakfast, Aria checks the schedule."
    
    aria "You have prenatal yoga at ten, then pool therapy at noon. This afternoon is your appointment with Dr. Marcus, and then shopping if you're feeling up to it!"
    
    menu:
        "How do I feel about today's schedule?"
        
        "That sounds exhausting":
            protag "That's a lot. Can I skip anything?"
            sophie "Oh honey, these activities are all part of your wellness plan. We can't skip them."
            aria "But we'll make sure you rest between each one! We take such good care of you."
            $ resistance -= 5
            
        "Okay":
            protag "Okay."
            $ fatigue += 5
            "What else can I say? They'll do what they think is best anyway."
    
    jump prenatal_yoga


label prenatal_yoga:
    
    scene bg yoga studio
    
    "The yoga studio is all natural light and bamboo floors. About eight other pregnant women are already setting up their mats."

    "They're all moving independently. Bending, stretching, chatting. Most of them are taller than me even when I'm standing. Sitting on the floor, I'd come up to their hip bones."

    "Aria and Sophie guide me to a corner with approximately seventeen pillows already arranged. Aria has to crouch to settle me down, her long legs folding gracefully, her hands spanning the width of my back as she eases me onto the mat."

    "The instructor, Luna, begins the class. She's impossibly willowy - nearly six feet of lean muscle in a sports bra and leggings, her dark skin luminous, her braids swept up in a crown. Her belly is flat. Her body does exactly what she tells it to."
    
    luna "Good morning, mothers. Let's begin in a comfortable seated position..."
    
    "The other women sit cross-legged or in modified positions."
    
    "I'm on my side. Supported by pillows. Like a beached whale."
    
    luna "Now, let's move into cat-cow position..."
    
    "Everyone shifts to hands and knees, arching and rounding their backs."
    
    "I can't get on my hands and knees. My belly hangs to the floor when I try. My stick-thin arms tremble under the redistributed weight. It's impossible."
    
    luna "Lily, honey, just keep breathing. You're doing exactly what your body needs."

    "She kneels beside me and pushes a strand of hair from my face. The gesture is tender and automatic - the way you'd comfort a child."

    luna "You're so brave, little one."

    "Little one. I'm two years older than her."

    "Which is... lying here. Watching everyone else do yoga while I breathe."
    
    $ dignity -= 15
    
    "One of the women - a statuesque brunette about seven months along, five-nine, all legs, her single pregnancy barely disrupting the line of her body - catches my eye from a perfect warrior pose and gives me a sympathetic smile."

    woman "You're doing great! Just being here is wonderful."

    "I want to scream. She's balancing on one leg. I can't balance on two."
    
    "The class continues. They move through poses - warrior, tree, gentle twists. I lie on my side and occasionally shift positions with Sophie's help."
    
    "This is 'prenatal yoga' for me. Pillow-assisted existing."
    
    $ fatigue += 15
    $ first_yoga = True
    
    aria "You did so well, sweetheart! I'm so proud of you."
    
    "For what? Lying there?"
    
    jump pool_therapy


label pool_therapy:
    
    scene bg pool area
    
    "The pool is gorgeous - heated, with underwater lights and comfortable loungers around the edges."
    
    "Getting me into a swimsuit required both Aria and Sophie, and took fifteen minutes. The suit is a custom one-piece in black with a massive ruched panel across the front. It still can't contain my belly, which spills over the elastic at the bottom."

    "Aria and Sophie changed into swimsuits too. Of course they did. Aria in a red one-piece that hugs every curve of her tall, full figure - wide hips, cinched waist, shoulders like a swimmer. Sophie in navy, her long athletic body tanned and toned. They look like lifeguards. I look like their rescue."

    "Getting me into the pool requires a motorized lift."

    "I'm strapped into a chair that slowly lowers me into the water while the other women - tall, beautiful, carrying their pregnancies like fashion statements - are already swimming laps or doing aquatic exercises."
    
    $ dignity -= 20
    
    "But once I'm in... oh."
    
    "The water supports my weight. For the first time in months, I don't feel like I'm carrying four bowling balls in my abdomen."
    
    "I can float. I can move. Sort of."
    
    $ fatigue -= 20
    
    protag "This actually feels amazing."
    
    sophie "See? We know what you need!"
    
    "She's in the water with me, keeping a hand near my arm 'just in case.'"
    
    "The pool instructor leads us through gentle movements. I can actually participate in some of them."
    
    "For half an hour, I feel almost human again."
    
    "Then it's time to get out, and I need the lift again, and I'm reminded of reality."
    
    $ first_pool = True
    
    scene bg bedroom afternoon
    
    "They dry me off, dress me in fresh clothes, settle me on the bed for a 'rest' before my doctor's appointment."
    
    "I didn't realize how tired I was. I fall asleep within minutes."
    
    "..."
    
    "I wake to voices. Quiet conversation near my door."
    
    aria "She's progressing beautifully. All four are measuring large, just as hoped."
    
    unknown "And she's been compliant?"
    
    sophie "Frustrated sometimes, but physically she has no choice. The size of the pregnancy ensures that."
    
    unknown "Good. Dr. Marcus will want to confirm the measurements this afternoon. If they're on track, we can begin preparing for the next cycle."
    
    aria "So soon after birth?"
    
    unknown "The hormones will make her more malleable. And she'll be in the first trimester fog before she can fully process what's happening."
    
    "My blood runs cold."
    
    "Next... cycle?"
    
    "Before I can process this, Aria sweeps back into the room."
    
    aria "Oh good, you're awake! Dr. Marcus is ready for you."
    
    menu:
        "What do I do?"
        
        "Confront her about what I heard":
            $ resistance += 10
            protag "What did you mean 'next cycle'?"
            aria "Hmm? Oh sweetie, you must have been dreaming. We were just discussing your yoga progress."
            "She says it so smoothly. So convincingly."
            "Was I dreaming?"
            $ dignity -= 10
            
        "Say nothing":
            $ resistance -= 5
            "I... maybe I misheard. I'm so foggy lately."
            "Pregnancy brain. That's all."
    
    jump doctor_appointment


label doctor_appointment:
    
    scene bg medical office
    
    "Dr. Marcus's office is less clinical than I expected. Soft lighting, comfortable chairs, abstract art on the walls."

    "Of course, I'm not in a chair. I'm on an examination table, already in a paper gown that barely closes around my belly, my skinny legs dangling off the edge like a child's. Aria and Sophie stand flanking me - tall, gorgeous sentinels in their matching scrubs."

    "Dr. Marcus is a big man. Broad, silver-haired, with thick hands that look like they could palm my entire belly. His smile is practiced and warm. He looks at me the way pediatricians look at their patients - gentle, faintly amused, certain that he knows better."

    "The first time we met, he asked Aria where the patient's mother was. He was looking right at me."

    marcus "How are we feeling today, Lily?"
    
    protag "Tired. Sore. The usual."
    
    marcus "That's perfectly normal at your stage with quadruplets. Let's take a look."
    
    "He performs the ultrasound. I can see the four babies on the screen, moving and growing inside me."
    
    "They look healthy. Perfect, even."
    
    "I should feel joy. Maternal warmth. Something."
    
    "Instead, I feel..."
    
    "I don't know what I feel."
    
    marcus "Excellent. All four are measuring in the 95th percentile. This is exactly what we hoped for."
    
    "Hoped for? That's an odd way to put it."
    
    marcus "Your cervix is holding beautifully. I think we can safely plan for another twelve weeks."
    
    protag "Twelve weeks? I thought quadruplets usually come earlier-"
    
    marcus "Every pregnancy is different. Your body is doing wonderfully. We'll keep you on bedrest, of course, to maximize the growth period."
    
    "Bedrest? He never mentioned bedrest before."
    
    menu:
        "How do I respond?"
        
        "Question the bedrest order":
            $ resistance += 10
            protag "Bedrest? I can barely move as it is. Won't that make me weaker?"
            marcus "Your job right now is to grow healthy babies, Lily. Movement can wait."
            "He pats my knee. The way you'd pat a kid who asked a silly question."
            aria "We'll take such good care of you, sweetie. You won't have to worry about anything."
            
        "Accept it":
            $ resistance -= 10
            $ dignity -= 10
            protag "Okay."
            "What choice do I have?"
    
    marcus "Excellent. I'll see you next week. Keep up the good work."
    
    "Keep up the good work. Like I'm an employee."
    
    "Like I'm a... a..."
    
    scene bg bedroom evening
    
    "That evening, Aria lifts my legs into bed one at a time - her hands encircling my calves completely, her arms steady and unhurried. Sophie is preparing a 'special treat' - warm milk with honey."
    
    "I don't like warm milk. I've told them this."
    
    "They bring it anyway. 'It helps you sleep, sweetheart.'"
    
    "As I lie there, too exhausted to even read, I think about what I overheard."
    
    "Next cycle."
    
    "Begin preparing."
    
    "More malleable."
    
    "But that's crazy. I must have misunderstood."
    
    "This is a luxury wellness facility. These women care about me."
    
    "Don't they?"
    
    aria "Drink up, sweet girl. You need your rest."
    
    "She holds the cup to my lips. I drink."
    
    "The milk is warm and sweet and makes me drowsy almost immediately."
    
    "As I drift off, I feel her hand stroking my hair, her voice humming softly."
    
    aria "Such a good girl. Such a perfect vessel."
    
    "Vessel."
    
    "The word follows me into sleep."
    
    "..."
    
    scene bg black
    
    centered "DAYS PASS"
    
    centered "WEEKS PASS"
    
    centered "THE PREGNANCY PROGRESSES"
    
    centered "YOU GROW LARGER"
    
    centered "MORE DEPENDENT"
    
    centered "MORE CONFUSED"
    
    centered "UNTIL..."
    
    jump birth_sequence


label birth_sequence:
    
    scene bg medical room
    
    "Labor is a blur of pain and hands and voices telling me to push, push, good girl, you're doing so well."
    
    "I deliver four healthy babies. Two boys, two girls."
    
    "They're beautiful."
    
    "I hold each one for exactly thirty seconds before they're whisked away 'for evaluation.'"
    
    protag "When can I see them again?"
    
    marcus "Soon, Lily. You need to rest now. You've done wonderfully."
    
    "They give me something for the pain. Something that makes everything soft and distant."
    
    "..."
    
    scene bg bedroom morning
    
    "I wake in my room. My belly is smaller but still swollen, the skin loose and stretched where it was once drum-tight. My breasts are engorged and leaking, heavy and hot, enormous on my small frame. My body feels like a deflated balloon - something used and emptied."

    "There are no babies."
    
    protag "Where are my babies?"
    
    aria "They're in the nursery, sweetheart. Being cared for by our expert staff."
    
    protag "I want to see them."
    
    aria "Of course! Once you're recovered. Dr. Marcus says you need at least a week of rest first."
    
    "A week?"
    
    "That's not... that's not normal..."
    
    "But I'm so tired. And foggy. And my body hurts."
    
    "..."
    
    scene bg black
    
    centered "ONE WEEK LATER"
    
    scene bg bedroom morning
    
    "I wake to familiar sensations."
    
    "Hands in my hair."
    
    "Aria's voice."
    
    "And something else."
    
    "Nausea. Deep, bone-deep exhaustion. A strange tightness in my abdomen."
    
    aria "Good morning, mama. How are we feeling?"
    
    protag "Awful. I think I'm sick. And I want to see my babies. You keep saying later and-"
    
    aria "Oh sweetheart. You're not sick."
    
    "She places a hand on my belly. It's still rounded. Swollen from birth, I assumed."
    
    aria "You're pregnant again. Isn't that wonderful?"
    
    "The world stops."
    
    protag "What?"
    
    aria "The IVF took beautifully. Dr. Marcus transferred the embryos while you were recovering. You're already six weeks along."
    
    "Six weeks."
    
    "That means..."
    
    "That means..."
    
    protag "You... you got me pregnant again without my consent?"
    
    sophie "Oh honey, you signed the consent forms. Don't you remember?"
    
    "I don't. I don't remember."
    
    "The foggy week. The medications. The..."
    
    protag "My babies. Where are my babies?"
    
    aria "They've been placed with their families, sweetie. Loving homes. You helped create such beautiful children."
    
    "Their families."
    
    "Not... not mine."
    
    protag "I want to leave. I want to leave right now."
    
    "I try to sit up. I can't. I'm ninety pounds of nothing, too weak from the birth, too nauseous, too..."
    
    aria "Lily, sweetheart. Where would you go? You signed a contract. Five cycles. This is only your second."
    
    protag "Five... no. No, I never-"
    
    sophie "Shh, shh. It's okay. You're just hormonal. This is all very normal. You're safe here. Cared for."
    
    aria "Loved."
    
    "She strokes my hair as I start to cry."
    
    aria "You're special, Lily. So perfect for this. That little body of yours makes such healthy babies. And you'll still look twenty when you're forty - won't that be nice?"
    
    protag "You're keeping me pregnant. You're... you're using me..."
    
    aria "We're caring for you. Giving you purpose. You've never been so important, have you? So needed?"
    
    "And god help me, part of me..."
    
    "Part of me..."
    
    sophie "Let's get you washed up. You'll feel better after breakfast."
    
    "They lift me from the bed. Sophie scoops me up like I weigh nothing - and I almost don't. One arm under my knees, one behind my back. I'm cradled against her chest, my head barely reaching her shoulder, my swelling belly pressed between us."

    "I'm boneless. Helpless. A small, pretty, pregnant doll that everyone mistakes for a child."

    "For the second time of five."

    "And I can't even stand on my own."
    
    scene bg black
    
    centered "CYCLE ONE COMPLETE"
    
    centered "YOU NOW UNDERSTAND THE TRUTH"
    
    centered "BUT UNDERSTANDING DOESN'T MEAN ESCAPE"
    
    centered "YOUR BODY IS THEIR VESSEL"
    
    centered "YOUR COMPLIANCE IS ENSURED BY YOUR OWN BIOLOGY"
    
    centered "WELCOME TO CYCLE TWO"
    
    menu:
        "Begin Cycle Two":
            jump cycle_two_start

        "Return to Start":
            jump start
