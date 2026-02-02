# Pro Image Cropper Plus — Streamlit (Full Source Code)

**Pro Image Cropper Plus** is a Python web application built with **Streamlit** for **precision image cropping, batch export, undo/redo, zoom control, and preset aspect ratios**.  
This repository contains the full source code, allowing you to customize **cropping logic, presets, filename templates, batch processing, and UI components** for personal, learning, or professional image editing.

------------------------------------------------------------
🌟 FEATURES
------------------------------------------------------------

- 🖼 Multi-Image Support — Upload multiple PNG, JPEG, and GIF files  
- ✂ Precision Cropping — Freeform or fixed aspect ratios (1:1, 16:9, 4:5, 9:16)  
- 🔁 Undo / Redo — Track crop history with multiple steps  
- 🔍 Zoom Control — Zoom in/out while cropping for better precision  
- 📐 Presets — Instagram, YouTube, TikTok/Reels, and custom crop sizes  
- 💾 Export — Save individual images or batch-export as ZIP  
- 🖥 Live Preview — See cropped result and dimensions in real-time  
- 🧮 Filename Templates — Original, original_cropped, or custom base names  
- ⌨ Keyboard Shortcuts — J/K for navigation, U/R for undo/redo  
- 🎨 Dark Mode Styling — Custom UI colors for file uploader and buttons  

------------------------------------------------------------
🚀 INSTALLATION
------------------------------------------------------------

1. Clone or download this repository:


```
git clone https://github.com/rogers-cyber/ProImageCropperPlusStreamlit.git
cd ProImageCropperPlusStreamlit
```

2. Install required Python packages:

```
pip install streamlit pillow streamlit-cropper streamlit-sortables
```

3. Run the application:

```
streamlit run app.py
```

------------------------------------------------------------
💡 USAGE
------------------------------------------------------------

1. Upload Images:
   - Use the sidebar to select PNG, JPEG, or GIF files  
   - Reorder images using drag-and-drop  

2. Crop Images:
   - Choose **Aspect Ratio** or use preset buttons  
   - Adjust zoom for precise cropping  
   - Reset crop or zoom anytime  

3. Undo / Redo:
   - Use sidebar buttons or keyboard shortcuts (U / R)  

4. Save Images:
   - Save current image individually with download button  
   - Batch-export all images as a ZIP file  

5. Filename Templates:
   - Options: `original`, `original_cropped`, or `custom`  
   - Enter a custom base name if desired  

------------------------------------------------------------
⚙️ CONFIGURATION OPTIONS
------------------------------------------------------------

Option               | Description
-------------------  | --------------------------------------------------
Aspect Ratio          | Free, 1:1, 16:9, 4:5, 9:16 or preset crop sizes  
Zoom                  | Adjust crop area zoom from 0.3× to 3×  
Output Format         | PNG, JPEG, or GIF  
Filename Template     | Original, Original + Cropped, or Custom base  
Presets               | Instagram, YouTube, TikTok/Reels sizes  
Undo / Redo           | Track crop changes per image  
Batch Export          | Download all cropped images as ZIP  

------------------------------------------------------------
📦 OUTPUT
------------------------------------------------------------

- Cropped Images — Individually downloadable in chosen format  
- Image Dimensions — Displayed live in preview pane  
- Batch Export — ZIP containing all cropped images with proper filenames  

------------------------------------------------------------
📦 DEPENDENCIES
------------------------------------------------------------

- Python 3.10+  
- Streamlit — Web app framework  
- Pillow — Image processing  
- streamlit-cropper — Interactive cropper component  
- streamlit-sortables — Drag-and-drop reordering  

------------------------------------------------------------
📝 NOTES
------------------------------------------------------------

- Fully online: runs locally via Streamlit in your browser  
- GIF images are converted using adaptive palette for export  
- Cropping history is limited to 10 steps per image  
- Preset sizes are automatically applied if selected  
- Keyboard shortcuts improve navigation and workflow  

------------------------------------------------------------
👤 ABOUT
------------------------------------------------------------

**Pro Image Cropper Plus** is maintained by **Mate Technologies**, providing a **Streamlit-based precision cropping and batch image export tool** for personal, educational, or professional use.  

Website / Contact: https://github.com/rogers-cyber

------------------------------------------------------------
📜 LICENSE
------------------------------------------------------------

Distributed as source code.  
You may use it for personal or educational projects.  
Redistribution, resale, or commercial use requires explicit permission.
