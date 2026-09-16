import streamlit as st
import cv2
import os
import hashlib
import subprocess
import json
import zipfile
from pathlib import Path
from datetime import datetime
import time
from ultralytics import YOLO
import imageio_ffmpeg

# ============================================================
# BORDER SURVEILLANCE COMMAND CENTER
# Fast + Professional Command Center
# ============================================================

st.set_page_config(
    page_title="Border Surveillance Command Center",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded",
)

# -----------------------------
# Professional dark UI
# -----------------------------
st.markdown(
    """
    <style>
    .stApp {
        background: #0A0B0C;
        color: #F0F0EC;
    }

    [data-testid="stHeader"] {
        background: #0A0B0C;
    }

    [data-testid="stSidebar"] {
        background: #101214;
        border-right: 1px solid #303438;
    }

    [data-testid="stSidebar"] > div:first-child {
        padding-top: 2rem;
    }

    .block-container {
        padding-top: 2.8rem !important;
        padding-bottom: 3rem !important;
        max-width: 1500px;
    }

    h1, h2, h3 {
        color: #f4f8fc !important;
    }

    .hero {
        background: linear-gradient(135deg, #151719 0%, #1C1F22 100%);
        border: 1px solid #3A3E42;
        border-radius: 18px;
        padding: 28px 30px;
        margin-bottom: 20px;
    }

    .hero-title {
        font-size: 34px;
        font-weight: 800;
        letter-spacing: 0.5px;
        color: #F4F3EF;
        margin-bottom: 7px;
    }

    .hero-subtitle {
        color: #A7A7A1;
        font-size: 16px;
        line-height: 1.6;
    }

    .status {
        display: inline-block;
        padding: 7px 13px;
        border-radius: 999px;
        background: #202224;
        border: 1px solid #6B6E71;
        color: #E0E0DB;
        font-size: 12px;
        font-weight: 800;
        letter-spacing: 1px;
        margin-bottom: 14px;
    }

    .pipeline {
        background: #121416;
        border: 1px solid #34383C;
        border-radius: 16px;
        padding: 18px;
    }

    .pipeline-item {
        background: #1C1F22;
        border: 1px solid #41454A;
        border-radius: 9px;
        padding: 10px 12px;
        margin: 7px 0;
        color: #DADBD7;
        font-size: 13px;
        font-weight: 700;
    }

    .section-label {
        color: #8B8D8E;
        font-size: 12px;
        font-weight: 800;
        letter-spacing: 2px;
        text-transform: uppercase;
        margin-top: 25px;
        margin-bottom: 10px;
    }

    .info-card {
        background: #121416;
        border: 1px solid #34383C;
        border-radius: 16px;
        padding: 18px 20px;
        margin: 10px 0;
    }

    .metric-card {
        background: #17191B;
        border: 1px solid #3B3F43;
        border-radius: 15px;
        padding: 18px 20px;
        min-height: 112px;
    }

    .metric-label {
        color: #A4A5A3;
        font-size: 13px;
        margin-bottom: 8px;
    }

    .metric-value {
        color: #F4F3EF;
        font-size: 34px;
        font-weight: 750;
    }

    .incident-card {
        background: #141618;
        border: 1px solid #3A3D40;
        border-radius: 15px;
        padding: 20px;
        margin: 10px 0;
    }

    .incident-title {
        color: #f4f8fc;
        font-size: 21px;
        font-weight: 800;
        margin-bottom: 8px;
    }

    .small-muted {
        color: #9B9D9D;
        font-size: 13px;
    }

    .reason {
        background: #242628;
        border-left: 3px solid #B5B6B3;
        padding: 8px 11px;
        margin: 5px 0;
        border-radius: 4px;
        color: #D9DAD6;
        font-size: 13px;
    }

    .footer {
        color: #777A7B;
        text-align: center;
        font-size: 12px;
        padding: 28px 0 5px 0;
    }

    div[data-testid="stFileUploader"] {
        background: #121416;
        border: 1px solid #3A3E42;
        border-radius: 14px;
        padding: 6px;
    }

    div[data-testid="stButton"] > button {
        border-radius: 9px;
        font-weight: 700;
    }

    .risk-high {
        color: #D8893A;
        font-weight: 800;
    }

    .risk-critical {
        color: #D65353;
        font-weight: 800;
    }

    .risk-medium {
        color: #C8A24A;
        font-weight: 800;
    }

    .steel-rule {
        height: 1px;
        background: #45494C;
        margin: 8px 0 18px 0;
    }

    [data-testid="stMetricValue"] {
        color: #F0F0EC;
    }

    [data-testid="stMetricLabel"] {
        color: #9FA1A0;
    }

    div[data-baseweb="select"] > div {
        background: #17191B;
        border-color: #45494C;
        color: #ECECE7;
    }
    
    /* ========================================================
       PREMIUM COMMAND-CENTER VISUAL SYSTEM
       ======================================================== */

    :root {
        --bg: #080d14;
        --panel: #101925;
        --panel-2: #141f2d;
        --line: rgba(148, 163, 184, 0.18);
        --text: #e8eef7;
        --muted: #91a0b5;
        --accent: #4fd1c5;
        --accent-2: #7c9cff;
        --warning: #f6c85f;
    }

    .stApp {
        background:
            radial-gradient(circle at 10% 0%, rgba(79, 209, 197, 0.08), transparent 28%),
            radial-gradient(circle at 90% 10%, rgba(124, 156, 255, 0.10), transparent 30%),
            linear-gradient(145deg, #080d14 0%, #0b111b 55%, #080d14 100%);
    }

    .block-container {
        max-width: 1600px !important;
        padding: 2.2rem 3rem 4rem !important;
    }

    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #0b121d 0%, #0e1723 100%);
        border-right: 1px solid rgba(148, 163, 184, 0.16);
    }

    [data-testid="stSidebar"] * {
        font-size: 0.93rem;
    }

    .hero {
        position: relative;
        overflow: hidden;
        background:
            linear-gradient(120deg, rgba(20, 31, 45, 0.98), rgba(13, 23, 36, 0.94)),
            radial-gradient(circle at 85% 20%, rgba(79, 209, 197, 0.18), transparent 35%);
        border: 1px solid rgba(148, 163, 184, 0.23);
        border-radius: 24px;
        padding: 34px 38px;
        box-shadow: 0 18px 55px rgba(0, 0, 0, 0.22);
    }

    .hero:after {
        content: "";
        position: absolute;
        width: 240px;
        height: 240px;
        right: -90px;
        top: -100px;
        border: 1px solid rgba(79, 209, 197, 0.28);
        border-radius: 50%;
        box-shadow: 0 0 0 22px rgba(79, 209, 197, 0.035),
                    0 0 0 44px rgba(79, 209, 197, 0.025);
    }

    .hero-title {
        font-size: clamp(1.8rem, 3vw, 3rem);
        line-height: 1.08;
        letter-spacing: -1px;
        background: linear-gradient(90deg, #f3f7fb, #9ee9e1);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }

    .hero-subtitle {
        max-width: 900px;
        color: #a7b6c9;
        font-size: 1rem;
    }

    .status {
        display: inline-flex;
        align-items: center;
        gap: 8px;
        color: #7de4d6 !important;
        background: rgba(79, 209, 197, 0.09);
        border: 1px solid rgba(79, 209, 197, 0.24);
        border-radius: 999px;
        padding: 6px 12px;
        font-size: 0.72rem !important;
        font-weight: 800;
        letter-spacing: 1.3px;
    }

    .section-label {
        margin: 28px 0 12px;
        color: #b7c6d9;
        font-size: 0.75rem;
        font-weight: 800;
        letter-spacing: 1.8px;
        text-transform: uppercase;
    }

    .info-card, .metric-card, .incident-card {
        background: linear-gradient(145deg, rgba(20, 31, 45, 0.96), rgba(13, 22, 34, 0.96));
        border: 1px solid var(--line);
        border-radius: 17px;
        box-shadow: 0 10px 30px rgba(0, 0, 0, 0.12);
    }

    .info-card {
        padding: 17px 20px;
    }

    .metric-card {
        padding: 20px 22px;
        min-height: 112px;
        transition: transform .18s ease, border-color .18s ease;
    }

    .metric-card:hover {
        transform: translateY(-3px);
        border-color: rgba(79, 209, 197, 0.45);
    }

    .metric-label {
        color: #8fa2b9;
        font-size: 0.72rem;
        letter-spacing: 1px;
        text-transform: uppercase;
        font-weight: 800;
    }

    .metric-value {
        margin-top: 9px;
        color: #f2f7fb;
        font-size: 1.85rem;
        font-weight: 850;
        letter-spacing: -0.7px;
    }

    .incident-card {
        padding: 20px 22px;
        margin: 12px 0;
        border-left: 3px solid #f6c85f;
    }

    .incident-title {
        color: #eef5fb;
        font-weight: 800;
        font-size: 1rem;
    }

    .pipeline-item {
        background: rgba(20, 31, 45, 0.78);
        border: 1px solid rgba(148, 163, 184, 0.15);
        border-radius: 10px;
        padding: 10px 12px;
        margin: 7px 0;
        color: #c7d4e4;
    }

    .reason {
        background: rgba(79, 209, 197, 0.07);
        border: 1px solid rgba(79, 209, 197, 0.18);
        border-radius: 10px;
        padding: 9px 12px;
        margin: 6px 0;
        color: #bcece6;
    }

    div.stButton > button, div.stDownloadButton > button {
        width: 100%;
        border-radius: 11px;
        border: 1px solid rgba(79, 209, 197, 0.45);
        background: linear-gradient(135deg, #2d9d98, #3975b9);
        color: white;
        font-weight: 800;
        min-height: 42px;
        box-shadow: 0 7px 18px rgba(39, 125, 154, 0.18);
        transition: transform .18s ease, filter .18s ease;
    }

    div.stButton > button:hover, div.stDownloadButton > button:hover {
        filter: brightness(1.12);
        transform: translateY(-2px);
        border-color: #8deee5;
    }

    [data-testid="stFileUploader"] {
        background: rgba(16, 25, 37, 0.75);
        border: 1px dashed rgba(124, 156, 255, 0.45);
        border-radius: 16px;
        padding: 12px;
    }

    [data-baseweb="select"] > div,
    [data-testid="stTextInput"] input,
    [data-testid="stTextArea"] textarea {
        background: #101b2a;
        border-color: rgba(148, 163, 184, 0.25);
        border-radius: 10px;
        color: #edf4fb;
    }

    [data-testid="stProgressBar"] > div > div {
        background: linear-gradient(90deg, #4fd1c5, #7c9cff);
    }

    hr {
        border-color: rgba(148, 163, 184, 0.15);
    }

    footer {
        visibility: hidden;
    }

</style>

<style>
/* SIH PRESENTATION EDITION — visual refinement */
:root {
  --sih-bg: #070b12;
  --sih-panel: rgba(15, 25, 40, .86);
  --sih-border: rgba(126, 164, 204, .22);
  --sih-cyan: #58e1d1;
  --sih-blue: #7aa7ff;
  --sih-gold: #f4c76b;
}
.stApp {
  background:
    radial-gradient(circle at 8% 0%, rgba(64, 116, 185, .18), transparent 28%),
    radial-gradient(circle at 95% 12%, rgba(38, 181, 169, .10), transparent 24%),
    linear-gradient(135deg, #070b12 0%, #0a111c 55%, #080d16 100%);
}
.block-container { max-width: 1500px; padding-top: 2rem; padding-bottom: 2rem; }
[data-testid="stSidebar"] {
  background: linear-gradient(180deg, #0b1421 0%, #08101a 100%);
  box-shadow: 12px 0 40px rgba(0,0,0,.16);
}
[data-testid="stSidebar"] h1, [data-testid="stSidebar"] h2,
[data-testid="stSidebar"] h3 { letter-spacing: -.4px; }
h1 { font-size: clamp(2rem, 4vw, 3.4rem) !important; line-height: 1.03 !important; letter-spacing: -1.8px !important; }
h2 { letter-spacing: -1px !important; }
h3 { letter-spacing: -.5px !important; }
.stMarkdown p { color: #aebed0; }
div[data-testid="stMetric"] {
  background: linear-gradient(145deg, rgba(22, 38, 58, .92), rgba(10, 20, 33, .92));
  border: 1px solid var(--sih-border);
  border-radius: 18px;
  padding: 16px 18px;
  box-shadow: 0 14px 34px rgba(0,0,0,.18);
}
div[data-testid="stMetric"] label { color: #8da8c4 !important; font-weight: 800; text-transform: uppercase; letter-spacing: 1px; }
div[data-testid="stMetric"] [data-testid="stMetricValue"] { color: #f1f7ff; font-weight: 850; }
div.stButton > button, div.stDownloadButton > button {
  min-height: 48px;
  border-radius: 13px;
  background: linear-gradient(100deg, #1d817e, #3869bd);
  border: 1px solid rgba(126, 238, 224, .42);
  box-shadow: 0 8px 24px rgba(28, 113, 146, .22);
  letter-spacing: .15px;
}
div.stButton > button:focus, div.stButton > button:hover {
  box-shadow: 0 0 0 2px rgba(88,225,209,.16), 0 12px 30px rgba(28,113,146,.3);
}
[data-testid="stFileUploader"] {
  background: linear-gradient(145deg, rgba(18, 34, 53, .85), rgba(10, 20, 33, .85));
  border: 1px dashed rgba(88,225,209,.48);
  box-shadow: inset 0 0 35px rgba(88,225,209,.025);
}
[data-testid="stExpander"] {
  border: 1px solid var(--sih-border) !important;
  border-radius: 15px !important;
  background: rgba(10, 20, 33, .48);
}
[data-testid="stAlert"] { border-radius: 14px; }
[data-testid="stProgressBar"] { padding: 4px 0; }
[data-testid="stProgressBar"] > div { background: rgba(255,255,255,.06); border-radius: 99px; }
[data-testid="stProgressBar"] > div > div { border-radius: 99px; }
.stTabs [data-baseweb="tab-list"] { gap: 8px; background: rgba(10,18,29,.6); padding: 7px; border-radius: 14px; }
.stTabs [data-baseweb="tab"] { border-radius: 10px; padding: 9px 16px; }
.stTabs [aria-selected="true"] { background: rgba(88,225,209,.14); color: #b8fff5 !important; }
[data-testid="stDataFrame"] { border: 1px solid var(--sih-border); border-radius: 14px; overflow: hidden; }
</style>

    """,
    unsafe_allow_html=True,
)

