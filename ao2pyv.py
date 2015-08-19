""" Converts Archive.org video searches into PyVideo.org API submissions.
"""

import json

import requests
import click


ARCHIVE_ORG_SEARCH_URL = 'https://archive.org/advancedsearch.php'
ARCHIVE_ORG_DETAILS_URL = 'https://archive.org/details/'


class FunctionSet(object):
    """ Register a set of functions.
    """
    def __init__(self):
        self._values = {}
        self._default = None

    def __getitem__(self, name):
        return self._values[name]

    def register(self, name, default=False):
        def deco(f):
            self._values[name] = f
            if default:
                self.set_default(name)
            return f
        return deco

    def set_default(self, name):
        if self._default is not None:
            raise ValueError("Default already set to %r" % (self._name,))
        self._default = name

    def keys(self):
        return sorted(self._values.keys())

    @property
    def default(self):
        if self._default is None:
            raise ValueError("Default is not set.")
        return self._default

inputs = FunctionSet()
transforms = FunctionSet()
outputs = FunctionSet()


@inputs.register('archive.org', default=True)
def input_archive_dot_org(source):
    """ Search archive.org for a query and return a list of results.
    """
    r = requests.get(ARCHIVE_ORG_SEARCH_URL, params={
        "q": source,
        "output": "json",
    })
    j = r.json()
    return j["response"]["docs"]


@inputs.register('json_file')
def input_json_file(source):
    """ Return results from a JSON file.
    """
    with open(source) as f:
        return json.loads(f.read())


@transforms.register('none')
def transform_none(video, category, state):
    """ Transform a video result not at all.
    """
    return video


@transforms.register('ao2pyv', default=True)
def transform_ao2pyv(video, category, state):
    """ Transform a video result from archive.org to pyvideo.org format.

        See http://richard.readthedocs.org/en/latest/admin/api.html#videos for
        a description of the pyvideo.org format.
    """
    return {
        "category": category,
        "title": video["title"],
        "language": video["language"][0],
        "state": state,  # 1 == live, 2 == draft
        "speakers": video["creator"],
        "tags": video["subject"],
        "summary": video["description"],  # TODO: truncate to first paragraph
        "description": video["description"],
        "source_url": ARCHIVE_ORG_DETAILS_URL + video["identifier"],
    }


@outputs.register('json_file')
def output_file(destination, videos):
    """ Output results to a file.
    """
    with open(destination, "wb+") as f:
        f.write(json.dumps(videos))


@outputs.register('print', default=True)
def output_print(_destination, videos):
    import pprint
    pprint.pprint(videos)


@click.command()
@click.option(
    '--input', type=click.Choice(inputs.keys()),
    default=inputs.default)
@click.option(
    '--transform', type=click.Choice(transforms.keys()),
    default=transforms.default)
@click.option(
    '--output', type=click.Choice(outputs.keys()),
    default=outputs.default)
@click.option('--draft', 'state', flag_value=2, default=True)
@click.option('--live', 'state', flag_value=1)
@click.argument('category')
@click.argument('source')
@click.argument('destination')
def ao2pyv(category, source, destination, input, transform, output, state):
    videos = inputs[input](source)
    transform = transforms[transform]
    videos = [transform(v, category, state) for v in videos]
    outputs[output](destination, videos)


if __name__ == "__main__":
    ao2pyv()
