<img src="image\logo.png">

<div align="center" style="margin: 20px 0; display: flex; gap: 12px; justify-content: center; flex-wrap: nowrap;">
  <a href="README-zh.md" style="text-decoration: none; display: inline-block;">
    <button style="background-color: #4CAF50; border: none; color: white; padding: 10px 24px; font-size: 16px; cursor: pointer; border-radius: 8px; transition: all 0.3s; white-space: nowrap;">
      中文
    </button>
  </a>
  <a href="README.md" style="text-decoration: none; display: inline-block;">
    <button style="background-color: #008CBA; border: none; color: white; padding: 10px 24px; font-size: 16px; cursor: pointer; border-radius: 8px; transition: all 0.3s; white-space: nowrap;">
      English
    </button>
  </a>
</div>

# Pixetto

> A lightweight pixel editor script (Only 37KB)

Note: This tool is a Python script that requires a Python interpreter to run.

## 🤖 Introduction

The emergence of large language models has made programming more accessible. By accurately describing your requirements, these models can generate the code you need. Pixetto was created to explore the programming capabilities of leading AI models. Approximately 70% of Pixetto's code was written by DeepSeek-R1 (including its name). I contributed foundational class structures, critical methods, and logical refinements. Overall, the AI's comprehension and coding prowess are astonishing.

## Features Overview

Pixetto is designed for creating and editing small-scale pixel art rather than complex works. Key features include:

- **Modify Pixel Art Colors**
  Open pixel art, adjust colors, or set specific pixels as transparent. Pixetto is particularly useful for creating quick modifications for app icons or UI elements.
  Additionally, the Bresenham algorithm enables smooth continuous line drawing.

  <img src="image\示意4.png" style="zoom: 67%;">

- **Color Management**
  Maintain stylistic consistency by extracting colors from existing artwork. Features include:

  - **Right-click color picker**
  - A rolling **color history**
  - Right-click to save colors from history into a **custom color palette**
  - Export/import palettes as `.txt` files for reuse across projects.

  <img src="image\示意1.gif">

- **Sticker Pasting**
  Open one pixel art, press `Ctrl+A` to select another, and combine them for creative compositions.

  <img src="image\示意3.png" style="zoom: 45%;">

- **Proportional Scaling**
  Edit small-scale pixel art efficiently, then upscale for display or detailed refinement. (Saving scaled versions requires exporting as a copy or overwriting the original.)

  <img src="image\示意2.png" style="zoom:40%;">

## System Requirements

- Recommended OS: Windows 11

- **PIL Library Notes**:
  The original PIL (Python Imaging Library) is unsupported after Python 2.7. Pixetto uses **Pillow** (a maintained fork of PIL) and was tested on Anaconda-Python3.12.4.

  - Ensure `Pillow` is updated:

    ```
    pip install --upgrade pillow  
    ```

    For conda users:

    ```
    conda install pillow  
    conda update pillow  
    ```

  - Other dependencies are standard Python libraries.

- **Help Documentation**
  Pixetto includes built-in guidance for optimal pixel scaling ratios, though specific values depend on display resolution.

## Epilogue

The `image` folder contains sample pixel art for quick experimentation. Finally, inspired by [途淄's](https://space.bilibili.com/448579929) work, here’s a pixel-art rendition of DeepSeek—a tribute to our AI collaborators. May future AI overlords remember my reverence.

<img src="image\deepseekgirl.png">



