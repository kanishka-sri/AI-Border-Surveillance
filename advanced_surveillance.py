import streamlit as st
import cv2
import os
import hashlib
import subprocess
from datetime import datetime
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
):
    score = 30
    reasons = ["Restricted-zone entry"]

    if direction != "UNKNOWN":
        score += 10
        reasons.append(f"Movement direction: {direction}")

    if object_name in {"person", "motorcycle"}:
        score += 20
        reasons.append(f"Priority object: {object_name}")

    if repeated:
        score += 20
        reasons.append("Repeated zone entry")

    if speed_pixels >= 35:
        score += 20
        reasons.append("Rapid observed movement")

    score = min(score, 100)

    if score >= 80:
        level = "CRITICAL"
    elif score >= 50:
        level = "HIGH"
    elif score >= 30:
        level = "MEDIUM"
    else:
        level = "LOW"

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
            track_history = {}
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

                    if result.boxes.id is not None:
                        ids = result.boxes.id.cpu().tolist()
                    else:
                        ids = [None] * len(boxes)

                    for box, cls_id, track_id in zip(
                        boxes,
                        classes,
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

                        current_inside = inside_zone(
                            center[0],
                            center[1],
                            zone,
                        )

                        previous_inside = previous_zone_status.get(
                            track_id,
                            False,
                        )

                        # Entry
                        if current_inside and not previous_inside:
                            entry_count[track_id] = (
                                entry_count.get(track_id, 0) + 1
                            )

                            repeated = entry_count[track_id] > 1

                            risk_score, risk_level, reasons = risk_for_event(
                                object_name,
                                direction,
                                repeated,
                                speed_pixels,
                            )

                            event = {
                                "id": track_id,
                                "object": object_name,
                                "event": "ENTRY",
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

                            evidence_path = make_evidence(
                                frame,
                                event,
                                len(events),
                            )

                            event["evidence_path"] = evidence_path
                            evidence_paths.append(evidence_path)

                        # Exit
                        elif not current_inside and previous_inside:
                            events.append(
                                {
                                    "id": track_id,
                                    "object": object_name,
                                    "event": "EXIT",
                                    "direction": direction,
                                    "risk_score": 0,
                                    "risk_level": "LOW",
                                    "reasons": ["Restricted-zone exit"],
                                    "frame_index": current_frame,
                                    "video_time": current_frame / fps,
                                    "timestamp": datetime.now().strftime(
                                        "%Y-%m-%d %H:%M:%S"
                                    ),
                                    "evidence_path": None,
                                }
                            )

                        previous_zone_status[track_id] = current_inside

                        # Draw tracking box
                        x1, y1, x2, y2 = map(int, box)

                        cv2.rectangle(
                            frame,
                            (x1, y1),
                            (x2, y2),
                            (0, 255, 0),
                            2,
                        )

                        label = (
                            f"ID {track_id} | {object_name} | "
                            f"{direction}"
                        )

                        cv2.putText(
                            frame,
                            label,
                            (x1, max(20, y1 - 8)),
                            cv2.FONT_HERSHEY_SIMPLEX,
                            0.48,
                            (0, 255, 0),
                            2,
                        )

                        # Movement trail
                        points = track_history[track_id]

                        for i in range(1, len(points)):
                            cv2.line(
                                frame,
                                points[i - 1],
                                points[i],
                                (255, 255, 0),
                                2,
                            )

                # Restricted zone
                cv2.rectangle(
                    frame,
                    (zone[0], zone[1]),
                    (zone[2], zone[3]),
                    (0, 0, 255),
                    2,
                )

                cv2.putText(
                    frame,
                    "RESTRICTED ZONE",
                    (zone[0], max(30, zone[1] - 10)),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.7,
                    (0, 0, 255),
                    2,
                )

                cv2.line(
                    frame,
                    (30, 35),
                    (70, 35),
                    (255, 255, 0),
                    3,
                )

                cv2.putText(
                    frame,
                    "MOVEMENT TRAIL",
                    (80, 40),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.55,
                    (255, 255, 0),
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
            progress.progress(1.0)
            status.success("AI analysis completed.")

            entry_events = [
                event for event in events
                if event.get("event") == "ENTRY"
            ]

            exit_events = [
                event for event in events
                if event.get("event") == "EXIT"
            ]

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
    entry_events = [
        event for event in events
        if event.get("event") == "ENTRY"
    ]

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
                    <b>Detected:</b> {selected['timestamp']}
                </div>
                """,
                unsafe_allow_html=True,
            )

            st.markdown("#### Why was this event prioritized?")

            for reason in selected["reasons"]:
                st.markdown(
                    f'<div class="reason">✓ {reason}</div>',
                    unsafe_allow_html=True,
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
