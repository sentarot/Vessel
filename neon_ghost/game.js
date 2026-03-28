/**
 * NEON GHOST - Cyberpunk Life Simulator
 * Main Game Engine
 */

class NeonGhost {
    constructor() {
        // Player state
        this.player = {
            name: 'GHOST_NULL',
            health: 100,
            maxHealth: 100,
            energy: 100,
            maxEnergy: 100,
            stress: 15,
            chrome: 23, // Cyberware percentage
            money: 2450,
            streetCred: 127,

            // Skills
            skills: {
                netrunning: 15,
                combat: 10,
                tech: 20,
                stealth: 12,
                social: 8
            },

            // Inventory
            inventory: [
                { id: 'credchip', name: 'Credchip', icon: '💳', desc: 'Encrypted currency storage' },
                { id: 'stimpack', name: 'Stim Pack', icon: '💉', desc: 'Restores 30 energy', quantity: 3 },
                { id: 'neural_booster', name: 'Neural Booster', icon: '🧠', desc: '+10 Netrunning for 1 hour' }
            ],

            // Augmentations
            augments: [
                { id: 'neural_link', name: 'Zetatech Neural Link', icon: '🔌', desc: 'Basic brain-computer interface', slot: 'neural', stats: '+5 Netrunning' },
                { id: 'optic_shunt', name: 'Kiroshi Optics Mk.1', icon: '👁', desc: 'Enhanced vision with HUD overlay', slot: 'eyes', stats: '+3 Perception' },
                { id: 'subdermal_armor', name: 'Subdermal Weave', icon: '🛡', desc: 'Lightweight armor beneath skin', slot: 'skin', stats: '+10 Max Health' }
            ],

            // Contacts
            contacts: [
                { id: 'dex', name: 'Dexter DeShawn', role: 'FIXER', avatar: 'D', trust: 35, desc: 'Big-time fixer. Always has work.' },
                { id: 'vik', name: 'Viktor Vektor', role: 'RIPPERDOC', avatar: 'V', trust: 60, desc: 'Chrome installer. Fair prices.' },
                { id: 'mox', name: 'Moxie', role: 'NETRUNNER', avatar: 'M', trust: 45, desc: 'Elite hacker. Paranoid but skilled.' },
                { id: 'jackie', name: 'Jackie Welles', role: 'MERC', avatar: 'J', trust: 80, desc: 'Best friend. Loyal to a fault.' }
            ]
        };

        // Time system
        this.time = {
            hour: 22,
            minute: 47,
            day: 15,
            month: 3,
            year: 2087
        };

        // Location system
        this.locations = {
            apartment: { name: 'Megabuilding H10 // Apt 1242', sector: 'WATSON', danger: 0 },
            downtown: { name: 'Downtown // Neon District', sector: 'CITY CENTER', danger: 2 },
            kabuki: { name: 'Kabuki Market', sector: 'WATSON', danger: 3 },
            afterlife: { name: 'The Afterlife', sector: 'WATSON', danger: 1 },
            badlands: { name: 'Badlands // Nomad Camp', sector: 'OUTSKIRTS', danger: 5 },
            corpo_plaza: { name: 'Corpo Plaza', sector: 'CITY CENTER', danger: 2 },
            pacifica: { name: 'Pacifica // Combat Zone', sector: 'PACIFICA', danger: 8 }
        };
        this.currentLocation = 'apartment';

        // Jobs available
        this.jobs = [
            {
                id: 'data_heist',
                title: 'Data Heist',
                fixer: 'Dexter DeShawn',
                pay: 5000,
                desc: 'Infiltrate Arasaka subsidiary. Extract research data. No casualties preferred.',
                tags: ['STEALTH', 'NETRUNNING'],
                danger: 'HIGH',
                requirements: { netrunning: 20 }
            },
            {
                id: 'package_delivery',
                title: 'Special Delivery',
                fixer: 'Street Contact',
                pay: 800,
                desc: 'Deliver package to Kabuki. No questions asked.',
                tags: ['COURIER'],
                danger: 'LOW',
                requirements: {}
            },
            {
                id: 'bounty_hunt',
                title: 'Bounty: Chrome Ripper',
                fixer: 'NCPD',
                pay: 3500,
                desc: 'Target: Marcus "Chrome" Webb. Wanted for illegal augment harvesting.',
                tags: ['COMBAT', 'INVESTIGATION'],
                danger: 'MEDIUM',
                requirements: { combat: 15 }
            },
            {
                id: 'netwatch_trace',
                title: 'Ghost Hunt',
                fixer: 'Moxie',
                pay: 7500,
                desc: 'NetWatch is tracking someone. Find out who before they do.',
                tags: ['NETRUNNING', 'STEALTH'],
                danger: 'EXTREME',
                requirements: { netrunning: 30 }
            }
        ];

        // Narrative state
        this.narrative = {
            currentScene: 'intro',
            flags: {},
            history: []
        };

        // Game scenes / events
        this.scenes = this.initScenes();

        // UI state
        this.ui = {
            currentPanel: null,
            typingSpeed: 30,
            isTyping: false
        };
    }

