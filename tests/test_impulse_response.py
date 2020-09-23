import os
import torch
import unittest
from torch_audiomentations import ApplyImpulseResponse, load_audio
from .utils import TEST_FIXTURES_DIR


class TestApplyImpulseResponse(unittest.TestCase):
    def setUp(self):
        self.sample_rate = 16000
        self.batch_size = 32
        self.input_audio = torch.from_numpy(load_audio(os.path.join(TEST_FIXTURES_DIR, "acoustic_guitar_0.wav"), self.sample_rate))
        self.input_audios = torch.stack([self.input_audio] * self.batch_size)
        self.ir_path = os.path.join(TEST_FIXTURES_DIR, "ir")
        self.ir_transform = ApplyImpulseResponse(self.ir_path, p=1.0)

    def test_impulse_response_with_single_tensor_input(self):
        mixed_input = self.ir_transform(self.input_audio, self.sample_rate)
        self.assertNotEqual(mixed_input.size(-1), self.input_audio.size(-1))

    def test_impulse_response_with_batched_tensor_input(self):
        mixed_inputs = self.ir_transform(self.input_audios, self.sample_rate)
        self.assertEqual(mixed_inputs.size(0), self.input_audios.size(0))
        self.assertNotEqual(mixed_inputs.size(-1), self.input_audios.size(-1))
