
  

  

# Django WebRTC Broadcasting Application

  

  

A real-time video broadcasting application built with Django and WebRTC. This application allows users to create WebRTC broadcasts and share them with viewers through unique stream IDs.

  

  

  

## Features

  

  

* Real-time video broadcasting using WebRTC

  

  

* WebSocket-based signaling server built with Django Channels

  

  

* Unique stream IDs for each broadcast

  

  

* Dedicated broadcaster and viewer interfaces

  

  

* Containerized deployment with Docker

  

  

  

## Prerequisites

* Docker

  

## Installation with Docker (Recommended)

  

  

1.  **Clone the repository**

   
```bash
git  clone <repository-url>
cd <project-directory>
```

2.  **Build the Docker image**

```bash
sudo docker  build  -t  django-webrtc-app  .
```


3.  **Run the container**

```bash
sudo docker  run  -p  8000:8000  django-webrtc-app
```

  

  

## Usage

  

  

  

After starting the application, you can access:

  

  

  

*  **Broadcaster interface**: http://localhost:8000/broadcast/

  

  

*  **Generate stream ID**: http://localhost:8000/api/get-stream-id/

  

  

*  **Viewer interface**: http://localhost:8000/view/<stream_id>/

  

  

## WebRTC Signaling Flow

  

  

1. Broadcaster creates a stream with unique ID

  

  

2. Viewers connect to the stream using this ID

  

  

3. WebSocket connections established through `/ws/webrtc/<stream_id>/`

  

  

4. WebRTC signaling messages (offers, answers, ICE candidates) exchanged through WebSockets

  

  

5. Direct peer-to-peer connection established between broadcaster and viewers

  

  

  

## Production Considerations

  

  

For production deployment:

  

  

* Replace `InMemoryChannelLayer` with Redis backend for Channels

  

  

* Set `DEBUG=False` in settings

  

  

* Use proper secret key management

  

  

* Configure HTTPS (required for WebRTC in production)

  

  

* Consider adding authentication for broadcasters

  

  

  

## Docker Configuration

  

  

The included Dockerfile:

  

  

* Uses Alpine Linux for minimal image size

  

  

* Implements multi-stage build to reduce final image size

  

  

* Runs as a non-root user for better security

  

  

* Exposes port 8000 for the Daphne ASGI server