    // Initialize all narrative scenes
    initScenes() {
        return {
            intro: {
                location: 'apartment',
                text: `You jack out of the local net, neural link buzzing with residual static. Another night in <span class="location">Night City</span>. The neon glow from the window paints your cramped apartment in shifting colors—pink, blue, purple.

Your agent chirps. Message from <span class="npc-name">Dexter DeShawn</span>. The big fixer's been sniffing around, heard about your skills. Could be an opportunity. Could be a bullet.

In this city, they're often the same thing.`,
                choices: [
                    { text: 'Check the message from Dex', next: 'dex_message', effects: {} },
                    { text: 'Ignore it and get some sleep', next: 'sleep_scene', effects: { energy: 30, time: 6 } },
                    { text: 'Hit the streets—need to clear your head', next: 'street_walk', effects: { stress: -10, time: 2 } },
                    { text: 'Jack into the Net for some quick eddies', next: 'netrun_intro', effects: {}, requirements: { netrunning: 10 } }
                ]
            },

            dex_message: {
                location: 'apartment',
                text: `The holo flickers to life. Dex's face fills the frame—gold teeth, knowing smile, danger in every pixel.

<span class="npc-name">"Ghost. Word on the wire says you're good with code. Real good. Got a client needs something extracted from an Arasaka subnet. Pay's fifteen large. Interested?"</span>

Fifteen thousand eddies. That's three months rent. Or a decent neural upgrade. Or a ticket out of this hellhole.

But Arasaka doesn't play nice. Their ICE has flatlined better runners than you.`,
                choices: [
                    { text: '"I\'m in. Send the details."', next: 'accept_job', effects: { streetCred: 10 } },
                    { text: '"Fifteen\'s light for Arasaka work. Twenty or I walk."', next: 'negotiate_pay', effects: {}, requirements: { social: 15 } },
                    { text: '"Need to think about it. I\'ll call you."', next: 'delay_decision', effects: { stress: 5 } },
                    { text: '"Not touching corpo jobs. Too hot."', next: 'refuse_job', effects: { streetCred: -5 } }
                ]
            },

            accept_job: {
                location: 'apartment',
                text: `Dex's smile widens. Gold teeth catch the neon.

<span class="npc-name">"Smart choice, Ghost. I'll send the details to your link. You got 48 hours to prep. After that, the window closes and my client finds someone else."</span>

The holo cuts. A data package arrives—building schematics, guard rotations, subnet architecture. This is real. Professional.

Your heart hammers against your ribs. This is the big leagues now.

<span class="highlight">+10 Street Cred</span>
<span class="item">New Job: Data Heist</span>`,
                choices: [
                    { text: 'Study the schematics', next: 'study_job', effects: { time: 3, energy: -15 } },
                    { text: 'Call Viktor—need new chrome for this', next: 'visit_vik', effects: {} },
                    { text: 'Contact Moxie for netrunning intel', next: 'contact_moxie', effects: {}, requirements: { netrunning: 15 } },
                    { text: 'Get some rest first', next: 'sleep_scene', effects: { energy: 30, time: 6 } }
                ],
                onEnter: (game) => {
                    game.narrative.flags.accepted_dex_job = true;
                }
            },

            negotiate_pay: {
                location: 'apartment',
                text: `You lean back, keeping your voice flat.

"Fifteen's light for corpo work, Dex. Their black ICE alone is worth hazard pay. Twenty thousand, plus expenses. Or find another ghost."

A pause. Dex's eyes narrow—calculating. Then that gold-tooth grin returns.

<span class="npc-name">"Got some steel in you after all. Alright, twenty it is. But you flatline, I keep the advance. Those are my terms."</span>

Better money. Higher stakes. Same city.

<span class="highlight">+15 Street Cred</span>
<span class="item">Job Pay: €$20,000</span>`,
                choices: [
                    { text: '"Deal. Send the details."', next: 'accept_job', effects: { streetCred: 15, money: 5000 } },
                    { text: '"Let me think on it."', next: 'delay_decision', effects: {} }
                ]
            },

            delay_decision: {
                location: 'apartment',
                text: `"I'll be in touch."

The holo cuts before Dex can respond. You stare at the ceiling, brain churning through scenarios. Risk versus reward. The eternal Night City calculation.

Outside, a police AV screams past, spotlight sweeping the megabuilding's facade. Someone else's problem. For now.

Your stomach growls. When did you last eat? The fridge hums in the corner—probably empty. Just like your account if you don't find work soon.`,
                choices: [
                    { text: 'Call Dex back—take the job', next: 'accept_job', effects: {} },
                    { text: 'Head to the Afterlife for other work', next: 'afterlife_scene', effects: { time: 1 } },
                    { text: 'Check the local net for smaller gigs', next: 'small_gigs', effects: { time: 1 } },
                    { text: 'Sleep on it', next: 'sleep_scene', effects: { energy: 30, time: 6 } }
                ]
            },

            refuse_job: {
                location: 'apartment',
                text: `"Not touching corpo work, Dex. Arasaka's got long memories and longer reach. Find someone else to flatline."

His smile doesn't waver, but something cold flickers behind his eyes.

<span class="npc-name">"Your loss, Ghost. But in this city, opportunities don't knock twice. Remember that."</span>

The holo dies. Silence fills the apartment, broken only by the hum of the city outside.

Maybe smart. Maybe stupid. Time will tell.

<span class="highlight">-5 Street Cred</span>`,
                choices: [
                    { text: 'Head to the Afterlife for other work', next: 'afterlife_scene', effects: { time: 1 } },
                    { text: 'Hit the streets', next: 'street_walk', effects: { stress: -10, time: 2 } },
                    { text: 'Jack into the local net', next: 'netrun_intro', effects: {} }
                ]
            },

            sleep_scene: {
                location: 'apartment',
                text: `You collapse onto the thin mattress. Outside, Night City never sleeps—but you need to.

Dreams come fragmented. Neon corridors. Faceless corpos. The sensation of falling through digital space. Somewhere, a woman's voice whispers coordinates you can't quite hear.

You wake to grey light filtering through the blinds. Morning in the megabuilding. Another day in paradise.

<span class="highlight">+30 Energy</span>
<span class="highlight">6 hours passed</span>`,
                choices: [
                    { text: 'Check your messages', next: 'morning_messages', effects: {} },
                    { text: 'Make some synth-coffee', next: 'morning_routine', effects: { energy: 10 } },
                    { text: 'Head out immediately', next: 'street_walk', effects: {} }
                ],
                onEnter: (game) => {
                    game.advanceTime(6);
                    game.player.energy = Math.min(game.player.maxEnergy, game.player.energy + 30);
                }
            },

            street_walk: {
                location: 'downtown',
                text: `The streets pulse with life—electric and organic intertwined. Holographic advertisements scream deals from every surface. Street vendors hawk black-market chrome. A joytoy winks from a doorway.

<span class="location">Night City</span>. Home to eight million people, all chasing the same dream. Most of them will die trying.

A group of Tyger Claws eye you from across the street. Gang colors bright under the neon. You keep walking, hand near your piece.

The <span class="location">Afterlife</span> is a few blocks north. The markets of <span class="location">Kabuki</span> sprawl to the east. Or you could find a quiet corner to jack in...`,
                choices: [
                    { text: 'Head to the Afterlife', next: 'afterlife_scene', effects: { time: 1 } },
                    { text: 'Browse Kabuki Market', next: 'kabuki_market', effects: { time: 2 } },
                    { text: 'Find a public terminal and jack in', next: 'public_netrun', effects: { time: 1 } },
                    { text: 'Return to your apartment', next: 'intro', effects: { time: 1 } }
                ],
                onEnter: (game) => {
                    game.currentLocation = 'downtown';
                    game.player.stress = Math.max(0, game.player.stress - 10);
                }
            },

            afterlife_scene: {
                location: 'afterlife',
                text: `The Afterlife. Where legends are born and forgotten in the same breath.

The bouncer—a mountain of muscle and chrome—nods you through. Inside, mercenaries and fixers crowd the bar. A corpo slumming it in the corner. The eternal poker game in the back room.

<span class="npc-name">Rogue Amendiares</span> holds court at her usual booth. Queen of the fixers. Word is she knew Johnny Silverhand back in the day, before Arasaka turned him into a cautionary tale.

The air smells like synth-whiskey and broken dreams.`,
                choices: [
                    { text: 'Approach Rogue for work', next: 'talk_rogue', effects: {}, requirements: { streetCred: 200 } },
                    { text: 'Check the job board', next: 'afterlife_jobs', effects: {} },
                    { text: 'Order a drink and listen to gossip', next: 'afterlife_gossip', effects: { money: -50, time: 1 } },
                    { text: 'Leave', next: 'street_walk', effects: {} }
                ],
                onEnter: (game) => {
                    game.currentLocation = 'afterlife';
                }
            },

            afterlife_jobs: {
                location: 'afterlife',
                text: `The job board flickers—a constant stream of work for those willing to risk everything.

Most of it's garbage. Delivery runs. Debt collection. But a few postings catch your eye:

<span class="item">• COURIER RUN</span> - €$800 - Deliver package to Kabuki, no questions
<span class="item">• BOUNTY</span> - €$3,500 - Target: Chrome Ripper, wanted for organ harvesting
<span class="item">• EXTRACTION</span> - €$12,000 - Scientist needs out of Militech facility

The extraction job has a red warning tag. <span class="highlight">COMBAT EXPECTED</span>.`,
                choices: [
                    { text: 'Take the courier job', next: 'courier_job', effects: { money: 800, time: 3 } },
                    { text: 'Take the bounty job', next: 'bounty_job', effects: {}, requirements: { combat: 15 } },
                    { text: 'Take the extraction job', next: 'extraction_job', effects: {}, requirements: { combat: 20, streetCred: 150 } },
                    { text: 'Nothing interesting. Leave.', next: 'street_walk', effects: {} }
                ]
            },

            afterlife_gossip: {
                location: 'afterlife',
                text: `You slide onto a barstool and order something brown. The bartender doesn't ask questions—that's why the Afterlife endures.

Around you, conversations flutter like digital ghosts:

<span class="npc-name">"...heard Arasaka's testing something new in the subnet. Black ICE that eats your memories..."</span>

<span class="npc-name">"...Militech convoy hit in the Badlands. Nomads getting bold..."</span>

<span class="npc-name">"...another body in the Combat Zone. Third this week with their chrome ripped out..."</span>

The whiskey burns going down. In Night City, information is currency. You file it all away.

<span class="highlight">-€$50</span>`,
                choices: [
                    { text: 'Ask about the chrome ripper', next: 'gossip_ripper', effects: {} },
                    { text: 'Ask about Arasaka\'s new ICE', next: 'gossip_arasaka', effects: {} },
                    { text: 'Head out', next: 'street_walk', effects: {} }
                ],
                onEnter: (game) => {
                    game.player.money -= 50;
                    game.advanceTime(1);
                }
            },

            kabuki_market: {
                location: 'kabuki',
                text: `Kabuki Market sprawls through the underbelly of Watson—a maze of stalls, vendors, and back-alley ripperdocs.

The air is thick with cooking oil, ozone, and desperation. Neon signs advertise everything from synth-meat to military-grade cyberware. A Buddhist monk sits in quiet meditation beside a weapons dealer.

This is where you come when you can't afford Corpo Plaza prices. Or when you need something that doesn't exist on any official manifest.

<span class="npc-name">Viktor's clinic</span> is nearby. So is <span class="npc-name">Misty's Esoterica</span>—tarot readings and braindance gear.`,
                choices: [
                    { text: 'Visit Viktor for chrome', next: 'visit_vik', effects: {} },
                    { text: 'Browse the weapons stalls', next: 'weapons_market', effects: { time: 1 } },
                    { text: 'Check the tech vendors', next: 'tech_market', effects: { time: 1 } },
                    { text: 'Visit Misty\'s Esoterica', next: 'misty_shop', effects: { time: 1 } },
                    { text: 'Leave the market', next: 'street_walk', effects: {} }
                ],
                onEnter: (game) => {
                    game.currentLocation = 'kabuki';
                }
            },

            visit_vik: {
                location: 'kabuki',
                text: `Viktor's clinic sits below street level—follow the flickering neon hand sign down the concrete stairs.

The old ripperdoc looks up from his workbench. Chrome fingers delicate as a surgeon's. He was one of the best, once. Before whatever brought him to this basement.

<span class="npc-name">"Ghost. Been a while. You here for maintenance or an upgrade?"</span>

His prices are fair. His work is clean. In this city, that's worth more than gold.`,
                choices: [
                    { text: 'Browse available cyberware', next: 'vik_shop', effects: {} },
                    { text: 'Ask for maintenance check', next: 'vik_maintenance', effects: { money: -200, chrome: 5 } },
                    { text: 'Just catching up', next: 'vik_chat', effects: {} },
                    { text: 'Leave', next: 'kabuki_market', effects: {} }
                ]
            },

            vik_shop: {
                location: 'kabuki',
                text: `Viktor pulls up his inventory on a scratched holo-display.

<span class="item">NEURAL UPGRADES:</span>
• <span class="highlight">Zetatech Neural Link Mk.2</span> - €$8,000 - +10 Netrunning
• <span class="highlight">Reflex Booster</span> - €$5,000 - +5 Combat reflexes

<span class="item">OPTICAL:</span>
• <span class="highlight">Kiroshi Optics Mk.3</span> - €$12,000 - Threat detection, zoom, recording

<span class="item">COMBAT:</span>
• <span class="highlight">Mantis Blades</span> - €$15,000 - Retractable arm blades
• <span class="highlight">Gorilla Arms</span> - €$10,000 - Enhanced strength

<span class="npc-name">"Quality chrome, fair prices. You know I don't deal in that back-alley garbage."</span>`,
                choices: [
                    { text: 'Buy Neural Link Mk.2', next: 'buy_neural', effects: { money: -8000 }, requirements: { money: 8000 } },
                    { text: 'Buy Reflex Booster', next: 'buy_reflex', effects: { money: -5000 }, requirements: { money: 5000 } },
                    { text: 'Not today', next: 'visit_vik', effects: {} }
                ]
            },

            netrun_intro: {
                location: 'apartment',
                text: `You slot into your deck and let the world dissolve.

The Net unfolds around you—infinite corridors of light and data. Here, meat is meaningless. Only the code matters.

Your avatar flickers into existence: a ghost in the machine. The local subnet stretches before you like a digital city—data fortresses, traffic streams, and somewhere in the dark, things that hunt runners like you.

<span class="highlight">NEURAL LINK ACTIVE</span>
<span class="highlight">ICE DETECTION: NOMINAL</span>`,
                choices: [
                    { text: 'Scan for vulnerable systems', next: 'netrun_scan', effects: { time: 1, energy: -20 } },
                    { text: 'Access the public boards', next: 'netrun_boards', effects: { time: 1 } },
                    { text: 'Jack out', next: 'intro', effects: {} }
                ]
            },

            netrun_scan: {
                location: 'apartment',
                text: `Your scanning protocols fan out across the subnet, searching for weakness.

<span class="highlight">SCAN RESULTS:</span>

• <span class="item">LOCAL BUSINESS</span> - Weak ICE - Est. €$200-500
• <span class="item">MEDICAL DATABASE</span> - Medium ICE - Est. €$1,000-2,000
• <span class="item">CORPO SUBSIDIARY</span> - Heavy ICE - Est. €$5,000+ (DANGER)

The corpo target pulses red. Heavy security. Countermeasure ICE. But the potential payout...

<span class="highlight">-20 Energy</span>`,
                choices: [
                    { text: 'Hit the local business', next: 'netrun_easy', effects: { money: 350, time: 1, stress: 5 } },
                    { text: 'Try the medical database', next: 'netrun_medium', effects: {}, requirements: { netrunning: 15 } },
                    { text: 'Risk the corpo system', next: 'netrun_hard', effects: {}, requirements: { netrunning: 25 } },
                    { text: 'Jack out', next: 'intro', effects: {} }
                ],
                onEnter: (game) => {
                    game.player.energy -= 20;
                }
            },

            netrun_easy: {
                location: 'apartment',
                text: `The business subnet folds like wet paper. Pathetic ICE—probably default passwords and outdated firewalls.

You ghost through their financial records, skimming eddies from transaction fees. Nothing they'll notice. Nothing that'll bring heat.

<span class="highlight">+€$350</span>
<span class="highlight">+5 Stress</span>

Small scores. That's how you survive in this city. The big plays... those get you noticed. And noticed gets you dead.`,
                choices: [
                    { text: 'Run another scan', next: 'netrun_scan', effects: { time: 1, energy: -20 } },
                    { text: 'Jack out', next: 'intro', effects: {} }
                ],
                onEnter: (game) => {
                    game.player.money += 350;
                    game.player.stress += 5;
                }
            },

            morning_messages: {
                location: 'apartment',
                text: `Your neural link floods with overnight notifications:

<span class="item">3 MISSED CALLS</span> - Unknown Number
<span class="item">1 MESSAGE</span> - Jackie Welles
<span class="item">1 JOB UPDATE</span> - Fixer Network

Jackie's message plays: <span class="npc-name">"Yo, Ghost! Got a line on something big. Meet me at El Coyote Cojo tonight? Drinks on me, hermano."</span>

The unknown calls are probably spam. Or someone who doesn't want to be traced. In Night City, those are often the same thing.`,
                choices: [
                    { text: 'Call Jackie back', next: 'call_jackie', effects: {} },
                    { text: 'Check the job update', next: 'job_update', effects: {} },
                    { text: 'Try to trace the unknown calls', next: 'trace_calls', effects: { time: 1 }, requirements: { netrunning: 20 } },
                    { text: 'Ignore everything and head out', next: 'street_walk', effects: {} }
                ]
            },

            call_jackie: {
                location: 'apartment',
                text: `Jackie picks up on the second ring. His face fills your HUD—big grin, bigger heart.

<span class="npc-name">"Ghost! You got my message? Listen, I got a contact at Militech—don't ask how. Says they're moving something valuable through the Badlands tomorrow night. Convoy job."</span>

He leans closer to the camera.

<span class="npc-name">"This is the big one, hermano. The score that sets us up for life. You in?"</span>

Jackie's enthusiasm is infectious. Also dangerous. His plans have a way of going sideways.`,
                choices: [
                    { text: '"Tell me more about this convoy."', next: 'convoy_details', effects: {} },
                    { text: '"Sounds risky. What\'s the split?"', next: 'convoy_split', effects: {} },
                    { text: '"I got other jobs lined up, Jack."', next: 'refuse_jackie', effects: {} },
                    { text: '"I\'m in. When do we ride?"', next: 'accept_convoy', effects: { streetCred: 5 } }
                ]
            },

            convoy_details: {
                location: 'apartment',
                text: `Jackie's eyes light up as he explains.

<span class="npc-name">"Militech convoy, four vehicles. Two APCs, two support. Moving through Badlands Route 7 around 0200. My contact says they're carrying prototype tech—next-gen neural interface stuff."</span>

He pulls up a rough map on your shared display.

<span class="npc-name">"We hit them at the canyon crossing. Nomads will provide backup—for a cut, of course. In and out in ten minutes. Clean."</span>

Nothing's ever clean in Night City. But the payout could be massive.`,
                choices: [
                    { text: '"The Nomads reliable?"', next: 'nomad_question', effects: {} },
                    { text: '"What kind of security we facing?"', next: 'convoy_security', effects: {} },
                    { text: '"I need to think about it."', next: 'delay_convoy', effects: {} },
                    { text: '"Alright. I\'m in."', next: 'accept_convoy', effects: { streetCred: 5 } }
                ]
            }
        };
    }