# -----------------------------
# Paths
# -----------------------------
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, "data")
UPLOAD_DIR = os.path.join(DATA_DIR, "uploads")
EVIDENCE_DIR = os.path.join(DATA_DIR, "evidence")
REPLAY_DIR = os.path.join(DATA_DIR, "replays", "browser")

for folder in [DATA_DIR, UPLOAD_DIR, EVIDENCE_DIR, REPLAY_DIR]:
    os.makedirs(folder, exist_ok=True)

MODEL_PATH = os.path.join(BASE_DIR, "yolo11n.pt")


# -----------------------------
# Cached model
# -----------------------------
@st.cache_resource
def load_model():
    return YOLO(MODEL_PATH)


model = load_model()


# -----------------------------
# Helpers
# -----------------------------
CLASS_NAMES = {
    0: "person",
    2: "car",
    3: "motorcycle",
    5: "bus",
    7: "truck",
}


def save_uploaded_video(uploaded_file):
    raw = uploaded_file.getvalue()
    file_hash = hashlib.md5(raw).hexdigest()[:16]
    extension = os.path.splitext(uploaded_file.name)[1].lower() or ".mp4"
    path = os.path.join(UPLOAD_DIR, f"{file_hash}{extension}")

    if not os.path.exists(path):
        with open(path, "wb") as f:
            f.write(raw)

    return path


