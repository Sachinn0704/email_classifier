import unittest

from masking import mask_pii, restore_pii


class MaskingTests(unittest.TestCase):
    def test_masking_and_restoration_preserve_original_text(self):
        original = "Contact John Smith at john.smith@example.com or 1234567890."
        masked, entities = mask_pii(original)

        self.assertNotIn("john.smith@example.com", masked)
        self.assertNotIn("1234567890", masked)
        self.assertEqual(restore_pii(masked, entities), original)

    def test_replacements_do_not_corrupt_later_match_positions(self):
        original = "Email jane@example.com; call 9876543210; DOB 12/03/2001."
        masked, entities = mask_pii(original)

        self.assertIn("[email]", masked)
        self.assertIn("[phone_number]", masked)
        self.assertIn("[dob]", masked)
        self.assertEqual(restore_pii(masked, entities), original)

    def test_card_number_is_not_also_masked_as_cvv(self):
        original = "Card 4111 1111 1111 1111 expires 12/28."
        masked, entities = mask_pii(original)

        classifications = [entity["classification"] for entity in entities]
        self.assertIn("credit_debit_no", classifications)
        self.assertNotIn("cvv_no", classifications)
        self.assertEqual(restore_pii(masked, entities), original)

    def test_non_string_input_is_rejected(self):
        with self.assertRaises(TypeError):
            mask_pii(None)


if __name__ == "__main__":
    unittest.main()