    // === GAME INITIALIZATION ===

    init() {
        this.bindEvents();
        this.initBootSequence();
    }

    initBootSequence() {
        const bootLines = document.querySelectorAll('.boot-line');
        bootLines.forEach((line, index) => {
            const delay = parseInt(line.dataset.delay) || 0;
            setTimeout(() => {
                line.style.animationDelay = '0s';
                line.style.opacity = '1';
            }, delay);
        });

        document.getElementById('start-btn').addEventListener('click', () => {
            this.startGame();
        });
    }

    startGame() {
        document.getElementById('boot-sequence').classList.add('hidden');
        document.getElementById('game-container').classList.remove('hidden');

        // Start music
        if (window.synthwave) {
            window.synthwave.start();
            document.getElementById('music-toggle').textContent = '⏸';
        }

        this.updateUI();
        this.showScene('intro');
    }

    // === EVENT BINDING ===

    bindEvents() {
        // Neural app buttons
        document.querySelectorAll('.neural-btn').forEach(btn => {
            btn.addEventListener('click', () => {
                const panel = btn.dataset.panel;
                this.openPanel(panel);
            });
        });

        // Action buttons
        document.querySelectorAll('.action-btn').forEach(btn => {
            btn.addEventListener('click', () => {
                const action = btn.dataset.action;
                this.handleAction(action);
            });
        });

        // Modal close
        document.querySelector('.close-btn')?.addEventListener('click', () => {
            this.closePanel();
        });

        document.getElementById('modal-overlay')?.addEventListener('click', (e) => {
            if (e.target.id === 'modal-overlay') {
                this.closePanel();
            }
        });
    }