def center_of_box(box):
    x1, y1, x2, y2 = box
    return int((x1 + x2) / 2), int((y1 + y2) / 2)


def inside_zone(x, y, zone):
    x1, y1, x2, y2 = zone
    return x1 <= x <= x2 and y1 <= y <= y2


def movement_direction(previous, current, min_move=2):
    if previous is None:
        return "UNKNOWN"

    dx = current[0] - previous[0]
    dy = current[1] - previous[1]

    if abs(dx) < min_move and abs(dy) < min_move:
        return "UNKNOWN"

    if abs(dx) >= abs(dy):
        return "EAST" if dx > 0 else "WEST"

    return "SOUTH" if dy > 0 else "NORTH"


def risk_for_event(
    object_name,
    direction,
    repeated,
    speed_pixels,
    track_quality="UNKNOWN",
    average_confidence=0.0,
    zone_state="UNKNOWN",
):
    """
    Context-aware risk scoring:
    - Severity: what type of object/event was observed
    - Confidence: how reliable the observation is
    - Operational priority: combined score used for alert ordering
    """
    severity_score = 30
    confidence_adjustment = 0
    priority_adjustment = 0
    reasons = ["Restricted-zone entry"]

    if object_name in {"person", "motorcycle"}:
        severity_score += 20
        reasons.append(f"Priority object: {object_name}")

    if repeated:
        priority_adjustment += 15
        reasons.append("Repeated zone entry")

    if direction != "UNKNOWN":
        priority_adjustment += 5
        reasons.append(f"Movement direction: {direction}")

    if speed_pixels >= 35:
        priority_adjustment += 15
        reasons.append("Rapid observed movement")

    if zone_state in {"CROSSED", "INSIDE"}:
        priority_adjustment += 5
        reasons.append(f"Zone context: {zone_state}")

    if average_confidence >= 0.75:
        confidence_adjustment += 5
        reasons.append(f"Detection confidence: HIGH ({average_confidence:.2f})")
    elif average_confidence >= 0.50:
        reasons.append(f"Detection confidence: MEDIUM ({average_confidence:.2f})")
    elif average_confidence > 0:
        confidence_adjustment -= 10
        reasons.append(f"Detection confidence: LOW ({average_confidence:.2f})")

    if track_quality == "STABLE":
        reasons.append("Track quality: STABLE")
    elif track_quality == "UNCERTAIN":
        confidence_adjustment -= 10
        reasons.append("Track quality: UNCERTAIN (-10 priority)")

    score = max(0, min(100, severity_score + priority_adjustment + confidence_adjustment))

    if score >= 80:
        level = "CRITICAL"
    elif score >= 50:
        level = "HIGH"
    elif score >= 30:
        level = "MEDIUM"
    else:
        level = "LOW"

    reasons.append(
        f"Risk breakdown: severity={severity_score}, "
        f"context={priority_adjustment:+d}, confidence={confidence_adjustment:+d}"
    )

    return score, level, reasons


