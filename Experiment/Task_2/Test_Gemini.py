import base64
import re
import os
import time
from tqdm import tqdm
from openai import OpenAI
import json
from pathlib import Path

try:
    from IllusionDict import ILLUSION_DICT
except ImportError:
    print("Error: IllusionDict.py not found. Please ensure it is in the same directory.")
    ILLUSION_DICT = {}

# ================= CONFIGURATION =================
API_KEY = "sk-HnSkFsGko8GUNILGNPUT3uPSH4vYnyJYXAFGhGiTMu3GEkbm"
MODEL_NAME = "gemini-3.1-flash-lite-preview"
client = OpenAI(
    api_key=API_KEY,
    base_url="https://www.dmxapi.cn/v1"
)

current_script_path = Path(__file__).resolve()
parent_dir = current_script_path.parents[2]
cwd = os.path.join(parent_dir, 'Task2_test_data')

IMAGE_ROOT = os.path.join(cwd, "processed_pngs_mix")
ICL_IMAGE_ROOT = os.path.join(cwd, "ICL_images2")
INPUT_JSON = os.path.join(cwd, f"test.json")
OPTION_MAP = {'A': 0, 'B': 1, 'C': 2, 'D': 3}
REFERENCE_IMAGE_PATH = os.path.join(cwd, "Illusion_example.png")
OUTPUT_TXT = os.path.join(cwd, '2Stage_ICL_results', f"ICL_{MODEL_NAME}_results.txt")


# ================= UTILITY FUNCTIONS =================

def encode_image(image_path):
    """Encode local image to Base64."""
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode('utf-8')

def get_png_path(image_name):
    base = os.path.splitext(image_name)[0]
    return f"{base}.png"

def extract_index_from_filename(image_name):
    """extract number from file name"""
    match = re.search(r'(\d+)', image_name)
    return match.group(1) if match else "0"

# ================= PROCESSING PIPELINE =================

