from unittest import TestCase
import JobChecker



class TestScrape(TestCase):

    def test_Url(self):
        assert JobChecker.run(
            'https://stackoverflow.com/jobs/feed?l=Boston%2c+MA%2c+United+States&u=Miles&d=50') is not None

    #test for user inputting number of jobs to output, fails if input is 0
    def test_UserInput(self):
        assert JobChecker.testUserInput(1) is not 0

    #test for user inputting number of jobs to output, fails if input is greater than 120 (no more than 120 jobs should be available)
    def test_UserInput2(self):
        assert JobChecker.testUserInput(120) is False

    def test_listOfLonLatUpdate(self):
        assert len(JobChecker.listOfLatLonUpdate([],0,0))==1