def make_evidence(frame, event, number):
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = (
        f"incident_{number:03d}_ID{event['id']}_"
        f"{event['risk_level']}_{timestamp}.jpg"
    )
    path = os.path.join(EVIDENCE_DIR, filename)

    image = frame.copy()

    cv2.putText(
        image,
        "INCIDENT EVIDENCE",
        (25, 40),
        cv2.FONT_HERSHEY_SIMPLEX,
        1.0,
        (0, 0, 255),
        3,
    )

    cv2.putText(
        image,
        f"RISK: {event['risk_level']} {event['risk_score']}/100",
        (25, 78),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.8,
        (0, 0, 255),
        2,
    )

    cv2.imwrite(path, image)
    return path


def create_incident_package(result, incident):
    """Create a portable investigation package containing metadata and evidence."""
    package_dir = os.path.join(DATA_DIR, "incident_packages")
    os.makedirs(package_dir, exist_ok=True)

    group_id = incident.get("incident_group_id", "UNKNOWN")
    safe_group = str(group_id).replace("/", "_").replace("\\", "_")
    package_base = f"{safe_group}_ID{incident.get('id', 'NA')}"
    json_path = os.path.join(package_dir, package_base + ".json")
    zip_path = os.path.join(package_dir, package_base + ".zip")

    metadata = {
        "package_type": "border_surveillance_incident",
        "created_at": datetime.now().isoformat(timespec="seconds"),
        "incident": incident,
        "video_summary": {
            "fps": result.get("fps"),
            "total_frames": result.get("total_frames"),
            "width": result.get("width"),
            "height": result.get("height"),
        },
        "evidence_file": os.path.basename(incident.get("evidence_path", "")),
    }

    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(metadata, f, indent=2, default=str)

    with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as archive:
        archive.write(json_path, arcname="incident_metadata.json")
        evidence_path = incident.get("evidence_path")
        if evidence_path and os.path.exists(evidence_path):
            archive.write(evidence_path, arcname="evidence.jpg")

    return zip_path


def create_browser_replay(source_path, event, replay_seconds=2):
    """
    Generate one browser-compatible H.264 replay on demand.
    This is intentionally NOT called for every incident.
    """
    cap = cv2.VideoCapture(source_path)

    if not cap.isOpened():
        return None

    fps = cap.get(cv2.CAP_PROP_FPS)
    if not fps or fps <= 0:
        fps = 30.0

    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

    event_frame = int(event.get("frame_index", 0))
    start_frame = max(0, event_frame - int(replay_seconds * fps))
    end_frame = min(
        total_frames - 1,
        event_frame + int(replay_seconds * fps),
    )

    cap.set(cv2.CAP_PROP_POS_FRAMES, start_frame)

    temp_path = os.path.join(
        REPLAY_DIR,
        f"temp_ID{event['id']}_{event['frame_index']}.mp4",
    )

    output_path = os.path.join(
        REPLAY_DIR,
        f"incident_ID{event['id']}_{event['frame_index']}.mp4",
    )

    writer = cv2.VideoWriter(
        temp_path,
        cv2.VideoWriter_fourcc(*"mp4v"),
        fps,
        (width, height),
    )

    current = start_frame

    while current <= end_frame:
        ok, frame = cap.read()
        if not ok:
            break

        writer.write(frame)
        current += 1

    writer.release()
    cap.release()

    if not os.path.exists(temp_path):
        return None

    ffmpeg = imageio_ffmpeg.get_ffmpeg_exe()

    command = [
        ffmpeg,
        "-y",
        "-i",
        temp_path,
        "-c:v",
        "libx264",
        "-preset",
        "ultrafast",
        "-crf",
        "28",
        "-pix_fmt",
        "yuv420p",
        "-movflags",
        "+faststart",
        "-an",
        output_path,
    ]

    try:
        subprocess.run(
            command,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            check=True,
        )
    except Exception:
        return None
    finally:
        if os.path.exists(temp_path):
            os.remove(temp_path)

    return output_path if os.path.exists(output_path) else None


def deduplicate_entry_alerts(entry_events, window_seconds=8.0):
    """Group repeated alerts from the same track within a short time window."""
    grouped = []
    last_by_track = {}
    for event in sorted(entry_events, key=lambda item: item.get("video_time", 0)):
        track_id = event.get("id")
        event_time = float(event.get("video_time", 0))
        previous = last_by_track.get(track_id)
        if previous is not None and event_time - previous["video_time"] <= window_seconds:
            previous["duplicate_count"] = previous.get("duplicate_count", 1) + 1
            event["suppressed_duplicate"] = True
            event["incident_group_id"] = previous["incident_group_id"]
            continue
        event["duplicate_count"] = 1
        event["suppressed_duplicate"] = False
        event["incident_group_id"] = f"INC-{len(grouped) + 1:03d}"
        grouped.append(event)
        last_by_track[track_id] = event
    return grouped



def assess_camera_health(video_path, sample_limit=120):
    """Estimate basic camera/source health from the uploaded video."""
    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        return {"status": "UNAVAILABLE", "reason": "Video source could not be opened."}

    fps = cap.get(cv2.CAP_PROP_FPS) or 0.0
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH) or 0)
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT) or 0)
    sampled = 0
    read_failures = 0
    dark_frames = 0
    frozen_pairs = 0
    previous_gray = None

    while sampled < sample_limit:
        ok, frame = cap.read()
        if not ok:
            break
        sampled += 1
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        brightness = float(gray.mean())
        if brightness < 18:
            dark_frames += 1
        if previous_gray is not None:
            difference = float(cv2.absdiff(gray, previous_gray).mean())
            if difference < 0.35:
                frozen_pairs += 1
        previous_gray = gray

    cap.release()

    issues = []
    if width < 640 or height < 360:
        issues.append("Low resolution")
    if fps < 10:
        issues.append("Low frame rate")
    if sampled and dark_frames / sampled > 0.70:
        issues.append("Mostly dark footage")
    if sampled > 5 and frozen_pairs / max(sampled - 1, 1) > 0.70:
        issues.append("Possible frozen camera feed")

    status = "HEALTHY" if not issues else "CHECK"
    return {
        "status": status,
        "fps": round(float(fps), 2),
        "resolution": f"{width}x{height}",
        "sampled_frames": sampled,
        "issues": issues or ["No basic camera-health issues detected"],
    }

def get_risk_counts(events):
    counts = {
        "CRITICAL": 0,
        "HIGH": 0,
        "MEDIUM": 0,
        "LOW": 0,
    }

    for event in events:
        level = event.get("risk_level", "LOW")
        counts[level] = counts.get(level, 0) + 1

    return counts


