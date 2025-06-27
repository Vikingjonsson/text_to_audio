"""
Test runner for all text-to-audio tests.

This module provides a convenient way to run all test suites:
- Voice Management Tests (listing voices, finding voice IDs)
- Voice Selection Tests (interactive voice selection)
- Audio Generation Tests (creating and saving audio files)
"""

import unittest

from text_to_audio.test_audio_generation import TestAudioGeneration
from text_to_audio.test_voice_management import TestVoiceManagement
from text_to_audio.test_voice_selection import TestVoiceSelection


def create_test_suite():
    """Create a test suite containing all test cases."""
    test_suite = unittest.TestSuite()

    test_suite.addTest(unittest.makeSuite(TestVoiceManagement))
    test_suite.addTest(unittest.makeSuite(TestVoiceSelection))
    test_suite.addTest(unittest.makeSuite(TestAudioGeneration))

    return test_suite


def run_all_tests():
    """Run all tests with verbose output."""
    runner = unittest.TextTestRunner(verbosity=2)
    suite = create_test_suite()
    result = runner.run(suite)
    return result.wasSuccessful()


if __name__ == "__main__":
    import sys

    success = run_all_tests()
    sys.exit(0 if success else 1)
