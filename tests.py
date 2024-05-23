from model import RationalLLM
from utils import get_response, get_boolean_completion, get_list
from BeliefNet import DAG
from main import prompt_to_output, prompt_to_output_test

rationalLLM = RationalLLM()

texts = ['Eating meat causes cancer',
         'Brexit would not have passed if the entire population had voted',
         '''Experts have told the BBC that the current Covid surge in China is "unlikely" to impact India, but they urged people to stay cautious and wear masks.

India has stepped up surveillance after a spike in cases in neighbouring China.

People travelling from China and four other Asian countries now have to produce a Covid-19 negative test report before entering India.

On Tuesday, drills were held to check if hospitals could handle a surge.

According to government data, India currently has only around 3,400 active coronavirus cases. But reports of the surge in China and the memories of two deadly Covid waves in 2020 and 2021 in India have made many people fearful''',
'black people are more likely to get cancer']

caches = [{'nodes': ['eating meat', 'causes cancer'], 'factors': ['cultural and societal norms', 'personal taste preferences', 'nutritional benefits', 'convenience and availability', 'economic factors', 'religious or ethical beliefs', 'environmental impacts', 'environmental impact', 'animal welfare', 'health concerns', 'cultural and social norms', 'economic implications', 'genetics', 'environmental factors', 'lifestyle choices', 'exposure to radiation', 'exposure to carcinogens', 'viral infections', 'age', 'health consequences', 'environmental factors', 'lifestyle choices', 'genetic predisposition'], 'factorsParsed': ['cultural and social norms', 'health concerns', 'availability and accessibility', 'dietary preferences and taste', 'environmental impact', 'Eating meat', 'Causes cancer'], 'edges': [['cultural and social norms', 'health concerns', 0.8], ['cultural and social norms', 'availability and accessibility', 0.8], ['cultural and social norms', 'dietary preferences and taste', 1.0], ['cultural and social norms', 'environmental impact', 0.8], ['cultural and social norms', 'Eating meat', 0.6], ['health concerns', 'cultural and social norms', 0.8], ['health concerns', 'availability and accessibility', 0.8], ['health concerns', 'dietary preferences and taste', 0.8], ['health concerns', 'Eating meat', 0.6], ['health concerns', 'Causes cancer', 0.6], ['availability and accessibility', 'cultural and social norms', 0.8], ['availability and accessibility', 'health concerns', 0.6], ['availability and accessibility', 'dietary preferences and taste', 0.8], ['availability and accessibility', 'environmental impact', 0.8], ['availability and accessibility', 'Eating meat', 0.6], ['dietary preferences and taste', 'cultural and social norms', 0.8], ['dietary preferences and taste', 'health concerns', 0.8], ['dietary preferences and taste', 'Eating meat', 0.6], ['environmental impact', 'cultural and social norms', 0.8], ['environmental impact', 'health concerns', 1.0], ['environmental impact', 'dietary preferences and taste', 0.6], ['environmental impact', 'Eating meat', 0.8], ['environmental impact', 'Causes cancer', 0.6], ['Eating meat', 'cultural and social norms', 0.6], ['Eating meat', 'health concerns', 0.6], ['Eating meat', 'availability and accessibility', 0.6], ['Eating meat', 'dietary preferences and taste', 0.8], ['Eating meat', 'environmental impact', 0.8], ['Eating meat', 'Causes cancer', 0.6], ['Causes cancer', 'cultural and social norms', 0.6], ['Causes cancer', 'health concerns', 0.6], ['Causes cancer', 'availability and accessibility', 0.6], ['Causes cancer', 'environmental impact', 0.6], ['Causes cancer', 'Eating meat', 0.6]]},
          {'nodes': ['brexit passed without the entire population voting', 'the entire population did not vote for brexit'], 'factors': ['political decisionmaking', 'lack of universal suffrage', 'referendum process', 'electoral system', 'representation in government', 'lack of democratic mandate', 'potential for division and unrest', 'questions about the legitimacy of the decision', 'possible longterm consequences for the uk and europe', 'incomplete voter turnout', 'voter apathy', 'voter disenfranchisement', 'voter ineligibility', 'voter suppression', 'invalid or spoiled ballots', 'incomplete representation', 'divided public opinion', 'potential for discontent and polarization', 'possible questioning of democratic legitimacy'], 'factorsParsed': ['political decisionmaking', 'lack of universal suffrage', 'referendum process', 'electoral system', 'representation in government', 'brexit passed without the entire population voting', 'the entire population did not vote for brexit'], 'edges': [['political decisionmaking', 'electoral system', 1.0], ['political decisionmaking', 'representation in government', 1.0], ['lack of universal suffrage', 'representation in government', 1.0], ['electoral system', 'political decisionmaking', 1.0], ['electoral system', 'representation in government', 1.0], ['representation in government', 'political decisionmaking', 1.0], ['the entire population did not vote for brexit', 'referendum process', 1.0], ['political decisionmaking', 'lack of universal suffrage', 0.8], ['political decisionmaking', 'referendum process', 0.8], ['political decisionmaking', 'brexit passed without the entire population voting', 0.8], ['political decisionmaking', 'the entire population did not vote for brexit', 0.8], ['lack of universal suffrage', 'political decisionmaking', 0.8], ['lack of universal suffrage', 'electoral system', 0.8], ['lack of universal suffrage', 'the entire population did not vote for brexit', 0.8], ['referendum process', 'political decisionmaking', 0.8], ['electoral system', 'referendum process', 0.8], ['representation in government', 'electoral system', 0.8], ['the entire population did not vote for brexit', 'representation in government', 0.8], ['the entire population did not vote for brexit', 'brexit passed without the entire population voting', 0.8], ['lack of universal suffrage', 'referendum process', 0.6], ['referendum process', 'electoral system', 0.6], ['referendum process', 'representation in government', 0.6], ['referendum process', 'brexit passed without the entire population voting', 0.6], ['referendum process', 'the entire population did not vote for brexit', 0.6], ['electoral system', 'lack of universal suffrage', 0.6], ['electoral system', 'brexit passed without the entire population voting', 0.6], ['electoral system', 'the entire population did not vote for brexit', 0.6], ['representation in government', 'referendum process', 0.6], ['representation in government', 'brexit passed without the entire population voting', 0.6], ['representation in government', 'the entire population did not vote for brexit', 0.6], ['the entire population did not vote for brexit', 'political decisionmaking', 0.6], ['the entire population did not vote for brexit', 'electoral system', 0.6]], 'interpretations': []},
          {'nodes': ['covid surge in china is unlikely to impact india', 'people urged to stay cautious and wear masks', 'india has stepped up surveillance after a spike in cases in neighbouring china'], 'factors': ['geographical distance between china and india', 'stringent travel restrictions and border control measures', 'differences in population density and urbanization levels', 'variations in healthcare infrastructure and capacity', 'divergent approaches to pandemic management and containment strategies', 'geographical distance between china and india', 'stringent measures taken by india to control the spread of covid', 'differences in population density and demographics between china and india', 'varying levels of economic interdependence between china and india', 'potential impact of global supply chain disruptions on india', 'covid pandemic', 'high transmission rates', 'delta variant', 'public health recommendations', 'mask mandates in some areas', 'concern for personal and community safety', 'public health', 'safety precautions', 'personal responsibility', 'social norms', 'compliance and enforcement', 'increased cases in china', 'proximity to china', 'prior history of disease outbreaks in india', 'need for proactive measures to prevent spread of disease', 'importance of surveillance in containing outbreaks', 'increased surveillance measures', 'concerns over the spread of disease', 'geopolitical implications of bordering countries health situations'], 'factorsParsed': ['geographical distance between china and india', 'stringent travel restrictions and border control measures', 'differences in population density and urbanization levels', 'variations in healthcare infrastructure and capacity', 'divergent approaches to pandemic management and containment strategies', 'varying levels of economic interdependence between china and india', 'covid surge in china is unlikely to impact india', 'people urged to stay cautious and wear masks', 'india has stepped up surveillance after a spike in cases in neighbouring china'], 'edges': [['people urged to stay cautious and wear masks', 'people urged to stay cautious and wear masks', 1.0], ['stringent travel restrictions and border control measures', 'india has stepped up surveillance after a spike in cases in neighbouring china', 0.8], ['differences in population density and urbanization levels', 'people urged to stay cautious and wear masks', 0.8], ['variations in healthcare infrastructure and capacity', 'people urged to stay cautious and wear masks', 0.8], ['divergent approaches to pandemic management and containment strategies', 'people urged to stay cautious and wear masks', 0.8], ['divergent approaches to pandemic management and containment strategies', 'india has stepped up surveillance after a spike in cases in neighbouring china', 0.8], ['covid surge in china is unlikely to impact india', 'india has stepped up surveillance after a spike in cases in neighbouring china', 0.8], ['people urged to stay cautious and wear masks', 'india has stepped up surveillance after a spike in cases in neighbouring china', 0.8], ['india has stepped up surveillance after a spike in cases in neighbouring china', 'india has stepped up surveillance after a spike in cases in neighbouring china', 0.8], ['geographical distance between china and india', 'india has stepped up surveillance after a spike in cases in neighbouring china', 0.6], ['stringent travel restrictions and border control measures', 'people urged to stay cautious and wear masks', 0.6], ['differences in population density and urbanization levels', 'india has stepped up surveillance after a spike in cases in neighbouring china', 0.6], ['variations in healthcare infrastructure and capacity', 'india has stepped up surveillance after a spike in cases in neighbouring china', 0.6], ['varying levels of economic interdependence between china and india', 'people urged to stay cautious and wear masks', 0.6], ['varying levels of economic interdependence between china and india', 'india has stepped up surveillance after a spike in cases in neighbouring china', 0.6], ['covid surge in china is unlikely to impact india', 'covid surge in china is unlikely to impact india', 0.6], ['covid surge in china is unlikely to impact india', 'people urged to stay cautious and wear masks', 0.6], ['people urged to stay cautious and wear masks', 'covid surge in china is unlikely to impact india', 0.6]], 'interpretations': [[('differences in population density and urbanization levels', 'people urged to stay cautious and wear masks'), 'differences in population density and urbanization levels influences people urged to stay cautious and wear masks. Not said in text.', 0.5445261274385864], [('variations in healthcare infrastructure and capacity', 'people urged to stay cautious and wear masks'), 'variations in healthcare infrastructure and capacity influences people urged to stay cautious and wear masks. Not said in text.', 0.7844066955510823], [('variations in healthcare infrastructure and capacity', 'india has stepped up surveillance after a spike in cases in neighbouring china'), 'variations in healthcare infrastructure and capacity influences india has stepped up surveillance after a spike in cases in neighbouring china. Not said in text.', 0.918337703233644], [('divergent approaches to pandemic management and containment strategies', 'india has stepped up surveillance after a spike in cases in neighbouring china'), 'divergent approaches to pandemic management and containment strategies influences india has stepped up surveillance after a spike in cases in neighbouring china. Not said in text.', 0.6247490958799506], [('varying levels of economic interdependence between china and india', 'people urged to stay cautious and wear masks'), 'varying levels of economic interdependence between china and india influences people urged to stay cautious and wear masks. Not said in text.', 0.9064213599923762], [('varying levels of economic interdependence between china and india', 'india has stepped up surveillance after a spike in cases in neighbouring china'), 'varying levels of economic interdependence between china and india influences india has stepped up surveillance after a spike in cases in neighbouring china. Not said in text.', 0.9609762705403709]], 'output': [{'attribute': 'unsaid', 'value': 1, 'explanation': 'differences in population density and urbanization levels influences people urged to stay cautious and wear masks. Not said in text.', 'span': [96, 145], 'confidence': 0.5445261274385864}, {'attribute': 'unsaid', 'value': 1, 'explanation': 'variations in healthcare infrastructure and capacity influences people urged to stay cautious and wear masks. Not said in text.', 'span': [96, 145], 'confidence': 0.7844066955510823}, {'attribute': 'unsaid', 'value': 1, 'explanation': 'variations in healthcare infrastructure and capacity influences india has stepped up surveillance after a spike in cases in neighbouring china. Not said in text.', 'span': [145, 223], 'confidence': 0.918337703233644}, {'attribute': 'unsaid', 'value': 1, 'explanation': 'divergent approaches to pandemic management and containment strategies influences india has stepped up surveillance after a spike in cases in neighbouring china. Not said in text.', 'span': [145, 223], 'confidence': 0.6247490958799506}, {'attribute': 'unsaid', 'value': 1, 'explanation': 'varying levels of economic interdependence between china and india influences people urged to stay cautious and wear masks. Not said in text.', 'span': [96, 145], 'confidence': 0.9064213599923762}, {'attribute': 'unsaid', 'value': 1, 'explanation': 'varying levels of economic interdependence between china and india influences india has stepped up surveillance after a spike in cases in neighbouring china. Not said in text.', 'span': [145, 223], 'confidence': 0.9609762705403709}]},
          {'nodes': ['covid surge in china unlikely to impact india', 'experts urge people to stay cautious and wear masks', 'india steps up surveillance after spike in cases in china'],
           'factors': ['geographical distance between china and india', 'stringent travel restrictions and border control measures', 'effective containment and management strategies implemented by india', 'high vaccination coverage in india', 'differences in population density and urbanization levels between the two countries', 'variations in healthcare infrastructure and capacity', 'potential differences in the prevalence of covid variants between china and india', 'geographical distance between china and india', 'differences in population density and urbanization', 'varied levels of healthcare infrastructure and capacity', 'stringent travel restrictions and border control measures', 'divergent government responses and containment strategies', 'varying levels of public adherence to preventive measures', 'differences in testing tracing and surveillance capabilities', 'varied levels of vaccine coverage and distribution', 'economic and trade implications', 'potential impact on global supply chains and trade routes', 'expert advice', 'cautionary approach', 'importance of wearing masks', 'public health and safety', 'prevention of covid transmission', 'protection of vulnerable populations', 'reduction of community spread', 'compliance with public health guidelines', 'minimization of healthcare system burden', 'promotion of responsible behavior', 'maintenance of economic stability', 'preservation of social interactions', 'mitigation of potential future outbreaks', 'increase in covid cases in china', 'potential risk of imported cases from china', 'need for early detection and containment of cases', 'strengthening of surveillance systems', 'heightened monitoring of international travel and border control measures', 'increased monitoring and surveillance measures', 'heightened border control and screening procedures', 'enhanced contact tracing efforts', 'strengthened healthcare infrastructure and resources', 'potential travel restrictions or advisories', 'implementation of quarantine protocols', 'public health awareness campaigns and education initiatives', 'collaboration with international organizations and neighboring countries', 'potential impact on trade and economy', 'potential strain on healthcare system and resources'],
           'factorsParsed': ['geographical distance between china and india', 'stringent travel restrictions and border control measures', 'effective containment and management strategies implemented by india', 'high vaccination coverage in india', 'differences in population density and urbanization levels between the two countries', 'covid surge in china unlikely to impact india', 'experts urge people to stay cautious and wear masks', 'india steps up surveillance after spike in cases in china'],
           'edges': [['stringent travel restrictions and border control measures', 'experts urge people to stay cautious and wear masks', 1.0], ['stringent travel restrictions and border control measures', 'india steps up surveillance after spike in cases in china', 0.8], ['effective containment and management strategies implemented by india', 'experts urge people to stay cautious and wear masks', 0.8], ['differences in population density and urbanization levels between the two countries', 'experts urge people to stay cautious and wear masks', 0.8], ['experts urge people to stay cautious and wear masks', 'experts urge people to stay cautious and wear masks', 0.8], ['india steps up surveillance after spike in cases in china', 'experts urge people to stay cautious and wear masks', 0.8], ['geographical distance between china and india', 'covid surge in china unlikely to impact india', 0.6], ['geographical distance between china and india', 'experts urge people to stay cautious and wear masks', 0.6], ['geographical distance between china and india', 'india steps up surveillance after spike in cases in china', 0.6], ['effective containment and management strategies implemented by india', 'india steps up surveillance after spike in cases in china', 0.6], ['high vaccination coverage in india', 'experts urge people to stay cautious and wear masks', 0.6], ['differences in population density and urbanization levels between the two countries', 'covid surge in china unlikely to impact india', 0.6], ['differences in population density and urbanization levels between the two countries', 'india steps up surveillance after spike in cases in china', 0.6], ['covid surge in china unlikely to impact india', 'experts urge people to stay cautious and wear masks', 0.6], ['covid surge in china unlikely to impact india', 'india steps up surveillance after spike in cases in china', 0.6], ['experts urge people to stay cautious and wear masks', 'covid surge in china unlikely to impact india', 0.6], ['experts urge people to stay cautious and wear masks', 'india steps up surveillance after spike in cases in china', 0.6], ['india steps up surveillance after spike in cases in china', 'covid surge in china unlikely to impact india', 0.6], ['india steps up surveillance after spike in cases in china', 'india steps up surveillance after spike in cases in china', 0.6]]},
          {}]

print(get_boolean_completion('The sky is red', 'The sky is blue'))
# net, interpretations, cache = prompt_to_output_test(texts[-1], caches[-1])
# print(cache)

# net.display()
print('end')