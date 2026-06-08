import os
import streamlit as st
import base64
import cv2
import numpy as np
from ultralytics import YOLO
import supervision as sv
from supervision import Detections
from openai import OpenAI
from dotenv import load_dotenv
load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
model_path = 'yolov12n_vehiclebest.pt'
model = YOLO(model_path)
classes = ['bus', 'car', 'van']

import json
import datetime

# Create corrections folder
CORRECTIONS_FOLDER = "corrections"
if not os.path.exists(CORRECTIONS_FOLDER):
    os.makedirs(CORRECTIONS_FOLDER)

# Session state for manual corrections
if 'corrections' not in st.session_state:
    st.session_state.corrections = []
if 'original_image' not in st.session_state:
    st.session_state.original_image = None
if 'current_annotated_image' not in st.session_state:
    st.session_state.current_annotated_image = None
if 'deleted_indices' not in st.session_state:
    st.session_state.deleted_indices = set()
if 'current_detections' not in st.session_state:
    st.session_state.current_detections = None

st.set_page_config(page_title="Vehicle Detection", layout="wide")
st.title("Vehicle Detection")

## ------------------------------    Sidebar      -----------------------------------------------------------------
st.sidebar.header("Model Configurations")
model_type = st.sidebar.radio("Task", ["Detection"])
correction_mode = st.sidebar.radio("Correction Mode", ["None", "Add Box", "Delete Box"], key="correction_mode")

def save_correction_as_training_data(image, detection_info, correction_type):
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    correction_data = {"timestamp": timestamp, "correction_type": correction_type, "detection_info": detection_info, "image_shape": image.shape}
    st.session_state.corrections.append(correction_data)
    correction_path = os.path.join(CORRECTIONS_FOLDER, f"corrections_{timestamp}.json")
    with open(correction_path, "w") as f: json.dump(correction_data, f)
    return timestamp

def reannotate_image(image_rgb, detections):
    box_annotator = sv.BoxAnnotator()
    label_annotator = sv.LabelAnnotator()
    
    labels = [f"{classes[class_id]} {confidence:.2f}"
    for class_id, confidence in zip(detections.class_id, detections.confidence)]
    
    annotated_image = image_rgb.copy()
    if len(detections) > 0:
        annotated_image = box_annotator.annotate(scene=annotated_image, detections=detections)
        annotated_image = label_annotator.annotate(scene=annotated_image, detections=detections, labels=labels)
    return annotated_image

