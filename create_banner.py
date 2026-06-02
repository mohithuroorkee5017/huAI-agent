"""
Generate Haridwar University AI Logo/Banner as PNG
Run this script to create a logo image file
"""

from PIL import Image, ImageDraw, ImageFont
import os

def create_haridwar_banner(width=800, height=200, output_file='haridwar_banner.png'):
    """
    Create a professional banner image for Haridwar University AI
    
    Args:
        width: Banner width in pixels (default: 800)
        height: Banner height in pixels (default: 200)
        output_file: Output filename (default: haridwar_banner.png)
    """
    
    # Create image with turquoise gradient
    image = Image.new('RGB', (width, height), color=(29, 209, 161))  # Turquoise
    draw = ImageDraw.Draw(image)
    
    # Create gradient effect (turquoise to cyan)
    for y in range(height):
        # Gradient from turquoise (#1dd1a1) to cyan (#00d2d3)
        r = int(29 + (0 - 29) * (y / height))
        g = int(209 + (210 - 209) * (y / height))
        b = int(161 + (211 - 161) * (y / height))
        draw.rectangle([(0, y), (width, y + 1)], fill=(r, g, b))
    
    try:
        # Try to use a nice font, fallback to default if not available
        title_font = ImageFont.truetype("arial.ttf", 72)
        subtitle_font = ImageFont.truetype("arial.ttf", 32)
    except:
        # Fallback to default font
        title_font = ImageFont.load_default()
        subtitle_font = ImageFont.load_default()
    
    # Add text
    text_color = (255, 255, 255)  # White
    
    # Title: "HARIDWAR UNIV. AI"
    title = "🎤 HARIDWAR UNIV. AI"
    title_bbox = draw.textbbox((0, 0), title, font=title_font)
    title_width = title_bbox[2] - title_bbox[0]
    title_x = (width - title_width) // 2
    title_y = 40
    draw.text((title_x, title_y), title, fill=text_color, font=title_font)
    
    # Subtitle: "Voice-Based AI Assistant"
    subtitle = "Voice-Based AI Assistant"
    subtitle_bbox = draw.textbbox((0, 0), subtitle, font=subtitle_font)
    subtitle_width = subtitle_bbox[2] - subtitle_bbox[0]
    subtitle_x = (width - subtitle_width) // 2
    subtitle_y = title_y + 85
    draw.text((subtitle_x, subtitle_y), subtitle, fill=text_color, font=subtitle_font)
    
    # Save the image
    image.save(output_file)
    print(f"✅ Banner created: {output_file}")
    print(f"   Size: {width}x{height} pixels")
    return output_file

def create_logo_icon(size=256, output_file='haridwar_logo.png'):
    """
    Create a square logo icon for Haridwar University AI
    """
    
    image = Image.new('RGB', (size, size), color=(29, 209, 161))
    draw = ImageDraw.Draw(image)
    
    # Create gradient
    for i in range(size):
        r = int(29 + (0 - 29) * (i / size))
        g = int(209 + (210 - 209) * (i / size))
        b = int(161 + (211 - 161) * (i / size))
        draw.rectangle([(0, i), (size, i + 1)], fill=(r, g, b))
    
    # Add rounded corners effect
    draw.rectangle([(0, 0), (size-1, size-1)], outline=(255, 255, 255), width=3)
    
    try:
        font = ImageFont.truetype("arial.ttf", int(size // 3))
    except:
        font = ImageFont.load_default()
    
    text = "🎤"
    bbox = draw.textbbox((0, 0), text, font=font)
    text_width = bbox[2] - bbox[0]
    text_height = bbox[3] - bbox[1]
    x = (size - text_width) // 2
    y = (size - text_height) // 2
    
    draw.text((x, y), text, fill=(255, 255, 255), font=font)
    
    image.save(output_file)
    print(f"✅ Logo icon created: {output_file}")
    print(f"   Size: {size}x{size} pixels")
    return output_file

if __name__ == '__main__':
    print("Creating Haridwar University AI Branding Assets...\n")
    
    # Create banner
    create_haridwar_banner(
        width=800, 
        height=200, 
        output_file='haridwar_banner.png'
    )
    
    # Create logo icon
    create_logo_icon(
        size=256,
        output_file='haridwar_logo.png'
    )
    
    print("\n✅ All branding assets created successfully!")
    print("\nFiles generated:")
    print("  • haridwar_banner.png (800x200) - Use for web headers")
    print("  • haridwar_logo.png (256x256) - Use for favicon/branding")
