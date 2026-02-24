import torch
from diffusers import StableDiffusionPipeline
from datetime import datetime

def load_model():
    print("Loading AI model... Please wait.")

    model_id = "runwayml/stable-diffusion-v1-5"

    pipe = StableDiffusionPipeline.from_pretrained(
        model_id,
        torch_dtype=torch.float32
    )

    pipe = pipe.to("cpu")   # Change to "cuda" if GPU available

    print("Model loaded successfully.\n")
    return pipe


def generate_image(pipe, prompt, style, img_no):
    styled_prompt = f"{prompt}, {style} style, high quality, detailed"

    image = pipe(styled_prompt).images[0]

    filename = f"ai_output_{img_no}.png"
    image.save(filename)

    print(f"Image {img_no} generated and saved as {filename}")


def main():
    pipe = load_model()

    prompt = input("Enter image description: ")

    print("\nSelect style:")
    print("1. Realistic")
    print("2. Artistic")
    print("3. Pencil Sketch")
    print("4. Fantasy Art")

    style_choice = input("Enter choice (1-4): ")

    styles = {
        "1": "realistic",
        "2": "artistic painting",
        "3": "pencil sketch",
        "4": "fantasy digital art"
    }

    style = styles.get(style_choice, "realistic")

    num_images = int(input("\nHow many images to generate? "))

    print("\nGenerating images...\n")

    for i in range(1, num_images + 1):
        generate_image(pipe, prompt, style, i)

    print("\nAll images generated successfully.")


if __name__ == "__main__":
    main()