    // === TIME SYSTEM ===

    advanceTime(hours) {
        this.time.minute = 0;
        this.time.hour += hours;

        while (this.time.hour >= 24) {
            this.time.hour -= 24;
            this.time.day++;
        }

        // Energy decay
        this.player.energy = Math.max(0, this.player.energy - hours * 5);

        this.updateUI();
    }

    formatTime() {
        const h = String(this.time.hour).padStart(2, '0');
        const m = String(this.time.minute).padStart(2, '0');
        return `${h}:${m}`;
    }

    formatDate() {
        const d = String(this.time.day).padStart(2, '0');
        const mo = String(this.time.month).padStart(2, '0');
        return `${this.time.year}.${mo}.${d}`;
    }

    // === UI UPDATES ===

    updateUI() {
        // Time
        document.getElementById('time-display').textContent = this.formatTime();
        document.getElementById('date-display').textContent = this.formatDate();

        // Location
        const loc = this.locations[this.currentLocation];
        document.getElementById('location-display').textContent = loc.name;

        // Stats
        this.updateBar('health', this.player.health, this.player.maxHealth);
        this.updateBar('energy', this.player.energy, this.player.maxEnergy);
        this.updateBar('stress', this.player.stress, 100);
        this.updateBar('chrome', this.player.chrome, 100);

        // Values
        document.getElementById('health-value').textContent = this.player.health;
        document.getElementById('energy-value').textContent = this.player.energy;
        document.getElementById('stress-value').textContent = this.player.stress;
        document.getElementById('chrome-value').textContent = this.player.chrome;

        // Money and cred
        document.getElementById('money-number').textContent = this.player.money.toLocaleString();
        document.getElementById('cred-number').textContent = this.player.streetCred;
        document.getElementById('cred-rank').textContent = this.getCredRank();

        // Update music intensity based on location danger
        if (window.synthwave) {
            const danger = loc.danger / 10;
            window.synthwave.setIntensity(0.3 + danger * 0.7);
        }
    }

