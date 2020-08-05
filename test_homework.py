import unittest
import homework

class TestHomework(unittest.TestCase):
    test_data = {'test_none.csv': None, 
                        'test_oneword.csv': [['zebra']],
                        'test_blank.csv': [['Provider Name', 
                                            'CampaignID', 
                                            'Cost Per Ad Click', 
                                            'Redirect Link', 
                                            'Phone Number', 
                                            'Address', 
                                            'Zipcode']],
                        'test_missing_column.csv': [['Provider Name', 
                                                    'CampaignID', 
                                                    'Cost Per Ad Click', 
                                                    'Redirect Link', 
                                                    'Phone Number', 
                                                    # 'Address', 
                                                    'Zipcode']],
                        'Homework_auto.csv': [['Provider Name','Zipcode','Cost Per Ad Click','Redirect Link','AccountId','Phone Number','Address','CampaignID'],
                                                ["Auto R' Us", '"78702"', '"15.00"', 'autorus.com/auto1', '4', '8675309', 'Burton Street', 'AUTO1'],
                                                ['SafeAuto', '"78702"', '"15.00"', 'safeauto.com/auto2', '6', '8675309', 'Bat Street', 'AUTO2'],
                                                ['OddAutos', '"78702"', '"5.00"', 'oddautos.com/auto3', '7', '8675309', 'Tiger King Rd', 'AUTO3'],
                                                ['NoZip', '', '"15.00"', 'nozip.com/auto6', '8', '8675309', 'Halloween Town', ''],
                                                ['LowCostCoverage', '"78702"', '"15.50"', 'lcc.com/auto4', '0', '4592222', 'Christmas Town', 'AUTO4'],
                                                ['PhoneAuto', '78702', '"10.00"', 'phoneauto.com/auto5', '9', '', 'IDK Street', 'AUTO5']
                                                 ],
                        'Homework_home.csv': [['Provider Name','CampaignID','Phone Number','Redirect Link','Zipcode','Address','Cost Per Ad Click','TestColumn'],
                                                ["Home R' Us", 'HOME', '1234567', 'homerus.com', '"78705"', 'Tim Street', '5', 'testColumn'],
                                                ['HomeGuard', 'HOME1', '1234567', 'homeguard.com', '"78705"', 'Tam Street', '5.5', 'testColumn'],
                                                ['WeProtect', 'HOME2', '1234567', 'weprotect.com', '"78705"', '', '6', 'testColumn'],
                                                ['HomesOnly', 'HOME3', '', 'homesonly.com', '"78705"', '6th Street', '5', 'testColumn'],
                                                ['Homes4U', 'HOME5', '1234567', 'homes4u.com', '"78705"', 'North Pole', '6', 'testColumn']
                                                ]
                                            }

    schema = ['Provider Name', 
                'CampaignID', 
                'Cost Per Ad Click', 
                'Redirect Link', 
                'Phone Number', 
                'Address', 
                'Zipcode']

    test_output_file_path = 'test_output_file.csv'

    @classmethod
    def setUpClass(cls):
        import csv
        print('Setting up Test')
        #spin up a bunch of test csvs
        for k, data in cls.test_data.items():
            print(f'Making Test File: {k}')
            with open(k, 'w', newline='') as output_file:
                csv_writer = csv.writer(output_file, lineterminator="\n")
                if data == None:
                    continue
                else:
                    for row in data:
                        csv_writer.writerow(row)
        #spin up a test output csv
        print(f'Making Test Output File: {cls.test_output_file_path}')
        with open(cls.test_output_file_path, 'w', newline='') as output_file:
            csv_writer = csv.writer(output_file, lineterminator="\n")
            csv_writer.writerow(cls.schema)
        


    @classmethod
    def tearDownClass(cls):
        import os
        print('Tearing down Test Files')
        for file in cls.test_data:
            os.remove(file)
        
        os.remove(cls.test_output_file_path)

    # def setUp(self):
    #     pass

    # def tearDown(self):
    #     pass

    def test_null_check(self):
        self.assertFalse(homework.null_check(''))
        self.assertTrue(homework.null_check('zebra'))

    def test_file_checker(self):
        self.assertEqual(homework.file_checker('test_none.csv', TestHomework.schema), {'status': False, 'msg':'Input file is blank'})
        self.assertEqual(homework.file_checker('test_missing_column.csv', TestHomework.schema), {'status':False, 'msg':'Input file is missing required column(s): {\'Address\'}'})
        self.assertEqual(homework.file_checker('Homework_home.csv', TestHomework.schema), {'status':True, 'msg':'Input file valid'})
        
    def test_strip_quotes(self):
        self.assertEqual(homework.strip_quotes('zebra'), 'zebra')
        self.assertEqual(homework.strip_quotes('"zebra"'), 'zebra')
        self.assertEqual(homework.strip_quotes('\'"zebra"\''), 'zebra')
        self.assertEqual(homework.strip_quotes('"zebra'), '"zebra')
        self.assertEqual(homework.strip_quotes(''), '')

    def test_clean_field(self):
        self.assertEqual(homework.clean_field('Provider Name', ''), None)
        self.assertEqual(homework.clean_field('Provider Name', 'zebra'), 'zebra')
        self.assertEqual(homework.clean_field('Cost Per Ad Click', ''), None)
        self.assertEqual(homework.clean_field('Cost Per Ad Click', 'zebra'), None)
        self.assertEqual(homework.clean_field('Cost Per Ad Click', '1,000'), 1000.0)
        self.assertEqual(homework.clean_field('Cost Per Ad Click', '"1,000.05"'), 1000.05)
        self.assertEqual(homework.clean_field('Cost Per Ad Click', '.05'), .05)
        self.assertEqual(homework.clean_field('Cost Per Ad Click', '-.05'), -.05) #allowing negative numbers for this exercise
        self.assertEqual(homework.clean_field('Phone Number', ''), '')

    def test_process_file(self):
        self.assertEqual(homework.process_file('test_blank.csv', TestHomework.test_output_file_path, TestHomework.schema), 0)
        self.assertEqual(homework.process_file('Homework_auto.csv', TestHomework.test_output_file_path, TestHomework.schema), 5)
        self.assertEqual(homework.process_file('Homework_home.csv', TestHomework.test_output_file_path, TestHomework.schema), 4)
    
    def test_process_csvs(self):
        self.assertEqual(homework.process_csvs(list(TestHomework.test_data.keys()), TestHomework.test_output_file_path, TestHomework.schema), 3)



if __name__ == '__main__':
    unittest.main()


