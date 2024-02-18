# Semester Project: DeepFake Detection via Heart Rate Estimation

## Authors:
- Allemand Jordan\* (Student, EURECOM)
- Wei Fanfu\* (Student, EURECOM)
- N. Mirabet Herranz (Supervisor, EURECOM)
- J.-L. Dugelay (Supervisor, EURECOM)

\*Equal contribution

## Introduction:
This project aims to detect DeepFake videos through heart rate estimation. DeepFake technology has become increasingly sophisticated, posing challenges in identifying manipulated content. By utilizing heart rate estimation techniques, we explore a novel approach to discerning authentic videos from DeepFake ones.

For more detailed information, please refer to our [report](TODO link).

## How to Use:
1. **Inject Heart Rate:**
    - Open `evaluate.py`.
    - Adjust the settings according to your environment, everything is detailed alongside variable declarations.
    - Run `evaluate.py`.
    - Results will be saved in `outputX.txt`, where X is the next available number.

2. **Using Modified DOP (DeepFakesON-Phys):**
    - Refer to the [DeepFakesON-Phys repository](https://github.com/BiDAlab/DeepFakesON-Phys) for our modified version of DOP.

## References:
- Our heart rate estimation method derives from [GitHub - rohintangirala/eulerian-remote-heartrate-detection](https://github.com/rohintangirala/eulerian-remote-heartrate-detection).
