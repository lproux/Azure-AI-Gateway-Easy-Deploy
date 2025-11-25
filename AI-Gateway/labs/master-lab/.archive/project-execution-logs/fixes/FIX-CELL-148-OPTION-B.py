# Cell 148 Fix - Option B: Define Lowercase Alias

# Add at start of Cell 148
image_model = globals().get('IMAGE_MODEL') or 'gpt-image-1'

# Rest of cell remains the same
import time

TEST_PROMPT = "A tiny sketch of a futuristic Azure data center shaped like a cloud, line art"
print(f"[test] Attempting generation with model={image_model}")

start_time = time.time()
result = generate_image(image_model, TEST_PROMPT, '512x512')
elapsed = time.time() - start_time

if result.get('b64'):
    b64_result = result['b64']
    print(f"[test] Success in {elapsed:.2f}s; preview below (first 80 chars):")
    print(b64_result[:80] + '...')

    # Try to display the image
    try:
        from IPython.display import display
        import matplotlib.pyplot as plt
        import io
        import PIL.Image as Image

        img_bytes = base64.b64decode(b64_result)
        im = Image.open(io.BytesIO(img_bytes))
        plt.figure(figsize=(3,3))
        plt.imshow(im)
        plt.axis('off')
        plt.title(f"Test: {image_model}")
        display(plt.gcf())
    except Exception as e:
        print(f"[test] Could not display image: {e}")
else:
    print(f"[test] Failure after {elapsed:.2f}s")
    if result.get('error'):
        print(f"[test] Error: {result['error']}")
    else:
        print(f"[test] Model '{image_model}' did not return image data")
