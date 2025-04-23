<template>
  <div class="webcam-app">
    <div class="webcam-controls">
      <button @click="toggleWebcam" class="toggle-webcam-button primary">
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
import WebcamFeed from "./WebcamFeed.vue";

export default {
  name: "WebcamApp",
  components: {
    WebcamFeed,
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
        const imageData = webcamFeed.captureFrame();
        this.websocket.send(imageData);
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

  .detections-container {
    margin-top: 20px;
    background-color: #2c2c2c;
    color: #ffffff;
    padding: 10px;
    border-radius: 5px;
    width: 100%;
    max-width: 640px;
    box-shadow: 0 8px 16px rgba(0, 0, 0, 0.5);
  }

  .detections-container h3 {
    color: #ffffff;
  }

  .detections-container ul {
    list-style-type: none;
    padding: 0;
  }

  .detections-container li {
    margin: 5px 0;
    padding: 5px;
    background-color: #444444;
    color: #ffffff;
  }
</style>