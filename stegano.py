import argparse
from PIL import Image

def encode_image(img, msg):
    """
    Encode a message into an image using the least significant bit.
    """
    # Convert the message to binary
    binary_msg = ''.join([format(ord(char), '08b') for char in msg])
    # Ensure the message can be encoded in the image
    if len(binary_msg) > img.width * img.height * 3:  # Times 3 because we use R, G, B
        raise ValueError("Message is too long to be encoded in the image.")
    
    encoded_img = img.copy()
    pixels = encoded_img.load()
    data_iter = iter(binary_msg)

    for row in range(img.height):
        for col in range(img.width):
            pixel = list(pixels[col, row])
            for i in range(3):  # Modify R, G, B channels
                try:
                    bit = next(data_iter)
                except StopIteration:
                    pixels[col, row] = tuple(pixel)
                    return encoded_img
                pixel[i] = pixel[i] & ~1 | int(bit)
            pixels[col, row] = tuple(pixel)
    return encoded_img

def decode_image(img):
    """
    Decode a message from an image encoded using the least significant bit.
    """
    binary_data = []
    pixels = img.load()

    for row in range(img.height):
        for col in range(img.width):
            pixel = pixels[col, row]
            for i in range(3):  # Read R, G, B channels
                binary_data.append(pixel[i] & 1)

    binary_data = [str(bit) for bit in binary_data]
    # Convert binary data to ASCII
    chars = []
    for b in range(0, len(binary_data), 8):
        byte = binary_data[b:b+8]
        chars.append(chr(int(''.join(byte), 2)))
        if chars[-1] == '#':  # Assuming '#' is the delimiter
            break

    return ''.join(chars[:-1])  # Remove the last '#'

def main():
    parser = argparse.ArgumentParser(description="Image Steganography Tool")
    parser.add_argument("image_path", type=str, help="Path to the image file")
    parser.add_argument("message", nargs='?', default='', type=str, help="Message to encode or decode")
    parser.add_argument("--encode", action="store_true", help="Flag to encode the message into the image")
    parser.add_argument("--decode", action="store_true", help="Flag to decode the message from the image")

    args = parser.parse_args()

    img = Image.open(args.image_path)

    if args.encode:
        if not args.message:
            raise ValueError("No message provided for encoding.")
        secret_msg = args.message + '#'  # Using '#' as delimiter
        encoded_img = encode_image(img, secret_msg)
        encoded_img.save("encoded_image.png")
        print("Message encoded and saved in 'encoded_image.png'")
    elif args.decode:
        decoded_msg = decode_image(img)
        print("Decoded Message:", decoded_msg)
    else:
        print("No action selected. Use --encode or --decode.")

if __name__ == "__main__":
    main()
