import unittest
from io import StringIO

from robot.run import run_cli
from robot.running import TestSuite
from robot.utils.asserts import assert_equal


def run(suite: TestSuite, **kwargs):
    config = dict(output=None, log=None, report=None,
                  stdout=StringIO(), stderr=StringIO())
    config.update(kwargs)
    result = suite.run(**config)
    return result.suite


def assert_suite(suite, name, status, message='', tests=1):
    assert_equal(suite.name, name)
    assert_equal(suite.status, status)
    assert_equal(suite.message, message)
    assert_equal(len(suite.tests), tests)


def assert_test(test, name, status, tags=(), msg=''):
    assert_equal(test.name, name)
    assert_equal(test.status, status)
    assert_equal(test.message, msg)
    assert_equal(tuple(test.tags), tags)


class DependencyOnTest(unittest.TestCase):
    def test_dependency_on_passed_test(self):
        suite = TestSuite.from_file_system("data/suite_passed_01.robot").config(name="This suite")
        result = run(suite)
        assert_suite(result, 'This suite', 'PASS', tests=2)

    def test_dependency_on_skipped_test(self):
        suite = TestSuite.from_file_system("data/depends_on_test_skipped.robot").config(name="This suite")
        result = run(suite)
        assert_suite(result, 'This suite', 'SKIP', tests=2)
        assert_test(result.tests[0], 'Skipped Test', 'SKIP', msg="This test is skipped for some reason.")
        assert_test(result.tests[1], 'A Test that Depends on "Skipped Test"', 'SKIP',
                    msg="Dependency not met: test case 'Skipped Test' was skipped.")

    def test_dependency_on_failed_test(self):
        suite = TestSuite.from_file_system("data/depends_on_test_failed.robot").config(name="This suite")
        result = run(suite)
        assert_suite(result, 'This suite', 'FAIL', tests=2)
        assert_test(result.tests[0], 'Failing Test', 'FAIL', msg="This test failed for some reason.")
        assert_test(result.tests[1], 'A Test that Depends on "Failing Test"', 'SKIP',
                    msg="Dependency not met: test case 'Failing Test' failed.")

    def test_dependency_on_missing_test(self):
        suite = TestSuite.from_file_system("data/depends_on_test_missing.robot").config(name="This suite")
        result = run(suite)
        assert_suite(result, 'This suite', 'PASS', tests=1)
        assert_test(result.tests[0], 'A Test that Depends on "Missing Test"', 'PASS')
        # todo: assert test gives a warning "Dependency not met: test case 'Missing Test' not found."

    def test_dependency_on_self(self):
        suite = TestSuite.from_file_system("data/depends_on_test_self.robot").config(name="This suite")
        result = run(suite)
        assert_suite(result, 'This suite', 'PASS', tests=1)
        assert_test(result.tests[0], 'Depends on Self', 'PASS')
        # todo: assert test gives a warning "Dependency not met: test case 'Depends on Self' mid-execution."


    def test_dependency_on_multiple_tests(self):
        suite = TestSuite.from_file_system("data/depends_on_test_multiple.robot").config(name="This suite")
        result = run(suite)
        assert_suite(result, 'This suite', 'PASS', tests=3)


class DependencyOnSuite(unittest.TestCase):
    def test_dependency_on_passed_suite(self):
        failed_tests = run_cli(["data/suite_passed_01.robot", "data/depends_on_passed_suite.robot"], exit=False)
        assert_equal(failed_tests, 0)

    def test_dependency_on_missing_suite(self):
        suite = TestSuite.from_file_system("data/depends_on_passed_suite.robot").config(name="This suite")
        result = run(suite)
        assert_suite(result, 'This suite', 'PASS', tests=1)
        assert_test(result.tests[0], "A Test that Depends on an Entire Test Suite Passing", "PASS")
        # todo: assert test gives a warning "Dependency not met: test suite '01 Passing' not found."

    def test_dependency_on_skipped_suite(self):
        failed_tests = run_cli(["data/suite_skipped.robot", "data/depends_on_suite_skipped.robot"], exit=False)
        assert_equal(failed_tests, 0)

    def test_dependency_on_failed_suite(self):
        failed_tests = run_cli(["data/suite_failed.robot", "data/depends_on_suite_failed.robot"], exit=False)
        assert_equal(failed_tests, 1)

    def test_dependency_on_self(self):
        suite = TestSuite.from_file_system("data/depends_on_passed_suite.robot").config(name="Suite Passed 01")
        result = run(suite)
        assert_suite(result, 'Suite Passed 01', 'PASS', tests=1)
        assert_test(result.tests[0], "A Test that Depends on an Entire Test Suite Passing", "PASS")
        # todo: assert test gives a warning "Dependency not met: test suite 'Some Test Suite Name' mid-execution."

    def test_dependency_on_multiple_suites(self):
        failed_tests = run_cli(["data/suite_passed_01.robot", "data/suite_passed_02.robot", "data/depends_on_suite_multiple.robot"], exit=False)
        assert_equal(failed_tests, 0)


if __name__ == '__main__':
    unittest.main()
