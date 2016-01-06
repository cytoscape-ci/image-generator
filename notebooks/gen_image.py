
# coding: utf-8

# In[1]:

import luigi

import requests

# This is your service IP address.  You need to modify this!
BASE = 'http://192.168.99.100:5000/'

class Build(luigi.WrapperTask):

    def run(self):
        print("Finished----------------------")

    def requires(self):
        for i in range(20):
            yield GenerateImage(i)


class GenerateImage(luigi.Task):
    
    num = luigi.IntParameter()
 
    def requires(self):
        return []
 
    def output(self):
        return luigi.LocalTarget("graph_image_" + str(self.num) + ".svg")
    
    # Helper function to POST a local CX file
    def post_file(self, url, file_name):
        with open(file_name, 'r') as f:
            return requests.post(url, data=f)
 
    def run(self):
        with self.output().open('w') as f:
            svg_image_url = BASE + 'image/svg'
            res = self.post_file(svg_image_url, 'gal_filtered_2.json')
            f.write(res.content.decode('utf-8'))

if __name__ == '__main__':
    luigi.run(['Build', '--workers', '10'])

