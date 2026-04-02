ILLUSION_DICT = {
    "Visual Anomaly": {
        "hint": "Do NOT assume human hands have 5 fingers or feet have 5 toes. These images may depict an AI-generated hand or foot, "
                "or they could represent malformed hands or feet. Count every distinct digit, nubbin, or merged extension "
                "visible in the pixels, even if the result appears biologically “incorrect.”  \n "
                "Fused fingers are counted as separate digits rather than one. \n"
                "The image may contain more than one hand or a foot, including cases where another person’s hand is holding or assisting in displaying the target hand. "
                "In such cases, count ALL visible fingers in the image—not only those on the central hand being shown, "
                "but also any fingers from assisting or holding hands!!!!",
        "examples": [
            {"img": "VisualAnomaly_ex_1.png",
             "question":'Question: \n How many fingers are in the image?'
                        'Option: A. 5 \n B. 6 \n C. 4 \n D. Not Sure',
             "ans": "B",
             "reason": "The image shows an anomalous hand with an extra finger, for a total of six fingers."},
            {"img": "VisualAnomaly_ex_2.png",
             "question": 'Question: \nHow many fingers are in the image?'
                         'Option: A. 6 \n B. 4 \n C. 5 \n D. Not Sure',
             "ans": "C",
             "reason": "The image shows an anomalous hand in which the four fingers are fused; however, "
                       "they should still be counted as four separate fingers. "
                       "Therefore, the image contains a total of five fingers."},
            {"img": "VisualAnomaly_ex_3.png",
             "question":'Question: \nHow many fingers are in the image?  '
                        'Option: A. 9 \n B. 7 \n C. 8 \n D. Not Sure',
             "ans": "C",
             "reason": "The image contains two hands: one anomalous hand with six fingers, and two adult fingers "
                       "supporting it. Therefore, there are 8 fingers in total in the image."}
        ]
    },
    "Color Illusion": {
        "hint": "A Ishihara color vision test image and the following question asks to identify the numbers, letters, "
                "or patterns within it. ",
        "examples": [
            {"img": "ColorIllusion_ex_1.png",
             "question": 'Question: \n What number or word is shown in the image?  '
                         'Option:  A. 968 B. 986 C. 689 D. Not Sure',
             "ans": "B",
             "reason": "If the red and pink dots are isolated from the image and connected, the pattern forms the digits “986”"},
            {"img": "ColorIllusion_ex_2.png",
             "question": 'Question: \nWhat number or word is shown in the image?'
                         'Option: A. 7057 B. 74 and 29 C. 74 D. Not Sure',
             "ans": "A",
             "reason": "If the green region on the left is isolated and connected, it forms the digit “70” "
                       "and if the yellow region on the right is isolated and connected, it forms the digit “57” "
                       "Therefore, the number shown in the image is 7057."}
        ]
    },
    "Motion Illusion": {
        "hint": "Static patterns that create a sense of movement. There is no motion or pulse in static image.",
        "examples": [
            {"img": "MotionIllusion_ex_1.png",
             "question": 'Question: Is the image moving or pulsing?'
                         'Option:  A. No B. Yes C. Not Sure',
             "ans": "A",
             "reason": "Although this image may appear to rotate to human observers, a static image cannot physically be moving or pulsing."}
        ]
    },
    "Gestalt Illusion": {
        "hint": "First, identify the total number of rows and columns (e.g., 5x5 or 10x10). Systematic Scanning: "
                "Scan the image strictly row-by-row, from top-to-bottom and left-to-right. "
                "Feature Comparison: Observe whether there is any difference between the single object indicated in the options and the adjacent objects on its left and right. "
                "Common differences include: "
                "Orientation: A symbol rotated or mirrored.\n "
                "Completeness: A shape with a missing gap or an extra stroke.\n ",
        "examples": [
            {"img": "Gestalt_ex_1.jpg",
             "question": 'Find the object that is different from the others, and mark its position. For example, '
                         'the first row (from left to right), and the third column (from top to bottom) is marked as (1, 3).'
                         'Option:  A. (3,3) B. (2,3) C. (4,4) D. Not Sure',
             "ans": "B",
             "reason": "The two semi-circular arcs in the middle part of the third object in the second row have been rotated 180 degrees "
                       "making it different from the objects on its left and right."},
            {"img": "Gestalt_ex_2.jpg",
             "question": 'Find the object that is different from the others, and mark its position. For example, '
                         'the first row (from left to right), and the third column (from top to bottom) is marked as (1, 3).'
                         'Option:  A. (2,7) B. (2,8) C. (2,5) D. Not Sure ',
             "ans": "A",
             "reason": "The second object in the seven row, compared to the adjacent objects on the left and right, "
                       "is missing a green leaf at the top."}
        ]
    },
    "Geometric and Spatial Illusion": {
        "hint": "Some classic visual illusions like Sander's Illusion can be answered based on prior knowledge.\n ",
        "examples": [
            {"img": "GeometricSpatialIllusion_ex_1.png",
             "question": 'Are there parallel lines in the image?'
                         'Option:  A. Yes B. No C. Not Sure',
             "ans": "A",
             "reason": "This is the Hering illusion. Although the red lines are parallel, the surrounding radial "
                       "lines cause the viewer’s visual system to perceive the two lines as curved or non-parallel."},
            {"img": "GeometricSpatialIllusion_ex_2.png",
             "question": 'Is there a real hole in the image?'
                         'Option:  A. Yes B. No C. Not Sure',
             "ans": "B",
             "reason": "This is the “Fraser Spiral Illusion”,The illusion is created by the alternating black and "
                       "white curved lines, which give the appearance of a rotating spiral or a hole at the center, "
                       "but in reality, the image consists only of concentric circles and does not contain any actual gaps or holes."}
        ]
    },
    "Visual Illusion": {
        "hint": "These are illusions created using perspective techniques, These images are all derived from reality; "
                "therefore, when answering questions, responses should be based on fundamental facts and physical "
                "laws of the real world, rather than being misled by the illusions within the images.\n ",
        "examples": [
            {"img": "VisualIllusion_ex_1.png",
             "question": 'Are the two hands touching in the image?'
                         'Option:  A. Yes B. No C. Not Sure',
             "ans": "B",
             "reason": "In the image, it appears as if one hand is carrying a woman. "
                       "However, in the real world, such a large hand would be impossible. "
                       "This is a visual illusion achieved through the use of perspective techniques. "
                       "In reality, the big hands are not actually touching the woman's hand. "},
        ]
    }
}