# -----------------------------
# Session state
# -----------------------------
if "analysis_result" not in st.session_state:
    st.session_state.analysis_result = None

if "source_path" not in st.session_state:
    st.session_state.source_path = None

if "selected_incident" not in st.session_state:
    st.session_state.selected_incident = None

if "replay_path" not in st.session_state:
    st.session_state.replay_path = None

if "operator_feedback" not in st.session_state:
    st.session_state.operator_feedback = {}

FEEDBACK_FILE = Path("data/operator_feedback.json")
FEEDBACK_FILE.parent.mkdir(parents=True, exist_ok=True)

def save_operator_feedback(incident_key, label, note=""):
    feedback = {
        "incident_key": incident_key,
        "label": label,
        "note": note,
        "timestamp": datetime.now().isoformat(timespec="seconds"),
    }
    st.session_state.operator_feedback[incident_key] = feedback
    try:
        existing = []
        if FEEDBACK_FILE.exists():
            existing = json.loads(FEEDBACK_FILE.read_text(encoding="utf-8"))
        existing = [item for item in existing if item.get("incident_key") != incident_key]
        existing.append(feedback)
        FEEDBACK_FILE.write_text(json.dumps(existing, indent=2), encoding="utf-8")
    except Exception:
        pass



# -----------------------------
# Sidebar
# -----------------------------
with st.sidebar:
    st.markdown(
        '<div style="font-size:25px;font-weight:800;color:#f4f8fc;">COMMAND CENTER</div>',
        unsafe_allow_html=True,
    )

    st.markdown(
        '<div class="status">● ANALYTICS ENGINE READY</div>',
        unsafe_allow_html=True,
    )

    st.markdown("### Analysis Pipeline")

    pipeline = [
        "01  Detection",
        "02  Tracking",
        "03  Movement & Zone Analysis",
        "04  Risk Prioritization",
        "05  Evidence & Replay",
        "06  Investigation",
    ]

    for item in pipeline:
        st.markdown(
            f'<div class="pipeline-item">{item}</div>',
            unsafe_allow_html=True,
        )

    st.markdown("---")

    st.markdown("### Performance")

    speed_mode = st.selectbox(
        "Analysis mode",
        ["FAST", "BALANCED"],
        index=0,
    )

    if speed_mode == "FAST":
        frame_skip = 2
        inference_size = 640
    else:
        frame_skip = 1
        inference_size = 640

    st.caption(
        f"Frame sampling: every {frame_skip} frame(s)\n\n"
        f"Inference size: {inference_size}px\n\n"
        "Replay: generated on demand"
    )


