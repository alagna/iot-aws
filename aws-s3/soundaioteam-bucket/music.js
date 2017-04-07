const Music = {
  create: function (options = {}) {
    const audioCtx = new (window.AudioContext || window.webkitAudioContext)();

    // create Oscillator node
    const oscillatorNode = audioCtx.createOscillator();

    // create Gain node
    const gainNode = audioCtx.createGain();

    oscillatorNode.type = options.type || 'square';
    gainNode.gain.value = 0;

    oscillatorNode.connect(gainNode);
    gainNode.connect(audioCtx.destination);

    oscillatorNode.start();

    let stopped = false;

    const api = {
      playTone(frequency, volume) {
        api.setVolume(volume);
        api.setFrequency(frequency);
      },

      setFrequency(frequency) {
        if (stopped) {
          return;
        }

        oscillatorNode.frequency.value = Math.min(3951, Math.max(66, frequency));
      },

      setVolume(volume) {
        if (stopped) {
          return;
        }

        gainNode.gain.setValueAtTime(Math.min(1, Math.max(0, volume)), audioCtx.currentTime + 0.00);
      },

      start() {
        stopped = false;
      },

      stop() {
        api.setVolume(0);
        stopped = true;
      }
    }

    return api;
  }
};
