<template>
    <div class="webcam-app">
      <HeroIntro />
      <div class="webcam-controls">
        <button @click="toggleWebcam" class="toggle-webcam-button">
          {{ isWebcamActive ? "Stop Webcam" : "Start Webcam" }}
        </button>
      </div>
      <div v-if="isWebcamActive" class="webcam-feed-container">
        <WebcamFeed />
      </div>
    </div>
  </template>

<script>
import HeroIntro from "./HeroIntro.vue";
import WebcamFeed from "./WebcamFeed.vue";

export default {
  name: "WebcamApp",
  components: {
    WebcamFeed,
    HeroIntro
  },
  data() {
    return {
      isWebcamActive: false,
    };
  },
  methods: {
    toggleWebcam() {
      this.isWebcamActive = !this.isWebcamActive;
    },
  },
};
</script>