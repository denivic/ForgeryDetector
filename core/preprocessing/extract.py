import fitz  # The PyMuPDF module
from PIL import Image
import io
from typing import Union, List


class ImageExtractor():
    def __init__(self):
        pass

    def docload(self, path: str = None) -> Union[List[None], int]:
        if path is None:
            print("[ERROR] No path(s) have been given.")
            return 0

        try:
            with fitz.open(path) as pdf_file:
                for page_number in range(1, len(pdf_file) + 1):
                    # Access individual page
                    page = pdf_file[page_number - 1]
                    images = page.get_images()

                    if images:
                        print(f"Found {len(images)} image/s on page number {page_number}.")

                    # loop through all images on the page
                    for image_number, image in enumerate(page.get_images(), start=1):
                        # Access image xref (a unique identifier)
                        xref_value = image[0]

                        # Extract image information
                        base_image = pdf_file.extract_image(xref_value)

                        # Access the image itself
                        image_bytes = base_image["image"]

                        # Get image extension
                        ext = base_image["ext"]

                        # Load and then save image
                        image = Image.open(io.BytesIO(image_bytes))
                        image.save(open(f"Page{page_number}Image{image_number}.{ext}", "wb"))
        except Exception as e:
            print(e)
