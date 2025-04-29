# IoT Object Detection App

This project is an AI-powered object detection application designed to run on a Raspberry Pi. It consists of a **frontend** built with Vue.js and a **backend** powered by TensorFlow Lite for object detection. The application uses the **SSD MobileNet** dataset for object classification.

## Features

- **Frontend**:
  - Responsive UI with Vue.js.
  - Webcam integration for real-time object detection.
  - Styled with global CSS and scoped styles.

- **Backend**:
  - TensorFlow Lite model loading and inference.
  - Model conversion tools for optimizing TensorFlow models.
  - Logging and environment variable support.
  - Object classification using the **SSD MobileNet** dataset.

---

## Project Structure

### Frontend
- **Framework**: Vue.js
- **Key Components**:
  - `AppHeader`: Header of the application.
  - `HeroIntro`: Introduction section.
  - `WebcamApp`: Webcam-based object detection interface.
- **Global Styles**: Located in `src/assets/styles/global.css`.

### Backend
- **Framework**: Python
- **Key Features**:
  - TensorFlow Lite model loading (`model_loader.py`).
  - Model conversion script (`tools/modelconverter.py`).
  - Environment variable support via `.env`.
  - Pre-trained **SSD MobileNet** model for object detection.

---

## Setup Instructions

### Prerequisites
- **Frontend**:
  - Node.js and npm installed.
- **Backend**:
  - Python 3.8+ installed.
  - TensorFlow and TensorFlow Lite dependencies installed.

---

### Frontend Setup

1. Navigate to the `frontend` directory:
   ```bash
   cd frontend
   ```

2. Install dependencies:
   ```bash
   npm install
   ```

3. Run the development server:
   ```bash
   npm run serve
   ```

4. Build for production:
   ```bash
   npm run build
   ```

5. Lint and fix files:
   ```bash
   npm run lint
   ```

---

### Backend Setup

1. Navigate to the `backend` directory:
   ```bash
   cd backend
   ```

2. Install Python dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Set up environment variables:
   - Create a `.env` file in the `backend` directory.
   - Add the following:
     ```
     MODEL_PATH=path/to/your/ssd_mobilenet.tflite
     ```

4. Run the backend service:
   ```bash
   python app/main.py
   ```

5. Convert a TensorFlow model to TensorFlow Lite:
   ```bash
   python tools/modelconverter.py
   ```

---

## Usage

1. Start the backend service to load the TensorFlow Lite model.
2. Run the frontend application to access the UI.
3. Use the webcam interface to detect objects in real-time using the **SSD MobileNet** model.

---

## File Overview

### Frontend
- `src/App.vue`: Main Vue component.
- `src/components`: Contains reusable Vue components.
- `src/assets/styles/global.css`: Global styles for the application.
- `babel.config.js`: Babel configuration for Vue.
- `vue.config.js`: Vue CLI configuration.

### Backend
- `app/services/model_loader.py`: Loads TensorFlow Lite models.
- `tools/modelconverter.py`: Converts TensorFlow models to TensorFlow Lite.
- `.env`: Environment variables for backend configuration.

---

## Resources

- [Vue.js Documentation](https://vuejs.org/)
- [TensorFlow Lite Documentation](https://www.tensorflow.org/lite)
- [SSD MobileNet Documentation](https://github.com/tensorflow/models/blob/master/research/object_detection/g3doc/detection_model_zoo.md)
- [Raspberry Pi Documentation](https://www.raspberrypi.org/documentation/)

---

## License

This project is licensed under the MIT License.