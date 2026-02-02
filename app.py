import streamlit as st
from PIL import Image
from streamlit_cropper import st_cropper
from io import BytesIO
import zipfile
import os
from streamlit_sortables import sort_items

APP_NAME = "Pro Image Cropper Plus — Streamlit"

st.set_page_config(
    page_title=APP_NAME,
    layout="wide",
    initial_sidebar_state="expanded",
)

# ---------------- Dark Styling ----------------
st.markdown("""
<style>
[data-testid="stFileUploaderDropzone"] {
    background-color: #020617 !important;
    border: 1px dashed #334155 !important;
}
[data-testid="stFileUploaderDropzone"] p,
[data-testid="stFileUploaderDropzone"] small {
    color: #ffffff !important;
    opacity: 1 !important;
}
[data-testid="stFileUploaderDropzone"] button {
    background-color: #020617 !important;
    color: #ffffff !important;
    border: 1px solid #334155 !important;
}
[data-testid="stFileUploaderDropzone"] button:hover { border-color: #ef4444 !important; }
[data-testid="stFileUploaderDropzone"] svg { fill: white !important; }
[data-testid="stFileUploaderDropzone"] * { color: #ffffff !important; }
button.preset:hover { background-color: #ef4444; color: white; }
</style>
""", unsafe_allow_html=True)

st.markdown(f"<h1 style='color:#ef4444'>{APP_NAME}</h1>", unsafe_allow_html=True)
st.caption("Precision cropping • batch export • undo/redo • reset zoom/crop")

# ---------------- Session State ----------------
HISTORY_LIMIT = 10

def init_state():
    st.session_state.setdefault("images", [])
    st.session_state.setdefault("index", 0)
    st.session_state.setdefault("history", {})
    st.session_state.setdefault("redo", {})
    st.session_state.setdefault("crops", {})
    st.session_state.setdefault("preset", None)
    st.session_state.setdefault("custom_base", "")
    st.session_state.setdefault("zoom", 1.0)

init_state()

# ---------------- Helpers ----------------
PRESETS = {
    "Instagram Square": ((1,1), (1080,1080)),
    "Instagram Portrait": ((4,5), (1080,1350)),
    "YouTube Thumbnail": ((16,9), (1280,720)),
    "TikTok / Reels": ((9,16), (1080,1920)),
}

def ext_from_format(fmt):
    return "jpg" if fmt == "JPEG" else fmt.lower()

def aspect_tuple(v):
    return {
        "Free": None,
        "1:1": (1,1),
        "16:9": (16,9),
        "4:5": (4,5),
        "9:16": (9,16)
    }[v]

def push_history(idx, img):
    h = st.session_state.history.setdefault(idx, [])
    h.append(img.copy())
    if len(h) > HISTORY_LIMIT:
        h.pop(0)
    st.session_state.redo[idx] = []

def undo(idx):
    h = st.session_state.history.get(idx, [])
    if h:
        st.session_state.redo.setdefault(idx, []).append(st.session_state.crops[idx])
        st.session_state.crops[idx] = h.pop()

def redo(idx):
    r = st.session_state.redo.get(idx, [])
    if r:
        st.session_state.history.setdefault(idx, []).append(st.session_state.crops[idx])
        st.session_state.crops[idx] = r.pop()

def filename_template(name, i, mode, custom_base=None):
    base = os.path.splitext(name)[0]
    if mode == "original":
        return base
    if mode == "original_cropped":
        return f"{base}_cropped"
    return custom_base or f"custom_{i+1}"

# ---------------- Sidebar ----------------
with st.sidebar:
    st.header("Controls")

    uploads = st.file_uploader(
        "Open Images",
        type=["png","jpg","jpeg","gif"],
        accept_multiple_files=True
    )

    if uploads:
        names = [u.name for u in uploads]
        order = sort_items(names)
        reordered = [u for name in order for u in uploads if u.name == name]
        st.session_state.images = reordered
        st.session_state.index = 0
        st.session_state.history.clear()
        st.session_state.redo.clear()
        st.session_state.crops.clear()
        st.session_state.preset = None
        st.session_state.custom_base = ""
        st.session_state.zoom = 1.0

    aspect = st.selectbox("Aspect Ratio", ["Free","1:1","16:9","4:5","9:16"])
    st.session_state.zoom = st.slider("Zoom", 0.3, 3.0, st.session_state.zoom, 0.1)

    out_format = st.selectbox("Output Format", ["PNG","JPEG","GIF"])
    fname_mode = st.selectbox("Filename Template", ["original","original_cropped","custom"])
    if fname_mode == "custom":
        st.session_state.custom_base = st.text_input("Custom Base Name", st.session_state.custom_base)

    st.subheader("Presets")
    preset_cols = st.columns(2)
    for i,(k,v) in enumerate(PRESETS.items()):
        if preset_cols[i%2].button(k, key=f"preset-{k}"):
            st.session_state["preset"] = k

    col1,col2 = st.columns(2)
    with col1:
        if st.button("Prev (J)", key="prev-btn"):
            st.session_state.index = (st.session_state.index-1)%len(st.session_state.images)
            st.session_state.zoom = 1.0
    with col2:
        if st.button("Next (K)", key="next-btn"):
            st.session_state.index = (st.session_state.index+1)%len(st.session_state.images)
            st.session_state.zoom = 1.0

    col3,col4 = st.columns(2)
    with col3:
        if st.button("Undo (U)", key="undo-btn"):
            undo(st.session_state.index)
    with col4:
        if st.button("Redo (R)", key="redo-btn"):
            redo(st.session_state.index)

