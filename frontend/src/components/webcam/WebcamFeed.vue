<template>
  <div ref="videoWrapper" class="webcam-container">
    <video ref="webcam" autoplay playsinline></video>
    <canvas ref="videoCanvas" class="video-canvas"></canvas>
    <canvas ref="overlayCanvas" class="overlay-canvas"></canvas>
  </div>
</template>

<script>
import { getRandomColor } from "../../utils/labelColors";

export default {
  name: "WebcamFeed",
  data() {
    return {
      labelColorMap: {},
    };
  },
  mounted() {
    this.startWebcam();
    window.addEventListener("resize", this.onResize);
  },
  beforeUnmount() {
    window.removeEventListener("resize", this.onResize);
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
          this.setupCanvasDimensions();
          this.renderVideoToCanvas();
        };
      } catch (error) {
        console.error("Error accessing webcam:", error);
      }
    },
    setupCanvasDimensions() {
      const video = this.$refs.webcam;
      const videoCanvas = this.$refs.videoCanvas;
      const overlayCanvas = this.$refs.overlayCanvas;
      const videoWrapper = this.$refs.videoWrapper;

      // Get the original video dimensions
      const originalWidth = video.videoWidth;
      const originalHeight = video.videoHeight;

      // Calculate the aspect ratio
      const aspectRatio = originalWidth / originalHeight;

      // Set the container width based on the screen size
      const containerWidth = Math.min(window.innerWidth * 0.9, 640); // 90% of screen width or max 640px
      const containerHeight = containerWidth / aspectRatio;

      // Update canvas and container dimensions
      [videoCanvas, overlayCanvas].forEach((canvas) => {
        canvas.width = originalWidth;
        canvas.height = originalHeight;
        canvas.style.width = `${containerWidth}px`;
        canvas.style.height = `${containerHeight}px`;
      });

      videoWrapper.style.width = `${containerWidth}px`;
      videoWrapper.style.height = `${containerHeight}px`;
    },
    onResize() {
      // Recalculate dimensions on window resize
      if (this.$refs.webcam.readyState === this.$refs.webcam.HAVE_ENOUGH_DATA) {
        this.setupCanvasDimensions();
      }
    },
    renderVideoToCanvas() {
      const video = this.$refs.webcam;
      const videoCanvas = this.$refs.videoCanvas;
      const context = videoCanvas.getContext("2d");

      const render = () => {
        if (video.readyState === video.HAVE_ENOUGH_DATA) {
          context.drawImage(video, 0, 0, videoCanvas.width, videoCanvas.height);
        }
        requestAnimationFrame(render);
      };

      render();
    },
    captureFrame() {
      const videoCanvas = this.$refs.videoCanvas;
      return videoCanvas.toDataURL("image/jpeg").split(",")[1];
    },
    drawBoundingBoxes(detections) {
      const overlayCanvas = this.$refs.overlayCanvas;
      const context = overlayCanvas.getContext("2d");

      // Clear the overlay canvas
      context.clearRect(0, 0, overlayCanvas.width, overlayCanvas.height);

      // Draw each bounding box
      detections.forEach((detection) => {
        const { ymin, xmin, ymax, xmax, label, confidence } = detection;

        if (!this.labelColorMap[label]) {
          this.labelColorMap[label] = getRandomColor();
        }
        const color = this.labelColorMap[label];

        // Draw the rectangle
        context.strokeStyle = color;
        context.lineWidth = 2;
        context.strokeRect(xmin, ymin, xmax - xmin, ymax - ymin);

        // Draw the label and confidence
        context.fillStyle = color;
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
  width: 100%;
  max-width: 640px;
  margin: 0 auto;
  box-shadow: 0 8px 16px rgba(0, 0, 0, 0.5);
  border-radius: 8px;
}

.webcam-container video{
  display: none;
}

.video-canvas,
.overlay-canvas {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: auto;
  border-radius: 8px;
}

@media screen and (max-width: 768px) {
  .webcam-container {
    max-width: 100%;
    padding: 0 10px;
  }

  .video-canvas,
  .overlay-canvas {
    border-radius: 4px;
  }
}
</style>