    updateBar(stat, value, max) {
        const bar = document.getElementById(`${stat}-bar`);
        if (bar) {
            bar.style.width = `${(value / max) * 100}%`;
        }
    }

    getCredRank() {
        const cred = this.player.streetCred;
        if (cred < 50) return 'NOBODY';
        if (cred < 150) return 'STREET KID';
        if (cred < 300) return 'PROFESSIONAL';
        if (cred < 500) return 'HARDENED';
        if (cred < 800) return 'VETERAN';
        if (cred < 1200) return 'LEGENDARY';
        return 'MYTH';
    }

    // === NARRATIVE SYSTEM ===

    showScene(sceneId) {
        const scene = this.scenes[sceneId];
        if (!scene) {
            console.error(`Scene not found: ${sceneId}`);
            return;
        }

        this.narrative.currentScene = sceneId;

        // Update location if specified
        if (scene.location && this.locations[scene.location]) {
            this.currentLocation = scene.location;
        }

        // Run onEnter callback
        if (scene.onEnter) {
            scene.onEnter(this);
        }

        // Type out narrative text
        this.typeText(scene.text, () => {
            this.showChoices(scene.choices);
        });

        this.updateUI();
    }

    typeText(text, callback) {
        const textEl = document.getElementById('narrative-text');
        textEl.innerHTML = '';
        this.ui.isTyping = true;

        let index = 0;
        let inTag = false;
        let currentTag = '';

        const type = () => {
            if (index < text.length) {
                const char = text[index];

                if (char === '<') {
                    inTag = true;
                    currentTag = '<';
                } else if (char === '>') {
                    inTag = false;
                    currentTag += '>';
                    textEl.innerHTML += currentTag;
                    currentTag = '';
                } else if (inTag) {
                    currentTag += char;
                } else {
                    textEl.innerHTML += char;
                }

                index++;
                setTimeout(type, inTag ? 0 : this.ui.typingSpeed);
            } else {
                this.ui.isTyping = false;
                if (callback) callback();
            }
        };

        type();
    }

