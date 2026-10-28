"""
Official Scannable QR Code Generator
Uses official qrcode library for 100% instant smartphone scanning.
"""
import os
import qrcode

def create_qr_code(text: str, output_path: str):
    """Generates official standard QR code PNG scannable by any mobile camera."""
    qr = qrcode.QRCode(
        version=None,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=12,
        border=4  # Official ISO/IEC 18004 required quiet zone
    )
    qr.add_data(text)
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white")
    img.save(output_path)
    return output_path
