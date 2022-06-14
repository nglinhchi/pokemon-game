import junitxml
import unittest

if __name__ == '__main__':
    suite = unittest.defaultTestLoader.discover('tests')
    filename = "TestResult.xml"
    FILE = open(filename, "w")
    result = junitxml.JUnitXmlResult(FILE)
    result.startTestRun()
    suite.run(result)
    result.stopTestRun()