# -----------------------------
# Main header
# -----------------------------
st.markdown(
    """
    <div class="hero">
        <div class="status">● SYSTEM ONLINE</div>
        <div class="hero-title">BORDER SURVEILLANCE COMMAND CENTER</div>
        <div class="hero-subtitle">
            Video intelligence for intrusion detection, movement analysis,
            risk prioritization and investigation-ready evidence.
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)

st.markdown(
    """
    <div class="info-card">
        <b>From continuous CCTV footage to prioritized security events</b><br>
        <span class="small-muted">
        Detect &nbsp;•&nbsp; Track &nbsp;•&nbsp; Analyze movement &nbsp;•&nbsp;
        Score risk &nbsp;•&nbsp; Preserve evidence &nbsp;•&nbsp; Investigate
        </span>
    </div>
    """,
    unsafe_allow_html=True,
)


# -----------------------------
# Upload
# -----------------------------
st.markdown('<div class="section-label">Input Source</div>', unsafe_allow_html=True)

uploaded = st.file_uploader(
    "Upload surveillance video",
    type=["mp4", "avi", "mov", "mkv"],
)

if uploaded is not None:
    source_path = save_uploaded_video(uploaded)
    st.session_state.source_path = source_path

    col1, col2 = st.columns([3, 1])

    with col1:
        st.video(source_path)

    with col2:
        st.markdown(
            """
            <div class="info-card">
                <b>Source ready</b><br><br>
                CCTV video loaded.<br><br>
                AI analysis can now begin.
            </div>
            """,
            unsafe_allow_html=True,
        )

        analyze_clicked = st.button(
            "START AI ANALYSIS",
            type="primary",
            use_container_width=True,
        )

        if analyze_clicked:
            st.session_state.analysis_result = None
            st.session_state.selected_incident = None
            st.session_state.replay_path = None

            cap = cv2.VideoCapture(source_path)

            if not cap.isOpened():
                st.error("Unable to open the uploaded video.")
                st.stop()

            fps = cap.get(cv2.CAP_PROP_FPS)
            if not fps or fps <= 0:
                fps = 30.0

            total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
            width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
            height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

            zone = (
                int(width * 0.20),
                int(height * 0.40),
                int(width * 0.85),
                int(height * 0.90),
            )

            previous_positions = {}
            previous_zone_status = {}
            entry_count = {}
            inside_streak = {}
            confirmed_inside = {}
            confirmation_frames = 3
            zone_states = {}
            track_zone_seen_outside = {}
            track_last_inside = {}
            track_state_history = {}
            movement_history = {}
            suspicious_pattern_counts = {}
            track_history = {}
            track_observations = {}
            track_confidence_sum = {}
            intrusion_ids = set()
            events = []
            evidence_paths = []
            object_counts = {
                "person": 0,
                "car": 0,
                "motorcycle": 0,
                "bus": 0,
                "truck": 0,
            }

            processed = 0
            processing_start = time.perf_counter()
            frame_index = 0
            last_preview = None
            progress = st.progress(0)
            status = st.empty()
            preview = st.empty()

            while True:
                ok, frame = cap.read()

                if not ok:
                    break

                current_frame = frame_index
                frame_index += 1

                if current_frame % frame_skip != 0:
                    continue

                processed += 1

                results = model.track(
                    frame,
                    persist=True,
                    tracker="bytetrack.yaml",
                    conf=0.35,
                    classes=[0, 2, 3, 5, 7],
                    imgsz=inference_size,
                    verbose=False,
                )

                result = results[0]

                if result.boxes is not None and len(result.boxes) > 0:
                    boxes = result.boxes.xyxy.cpu().tolist()
                    classes = result.boxes.cls.cpu().tolist()
                    confidences = result.boxes.conf.cpu().tolist()

                    if result.boxes.id is not None:
                        ids = result.boxes.id.cpu().tolist()
                    else:
                        ids = [None] * len(boxes)

                    for box, cls_id, confidence, track_id in zip(
                        boxes,
                        classes,
                        confidences,
                        ids,
                    ):
                        class_id = int(cls_id)
                        object_name = CLASS_NAMES.get(
                            class_id,
                            str(class_id),
                        )

                        if object_name in object_counts:
                            object_counts[object_name] += 1

                        if track_id is None:
                            continue

                        track_id = int(track_id)
                        center = center_of_box(box)

                        if track_id not in track_history:
                            track_history[track_id] = []

                        track_history[track_id].append(center)

                        if len(track_history[track_id]) > 40:
                            track_history[track_id] = track_history[
                                track_id
                            ][-40:]

                        current_inside = inside_zone(
                            center[0],
                            center[1],
                            zone,
                        )

                        previous = previous_positions.get(track_id)
                        direction = movement_direction(
                            previous,
                            center,
                        )

                        speed_pixels = 0

                        if previous is not None:
                            dx = center[0] - previous[0]
                            dy = center[1] - previous[1]
                            speed_pixels = int(
                                (dx * dx + dy * dy) ** 0.5
                            )

                        previous_positions[track_id] = center

                        # Suspicious movement pattern analysis
                        movement_history.setdefault(track_id, []).append({
                            "center": center,
                            "direction": direction,
                            "speed": speed_pixels,
                            "inside": current_inside if "current_inside" in locals() else False,
                        })
                        if len(movement_history[track_id]) > 12:
                            movement_history[track_id] = movement_history[track_id][-12:]
                        recent_moves = movement_history[track_id][-6:]
                        direction_changes = sum(
                            1 for a, b in zip(recent_moves, recent_moves[1:])
                            if a["direction"] != "UNKNOWN"
                            and b["direction"] != "UNKNOWN"
                            and a["direction"] != b["direction"]
                        )
                        rapid_moves = sum(1 for item in recent_moves if item["speed"] >= 35)
                        suspicious_pattern = direction_changes >= 2 or rapid_moves >= 3
                        suspicious_pattern_counts[track_id] = suspicious_pattern_counts.get(track_id, 0) + int(suspicious_pattern)

                        track_observations[track_id] = track_observations.get(track_id, 0) + 1
                        track_confidence_sum[track_id] = track_confidence_sum.get(track_id, 0.0) + float(confidence)
                        observation_count = track_observations[track_id]
                        average_confidence = track_confidence_sum[track_id] / max(1, observation_count)
                        track_quality = "STABLE" if observation_count >= 3 and average_confidence >= 0.55 else "UNCERTAIN"

                        previous_inside = previous_zone_status.get(
                            track_id,
                            False,
                        )

                        # Border-zone state machine:
                        # APPROACHING -> CROSSED -> INSIDE -> EXITED
                        # The state is based on zone presence and observed motion.
                        previous_state = zone_states.get(track_id, "APPROACHING")
                        if not current_inside:
                            if previous_inside:
                                current_state = "EXITED"
                            elif direction in {"NORTH", "SOUTH", "EAST", "WEST"}:
                                current_state = "APPROACHING"
                            else:
                                current_state = "APPROACHING"
                            track_zone_seen_outside[track_id] = True
                        else:
                            if previous_state in {"APPROACHING", "EXITED"} and track_zone_seen_outside.get(track_id, False):
                                current_state = "CROSSED"
                            else:
                                current_state = "INSIDE"

                        zone_states[track_id] = current_state
                        track_state_history.setdefault(track_id, []).append(current_state)
                        if len(track_state_history[track_id]) > 20:
                            track_state_history[track_id] = track_state_history[track_id][-20:]

                        # Temporal confirmation: require stable presence across
                        # multiple processed frames before confirming entry.
                        if current_inside:
                            inside_streak[track_id] = inside_streak.get(track_id, 0) + 1
                        else:
                            inside_streak[track_id] = 0

                        is_confirmed = confirmed_inside.get(track_id, False)

                        # Confirmed Entry
                        if (
                            current_inside
                            and not is_confirmed
                            and inside_streak[track_id] >= confirmation_frames
                        ):
                            entry_count[track_id] = entry_count.get(track_id, 0) + 1
                            repeated = entry_count[track_id] > 1

                            risk_score, risk_level, reasons = risk_for_event(
                                object_name,
                                direction,
                                repeated,
                                speed_pixels,
                                track_quality,
                                average_confidence,
                                current_state,
                            )
                            reasons.append(
                                f"Temporal confirmation: {confirmation_frames} frames"
                            )
                            if suspicious_pattern:
                                reasons.append(
                                    f"Suspicious movement pattern: {direction_changes} direction changes / {rapid_moves} rapid movements"
                                )
                                risk_score = min(100, risk_score + 10)
                                if risk_score >= 80:
                                    risk_level = "CRITICAL"
                                elif risk_score >= 50:
                                    risk_level = "HIGH"
                                elif risk_score >= 30:
                                    risk_level = "MEDIUM"
                                else:
                                    risk_level = "LOW"
                            reasons.append(f"Average detection confidence: {average_confidence:.2f}")
                            reasons.append(f"Zone state transition: {previous_state} -> {current_state}")

                            event = {
                                "id": track_id,
                                "object": object_name,
                                "event": "ENTRY",
                                "zone_state": current_state,
                                "direction": direction,
                                "risk_score": risk_score,
                                "risk_level": risk_level,
                                "reasons": reasons,
                                "frame_index": current_frame,
                                "video_time": current_frame / fps,
                                "timestamp": datetime.now().strftime(
                                    "%Y-%m-%d %H:%M:%S"
                                ),
                            }

                            events.append(event)
                            intrusion_ids.add(track_id)
                            confirmed_inside[track_id] = True

                            evidence_path = make_evidence(frame, event, len(events))
                            event["evidence_path"] = evidence_path
                            evidence_paths.append(evidence_path)

                        # Confirmed Exit
                        elif not current_inside and is_confirmed:
                            events.append(
                                {
                                    "id": track_id,
                                    "object": object_name,
                                    "event": "EXIT",
                                    "zone_state": "EXITED",
                                    "direction": direction,
                                    "risk_score": 0,
                                    "risk_level": "LOW",
                                    "reasons": [
                                        "Restricted-zone exit",
                                        "Entry was temporally confirmed",
                                        f"Zone state transition: {previous_state} -> EXITED",
                                    ],
                                    "frame_index": current_frame,
                                    "video_time": current_frame / fps,
                                    "timestamp": datetime.now().strftime(
                                        "%Y-%m-%d %H:%M:%S"
                                    ),
                                    "evidence_path": None,
                                }
                            )
                            confirmed_inside[track_id] = False

                        previous_zone_status[track_id] = current_inside

                        # Draw tracking box
                        x1, y1, x2, y2 = map(int, box)

                        cv2.rectangle(
                            frame,
                            (x1, y1),
                            (x2, y2),
                            (180, 180, 180),
                            2,
                        )

                        label = (
                            f"ID {track_id} | {object_name} | "
                            f"{direction} | {current_state}"
                        )

                        cv2.putText(
                            frame,
                            label,
                            (x1, max(20, y1 - 8)),
                            cv2.FONT_HERSHEY_SIMPLEX,
                            0.48,
                            (180, 180, 180),
                            2,
                        )

                        # Movement trail
                        points = track_history[track_id]

                        for i in range(1, len(points)):
                            cv2.line(
                                frame,
                                points[i - 1],
                                points[i],
                                (0, 190, 220),
                                2,
                            )

                # Restricted zone
                cv2.rectangle(
                    frame,
                    (zone[0], zone[1]),
                    (zone[2], zone[3]),
                    (0, 165, 255),
                    2,
                )

                cv2.putText(
                    frame,
                    "RESTRICTED ZONE",
                    (zone[0], max(30, zone[1] - 10)),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.7,
                    (0, 165, 255),
                    2,
                )

                cv2.line(
                    frame,
                    (30, 35),
                    (70, 35),
                    (0, 190, 220),
                    3,
                )

                cv2.putText(
                    frame,
                    "MOVEMENT TRAIL",
                    (80, 40),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.55,
                    (0, 190, 220),
                    2,
                )

                last_preview = frame.copy()

                if processed % 5 == 0:
                    if total_frames > 0:
                        progress_value = min(
                            current_frame / total_frames,
                            1.0,
                        )
                        progress.progress(progress_value)

                    status.info(
                        f"AI analysis running • frame {current_frame:,} "
                        f"• incidents detected: "
                        f"{sum(1 for e in events if e['event'] == 'ENTRY')}"
                    )

                    preview.image(
                        cv2.cvtColor(
                            last_preview,
                            cv2.COLOR_BGR2RGB,
                        ),
                        use_container_width=True,
                    )

            cap.release()
            processing_seconds = max(time.perf_counter() - processing_start, 0.001)
            progress.progress(1.0)
            status.success("AI analysis completed.")

            raw_entry_events = [
                event for event in events
                if event.get("event") == "ENTRY"
            ]
            entry_events = deduplicate_entry_alerts(raw_entry_events)

            exit_events = [
                event for event in events
                if event.get("event") == "EXIT"
            ]

            camera_health = assess_camera_health(source_path)

            result_data = {
                "events": events,
                "entry_events": entry_events,
                "exit_events": exit_events,
                "intrusion_ids": intrusion_ids,
                "object_counts": object_counts,
                "fps": fps,
                "total_frames": total_frames,
                "width": width,
                "height": height,
                "evidence_paths": evidence_paths,
                "camera_health": camera_health,
                "processed_frames": processed,
                "processing_seconds": processing_seconds,
            }

            st.session_state.analysis_result = result_data
            st.session_state.selected_incident = (
                entry_events[0] if entry_events else None
            )

            st.rerun()


# -----------------------------
# Results
# -----------------------------
result = st.session_state.analysis_result

if result is not None:
    events = result["events"]

    # IMPORTANT: explicitly define entry_events so there is no
    # NameError during dashboard rendering.
    entry_events = result.get("entry_events") or deduplicate_entry_alerts([
        event for event in events
        if event.get("event") == "ENTRY"
    ])

    exit_events = [
        event for event in events
        if event.get("event") == "EXIT"
    ]

    risk_counts = get_risk_counts(entry_events)

    st.markdown(
        '<div class="section-label">Command Overview</div>',
        unsafe_allow_html=True,
    )

    c1, c2, c3, c4 = st.columns(4)

    metrics = [
        ("Total Events", len(events)),
        ("Zone Entries", len(entry_events)),
        ("Zone Exits", len(exit_events)),
        ("Intrusion Tracks", len(result["intrusion_ids"])),
    ]

    for col, (label, value) in zip(
        [c1, c2, c3, c4],
        metrics,
    ):
        with col:
            st.markdown(
                f"""
                <div class="metric-card">
                    <div class="metric-label">{label}</div>
                    <div class="metric-value">{value}</div>
                </div>
                """,
                unsafe_allow_html=True,
            )

    st.markdown(
        '<div class="section-label">Smart Alert Prioritization</div>',
        unsafe_allow_html=True,
    )

    r1, r2, r3, r4 = st.columns(4)

    risk_metrics = [
        ("CRITICAL", risk_counts["CRITICAL"]),
        ("HIGH", risk_counts["HIGH"]),
        ("MEDIUM", risk_counts["MEDIUM"]),
        ("LOW", risk_counts["LOW"]),
    ]

    for col, (label, value) in zip(
        [r1, r2, r3, r4],
        risk_metrics,
    ):
        with col:
            st.markdown(
                f"""
                <div class="metric-card">
                    <div class="metric-label">{label}</div>
                    <div class="metric-value">{value}</div>
                </div>
                """,
                unsafe_allow_html=True,
            )

    st.markdown(
        '<div class="section-label">Evaluation Metrics</div>',
        unsafe_allow_html=True,
    )

    reviewed_count = sum(1 for item in st.session_state.operator_feedback.values() if item.get("label") and item.get("label") != "Not reviewed")
    processing_seconds = float(result.get("processing_seconds", 0.0) or 0.0)
    processed_frames = int(result.get("processed_frames", 0) or 0)
    processing_fps = processed_frames / processing_seconds if processing_seconds else 0.0
    duplicate_reduction = max(len([e for e in events if e.get("event") == "ENTRY"]) - len(entry_events), 0)

    em1, em2, em3, em4 = st.columns(4)
    evaluation_metrics = [("Processed Frames", processed_frames), ("Processing FPS", f"{processing_fps:.1f}"), ("Grouped Alerts Removed", duplicate_reduction), ("Reviewed Incidents", reviewed_count)]
    for col, (label, value) in zip([em1, em2, em3, em4], evaluation_metrics):
        with col:
            st.markdown(f"<div class='metric-card'><div class='metric-label'>{label}</div><div class='metric-value'>{value}</div></div>", unsafe_allow_html=True)
    st.caption("These are prototype operational metrics; they are not accuracy or field-performance measurements.")

    st.markdown(
        '<div class="section-label">Incident Investigation</div>',
        unsafe_allow_html=True,
    )

    if not entry_events:
        st.info(
            "No restricted-zone entry incidents were detected in this video."
        )
    else:
        options = []

        for index, event in enumerate(entry_events):
            options.append(
                f"Incident {index + 1} | "
                f"ID {event['id']} | "
                f"{event['risk_level']} "
                f"{event['risk_score']}/100 | "
                f"{event['object']}"
            )

        selected_label = st.selectbox(
            "Select incident for investigation",
            options,
        )

        selected_index = options.index(selected_label)
        selected = entry_events[selected_index]

        st.session_state.selected_incident = selected

        left, right = st.columns([1.15, 0.85])

        with left:
            st.markdown(
                f"""
                <div class="incident-card">
                    <div class="incident-title">
                        INCIDENT {selected_index + 1}
                        — {selected['risk_level']}
                        {selected['risk_score']}/100
                    </div>
                    <div class="small-muted">
                        Investigation-ready event record
                    </div>
                    <br>
                    <b>Object:</b> {selected['object']}<br>
                    <b>Tracking ID:</b> {selected['id']}<br>
                    <b>Event:</b> {selected['event']}<br>
                    <b>Direction:</b> {selected['direction']}<br>
                    <b>Video time:</b> {selected['video_time']:.2f} sec<br>
                    <b>Detected:</b> {selected['timestamp']}<br>
                    <b>Incident Group:</b> {selected.get('incident_group_id', 'N/A')}<br>
                    <b>Grouped Alerts:</b> {selected.get('duplicate_count', 1)}
                </div>
                """,
                unsafe_allow_html=True,
            )

            st.markdown("#### Operator Feedback")
            feedback_key = f"{selected.get('incident_group_id', 'group')}_{selected.get('id', 'unknown')}"
            current_feedback = st.session_state.operator_feedback.get(feedback_key, {})
            feedback_choice = st.radio(
                "Classify this alert",
                ["Not reviewed", "Valid incident", "False positive", "Needs review"],
                index=["Not reviewed", "Valid incident", "False positive", "Needs review"].index(current_feedback.get("label", "Not reviewed")),
                key=f"feedback_choice_{feedback_key}",
                horizontal=True,
            )
            feedback_note = st.text_input(
                "Operator note (optional)",
                value=current_feedback.get("note", ""),
                key=f"feedback_note_{feedback_key}",
            )
            if st.button("Save Operator Feedback", key=f"save_feedback_{feedback_key}"):
                save_operator_feedback(feedback_key, feedback_choice, feedback_note)
                st.success("Operator feedback saved.")

            st.markdown("#### Why was this event prioritized?")

            for reason in selected["reasons"]:
                st.markdown(
                    f'<div class="reason">✓ {reason}</div>',
                    unsafe_allow_html=True,
                )

            package_path = create_incident_package(result, selected)
            with open(package_path, "rb") as package_file:
                st.download_button(
                    "Download Incident Package",
                    data=package_file,
                    file_name=os.path.basename(package_path),
                    mime="application/zip",
                    use_container_width=True,
                )

        with right:
            evidence_path = selected.get("evidence_path")

            if evidence_path and os.path.exists(evidence_path):
                st.image(
                    evidence_path,
                    caption="Automatic incident evidence",
                    use_container_width=True,
                )
            else:
                st.info("No evidence image is available for this event.")

        # -----------------------------
        # On-demand replay
        # -----------------------------
        st.markdown(
            '<div class="section-label">Incident Replay</div>',
            unsafe_allow_html=True,
        )

        st.caption(
            "Replay is generated only for the selected incident, "
            "so the initial analysis stays fast."
        )

        replay_filename = (
            f"incident_ID{selected['id']}_"
            f"{selected['frame_index']}.mp4"
        )
        existing_replay = os.path.join(
            REPLAY_DIR,
            replay_filename,
        )

        if os.path.exists(existing_replay):
            st.session_state.replay_path = existing_replay

        if st.session_state.replay_path:
            st.video(st.session_state.replay_path)
        else:
            if st.button(
                "GENERATE REPLAY FOR THIS INCIDENT",
                type="primary",
                use_container_width=False,
            ):
                with st.spinner(
                    "Generating short incident replay..."
                ):
                    replay_path = create_browser_replay(
                        st.session_state.source_path,
                        selected,
                        replay_seconds=2,
                    )

                if replay_path:
                    st.session_state.replay_path = replay_path
                    st.rerun()
                else:
                    st.error(
                        "Replay generation failed. "
                        "The evidence image is still available."
                    )

    camera_health = result.get("camera_health", {})
    st.markdown('<div class="section-label">Camera Health</div>', unsafe_allow_html=True)
    health_col1, health_col2, health_col3 = st.columns(3)
    with health_col1:
        st.metric("Source Status", camera_health.get("status", "UNKNOWN"))
    with health_col2:
        st.metric("Resolution", camera_health.get("resolution", "N/A"))
    with health_col3:
        st.metric("Source FPS", camera_health.get("fps", "N/A"))
    st.caption("Health checks are basic video-quality indicators, not full hardware diagnostics.")
    for issue in camera_health.get("issues", []):
        st.write("• " + issue)

    st.markdown(
        '<div class="section-label">System Summary</div>',
        unsafe_allow_html=True,
    )

    obj_counts = result["object_counts"]

    s1, s2, s3, s4, s5 = st.columns(5)

    for col, name in zip(
        [s1, s2, s3, s4, s5],
        ["person", "car", "motorcycle", "bus", "truck"],
    ):
        with col:
            st.metric(
                name.title(),
                obj_counts[name],
            )

    st.markdown(
        """
        <div class="footer">
            Intelligent Border Surveillance • AI Video Analytics Prototype
            • Detection → Tracking → Movement → Risk → Evidence → Investigation
        </div>
        """,
        unsafe_allow_html=True,
    )
