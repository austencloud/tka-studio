# Image Export Features

## Overview

The Kinetic Constructor allows you to export your sequences as high-quality images that can be shared or printed. The export functionality includes several features to enhance your exported images.

## Export Options

### Content Options

- **Include Start Position**: When enabled, the start position will be included in the exported image.
- **Add User Info**: When enabled, your username and a custom note will be added to the bottom of the exported image.
- **Add Word**: When enabled, the sequence word will be added to the top of the exported image.
- **Add Difficulty Level**: When enabled, the difficulty level will be displayed in the exported image.
- **Add Beat Numbers**: When enabled, beat numbers will be displayed in the exported image.
- **Add Reversal Symbols**: When enabled, reversal symbols will be displayed for reversed beats.

### User Information

- **Username**: Your username that will be displayed in the exported image when "Add User Info" is enabled.
- **Custom Note**: A custom note that will be displayed in the exported image when "Add User Info" is enabled.

### Directory Preferences

- **Remember Last Save Directory**: When enabled, the application will remember the last directory you saved to and default to it for future exports.

### Category Information

- **Use Categories**: When enabled, exports will be organized into categories.
- **Default Category**: The default category for organizing exports when "Use Categories" is enabled.

## Exporting Images

To export a sequence as an image:

1. Click the share button in the top-right corner of the sequence workbench.
2. Select "Download as Image" from the dropdown menu.
3. Choose a location to save the image.
4. Click "Save" to download the image.

## Finding Your Exported Images

After exporting an image, you can easily locate it using the following information:

### Desktop Platforms

- A toast notification will appear showing the exact save location and filename of your image.
- The notification will remain visible for several seconds, giving you time to note the location.
- For most browsers, exported images are saved to your Downloads folder by default.

### Mobile Platforms

- A toast notification will appear confirming that the image has been saved to your device's Downloads folder.
- You can access the image through your device's file manager or gallery app.

## Image Quality and Layout

The exported images are high-quality PNG files with the following features:

- Responsive layout that adapts to different sequence lengths
- Clear, readable text with proper scaling
- Proper spacing and alignment of beats
- Inclusion of metadata based on your export settings

For sequences with 6 beats and a start position, the layout will be arranged as follows:

```
s-1-2-3-4
x-5-6-x-x
```

Where "s" represents the start position, numbers represent beats, and "x" represents empty spaces.

## Troubleshooting

If you encounter issues with image export:

1. Ensure you have permission to write to the selected directory.
2. Check that you have enough disk space.
3. If the export fails, try selecting a different directory.
4. If you're using a mobile device, ensure you have granted the necessary permissions to save files.

## Customizing Export Settings

You can customize your export settings in the Settings dialog under the "Image Export" tab. These settings will be applied to all future exports until changed.
