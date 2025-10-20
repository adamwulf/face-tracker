# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a browser-based face tracking application that uses MediaPipe Face Mesh to detect and track facial features in real-time via webcam. The application displays facial landmarks overlaid on the webcam feed and drives an animated cartoon face that mirrors the user's expressions.

## Architecture

### Single-Page Application Structure
- **index.html**: Complete standalone application (no build process required)
  - Vanilla JavaScript implementation with no framework dependencies
  - MediaPipe Face Mesh loaded via CDN
  - Self-contained CSS styling and JavaScript logic

### Core Components

**FaceTracker Class** (index.html:230-719)
- Main application controller managing video capture, face detection, and animation
- Key responsibilities:
  - Webcam stream management
  - MediaPipe Face Mesh integration
  - Real-time landmark processing
  - Canvas overlay rendering for webcam
  - SVG animation for cartoon face

### Face Landmark System

MediaPipe Face Mesh provides 468 facial landmarks. The application uses specific landmark indices for different features:

- **Eyes**:
  - Left eye: landmarks 33, 7, 163, 144, 145, 153, 154, 155, 133, 173, 157, 158, 159, 160, 161, 246
  - Right eye: landmarks 362, 382, 381, 380, 374, 373, 390, 249, 263, 466, 388, 387, 386, 385, 384, 398
- **Mouth**: Uses inner lip contour (specific indices in fullMouthIndices array)
- **Nose**: landmarks 1, 2, 5, 4, 6, 19, 20, 94, 125, 141, 235, 236, 3, 51, 48, 115, 131, 134, 102, 49, 220, 305, 281, 360, 279
- **Ears**: Approximated using face contour points (no dedicated ear landmarks in MediaPipe)

### Animation System

**Dual Display Architecture**:
1. **Webcam Canvas Overlay** (index.html:32-43): Draws colored outlines on facial features over live video
2. **Cartoon Face SVG** (index.html:154-165): Animated character that mirrors user's expressions

**Animation Features**:
- Position smoothing (smoothingFactor: 0.3) to reduce jittery movement
- Automatic blinking system with randomized intervals (2-5 seconds)
- Head rotation based on nose tip position relative to eye landmarks
- Synchronized eye movement using landmark tracking
- Real-time mouth shape mirroring using landmark paths

### User Controls

**Feature Toggles**: Enable/disable rendering of eyes, mouth, nose, and ears
**Animation Sensitivity Sliders**:
- Animation Intensity (0-2): Global multiplier for all animations
- Eye Sensitivity (0-3): Eye movement responsiveness
- Mouth Sensitivity (0-3): Mouth animation responsiveness
- Head Rotation (0-2): Head turn/tilt sensitivity
- Blink Frequency (0-3): Automatic blink rate

## Development

### Running the Application

Open index.html directly in a web browser (no server required):
```bash
open index.html
```

Or use a local server if needed:
```bash
python -m http.server 8000
# Navigate to http://localhost:8000
```

### Python Dependencies

The requirements.txt file contains Python packages that may have been used for prototyping or backend experiments, but the current application is purely client-side JavaScript:
- opencv-python==4.8.1.78
- numpy==1.24.3
- runway-ml==0.1.0
- mediapipe==0.10.7

These are NOT required to run the current application.

### Browser Requirements

- Modern browser with WebRTC support (getUserMedia API)
- Webcam access permissions
- JavaScript enabled

## Key Implementation Details

### MediaPipe Configuration (index.html:299-304)
- maxNumFaces: 1 (single face tracking)
- refineLandmarks: true (higher accuracy for eye and lip tracking)
- minDetectionConfidence: 0.5
- minTrackingConfidence: 0.5

### Coordinate System Transformations
- MediaPipe returns normalized coordinates (0-1)
- Webcam overlay: Scaled to canvas dimensions (640x480)
- Cartoon face: Scaled to SVG viewBox (400x400)

### Blinking System Architecture (index.html:249-258, 577-608)
- Both eyes blink simultaneously
- Random blink image selection from eye-blink-1.png and eye-blink-2.png
- Configurable blink duration (150ms) and frequency intervals
- State machine: isBlinking flag prevents overlapping blinks

## Asset Files

- **facecam-1.png**: Cartoon face background
- **facecam-blank.png**: Alternative background
- **eye-left.png, eye-right.png**: Default eye states
- **eye-blink-1.png, eye-blink-2.png**: Blinking animation frames
- **default-smile.png**: Additional facial expression asset

## Debugging Tips

- Console logs mouth indices length during mouth rendering (index.html:444-446)
- Face detection status shown in UI status bar
- Check browser console for camera access errors
- MediaPipe models loaded from CDN - requires internet connection on first load
