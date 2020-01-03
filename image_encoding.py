from zlib import compress, decompress

from mss import mss

from CONSTANTS import MONITOR_NUMBER, WIDTH, HEIGHT, COMPRESSION_LEVEL, CHUNK_COUNT


def get_screenshot():
    # c = ((image.rgb[0] / 255) * 15) << 4 | (image.rgb[1] / 255) * 15
    with mss() as screenshot:
        monitor = screenshot.monitors[MONITOR_NUMBER]
        rect = {'top': monitor["top"], 'left': monitor["left"], 'width': WIDTH, 'height': HEIGHT,
                'mon': MONITOR_NUMBER}
        return screenshot.grab(rect)


def compress_screenshot(image):
    return compress(image.rgb, COMPRESSION_LEVEL)


def decompress_screenshot(compressed_image):
    return decompress(compressed_image, COMPRESSION_LEVEL)


def __cmpr_chunk__(image, image2, chunk_size, chunk_index):
    chunk_width, chunk_height = chunk_size
    for y in range(chunk_height * chunk_index, chunk_height * (chunk_index + 1)):
        for x in range(chunk_width * chunk_index, chunk_width * (chunk_index + 1)):
            if image.pixel(x, y) != image2.pixel(x, y):
                return False
    return True


def __get_changed_chunks__(prev_image, image, chunk_size):
    changed_chunks = []
    for chunk_index in range(0, CHUNK_COUNT):
        if not __cmpr_chunk__(prev_image, image, chunk_size, chunk_index):
            changed_chunks.append(chunk_index)
    return changed_chunks


def get_image_buffer(prev_image=None):
    image = get_screenshot()
    chunk_size = (image.width / CHUNK_COUNT, image.height / CHUNK_COUNT)
    buffer = bytearray()
    for chunk_index in __get_changed_chunks__(prev_image, image, chunk_size):
        buffer.append(chunk_index)
        x_start = chunk_index * chunk_size[0]
        y_start = chunk_index * chunk_size[1]
        for y in range(y_start, y_start + chunk_size[1]):
            for x in range(x_start, x_start + chunk_size[0]):
                buffer.append(image.pixel(x, y))
    return buffer
