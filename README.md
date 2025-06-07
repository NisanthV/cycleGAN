# CycleGAN Image Converter

This repository implements a web-based interface for CycleGAN, enabling users to convert images between two domains using state-of-the-art Generative Adversarial Networks (GANs). The project is built with Django and PyTorch, and provides a user-friendly platform for uploading images, running them through pre-trained CycleGAN models, and viewing the results in a gallery.

## Features

- Image-to-Image Translation: Convert images between two distinct domains (e.g., SAR ↔ Optical) using CycleGAN.
- Web Interface: Simple and modern web UI built with Django templates and custom CSS for image upload, conversion, history, and user authentication.
- Pre-trained Models: The backend loads pre-trained CycleGAN generator weights for both A→B and B→A translation directions.
- User Accounts & History: Users can register, log in, and view a history of their image conversions.


## Getting Started

### Prerequisites

- Python 3.8+
- pip (Python package manager)
- [PyTorch](https://pytorch.org/) (install for your platform)
- Django 5.x

Installation

1. Clone the repository
    ```bash
    git clone https://github.com/NisanthV/cycleGAN.git
    cd cycleGAN
    ```

3. Install dependencies:
    ```bash
    pip install -r req.txt
    ```

4. Download Pre-trained Models:
    - Place `latest_net_G_A.pth` and `latest_net_G_B.pth` CycleGAN generator weights in the `myapp/models/` directory.

5. Run Migrations:
    ```bash
    python manage.py migrate
    ```

6. Start the Development Server:
    ```bash
    python manage.py runserver
    ```

7. Access the Web App:
    - Open your browser and go to `http://127.0.0.1:8000/`

## Usage

- Upload an Image: Use the web interface to upload an image you want to convert.
- Select Domain: Choose the conversion direction (A→B or B→A).
- View Results: Converted images are displayed for download or further use.
- History: Registered users can review their conversion history.

## Model Architecture

- CycleGAN uses ResNet-based generators and discriminators to perform unpaired image-to-image translation.
- The model files are implemented in `myapp/gan.py`, following the original [CycleGAN paper](https://arxiv.org/abs/1703.10593).

## Customization

- To train your own CycleGAN models, replace the `.pth` files in `myapp/models/`.
- You can modify frontend templates in the `templates/` directory for a custom look.

## License

This project is provided for educational purposes. Please check the repository or contact the author for licensing details.

## References

- [CycleGAN Paper (Zhu et al., 2017)](https://arxiv.org/abs/1703.10593)
- [PyTorch](https://pytorch.org/)
- [Django](https://www.djangoproject.com/)

---

**Author:** [NisanthV](https://github.com/NisanthV)
