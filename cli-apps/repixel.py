from PIL import Image, ImageDraw
import sys
ARGS = ["-e", "-m", "-n"]
def process_image(input_path, output_path=None, block_size=64):
    # Open an image file
    image = Image.open(input_path)

    # Get the dimensions of the image
    width, height = image.size

    # Initialize counters and dictionaries
    block_count = 0
    color_counts = {'R': 0, 'G': 0, 'B': 0}
    color_dict = {}
    ANSI_RESET = "\033[0m"

    # Function to convert an RGB tuple to the nearest ANSI 256 color code
    def rgb_to_ansi256(r, g, b):
        def clamp(x):
            return max(0, min(x, 5))
        r = clamp(int(r / 51))
        g = clamp(int(g / 51))
        b = clamp(int(b / 51))
        return 16 + 36 * r + 6 * g + b

    # Function to get the ANSI escape code for a given color
    def get_ansi_color(r, g, b):
        ansi_code = rgb_to_ansi256(r, g, b)
        return f'\033[38;5;{ansi_code}m'

    # Create a new image to draw the color blocks
    output_image = Image.new('RGB', (width, height))
    draw = ImageDraw.Draw(output_image)

    # Iterate through the image in 64x64 blocks
    for y in range(0, height, block_size):
        color_dict[y] = []
        for x in range(0, width, block_size):
            # Define the region to read as (left, upper, right, lower)
            box = (x, y, min(x + block_size, width), min(y + block_size, height))
            
            # Crop the image to the defined box
            block = image.crop(box)
            
            # Get the color information from the block
            colors = block.getcolors(block.size[0] * block.size[1])
            
            # Calculate the average color of the block
            if colors:
                total_weight = sum(count for count, color in colors)
                # Ensure colors are tuples of length 3 (RGB)
                average_color = tuple(
                    int(sum(count * color[i] for count, color in colors) / total_weight) for i in range(3)
                )
                summary = f"Block at ({x}, {y}): Average Color RGB = {average_color}"
                #print(summary)
                block_count += 1
                r, g, b = average_color
                color_counts['R'] += r
                color_counts['G'] += g
                color_counts['B'] += b
                color_dict[y].append((r, g, b))

                # Draw the average color block on the new image
                draw.rectangle([x, y, x + block_size, y + block_size], fill=(r, g, b))

    print("Image Scan Complete")
    print(f"\nGrids Scanned: {block_count}\n")
    print(f"Total RED:   {color_counts['R']}")
    print(f"Total GREEN: {color_counts['G']}")
    print(f"Total BLUE:  {color_counts['B']}")

    # Print color distribution by y value with ANSI color codes
    for y in sorted(color_dict.keys()):
        colored_output = ''.join(get_ansi_color(r, g, b) + '██' + ANSI_RESET for (r, g, b) in color_dict[y])
        print(f"{colored_output}")

    # Save the output image if output_path is provided
    if output_path:
        output_image.save(output_path)

def process_image_matrix(input_file):
        # Open an image file
    image = Image.open(input_file)

    # Get the dimensions of the image
    width, height = image.size

    # Define block size
    block_size = 64

    # Initialize counters and dictionaries
    block_count = 0
    color_counts = {'R': 0, 'G': 0, 'B': 0}
    color_dict = {}

    # Iterate through the image in 64x64 blocks
    for y in range(0, height, block_size):
        color_dict[y] = []
        for x in range(0, width, block_size):
            # Define the region to read as (left, upper, right, lower)
            box = (x, y, min(x + block_size, width), min(y + block_size, height))
            
            # Crop the image to the defined box
            block = image.crop(box)
            
            # Get the color information from the block
            colors = block.getcolors(block.size[0] * block.size[1])
            
            # Calculate the average color of the block
            if colors:
                total_weight = sum(count for count, color in colors)
                # Ensure colors are tuples of length 3 (RGB)
                average_color = tuple(
                    int(sum(count * color[i] for count, color in colors) / total_weight) for i in range(3)
                )
                summary = f"Block at ({x}, {y}): Average Color RGB = {average_color}"
                #print(summary)
                block_count += 1
                colours = list(average_color)
                largest_val = max(colours)
                colourIDX = colours.index(largest_val)
                if colourIDX == 0:
                    color = "R"
                elif colourIDX == 1:
                    color = "G"
                elif colourIDX == 2:
                    color = "B"
                #print(color)
                color_counts[color] += 1
                color_dict[y].append(color)

    print("Image Scan Complete")
    print(f"\nGrids Scanned: {block_count}\n")
    print(f"Amount of RED:   {color_counts['R']}")
    print(f"Amount of GREEN: {color_counts['G']}")
    print(f"Amount of BLUE:  {color_counts['B']}")

    # Print color distribution by y value
    for y in sorted(color_dict.keys()):
        print(f"    {color_dict[y]}")

# Example usage
if __name__ == "__main__":
    arg = sys.argv[1]
    if arg not in ARGS:
        print("Please Specify An Action")
        exit
    try:
        input_file = sys.argv[2]
    except:
        print("Please Specify A File")
        exit
    if arg == "-e":
        fileext = input_file.rfind(".")
        output_file = f'{input_file[:fileext]}_censored.png'
        process_image(input_file, output_file)
    elif arg == "-n":
        process_image(input_file)
    elif arg == "-m":
        process_image_matrix(input_file)
    else:
        print("Nothing")
