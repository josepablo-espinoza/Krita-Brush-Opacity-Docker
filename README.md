# Brush Opacity Docker Documentation

<p align="center">
  <img src="/readme-assets/docker.png" />
</p>

<p align="center">
  <img src="/readme-assets/settings.png" />
</p>

## Overview

The Brush Opacity Docker plugin allows you to quickly and easily adjust the opacity of your brush in Krita using predefined opacity presets or by manually setting the opacity.

## Features

- **Preset Selector**: Choose from Small, Medium, Large, or Current Brush presets.
- **Current Brush preset**: It will use the current brush opacity to generte Opacity ranges
- **Manual Opacity Input**: Input box to type the exact opacity.
- **Opacity Slider**: Slider to adjust the preset.
- **User Defined Mode**: Allows the user to define opacities and ranges in the dialog at the top-right of the docker.
- **Shortcut**: Cycle through the opacities using a user-configurable shortcut, default: Ctrl+Alt+Shift+O.
- **Minimize / Hide Docker**: Allows to collapse the docker for better visibility when not in use
- **Pressure Sensitivy**: Toggle brush opacity pressure sensitivity
- **Brush Blending Mode**: Set brush in greater blending mode, handy to avoid "banding"




## Installation

### Method 1 (easiest)

Open Krita go to `Tools > Scripts > Import Python Plugin From Web` and paste the following URL.

https://github.com/josepablo-espinoza/krita-brush-opacity-docker/releases/latest/download/Krita-Brush-Opacity-Docker.zip

### Method 2

1. **Download latest release zip**:

  https://github.com/josepablo-espinoza/krita-brush-opacity-docker/releases/latest/download/Krita-Brush-Opacity-Docker.zip

2. **Upload the plugin into Krita**: 

  Open Krita go to `Tools > Scripts > Import Python Plugin From File` and load the zip file.

3. **Restart Krita**: If Krita was running, restart it to load the new Docker.

4. **Activate the Docker**: 
  Go to `Settings > Dockers > Brush Opacity Docker` to activate the Docker in Krita.

## Usage

Once the Brush Opacity Docker is enabled, it will appear as a new docker in Krita.

## Desired Enhancements

In its current version, all initial user cases have been covered. Leave an issue requesting a feature you think is missing and will improve the user experience.