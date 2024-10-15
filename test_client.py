# run with 'python -m unittest test_client.py'

import unittest
from client import basic_request


class TestBasicRequest(unittest.TestCase):

    def test_request(self):
        tests = [
            ("test_images/test_image_1.jpg", True),
            ("test_images/test_image_2.jpg", True),
            ("test_images/test_image_3.webp", True),  # Выдаст ошибку из-за неподходящего расширения файла
            ("test_images/test_image_4.png", True),
            ("test_images/test_image_5.png", True)  # Выдаст ошибку из-за того, что данного файла не существует
        ]
        
        for image_path, expected in tests:
            with self.subTest(image_path=image_path):
                self.assertEqual(basic_request(image_path), expected)


if __name__ == "__main__":
    unittest.main()
