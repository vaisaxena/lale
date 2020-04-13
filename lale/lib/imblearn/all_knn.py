# Copyright 2019 IBM Corporation
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from imblearn.under_sampling import AllKNN as OrigModel
import lale.operators 
from lale.lib.imblearn.base_resampler import BaseResamplerImpl, _input_fit_schema,\
                                            _input_transform_schema, _output_transform_schema,\
                                            _input_predict_schema, _output_predict_schema,\
                                            _input_predict_proba_schema, _output_predict_proba_schema,\
                                            _input_decision_function_schema, _output_decision_function_schema

class AllKNNImpl(BaseResamplerImpl):

    def __init__(self, operator = None, sampling_strategy='auto', random_state=None, 
                n_neighbors=3, kind_sel='all', allow_minority=False, n_jobs=1):
        self._hyperparams = {
            'sampling_strategy': sampling_strategy,
            'random_state': random_state,
            'n_neighbors': n_neighbors,
            'kind_sel': kind_sel,
            'allow_minority': allow_minority,
            'n_jobs': n_jobs}
    
        resampler_instance = OrigModel(**self._hyperparams)
        super(AllKNNImpl, self).__init__(
            operator = operator,
            resampler = resampler_instance)

_hyperparams_schema = {
    'allOf': [
    {   'type': 'object',
        'relevantToOptimizer': ['operator'],
        'additionalProperties': False,
        'properties': {
            'operator':{
                'laleType':'operator'},
            'sampling_strategy': {
                'description': """sampling_strategy : str, list or callable, default='auto'. 
Sampling information to resample the data set.
""",
                'anyOf': [
                    {   'description':"""When ``str``, specify the class targeted by the resampling. 
The number of samples in the different classes will be equalized.
Possible choices are:
``'minority'``: resample only the minority class;
``'not minority'``: resample all classes but the minority class;
``'not majority'``: resample all classes but the majority class;
``'all'``: resample all classes;
``'auto'``: equivalent to ``'not majority'``.""",
                        'enum': ['minority','not minority','not majority', 'all', 'auto']},
                    {   'description':"""- When ``list``, the list contains the classes targeted by the resampling.""",
                        'type': 'array'},
                    {   'description':"""When callable, function taking ``y`` and returns a ``dict``. 
The keys correspond to the targeted classes. The values correspond to the
desired number of samples for each class.""",
                        'laleType': 'Any'}],
                'default': 'auto'},
            'random_state': {
            'description':
                'Control the randomization of the algorithm.',
            'anyOf': [
                { 'description': 'RandomState used by np.random',
                'enum': [None]},
                { 'description': 'The seed used by the random number generator',
                'type': 'integer'},
                { 'description': 'Random number generator instance.',
                'laleType':'Any'}],
            'default': None},
            'n_neighbors':{
                'description': """If ``int``, size of the neighbourhood to consider to compute the nearest neighbors.  
If object, an estimator that inherits from
:class:`sklearn.neighbors.base.KNeighborsMixin` that will be used to
find the nearest-neighbors. Default of None corresponds to KNeighborsClassifier(n_neighbors=1)""",
                'anyOf': [
                    {'laleType':'Any'},
                    {'type': 'integer'}],
                'default': 3},
            'kind_sel':{
                'description':"""Strategy to use in order to exclude samples.
If ``all``, all neighbours will have to agree with the samples of interest to not be excluded.
If ``mode``, the majority vote of the neighbours will be used in order to exclude a sample.""",
                'enum':['all', 'mode'],
                'default':'all'},
            'allow_minority':{
                'description': """If True, it allows the majority classes to become the minority class without early stopping.""",
                'type':'boolean',
                'default': False},
            'n_jobs': {
                'description': 'The number of threads to open if possible.',
                'type': 'integer',
                'default': 1}}}]}

_combined_schemas = {
  '$schema': 'http://json-schema.org/draft-04/schema#',
  'description': """Class to perform under-sampling based on the AllKNN method.""",
  'documentation_url': '',
  'type': 'object',
  'tags': {
    'pre': [],
    'op': ['resampler'],
    'post': []},
  'properties': {
    'hyperparams': _hyperparams_schema,
    'input_fit': _input_fit_schema,
    'input_transform': _input_transform_schema,
    'output_transform': _output_transform_schema,
    'input_predict': _input_predict_schema,
    'output_predict': _output_predict_schema,
    'input_predict_proba': _input_predict_proba_schema,
    'output_predict_proba': _output_predict_proba_schema,
    'input_decision_function': _input_decision_function_schema,
    'output_decision_function': _output_decision_function_schema
}}

#lale.docstrings.set_docstrings(AllKNNImpl, _combined_schemas)

AllKNN = lale.operators.make_operator(AllKNNImpl, _combined_schemas)