    showChoices(choices) {
        const container = document.getElementById('choices-container');
        const panel = document.getElementById('choice-panel');

        container.innerHTML = '';

        choices.forEach((choice, index) => {
            const btn = document.createElement('button');
            btn.className = 'choice-btn';

            // Check requirements
            let meetsRequirements = true;
            let reqText = '';

            if (choice.requirements) {
                for (const [key, value] of Object.entries(choice.requirements)) {
                    if (key === 'money') {
                        if (this.player.money < value) meetsRequirements = false;
                    } else if (key === 'streetCred') {
                        if (this.player.streetCred < value) meetsRequirements = false;
                    } else if (this.player.skills[key] !== undefined) {
                        if (this.player.skills[key] < value) {
                            meetsRequirements = false;
                            reqText = `[Requires ${key}: ${value}]`;
                        }
                    }
                }
            }

            btn.innerHTML = choice.text;
            if (reqText) {
                btn.innerHTML += `<div class="choice-requirement">${reqText}</div>`;
            }

            if (!meetsRequirements) {
                btn.classList.add('disabled');
            } else {
                btn.addEventListener('click', () => {
                    this.makeChoice(choice);
                });
            }

            container.appendChild(btn);
        });

        panel.classList.remove('hidden');
    }

    makeChoice(choice) {
        document.getElementById('choice-panel').classList.add('hidden');

        // Apply effects
        if (choice.effects) {
            for (const [key, value] of Object.entries(choice.effects)) {
                if (key === 'money') this.player.money += value;
                else if (key === 'streetCred') this.player.streetCred += value;
                else if (key === 'health') this.player.health = Math.min(this.player.maxHealth, Math.max(0, this.player.health + value));
                else if (key === 'energy') this.player.energy = Math.min(this.player.maxEnergy, Math.max(0, this.player.energy + value));
                else if (key === 'stress') this.player.stress = Math.min(100, Math.max(0, this.player.stress + value));
                else if (key === 'chrome') this.player.chrome = Math.min(100, Math.max(0, this.player.chrome + value));
                else if (key === 'time') this.advanceTime(value);
            }
        }

        this.updateUI();

        // Go to next scene
        if (choice.next) {
            setTimeout(() => {
                this.showScene(choice.next);
            }, 300);
        }
    }