# ---------------- Keyboard Shortcuts ----------------
st.markdown("""
<script>
document.addEventListener("keydown", e=>{
 if(e.key=="j")document.getElementById("prev-btn")?.click();
 if(e.key=="k")document.getElementById("next-btn")?.click();
 if(e.key=="u")document.getElementById("undo-btn")?.click();
 if(e.key=="r")document.getElementById("redo-btn")?.click();
});
</script>
""", unsafe_allow_html=True)

# ---------------- Main ----------------
if not st.session_state.images:
    st.info("Upload images to begin.")
    st.stop()

idx = st.session_state.index
file = st.session_state.images[idx]
original_img = Image.open(file).convert("RGB")
img = original_img.copy()

# Apply zoom
if st.session_state.zoom != 1.0:
    w,h = img.size
    img = img.resize((int(w*st.session_state.zoom), int(h*st.session_state.zoom)), Image.LANCZOS)

# Preset handling
if st.session_state.preset:
    preset_ratio, preset_size = PRESETS[st.session_state.preset]
else:
    preset_ratio = aspect_tuple(aspect)
    preset_size = None

left,right = st.columns([3,1])

with left:
    st.subheader(f"{idx+1}/{len(st.session_state.images)}")

    # Reset buttons
    reset_col1, reset_col2 = st.columns(2)
    with reset_col1:
        if st.button("Reset Crop", key="reset-crop"):
            if idx in st.session_state.crops:
                st.session_state.crops.pop(idx)
    with reset_col2:
        if st.button("Reset Zoom", key="reset-zoom"):
            st.session_state.zoom = 1.0
            img = original_img.copy()

    cropped = st_cropper(
        img,
        aspect_ratio=preset_ratio,
        realtime_update=True
    )

    if preset_size:
        cropped = cropped.resize(preset_size, Image.LANCZOS)

# Save crop + history
if idx not in st.session_state.crops:
    st.session_state.crops[idx] = cropped
else:
    if cropped.tobytes() != st.session_state.crops[idx].tobytes():
        push_history(idx, st.session_state.crops[idx])
        st.session_state.crops[idx] = cropped

with right:
    st.subheader("Preview")
    st.image(st.session_state.crops[idx], width=300, clamp=True)
    w,h = st.session_state.crops[idx].size
    st.write(f"{w} × {h}")

    buf = BytesIO()
    fmt = out_format
    ext = ext_from_format(fmt)
    save_img = st.session_state.crops[idx]
    if fmt == "GIF":
        save_img = save_img.convert("P", palette=Image.ADAPTIVE)
    save_img.save(buf, format=fmt, save_all=(fmt=="GIF"))

    st.download_button(
        "Save Current",
        data=buf.getvalue(),
        file_name=filename_template(file.name, idx, fname_mode, st.session_state.custom_base)+f".{ext}",
        mime=f"image/{ext}"
    )

# ---------------- Batch Export ----------------
st.markdown("---")
if st.button("Batch Auto-Save (ZIP ALL)"):
    with st.spinner("Preparing ZIP..."):
        zip_buf = BytesIO()
        with zipfile.ZipFile(zip_buf, "w", zipfile.ZIP_DEFLATED) as z:
            for i, f in enumerate(st.session_state.images):
                im = st.session_state.crops.get(i)
                if im is None:
                    im = Image.open(f).convert("RGB")
                b = BytesIO()
                fmt = out_format
                ext = ext_from_format(fmt)
                im.save(b, format=fmt)
                name = filename_template(f.name, i, fname_mode, st.session_state.custom_base)
                z.writestr(f"{name}.{ext}", b.getvalue())
        zip_buf.seek(0)
        st.download_button(
            "Download ZIP",
            data=zip_buf,
            file_name="cropped_images.zip",
            mime="application/zip"
        )

st.markdown(
    "<a href='https://github.com/rogers-cyber' target='_blank'>Mate Technologies</a> • Streamlit Pro Edition",
    unsafe_allow_html=True
)
