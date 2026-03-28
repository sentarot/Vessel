/**
 * NEON GHOST - Perturbator-Inspired MIDI Soundtrack System
 * Dark Synthwave Audio Engine using Web Audio API
 */

class SynthwaveEngine {
    constructor() {
        this.audioCtx = null;
        this.masterGain = null;
        this.compressor = null;
        this.isPlaying = false;
        this.bpm = 110;
        this.currentBeat = 0;
        this.schedulerInterval = null;
        this.lookahead = 25.0; // ms
        this.scheduleAheadTime = 0.1; // seconds
        this.nextNoteTime = 0.0;
        this.volume = 0.7;

        // Track layers
        this.tracks = {
            kick: null,
            snare: null,
            hihat: null,
            bass: null,
            lead: null,
            pad: null,
            arp: null
        };

        // Musical data
        this.currentTrack = 0;
        this.patterns = this.initPatterns();
        this.scales = {
            minor: [0, 2, 3, 5, 7, 8, 10],
            phrygian: [0, 1, 3, 5, 7, 8, 10],
            dorian: [0, 2, 3, 5, 7, 9, 10],
            harmonicMinor: [0, 2, 3, 5, 7, 8, 11]
        };

        // Current musical state
        this.rootNote = 33; // A1 = 55Hz
        this.currentScale = this.scales.minor;
        this.intensity = 0.5;

        // Visualizer
        this.analyser = null;
        this.visualizerCanvas = null;
        this.visualizerCtx = null;
        this.animationFrame = null;
    }

    async init() {
        if (this.audioCtx) return;

        this.audioCtx = new (window.AudioContext || window.webkitAudioContext)();

        // Master chain
        this.compressor = this.audioCtx.createDynamicsCompressor();
        this.compressor.threshold.value = -24;
        this.compressor.knee.value = 30;
        this.compressor.ratio.value = 12;
        this.compressor.attack.value = 0.003;
        this.compressor.release.value = 0.25;

        this.masterGain = this.audioCtx.createGain();
        this.masterGain.gain.value = this.volume;

        // Reverb
        this.reverb = await this.createReverb();
        this.reverbGain = this.audioCtx.createGain();
        this.reverbGain.gain.value = 0.3;

        // Delay
        this.delay = this.audioCtx.createDelay(1.0);
        this.delay.delayTime.value = 60 / this.bpm / 2; // 8th note delay
        this.delayFeedback = this.audioCtx.createGain();
        this.delayFeedback.gain.value = 0.4;
        this.delayGain = this.audioCtx.createGain();
        this.delayGain.gain.value = 0.25;

        // Delay feedback loop
        this.delay.connect(this.delayFeedback);
        this.delayFeedback.connect(this.delay);
        this.delay.connect(this.delayGain);
        this.delayGain.connect(this.masterGain);

        // Reverb send
        this.reverbGain.connect(this.reverb);
        this.reverb.connect(this.masterGain);

        // Master output
        this.masterGain.connect(this.compressor);
        this.compressor.connect(this.audioCtx.destination);

        // Analyser for visualizer
        this.analyser = this.audioCtx.createAnalyser();
        this.analyser.fftSize = 256;
        this.masterGain.connect(this.analyser);

        this.initVisualizer();
    }

    async createReverb() {
        const convolver = this.audioCtx.createConvolver();
        const length = this.audioCtx.sampleRate * 2;
        const impulse = this.audioCtx.createBuffer(2, length, this.audioCtx.sampleRate);

        for (let channel = 0; channel < 2; channel++) {
            const channelData = impulse.getChannelData(channel);
            for (let i = 0; i < length; i++) {
                channelData[i] = (Math.random() * 2 - 1) * Math.pow(1 - i / length, 2);
            }
        }

        convolver.buffer = impulse;
        return convolver;
    }

