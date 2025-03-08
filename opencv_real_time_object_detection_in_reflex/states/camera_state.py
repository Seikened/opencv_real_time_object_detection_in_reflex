
import reflex as rx
from typing import TypedDict, List
import cv2
import base64
import numpy as np
import asyncio

class DetectionResult(TypedDict):
    id: int
    label: str
    confidence: float
    x: int
    y: int
    width: int
    height: int

class CameraState(rx.State):
    # Stream state
    camera_active: bool = False
    processing_active: bool = False
    current_frame: str = ""  # Base64 encoded image
    error_message: str = ""
    
    # Performance metrics
    fps: float = 0.0
    frame_count: int = 0
    last_frame_time: float = 0.0

    @rx.event
    def toggle_camera(self):
        self.camera_active = not self.camera_active
        if self.camera_active:
            return CameraState.process_camera_feed
        else:
            self.current_frame = ""

    @rx.event(background=True)
    async def process_camera_feed(self):
        try:
            cap = cv2.VideoCapture(0)
            if not cap.isOpened():
                async with self:
                    self.error_message = "Failed to open camera"
                    self.camera_active = False
                return

            async with self:
                self.processing_active = True
                self.error_message = ""

            while self.camera_active:
                ret, frame = cap.read()
                if not ret:
                    break

                # Convert frame to base64 for display
                _, buffer = cv2.imencode('.jpg', frame)
                img_base64 = base64.b64encode(buffer).decode('utf-8')
                
                # Update state with new frame
                async with self:
                    self.current_frame = f"data:image/jpeg;base64,{img_base64}"
                    self.frame_count += 1
                
                # Control frame rate
                await asyncio.sleep(1/30)  # Limit to ~30 fps
                
            cap.release()
            
        except Exception as e:
            async with self:
                self.error_message = f"Camera error: {str(e)}"
                self.camera_active = False
                self.processing_active = False
        
        finally:
            async with self:
                self.processing_active = False

