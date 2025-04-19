<template>
  <div class="webcam-app">
    <HeroIntro />
    <div class="webcam-controls">
      <button @click="toggleWebcam" class="toggle-webcam-button">
        {{ isWebcamActive ? "Stop Webcam" : "Start Webcam" }}
      </button>
    </div>
    <div v-if="isWebcamActive" class="webcam-feed-container">
      <WebcamFeed ref="webcamFeed" />
    </div>
    <div v-if="detections.length" class="detections-container">
      <h3>Detections:</h3>
      <ul>
        <li v-for="(detection, index) in detections" :key="index">
          {{ detection.label }} (Confidence: {{ (detection.confidence * 100).toFixed(2) }}%)
        </li>
      </ul>
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
    HeroIntro,
  },
  data() {
    return {
      isWebcamActive: false,
      detections: [],
      websocket: null,
    };
  },
  methods: {
    toggleWebcam() {
      this.isWebcamActive = !this.isWebcamActive;

      if (this.isWebcamActive) {
        this.startWebSocket();
      } else {
        this.stopWebSocket();
      }
    },
    startWebSocket() {
      this.websocket = new WebSocket("ws://localhost:8000/ws/detect");

      this.websocket.onopen = () => {
        console.log("WebSocket connection established");
        this.sendFrames();
      };

      this.websocket.onmessage = (event) => {
        const data = JSON.parse(event.data);
        if (data.detections) {
          this.detections = data.detections;

          // Pass detections to WebcamFeed to draw bounding boxes
          const webcamFeed = this.$refs.webcamFeed;
          webcamFeed.drawBoundingBoxes(this.detections);
        } else if (data.error) {
          console.error("Error from backend:", data.error);
        }
      };

      this.websocket.onclose = () => {
        console.log("WebSocket connection closed");
      };
    },
    stopWebSocket() {
      if (this.websocket) {
        this.websocket.close();
        this.websocket = null;
      }
    },
    async sendFrames() {
      const webcamFeed = this.$refs.webcamFeed;

      while (this.isWebcamActive && this.websocket && this.websocket.readyState === WebSocket.OPEN) {
        // Capture the current frame as Base64-encoded image data
        const imageData = webcamFeed.captureFrame();

        // Send the Base64 image data to the backend
        this.websocket.send(imageData);

        // Wait for a short interval before sending the next frame
        await new Promise((resolve) => setTimeout(resolve, 100));
      }
    },
  },
};
</script>

<style>
.webcam-app {
  display: flex;
  flex-direction: column;
  align-items: center;
  padding: 20px;
}

</style>