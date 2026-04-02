# A Two-Stage ICL Pipeline for Robust Visual Illusion Understanding

## Project Overview

This project is designed for A Two-Stage ICL Pipeline for Robust Visual Illusion Understanding. It provides the required script and data paths for the experiment.
Paper ID: 34
## Executable Script

- The main executable script is located at `Experiment/Task_2/Test_Gemini.py`.

## Result Storage Path

- The test results will be saved in the directory `Task2_test_data/2Stage_ICL_results`.

## ICL Reference Images

- The reference images for ICL are stored in the `Task2_test_data/ICL_images2` folder for use during testing.

## Image Format Conversion

- The images provided by this project have undergone a uniform format conversion. The processed images are saved in the `Task2_test_data/processed_pngs_mix` folder.

## Usage Instructions

1. **Run the Experiment**:
   Run the `Test_Gemini.py` script after ensuring all dependencies are installed and the data paths are configured properly.
   
2. **Viewing Results**:
   After the testing is complete, check the output results in the `Task2_test_data/2Stage_ICL_results` folder.

3. **Image Processing**:
   If you need to use the original images, the reference images are located in `Task2_test_data/ICL_images2`, and the processed images can be found in `Task2_test_data/processed_pngs_mix`.

## Dependencies

- Please ensure the required Python packages are installed by running:
    ```bash
    pip install -r requirements.txt
    ```

## Contact Information

If you have any questions, please contact [ming_zhang_sjtu@sjtu.edu.cn] or submit an issue through GitHub.