    // === ACTIONS ===

    handleAction(action) {
        switch (action) {
            case 'sleep':
                this.showScene('sleep_scene');
                break;
            case 'work':
                this.openPanel('jobs');
                break;
            case 'explore':
                this.showScene('street_walk');
                break;
            case 'netrun':
                if (this.player.skills.netrunning >= 10) {
                    this.showScene('netrun_intro');
                } else {
                    this.showNotification('Netrunning skill too low');
                }
                break;
            case 'socialize':
                this.openPanel('contacts');
                break;
        }
    }

    // === PANELS ===

    openPanel(panelType) {
        const overlay = document.getElementById('modal-overlay');
        const title = document.getElementById('modal-title');
        const content = document.getElementById('modal-content');

        this.ui.currentPanel = panelType;

        switch (panelType) {
            case 'inventory':
                title.textContent = 'INVENTORY';
                content.innerHTML = this.renderInventory();
                break;
            case 'augments':
                title.textContent = 'CYBERWARE';
                content.innerHTML = this.renderAugments();
                break;
            case 'contacts':
                title.textContent = 'CONTACTS';
                content.innerHTML = this.renderContacts();
                break;
            case 'jobs':
                title.textContent = 'AVAILABLE JOBS';
                content.innerHTML = this.renderJobs();
                break;
            case 'map':
                title.textContent = 'NIGHT CITY MAP';
                content.innerHTML = this.renderMap();
                break;
        }

        overlay.classList.remove('hidden');
    }