## -----------------------------------------    Vehicle Detection       ---------------------------------------------
st.markdown("Upload an image to detect vehicles")
uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    file_bytes = np.asarray(bytearray(uploaded_file.read()), dtype=np.uint8)
    image = cv2.imdecode(file_bytes,1)
    image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    st.session_state.original_image = image_rgb.copy()

    # Run inference only if this is a new image
    if st.session_state.current_detections is None or 'last_uploaded' not in st.session_state or st.session_state.last_uploaded != uploaded_file.name:
        results = model(image_rgb, verbose=False)[0]
        detections = sv.Detections.from_ultralytics(results)
        st.session_state.current_detections = detections
        st.session_state.deleted_indices = set()
        st.session_state.last_uploaded = uploaded_file.name
    
    # Get current detections from session state
    detections = st.session_state.current_detections
    
    # Remove deleted detections
    if len(st.session_state.deleted_indices) > 0 and len(detections) > 0:
        keep_indices = [i for i in range(len(detections)) if i not in st.session_state.deleted_indices]
        if keep_indices:
            detections = detections[keep_indices]
        else:
            detections = sv.Detections.empty()
        st.session_state.current_detections = detections
    
    # Annotate and display image
    annotated_image = reannotate_image(image_rgb, detections)
    st.session_state.current_annotated_image = annotated_image
    st.image(annotated_image, caption="Image for Vehicle Detections", use_container_width=True)
    
    # Count vehicles
    car_detections = detections[detections.class_id == classes.index('car')] if len(detections) > 0 else sv.Detections.empty()
    van_detections = detections[detections.class_id == classes.index('van')] if len(detections) > 0 else sv.Detections.empty()
    bus_detections = detections[detections.class_id == classes.index('bus')] if len(detections) > 0 else sv.Detections.empty()
        
    car_qty = len(car_detections)
    van_qty = len(van_detections)
    bus_qty = len(bus_detections)
    
    col1, col2, col3 = st.columns(3)
    with col1: st.metric("🚗 Cars", car_qty)
    with col2: st.metric("🚐 Vans", van_qty)
    with col3: st.metric("🚌 Buses", bus_qty)
    
    ## ------------------ MANUAL CORRECTION SECTION  ----------------------------------------------------------------------------
    st.markdown("---")
    st.subheader("✏️ Manual Correction")
    
    if correction_mode == "Delete Box" and len(detections) > 0:
        st.warning("🗑️ Delete Mode Active - Click delete button next to any detection")
        
        st.write("**Current Detections:**")
        for idx, (class_id, conf) in enumerate(zip(detections.class_id, detections.confidence)):
            col_a, col_b, col_c = st.columns([2, 2, 1])
            with col_a: st.write(f"**{idx+1}.** {classes[class_id]}")
            with col_b: st.write(f"Confidence: {conf:.2f}")
            with col_c:
                if st.button(f"🗑️ Delete", key=f"delete_btn_{idx}"):
                    st.session_state.deleted_indices.add(idx)
                    correction_info = {"class": classes[class_id], "confidence": float(conf), "original_index": idx, "type": "deletion"}
                    save_correction_as_training_data(image_rgb, correction_info, "delete_box")
                    st.rerun()
        
        if st.button("🔄 Reset All Deletions"):
            st.session_state.deleted_indices = set()
            st.rerun()
    
    elif correction_mode == "Add Box":
        st.write("**Add New Detection:**")
        st.info("📝 Enter coordinates for the bounding box. Use the image above as reference.")
        
        # Display image with grid for coordinate reference
        if st.checkbox("Show coordinate grid overlay"):
            grid_img = image_rgb.copy()
            h, w = grid_img.shape[:2]
            # Draw grid lines every 100 pixels
            for x in range(0, w, 100):
                cv2.line(grid_img, (x, 0), (x, h), (200, 200, 200), 1)
            for y in range(0, h, 100):
                cv2.line(grid_img, (0, y), (w, y), (200, 200, 200), 1)
            # Add coordinate labels
            for x in range(0, w, 100):
                cv2.putText(grid_img, str(x), (x+5, 20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 1)
            for y in range(0, h, 100):
                cv2.putText(grid_img, str(y), (5, y+15), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 1)
            st.image(grid_img, caption="Reference Grid (100px intervals)", use_container_width=True)
        
        col_a, col_b, col_c = st.columns(3)
        with col_a:
            new_class = st.selectbox("Class", classes, key="add_class")
            new_conf = st.slider("Confidence", 0.0, 1.0, 0.8, 0.01, key="add_conf")
        with col_b:
            st.write("**Top-Left Corner**")
            x1 = st.number_input("X1", 0, image_rgb.shape[1], 100, key="x1")
            y1 = st.number_input("Y1", 0, image_rgb.shape[0], 100, key="y1")
        with col_c:
            st.write("**Bottom-Right Corner**")
            x2 = st.number_input("X2", 0, image_rgb.shape[1], 200, key="x2")
            y2 = st.number_input("Y2", 0, image_rgb.shape[0], 150, key="y2")
        
        # Preview the box
        if x1 < x2 and y1 < y2:
            preview = image_rgb.copy()
            cv2.rectangle(preview, (x1, y1), (x2, y2), (0, 255, 0), 3)
            cv2.putText(preview, f"{new_class} {new_conf:.2f}", (x1, max(y1-5, 15)), 
                       cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)
            st.image(preview, caption="Preview - Box will appear here", use_container_width=True)
        else:
            st.error("⚠️ X1 must be less than X2 and Y1 must be less than Y2")
        
        if st.button("➕ Add Detection", key="add_btn"):
            if x1 < x2 and y1 < y2:
                new_bbox = np.array([[x1, y1, x2, y2]])
                new_detection = Detections(xyxy=new_bbox,
                    confidence=np.array([new_conf]),
                    class_id=np.array([classes.index(new_class)]))
                
                if len(detections) > 0:
                    combined_xyxy = np.vstack([detections.xyxy, new_detection.xyxy])
                    combined_confidence = np.hstack([detections.confidence, new_detection.confidence])
                    combined_class_id = np.hstack([detections.class_id, new_detection.class_id])
                    
                    detections = Detections(xyxy=combined_xyxy,
                        confidence=combined_confidence,
                        class_id=combined_class_id)
                else:
                    detections = new_detection
                
                st.session_state.current_detections = detections
                
                correction_info = {"class": new_class, "confidence": new_conf, "bbox": [x1, y1, x2, y2], "type": "manual_addition"}
                save_correction_as_training_data(image_rgb, correction_info, "add_box")
                st.success(f"✅ Added {new_class} at position ({x1},{y1}) to ({x2},{y2})")
                st.rerun()
            else:
                st.error("Invalid coordinates. Please fix the box coordinates.")
    
    # Display correction count
    if len(st.session_state.corrections) > 0:
        st.info(f"📝 {len(st.session_state.corrections)} corrections saved for this session")
        if st.button("💾 Export All Corrections"):
            timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
            export_path = os.path.join(CORRECTIONS_FOLDER, f"all_corrections_{timestamp}.json")
            with open(export_path, "w") as f:
                json.dump(st.session_state.corrections, f, indent=2)
            st.success(f"Saved {len(st.session_state.corrections)} corrections to {export_path}")
    
    ## ----------------------   OCR   -----------------------------------------------------------------------
    st.markdown("---")
    st.subheader("License Plate Recognition")
    
    def ai_ocr_carplate(image_np):
        try:
            _, buffer = cv2.imencode('.jpg', cv2.cvtColor(image_np, cv2.COLOR_RGB2BGR))
            b64_image = base64.b64encode(buffer).decode("utf-8")
            
            response = client.chat.completions.create(model='gpt-4o-mini',
                messages=[{"role": "user",
                        "content": [{"type": "text", "text": "Extract every vehicle license plate number detected as a bus, van, or car from this image. Return only the plate numbers as a comma-separated list. If no plates are visible, return 'None'."},
                            {"type": "image_url","image_url": {"url": f"data:image/jpeg;base64,{b64_image}"}}]}],)
            return response.choices[0].message.content
        except Exception as e:
            return f"Error: {str(e)}"
    
    if st.button("🔍 Extract License Plates with AI"):
        with st.spinner("Analyzing image with GPT-4o..."):
            plate_result = ai_ocr_carplate(image_rgb)
            st.success("Analysis Complete!")
            st.subheader("Detected License Plates:")
            st.write(plate_result)
            
            if plate_result != "None":
                timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
                plates_path = os.path.join(CORRECTIONS_FOLDER, f"plates_{timestamp}.txt")
                with open(plates_path, "w") as f:
                    f.write(f"Image: {uploaded_file.name}\n")
                    f.write(f"Plates: {plate_result}\n")
                    f.write(f"Vehicles: {car_qty} cars, {bus_qty} buses, {van_qty} vans\n")
                st.info(f"Results saved to {plates_path}")

else:
    st.info("📤 Please upload an image to get started.")