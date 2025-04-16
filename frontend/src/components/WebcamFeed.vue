<template>
    <div class="webcam-container">
      <video ref="webcam" autoplay playsinline></video>
    </div>
</template>
  
  <script>
  export default {
    name: "WebcamFeed",
    mounted() {
      this.startWebcam();
    },
    methods: {
      async startWebcam() {
        try {
          const stream = await navigator.mediaDevices.getUserMedia({ video: true });
          this.$refs.webcam.srcObject = stream;
        } catch (error) {
          console.error("Error accessing webcam:", error);
        }
      },
    },
  };
  </script>
  
  <style>
  .webcam-container {
    display: flex;
    justify-content: center;
    align-items: center;
  }
  
  video {
    width: 80%;
    max-width: 640px;
    border: 2px solid #2c3e50;
    border-radius: 8px;
  }
  </style>