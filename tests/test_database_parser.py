import unittest
from my_package.database_parser import parse_txt_to_jsonl
import os

class TestDatabaseParser(unittest.TestCase):

    def test_parser(self):
        # Test case to ensure the parser works as expected
        test_input = "chewbaca_test.txt"
        test_output = "Databases_test.jsonl"
        
        # Create a temporary input file
        with open(test_input, "w") as f:
            f.write("""
            ##########################
            ######## ID: 1 ###########
            ## Case/CPR:  Rent Roll ##
            ##########################
            Client Pin: 100084758 
            Client Name: Test Client 
            User Name: test_user
            Password: test_pass
            DB Server: test_server
            Instance: test_instance
            DB Name: test_db
            Webshare: https://test.com
            Last Login: 2023-09-01
            """)

        # Run the parser
        parse_txt_to_jsonl(test_input, test_output)
        
        # Check that the output file was created and contains the correct data
        with open(test_output, "r") as f:
            lines = f.readlines()
            self.assertIn('"Case/CPR": "Rent Roll"', lines[0])
        
        # Clean up the temporary files
        os.remove(test_input)
        os.remove(test_output)

if __name__ == "__main__":
    unittest.main()
