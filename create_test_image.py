"""
Create a test image for image analysis testing
"""

import os

try:
    from PIL import Image, ImageDraw, ImageFont
    
    # Create a simple test image
    img = Image.new('RGB', (800, 600), color='white')
    draw = ImageDraw.Draw(img)
    
    # Add some shapes and text
    draw.rectangle([50, 50, 300, 250], fill='lightblue', outline='blue', width=2)
    draw.ellipse([350, 50, 550, 250], fill='lightgreen', outline='green', width=2)
    draw.polygon([(600, 50), (750, 250), (600, 250)], fill='lightyellow', outline='orange', width=2)
    
    # Add text
    try:
        font = ImageFont.truetype("arial.ttf", 40)
    except:
        font = ImageFont.load_default()
    
    draw.text((100, 300), "HU Voice AI Test Image", fill='black', font=font)
    draw.text((100, 380), "Objects: Rectangle, Circle, Triangle", fill='darkblue', font=font)
    draw.text((100, 450), "Test Date: Image Analysis Demo", fill='darkgreen', font=font)
    
    # Save image
    output_path = os.path.join(os.path.dirname(__file__), 'test_image.png')
    img.save(output_path)
    
    print(f"✓ Test image created: {output_path}")
    print(f"✓ Image size: {img.size}")
    print(f"✓ Format: PNG")
    
except ImportError:
    print("[ERROR] Pillow not installed. Install with: pip install pillow")
    
    # Fallback: Create a minimal PNG programmatically
    import struct
    import zlib
    
    def create_minimal_png(filename, width=100, height=100):
        """Create a minimal valid PNG file"""
        
        # PNG signature
        png_sig = b'\x89PNG\r\n\x1a\n'
        
        # IHDR chunk (image header)
        ihdr_data = struct.pack('>IIBBBBB', width, height, 8, 2, 0, 0, 0)
        ihdr_crc = zlib.crc32(b'IHDR' + ihdr_data) & 0xffffffff
        ihdr_chunk = struct.pack('>I', 13) + b'IHDR' + ihdr_data + struct.pack('>I', ihdr_crc)
        
        # IDAT chunk (image data - simple red square)
        raw_data = b''
        for y in range(height):
            raw_data += b'\x00'  # filter type
            for x in range(width):
                raw_data += b'\xff\x00\x00'  # RGB red
        
        compressed_data = zlib.compress(raw_data)
        idat_crc = zlib.crc32(b'IDAT' + compressed_data) & 0xffffffff
        idat_chunk = struct.pack('>I', len(compressed_data)) + b'IDAT' + compressed_data + struct.pack('>I', idat_crc)
        
        # IEND chunk (image end)
        iend_crc = zlib.crc32(b'IEND') & 0xffffffff
        iend_chunk = struct.pack('>I', 0) + b'IEND' + struct.pack('>I', iend_crc)
        
        # Write PNG file
        with open(filename, 'wb') as f:
            f.write(png_sig + ihdr_chunk + idat_chunk + iend_chunk)
        
        return filename
    
    output_path = os.path.join(os.path.dirname(__file__), 'test_image.png')
    create_minimal_png(output_path, 100, 100)
    print(f"✓ Minimal test image created: {output_path}")
    print("[INFO] For better test images, install Pillow: pip install pillow")

except Exception as e:
    print(f"[ERROR] Failed to create test image: {str(e)}")
