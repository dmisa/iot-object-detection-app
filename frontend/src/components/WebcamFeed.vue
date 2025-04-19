<template>
  <div ref="videoWrapper" class="webcam-container">
    <video ref="webcam" autoplay playsinline></video>
    <canvas ref="videoCanvas" class="video-canvas"></canvas>
    <canvas ref="overlayCanvas" class="overlay-canvas"></canvas>
  </div>
</template>

<script>
import { getRandomColor } from "../utils/labelColors";

export default {
  name: "WebcamFeed",
  data() {
    return {
      labelColorMap: {},
    };
  },
  mounted() {
    this.startWebcam();
  },
  methods: {
    async startWebcam() {
      try {
        const stream = await navigator.mediaDevices.getUserMedia({ video: true });
        const video = this.$refs.webcam;
        video.srcObject = stream;

        // Wait for the video to be ready
        video.onloadedmetadata = () => {
          video.play();
          this.renderVideoToCanvas();
        };
      } catch (error) {
        console.error("Error accessing webcam:", error);
      }
    },
    renderVideoToCanvas() {
      const video = this.$refs.webcam;
      const videoCanvas = this.$refs.videoCanvas;
      const videoWrapper = this.$refs.videoWrapper;

      const context = videoCanvas.getContext("2d");

      // Set canvas dimensions to match the video
      videoCanvas.width = video.videoWidth;
      videoCanvas.height = video.videoHeight;

      videoCanvas.style.width = `${videoCanvas.width}px`;
      videoCanvas.style.height = `${videoCanvas.height}px`;

      videoWrapper.style.width = `${video.videoWidth}px`;
      videoWrapper.style.height = `${video.videoHeight}px`;

      const render = () => {
        // Ensure the video feed is ready before drawing
        if (video.readyState === video.HAVE_ENOUGH_DATA) {
          context.drawImage(video, 0, 0, videoCanvas.width, videoCanvas.height);
        }
        requestAnimationFrame(render); // Continuously render the video feed
      };

      render();
    },
    captureFrame() {
      const videoCanvas = this.$refs.videoCanvas;

      // Capture the current frame from the video canvas
      const base64Image = videoCanvas.toDataURL("image/jpeg"); // Get the full Base64 string
      return base64Image.split(",")[1]; // Remove the "data:image/jpeg;base64," prefix
    },
    drawBoundingBoxes(detections) {
      const overlayCanvas = this.$refs.overlayCanvas;
      const context = overlayCanvas.getContext("2d");

      // Set canvas dimensions to match the video
      overlayCanvas.width = this.$refs.videoCanvas.width;
      overlayCanvas.height = this.$refs.videoCanvas.height;

      // Clear the overlay canvas
      context.clearRect(0, 0, overlayCanvas.width, overlayCanvas.height);

      // Draw each bounding box
      detections.forEach((detection) => {
        const { ymin, xmin, ymax, xmax, label, confidence } = detection;

        // Assign a color to the label if it doesn't already have one
        if (!this.labelColorMap[label]) {
          this.labelColorMap[label] = getRandomColor();
        }
        const color = this.labelColorMap[label];

        // Draw the rectangle
        context.strokeStyle = color; // Use the color from the mapping
        context.lineWidth = 2;
        context.strokeRect(xmin, ymin, xmax - xmin, ymax - ymin);

        // Draw the label and confidence
        context.fillStyle = color; // Use the color from the mapping
        context.font = "16px Arial";
        context.fillText(
          `${label} (${(confidence * 100).toFixed(1)}%)`,
          xmin,
          ymin - 5
        );
      });
    },
  },
};
</script>

<style>
.webcam-container {
  display: flex;
  justify-content: center;
  align-items: center;
  position: relative;
}

video {
  display: none;
}

.video-canvas {
  position: absolute;
  top: 0;
  left: 0;
  width: 80%;
  max-width: 640px;
  border-radius: 8px;
}

.overlay-canvas {
  position: absolute;
  top: 0;
  left: 0;
  width: 80%;
  max-width: 640px;
}
</style>