def process_tasks():
    os.makedirs(os.path.dirname(OUTPUT_TXT), exist_ok=True)
    with open(OUTPUT_TXT, 'w', encoding='utf-8') as f:
        pass

    with open(INPUT_JSON, 'r', encoding='utf-8') as jf:
        df = json.load(jf)

    total_tasks = len(df)
    print(f"Starting processing {total_tasks} tasks...")

    # encode the reference image used on Stage 1
    if os.path.exists(REFERENCE_IMAGE_PATH):
        ref_img_b64 = encode_image(REFERENCE_IMAGE_PATH)
    else:
        print(f"Warning: Reference image not found at {REFERENCE_IMAGE_PATH}")
        ref_img_b64 = None

    overall_start_time = time.time()

    for item in tqdm(df, desc="Processing"):
        file_index = extract_index_from_filename(item['image_name'])

        target_img_filename = get_png_path(item['image_name'])
        task_img_path = os.path.join(IMAGE_ROOT, target_img_filename)
        if not os.path.exists(task_img_path):
            continue

        try:
            item_start_time = time.time()
            task_img_b64 = encode_image(task_img_path)

            # --- STAGE 1: CLASSIFICATION ---
            classify_msg = (
                "You are provided with a reference image containing 6 types of illusion questions. "
                "In the reference image, each illusion type is presented within a box along with its name. "
                "Some boxes may contain a visual example for the category. "
                "\n\nStudy the reference image carefully, then identify which illusion type the TARGET IMAGE belongs to. "
                "Possible category descriptions are as follows.: \n"
                "1. Visual Anomaly: the following question asks about the number of fingers or toes in the image;"
                "2. Color Illusion: a Ishihara color vision test image and the following question asks to identify the numbers, letters, or patterns within it;"
                "3. Motion Illusion: Static patterns that create a sense of movement."
                "4. Gestalt Illusion: A set of identical or highly similar objects is arranged in a row–column grid, and the following question asks you to identify the object that differs from the others and indicate its location."
                "5. Geometric and Spatial Illusion: Some classic visual illusions like Sander's Illusion;"
                "6. Visual Illusion: These are illusions created using perspective techniques, such as an image of a person lifting a car."
                "Choose ONLY from:[Visual Anomaly, Color Illusion, Motion Illusion, Gestalt Illusion, Geometric and Spacial Illusion, Visual Illusion]"
                "\n\nAnswer with the category name only."
            )

            classify_content = []
            if ref_img_b64:
                classify_content.append({"type": "text", "text": "REFERENCE IMAGE (6 Illusions Guide):"})
                classify_content.append(
                    {"type": "image_url", "image_url": {"url": f"data:image/png;base64,{ref_img_b64}"}})

            classify_content.append({"type": "text", "text": "TARGET IMAGE TO CLASSIFY:"})
            classify_content.append(
                {"type": "image_url", "image_url": {"url": f"data:image/png;base64,{task_img_b64}"}})
            classify_content.append({"type": "text", "text": classify_msg})

            response_class = client.chat.completions.create(
                model=MODEL_NAME,
                messages=[{"role": "user", "content": classify_content}],
                temperature=0,
                max_tokens=800
            )
            ill_type = response_class.choices[0].message.content.strip()

            # --- STAGE 2: BUILD MULTI-IMAGE ICL PROMPT ---
            info = ILLUSION_DICT.get(ill_type, {"hint": "Examine the geometry carefully.", "examples": []})
            messages = [{
                "role": "system",
                "content": "You are a high-precision visual perception engine. You can reason about the image–question pair using well-established prior knowledge and the physical laws of the real world, and provide the correct answer."
            }]

            user_content = [{"type": "text",
                             "text": f"Type: {ill_type}\nHint: {info['hint']}\n\nStudy these reference examples first:"}]

            for ex in info['examples']:
                ex_path = os.path.join(ICL_IMAGE_ROOT, ex["img"])
                if os.path.exists(ex_path):
                    user_content.append({"type": "text", "text": f"Reference Image ({ex['img']}):"})
                    user_content.append(
                        {"type": "image_url", "image_url": {"url": f"data:image/png;base64,{encode_image(ex_path)}"}})
                    user_content.append(
                        {"type": "text", "text": f"Question: {ex['question']}"})
                    user_content.append(
                        {"type": "text", "text": f"Correct Answer: {ex['ans']} (Reason: {ex['reason']})"})

            user_content.append({"type": "text",
                                 "text": f"\nNOW EVALUATE THIS TARGET IMAGE, Choose ONLY from['A', 'B', 'C', 'D'],"
                                         f"Do not choose option contain Not Sure "
                                         f"Answer with the letter you choose:"
                                         f"\nQuestion: {item['Question']}\nOutput: {item['option']}"})
            user_content.append({"type": "image_url", "image_url": {"url": f"data:image/png;base64,{task_img_b64}"}})

            messages.append({"role": "user", "content": user_content})

            final_response = client.chat.completions.create(
                model=MODEL_NAME,
                messages=messages,
                temperature=0,
                max_tokens=800
            )

            full_reply = final_response.choices[0].message.content

            # extract the option letter
            extraction_system_prompt = "You are a precise data extraction assistant specialized in analyzing model outputs for multiple-choice questions."

            extraction_user_prompt = f"""
            Analyze the following text and extract the final intended answer choice (A, B, C, or D).

            ### Constraints:
            1. Output ONLY the single uppercase letter corresponding to the final choice.
            2. Do not include any punctuation, headers, or explanatory text.
            3. If the text contains multiple mentioned options, identify the one that represents the model's FINAL decision.
            4. If no clear option (A, B, C, or D) is found, output "None".

            ### Text to Analyze:
            {full_reply}

            ### Final Option (Single Letter Only):
            """
            final_extraction = client.chat.completions.create(
                model=MODEL_NAME,
                messages=[
                    {"role": "system", "content": extraction_system_prompt},
                    {"role": "user", "content": extraction_user_prompt}
                ],
                temperature=0,  # 严禁随机性
                max_tokens=2
            )

            # 3. 清洗最终结果
            extracted_result = final_extraction.choices[0].message.content.strip().upper()

            # 4. 极端情况下的正则表达式检查 (Double Check)
            if len(extracted_result) > 1:
                import re
                match = re.search(r'[A-D]', extracted_result)
                extracted_result = match.group(0) if match else "None"

            choice_char = extracted_result

            final_val = OPTION_MAP.get(choice_char, 0)

            with open(OUTPUT_TXT, 'a', encoding='utf-8') as f:
                f.write(f"{file_index} {final_val}\n")

        except Exception as e:
            tqdm.write(f"Error at image {item['image_name']}: {e}")
            continue

        print(f"\nAll tasks completed. Results saved to {OUTPUT_TXT}")

    # 结束统计
    overall_end_time = time.time()
    total_duration = overall_end_time - overall_start_time
    avg_time = total_duration / total_tasks if total_tasks > 0 else 0

    print("\n" + "=" * 50)
    print(f"Processing Complete!")
    print(f"Total Time Taken: {total_duration / 60:.2f} minutes")
    print(f"Average Time per Image: {avg_time:.2f} seconds")
    print(f"Results saved in: {OUTPUT_TXT}")
    print("=" * 50)


if __name__ == "__main__":
    process_tasks()