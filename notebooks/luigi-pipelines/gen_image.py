import luigi
import json
import requests

# This is your service IP address.  You need to modify this!
# BASE = 'http://52.35.133.2:5000/'

BASE = 'http://192.168.99.100:5000/'
NDEX_URL = 'http://dev2.ndexbio.org/rest/'


class Build(luigi.Task):

    def requires(self):
        return {'id_list': SearchNetworks()}

    def run(self):
        id_list = self.input()['id_list'].open('r')
        ids = json.loads(id_list.read())

        for ndex_id in ids:
            yield GenerateImage(ndex_id)


class SearchNetworks(luigi.Task):
    '''
    Generate list of NDEx IDs.
    '''

    def output(self):
        return luigi.LocalTarget('ndex_id_list.json')

    def run(self):
        search_query = {
            "searchString": "*"
        }

        search_url = NDEX_URL + 'network/search/0/100'
        res = requests.post(search_url, json=search_query)

        result = res.json()
        ids = self.__filter(result)

        with self.output().open('w') as f:
            f.write(json.dumps(ids))

    def __filter(self, result):
        id_list = []

        for entry in result:
            if 'externalId' in entry:
                id_list.append(entry['externalId'])

        return id_list



class GetNetworkFile(luigi.Task):

    network_id = luigi.Parameter()

    def output(self):
        return luigi.LocalTarget(str(self.network_id) + '.json')

    def run(self):
        with self.output().open('w') as f:
            network_url = NDEX_URL + 'network/' + self.network_id + '/asCX'
            response = requests.get(network_url, stream=True)

            for block in response.iter_content(1024):
                f.write(block.decode('utf-8'))


class GenerateImage(luigi.Task):
    
    network_id = luigi.Parameter()

    def requires(self):
        return {'cx': GetNetworkFile(self.network_id)}

    def output(self):
        return luigi.LocalTarget("graph_image_" + self.network_id + ".svg")

    def run(self):
        with self.output().open('w') as f:
            svg_image_url = BASE + 'image/svg'
            cx_file = self.input()['cx'].open('r')
            data = json.loads(cx_file.read())
            res = requests.post(svg_image_url, json=data)
            cx_file.close()

            f.write(res.content.decode('utf-8'))

if __name__ == '__main__':
    luigi.run(['Build', '--workers', '10'])