    closePanel() {
        document.getElementById('modal-overlay').classList.add('hidden');
        this.ui.currentPanel = null;
    }

    renderInventory() {
        let html = '<div class="inventory-grid">';

        this.player.inventory.forEach(item => {
            html += `
                <div class="inventory-slot" data-item="${item.id}">
                    <span class="item-icon">${item.icon}</span>
                    <span class="item-name">${item.name}</span>
                    ${item.quantity ? `<span class="item-qty">x${item.quantity}</span>` : ''}
                </div>
            `;
        });

        // Empty slots
        for (let i = this.player.inventory.length; i < 16; i++) {
            html += '<div class="inventory-slot empty"></div>';
        }

        html += '</div>';
        return html;
    }

    renderAugments() {
        let html = '<div class="augment-list">';

        this.player.augments.forEach(aug => {
            html += `
                <div class="augment-item">
                    <div class="augment-icon">${aug.icon}</div>
                    <div class="augment-info">
                        <div class="augment-name">${aug.name}</div>
                        <div class="augment-desc">${aug.desc}</div>
                        <div class="augment-stats">${aug.stats}</div>
                    </div>
                </div>
            `;
        });

        html += '</div>';
        return html;
    }

    renderContacts() {
        let html = '<div class="contact-list">';

        this.player.contacts.forEach(contact => {
            html += `
                <div class="contact-item" data-contact="${contact.id}">
                    <div class="contact-avatar">${contact.avatar}</div>
                    <div class="contact-info">
                        <div class="contact-name">${contact.name}</div>
                        <div class="contact-role">${contact.role}</div>
                    </div>
                    <div class="contact-trust">
                        <div class="trust-label">TRUST</div>
                        <div class="trust-value">${contact.trust}</div>
                    </div>
                </div>
            `;
        });

        html += '</div>';
        return html;
    }

    renderJobs() {
        let html = '<div class="job-list">';

        this.jobs.forEach(job => {
            const canTake = this.meetsRequirements(job.requirements);
            html += `
                <div class="job-item ${canTake ? '' : 'disabled'}">
                    <div class="job-header">
                        <div class="job-title">${job.title}</div>
                        <div class="job-pay">€$${job.pay.toLocaleString()}</div>
                    </div>
                    <div class="job-desc">${job.desc}</div>
                    <div class="job-tags">
                        ${job.tags.map(t => `<span class="job-tag">${t}</span>`).join('')}
                        <span class="job-tag ${job.danger === 'EXTREME' || job.danger === 'HIGH' ? 'danger' : ''}">${job.danger}</span>
                    </div>
                </div>
            `;
        });

        html += '</div>';
        return html;
    }

    renderMap() {
        return `
            <div style="text-align: center; padding: 40px;">
                <div style="font-family: var(--font-display); font-size: 24px; color: var(--neon-cyan); margin-bottom: 20px;">
                    NIGHT CITY // 2087
                </div>
                <div style="display: grid; grid-template-columns: repeat(3, 1fr); gap: 15px;">
                    ${Object.entries(this.locations).map(([id, loc]) => `
                        <div class="location-tile" style="
                            padding: 15px;
                            background: ${id === this.currentLocation ? 'rgba(0, 255, 255, 0.2)' : 'rgba(0, 0, 0, 0.3)'};
                            border: 1px solid ${id === this.currentLocation ? 'var(--neon-cyan)' : 'rgba(0, 255, 255, 0.2)'};
                            border-radius: 4px;
                            cursor: pointer;
                        ">
                            <div style="font-family: var(--font-ui); font-size: 12px; color: var(--text-secondary);">${loc.sector}</div>
                            <div style="font-family: var(--font-display); font-size: 11px; color: var(--text-primary); margin-top: 5px;">${loc.name.split('//')[0]}</div>
                            <div style="font-size: 10px; color: ${loc.danger > 5 ? 'var(--neon-red)' : loc.danger > 2 ? 'var(--neon-orange)' : 'var(--neon-green)'}; margin-top: 5px;">
                                DANGER: ${'▮'.repeat(loc.danger)}${'▯'.repeat(10 - loc.danger)}
                            </div>
                        </div>
                    `).join('')}
                </div>
            </div>
        `;
    }

    meetsRequirements(reqs) {
        if (!reqs) return true;
        for (const [key, value] of Object.entries(reqs)) {
            if (key === 'money' && this.player.money < value) return false;
            if (key === 'streetCred' && this.player.streetCred < value) return false;
            if (this.player.skills[key] !== undefined && this.player.skills[key] < value) return false;
        }
        return true;
    }

    showNotification(text) {
        const notif = document.getElementById('event-notification');
        notif.querySelector('.notif-text').textContent = text;
        notif.classList.remove('hidden');

        setTimeout(() => {
            notif.classList.add('hidden');
        }, 3000);
    }
}

// Initialize game
const game = new NeonGhost();
document.addEventListener('DOMContentLoaded', () => {
    game.init();
});
