from django.apps import AppConfig
import torch
from pathlib import Path
from .gan import ResnetGenerator  # Import the official generator
import torch.nn as nn


class MyAppConfig(AppConfig):
    name = 'myapp'

    def ready(self):
        models_dir = Path(__file__).parent / 'models'

        global G_A2B, G_B2A

        # Initialize Generator A→B
        G_A2B = ResnetGenerator(
            input_nc=3,
            output_nc=3,
            ngf=64,
            norm_layer=nn.InstanceNorm2d,  # Critical change
            n_blocks=9,  # Most common value
            padding_type='reflect'
        )
        G_A2B.load_state_dict(
            torch.load(models_dir / 'latest_net_G_A.pth', map_location='cpu')
        )
        G_A2B.eval()

        # Initialize Generator B→A
        G_B2A = ResnetGenerator(
            input_nc=3,
            output_nc=3,
            ngf=64,
            norm_layer=nn.InstanceNorm2d,
            n_blocks=9,
            padding_type='reflect'
        )
        G_B2A.load_state_dict(
            torch.load(models_dir / 'latest_net_G_B.pth', map_location='cpu')
        )
        G_B2A.eval()