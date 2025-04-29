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
    <p v-if="errorMessage" class="error">{{ errorMessage }}</p>
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
      retryCount: 0,
      maxRetries: 5,
      errorMessage: '',
    };
  },
  methods: {
    toggleWebcam() {
      this.isWebcamActive = !this.isWebcamActive;

      if (this.isWebcamActive) {
        this.startWebSocket();
      } else {
        this.stopWebSocket();
        this.detections = [];
        this.errorMessage = '';
        this.retryCount = 0;
      }
    },

    startWebSocket() {
      this.websocket = new WebSocket("ws://localhost:8000/ws/detect");

      this.websocket.onopen = () => {
        console.log("WebSocket connection established");
        this.retryCount = 0;
        this.errorMessage = '';
        this.sendFrames();
      };

      this.websocket.onmessage = (event) => {
        try {
          const data = JSON.parse(event.data);
          if (data.detections) {
            this.detections = data.detections;
            const webcamFeed = this.$refs.webcamFeed;
            webcamFeed.drawBoundingBoxes(this.detections);
          } else if (data.error) {
            console.error("Error from backend:", data.error);
            this.errorMessage = `Backend error: ${data.error}`;
          }
        } catch (err) {
          console.error("Error parsing WebSocket message:", err);
          this.errorMessage = "Error processing data from server.";
        }
      };

      this.websocket.onerror = (event) => {
        console.error("WebSocket error:", event);
        this.errorMessage = "WebSocket encountered an error.";
      };

      this.websocket.onclose = () => {
        console.warn("WebSocket closed");

        if (this.isWebcamActive && this.retryCount < this.maxRetries) {
          this.retryCount++;
          this.errorMessage = `WebSocket connection lost. Retrying (${this.retryCount}/${this.maxRetries})...`;
          setTimeout(() => this.startWebSocket(), 2000);
        } else if (this.isWebcamActive) {
          this.errorMessage = "Failed to connect to WebSocket after multiple attempts.";
        }
      };
    },

    stopWebSocket() {
      if (this.websocket) {
        this.websocket.onopen = null;
        this.websocket.onmessage = null;
        this.websocket.onerror = null;
        this.websocket.onclose = null;
        this.websocket.close();
        this.websocket = null;
      }
    },

    async sendFrames() {
      const webcamFeed = this.$refs.webcamFeed;

      while (this.isWebcamActive && this.websocket && this.websocket.readyState === WebSocket.OPEN) {
        const imageData = webcamFeed.captureFrame();
        this.websocket.send(imageData);
        await new Promise((resolve) => setTimeout(resolve, 200));
      }
    },
  },

  beforeUnmount() {
    this.stopWebSocket();
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

  .error {
    color: red;
    font-weight: bold;
    padding: 1rem;
  }
</style>