    initPatterns() {
        return {
            // Kick patterns (16 steps)
            kick: [
                [1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0],
                [1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 1, 0],
                [1, 0, 0, 1, 0, 0, 1, 0, 1, 0, 0, 1, 0, 0, 1, 0],
                [1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 1, 0, 0]
            ],
            // Snare patterns
            snare: [
                [0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0],
                [0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 1],
                [0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0],
                [0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0]
            ],
            // Hi-hat patterns
            hihat: [
                [1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0],
                [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
                [1, 0, 1, 1, 1, 0, 1, 1, 1, 0, 1, 1, 1, 0, 1, 1],
                [1, 1, 0, 1, 1, 1, 0, 1, 1, 1, 0, 1, 1, 1, 0, 1]
            ],
            // Bass patterns (note indices in scale)
            bass: [
                [0, -1, -1, -1, 0, -1, -1, 3, 0, -1, -1, -1, 2, -1, -1, -1],
                [0, -1, 0, -1, 3, -1, 2, -1, 0, -1, 0, -1, 4, -1, 3, -1],
                [0, 0, -1, 0, -1, -1, 2, -1, 3, 3, -1, 3, -1, -1, 4, -1],
                [0, -1, -1, -1, 0, -1, 5, -1, 4, -1, -1, -1, 3, -1, 2, -1]
            ],
            // Arp patterns (note indices)
            arp: [
                [0, 2, 4, 2, 0, 2, 4, 5, 0, 2, 4, 2, 0, 2, 4, 2],
                [0, 4, 2, 4, 0, 4, 3, 4, 0, 4, 2, 4, 0, 4, 3, 4],
                [4, 2, 0, 2, 4, 5, 4, 2, 4, 2, 0, 2, 4, 5, 4, 2],
                [0, 2, 4, 6, 4, 2, 0, 2, 4, 6, 4, 2, 0, 2, 4, 6]
            ]
        };
    }

    midiToFreq(midi) {
        return 440 * Math.pow(2, (midi - 69) / 12);
    }

    scaleNote(index, octave = 0) {
        const scaleLen = this.currentScale.length;
        const octaveOffset = Math.floor(index / scaleLen);
        const noteIndex = ((index % scaleLen) + scaleLen) % scaleLen;
        return this.rootNote + this.currentScale[noteIndex] + (octave + octaveOffset) * 12;
    }

    // === SYNTHESIZERS ===

    playKick(time) {
        const osc = this.audioCtx.createOscillator();
        const gain = this.audioCtx.createGain();

        osc.type = 'sine';
        osc.frequency.setValueAtTime(150, time);
        osc.frequency.exponentialRampToValueAtTime(30, time + 0.15);

        gain.gain.setValueAtTime(0.8, time);
        gain.gain.exponentialRampToValueAtTime(0.01, time + 0.3);

        osc.connect(gain);
        gain.connect(this.masterGain);

        osc.start(time);
        osc.stop(time + 0.3);
    }

    playSnare(time) {
        // Noise component
        const noiseBuffer = this.audioCtx.createBuffer(1, this.audioCtx.sampleRate * 0.2, this.audioCtx.sampleRate);
        const noiseData = noiseBuffer.getChannelData(0);
        for (let i = 0; i < noiseBuffer.length; i++) {
            noiseData[i] = Math.random() * 2 - 1;
        }

        const noise = this.audioCtx.createBufferSource();
        noise.buffer = noiseBuffer;

        const noiseFilter = this.audioCtx.createBiquadFilter();
        noiseFilter.type = 'highpass';
        noiseFilter.frequency.value = 1000;

        const noiseGain = this.audioCtx.createGain();
        noiseGain.gain.setValueAtTime(0.5, time);
        noiseGain.gain.exponentialRampToValueAtTime(0.01, time + 0.15);

        noise.connect(noiseFilter);
        noiseFilter.connect(noiseGain);
        noiseGain.connect(this.masterGain);

        // Body component
        const osc = this.audioCtx.createOscillator();
        const oscGain = this.audioCtx.createGain();

        osc.type = 'triangle';
        osc.frequency.setValueAtTime(200, time);
        osc.frequency.exponentialRampToValueAtTime(80, time + 0.05);

        oscGain.gain.setValueAtTime(0.5, time);
        oscGain.gain.exponentialRampToValueAtTime(0.01, time + 0.1);

        osc.connect(oscGain);
        oscGain.connect(this.masterGain);

        noise.start(time);
        osc.start(time);
        osc.stop(time + 0.15);
    }

    playHihat(time, open = false) {
        const fundamental = 40;
        const ratios = [2, 3, 4.16, 5.43, 6.79, 8.21];

        const gainNode = this.audioCtx.createGain();
        const filter = this.audioCtx.createBiquadFilter();
        filter.type = 'highpass';
        filter.frequency.value = 7000;

        ratios.forEach(ratio => {
            const osc = this.audioCtx.createOscillator();
            osc.type = 'square';
            osc.frequency.value = fundamental * ratio;
            osc.connect(filter);
            osc.start(time);
            osc.stop(time + (open ? 0.3 : 0.08));
        });

        gainNode.gain.setValueAtTime(0.15, time);
        gainNode.gain.exponentialRampToValueAtTime(0.01, time + (open ? 0.3 : 0.08));

        filter.connect(gainNode);
        gainNode.connect(this.masterGain);
    }

    playBass(time, note, duration) {
        const freq = this.midiToFreq(note);

        // Main oscillator
        const osc1 = this.audioCtx.createOscillator();
        osc1.type = 'sawtooth';
        osc1.frequency.value = freq;

        // Sub oscillator
        const osc2 = this.audioCtx.createOscillator();
        osc2.type = 'sine';
        osc2.frequency.value = freq / 2;

        // Filter with envelope
        const filter = this.audioCtx.createBiquadFilter();
        filter.type = 'lowpass';
        filter.Q.value = 8;
        filter.frequency.setValueAtTime(freq * 4, time);
        filter.frequency.exponentialRampToValueAtTime(freq * 1.5, time + 0.1);

        // Gain envelope
        const gain = this.audioCtx.createGain();
        gain.gain.setValueAtTime(0.4, time);
        gain.gain.setValueAtTime(0.35, time + 0.02);
        gain.gain.exponentialRampToValueAtTime(0.01, time + duration);

        // Sub gain
        const subGain = this.audioCtx.createGain();
        subGain.gain.value = 0.3;

        // Routing
        osc1.connect(filter);
        filter.connect(gain);
        osc2.connect(subGain);
        subGain.connect(gain);
        gain.connect(this.masterGain);
        gain.connect(this.delay);

        osc1.start(time);
        osc2.start(time);
        osc1.stop(time + duration);
        osc2.stop(time + duration);
    }

    playArp(time, note, duration) {
        const freq = this.midiToFreq(note);

        // Detuned oscillators for width
        const osc1 = this.audioCtx.createOscillator();
        const osc2 = this.audioCtx.createOscillator();

        osc1.type = 'sawtooth';
        osc2.type = 'sawtooth';
        osc1.frequency.value = freq;
        osc2.frequency.value = freq * 1.005; // Slight detune

        // Filter
        const filter = this.audioCtx.createBiquadFilter();
        filter.type = 'lowpass';
        filter.Q.value = 5;
        filter.frequency.setValueAtTime(freq * 6, time);
        filter.frequency.exponentialRampToValueAtTime(freq * 2, time + duration * 0.8);

        // Gain envelope
        const gain = this.audioCtx.createGain();
        gain.gain.setValueAtTime(0, time);
        gain.gain.linearRampToValueAtTime(0.15, time + 0.01);
        gain.gain.exponentialRampToValueAtTime(0.01, time + duration);

        // Panning
        const panner = this.audioCtx.createStereoPanner();
        panner.pan.value = (Math.random() - 0.5) * 0.6;

        // Routing
        osc1.connect(filter);
        osc2.connect(filter);
        filter.connect(gain);
        gain.connect(panner);
        panner.connect(this.masterGain);
        panner.connect(this.reverbGain);
        panner.connect(this.delay);

        osc1.start(time);
        osc2.start(time);
        osc1.stop(time + duration);
        osc2.stop(time + duration);
    }

    playPad(time, notes, duration) {
        notes.forEach((note, i) => {
            const freq = this.midiToFreq(note);

            const osc = this.audioCtx.createOscillator();
            osc.type = 'sawtooth';
            osc.frequency.value = freq;

            const filter = this.audioCtx.createBiquadFilter();
            filter.type = 'lowpass';
            filter.frequency.value = 2000;
            filter.Q.value = 1;

            const gain = this.audioCtx.createGain();
            gain.gain.setValueAtTime(0, time);
            gain.gain.linearRampToValueAtTime(0.08, time + 0.5);
            gain.gain.setValueAtTime(0.08, time + duration - 0.5);
            gain.gain.linearRampToValueAtTime(0, time + duration);

            const panner = this.audioCtx.createStereoPanner();
            panner.pan.value = (i - 1) * 0.3;

            osc.connect(filter);
            filter.connect(gain);
            gain.connect(panner);
            panner.connect(this.masterGain);
            panner.connect(this.reverbGain);

            osc.start(time);
            osc.stop(time + duration);
        });
    }

    // === SEQUENCER ===

    scheduler() {
        while (this.nextNoteTime < this.audioCtx.currentTime + this.scheduleAheadTime) {
            this.scheduleNote(this.currentBeat, this.nextNoteTime);
            this.nextNote();
        }
    }

    nextNote() {
        const secondsPerBeat = 60.0 / this.bpm / 4; // 16th notes
        this.nextNoteTime += secondsPerBeat;
        this.currentBeat = (this.currentBeat + 1) % 16;

        // Change patterns every 4 bars
        if (this.currentBeat === 0) {
            if (Math.random() > 0.7) {
                this.currentTrack = (this.currentTrack + 1) % 4;
            }
            // Occasionally change scale
            if (Math.random() > 0.9) {
                const scales = Object.values(this.scales);
                this.currentScale = scales[Math.floor(Math.random() * scales.length)];
            }
        }
    }

    scheduleNote(beat, time) {
        const patterns = this.patterns;
        const track = this.currentTrack;
        const stepDuration = 60.0 / this.bpm / 4;

        // Drums
        if (patterns.kick[track][beat]) {
            this.playKick(time);
        }
        if (patterns.snare[track][beat]) {
            this.playSnare(time);
        }
        if (patterns.hihat[track][beat]) {
            this.playHihat(time, beat % 4 === 2);
        }

        // Bass (every other 16th)
        if (beat % 2 === 0) {
            const bassNote = patterns.bass[track][beat];
            if (bassNote >= 0) {
                const note = this.scaleNote(bassNote, 0);
                this.playBass(time, note, stepDuration * 1.5);
            }
        }

        // Arp (every 16th)
        if (this.intensity > 0.3) {
            const arpNote = patterns.arp[track][beat];
            const note = this.scaleNote(arpNote, 2);
            this.playArp(time, note, stepDuration * 0.8);
        }

        // Pad (every 4 bars, sustained)
        if (beat === 0 && Math.random() > 0.5) {
            const padNotes = [
                this.scaleNote(0, 1),
                this.scaleNote(2, 1),
                this.scaleNote(4, 1)
            ];
            this.playPad(time, padNotes, stepDuration * 32);
        }
    }

    // === CONTROLS ===

    async start() {
        await this.init();

        if (this.audioCtx.state === 'suspended') {
            await this.audioCtx.resume();
        }

        this.isPlaying = true;
        this.currentBeat = 0;
        this.nextNoteTime = this.audioCtx.currentTime;

        this.schedulerInterval = setInterval(() => this.scheduler(), this.lookahead);
        this.startVisualizer();
    }

    stop() {
        this.isPlaying = false;
        if (this.schedulerInterval) {
            clearInterval(this.schedulerInterval);
            this.schedulerInterval = null;
        }
        if (this.animationFrame) {
            cancelAnimationFrame(this.animationFrame);
            this.animationFrame = null;
        }
    }

    toggle() {
        if (this.isPlaying) {
            this.stop();
        } else {
            this.start();
        }
        return this.isPlaying;
    }

    setVolume(value) {
        this.volume = value;
        if (this.masterGain) {
            this.masterGain.gain.value = value;
        }
    }

    setIntensity(value) {
        this.intensity = Math.max(0, Math.min(1, value));
    }

    setBPM(bpm) {
        this.bpm = bpm;
        if (this.delay) {
            this.delay.delayTime.value = 60 / this.bpm / 2;
        }
    }

    // === VISUALIZER ===

    initVisualizer() {
        this.visualizerCanvas = document.getElementById('visualizer-canvas');
        if (!this.visualizerCanvas) return;

        this.visualizerCtx = this.visualizerCanvas.getContext('2d');
        this.resizeVisualizer();

        window.addEventListener('resize', () => this.resizeVisualizer());
    }

    resizeVisualizer() {
        if (!this.visualizerCanvas) return;
        const rect = this.visualizerCanvas.parentElement.getBoundingClientRect();
        this.visualizerCanvas.width = rect.width;
        this.visualizerCanvas.height = rect.height;
    }

    startVisualizer() {
        if (!this.analyser || !this.visualizerCtx) return;

        const bufferLength = this.analyser.frequencyBinCount;
        const dataArray = new Uint8Array(bufferLength);

        const draw = () => {
            this.animationFrame = requestAnimationFrame(draw);

            this.analyser.getByteFrequencyData(dataArray);

            const ctx = this.visualizerCtx;
            const width = this.visualizerCanvas.width;
            const height = this.visualizerCanvas.height;

            ctx.fillStyle = 'rgba(0, 0, 0, 0.3)';
            ctx.fillRect(0, 0, width, height);

            const barWidth = width / bufferLength * 2.5;
            let x = 0;

            for (let i = 0; i < bufferLength; i++) {
                const barHeight = (dataArray[i] / 255) * height;

                // Crustpunk colors - rust, bile green, dried blood
                const colors = ['#8b4513', '#6b8e23', '#722f37', '#556b2f', '#9a8b4f'];
                ctx.fillStyle = colors[i % colors.length];
                ctx.fillRect(x, height - barHeight, barWidth, barHeight);

                // No glow - gritty aesthetic
                ctx.shadowBlur = 0;

                x += barWidth + 1;
            }
        };

        draw();
    }

    // === TRACK NAMES ===

    getTrackName() {
        const names = [
            'RUST AND RUIN',
            'MEAT COLLAPSE',
            'GUTTER HYMN',
            'DEAD STATIC',
            'BURNT CHROME',
            'PLAGUE CARRIER',
            'NO FUTURE',
            'DECAY SIGNAL'
        ];
        return names[this.currentTrack % names.length];
    }
}

// Global instance
window.synthwave = new SynthwaveEngine();

// UI bindings
document.addEventListener('DOMContentLoaded', () => {
    const musicToggle = document.getElementById('music-toggle');
    const volumeSlider = document.getElementById('volume-slider');
    const trackInfo = document.querySelector('.track-name');

    if (musicToggle) {
        musicToggle.addEventListener('click', async () => {
            const playing = await window.synthwave.toggle();
            musicToggle.textContent = playing ? '⏸' : '▶';
            if (trackInfo) {
                trackInfo.textContent = window.synthwave.getTrackName();
            }
        });
    }

    if (volumeSlider) {
        volumeSlider.addEventListener('input', (e) => {
            window.synthwave.setVolume(e.target.value / 100);
        });
    }

    // Update track name periodically
    setInterval(() => {
        if (trackInfo && window.synthwave.isPlaying) {
            trackInfo.textContent = window.synthwave.getTrackName();
        }
    }, 5000);
});
