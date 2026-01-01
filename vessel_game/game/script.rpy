## Vessel - A Psychological Horror Simulator
## First Cycle

## Character Definitions
define protag = Character("Lily", color="#c8c8ff")
define aria = Character("Aria", color="#ffb6c1")
define sophie = Character("Sophie", color="#ffd4b8")
define marcus = Character("Dr. Marcus", color="#b8e6ff")
define vivian = Character("Vivian", color="#f0e68c")
define narrator = Character(None, kind=nvl)

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
    
    "Aria's voice is warm honey. Her fingers continue their gentle combing through my hair, untangling knots I got from tossing in my sleep."
    
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
    
    "But Aria's already pulling back the covers, revealing my massive belly under the soft nightgown. The quadruplets are active this morning - I can see movement rippling across my skin."
    
    aria "Oh! Look at them go! They're so lively today."
    
    "Her hand goes to my belly automatically. I used to flinch. Now I just... let it happen."
    
    scene bg bathroom
    
    "Sophie is testing the water temperature, her long dark hair pulled back in a neat bun. She looks up and smiles when we enter."
    
    sophie "Perfect timing! The water's just right."
    
    "Between the two of them, they help me out of my nightgown. I'm naked in front of them multiple times a day. You'd think I'd be used to it."
    
    "I'm not."
    
    $ dignity -= 5
    
    "They guide me to the enormous tub - custom-made to accommodate my size. The water is beautifully warm and smells like lavender."
    
    sophie "Easy does it, let us do the work..."
    
    "I have to. I literally cannot maneuver myself in and out of a bathtub anymore."
    
    "Once I'm settled, leaning back against the cushioned support, Sophie begins washing my hair while Aria soaps a soft cloth."
    
    protag "I can wash myself."
    
    "It comes out weaker than I intended."
    
    aria "Of course you could, sweetie. But what would you do if you dropped the soap? Your fingers are so puffy today."
    
    "She's right. My wedding ring - not that I'm married, it's just a ring I've worn since high school - had to be removed weeks ago. My hands look like inflated gloves."
    
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
    
    "A soft cotton dress in pale blue, custom-made to accommodate my belly. No bra - my breasts are too tender and swollen to tolerate one. Comfortable underwear. Compression socks that Aria rolls up my swollen calves."
    
    aria "There. You look lovely."
    
    "I catch my reflection in the mirror. I do look... cute. Pretty, even. Like a pregnant teenager."
    
    "I'm twenty-three. I was valedictorian. I ran track. I had a full scholarship."
    
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
    
    "The room is beautiful. Floor-to-ceiling windows overlook manicured gardens. Other residents are already eating, looking effortlessly elegant even at eight months pregnant."
    
    "I'm twenty-two weeks. I look more pregnant than any of them."
    
    vivian "Lily! Good morning!"
    
    "Vivian waves from her table. She's tall, blonde, radiantly pregnant with her second child. Her belly is perfectly round and proportional. She's wearing designer maternity activewear."
    
    "I'm in a muumuu."
    
    $ met_vivian = True
    
    protag "Morning."
    
    vivian "You look adorable today. That color is perfect on you."
    
    "Adorable. Not beautiful. Not elegant. Adorable."
    
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
            "She holds the fork to my lips, smiling encouragingly."
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
    
    vivian "Four! My god. And here I am complaining about one. You poor thing."
    
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
    
    "They're all moving independently. Bending, stretching, chatting."
    
    "Aria and Sophie guide me to a corner with approximately seventeen pillows already arranged."
    
    "The instructor, a serene woman named Luna, begins the class."
    
    luna "Good morning, mothers. Let's begin in a comfortable seated position..."
    
    "The other women sit cross-legged or in modified positions."
    
    "I'm on my side. Supported by pillows. Like a beached whale."
    
    luna "Now, let's move into cat-cow position..."
    
    "Everyone shifts to hands and knees, arching and rounding their backs."
    
    "I can't get on my hands and knees. The weight of my belly makes it impossible."
    
    luna "Lily, honey, just keep breathing. You're doing exactly what your body needs."
    
    "Which is... lying here. Watching everyone else do yoga while I breathe."
    
    $ dignity -= 15
    
    "One of the women, a elegant brunette about seven months along, catches my eye and gives me a sympathetic smile."
    
    woman "You're doing great! Just being here is wonderful."
    
    "I want to scream."
    
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
    
    "Getting me into a swimsuit required both Aria and Sophie, and took fifteen minutes."
    
    "Getting me into the pool requires a motorized lift."
    
    "I'm strapped into a chair that slowly lowers me into the water while the other women are already swimming laps or doing aquatic exercises."
    
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
    
    "Of course, I'm not in a chair. I'm on an examination table, already in a gown, with Aria and Sophie flanking me."
    
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
    
    "That evening, Aria helps me into bed. Sophie is preparing a 'special treat' - warm milk with honey."
    
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
    
    "I wake in my room. My belly is smaller but still swollen. My breasts are engorged and leaking."
    
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
    
    "I try to sit up. I can't. I'm too weak from the birth. Too nauseous. Too..."
    
    aria "Lily, sweetheart. Where would you go? You signed a contract. Five cycles. This is only your second."
    
    protag "Five... no. No, I never-"
    
    sophie "Shh, shh. It's okay. You're just hormonal. This is all very normal. You're safe here. Cared for."
    
    aria "Loved."
    
    "She strokes my hair as I start to cry."
    
    aria "You're special, Lily. So perfect for this. Your body makes such healthy babies."
    
    protag "You're keeping me pregnant. You're... you're using me..."
    
    aria "We're caring for you. Giving you purpose. You've never been so important, have you? So needed?"
    
    "And god help me, part of me..."
    
    "Part of me..."
    
    sophie "Let's get you washed up. You'll feel better after breakfast."
    
    "They lift me from the bed. I'm boneless. Helpless."
    
    "Pregnant again."
    
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
        "Begin Cycle Two (Coming Soon)":
            "Cycle Two is not yet implemented. Thank you for playing Cycle One."
            return
            
        "Return to Start":
            jump start
