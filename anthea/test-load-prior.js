// Copyright 2024 The Google Research Authors.
//
// Licensed under the Apache License, Version 2.0 (the "License");
// you may not use this file except in compliance with the License.
// You may obtain a copy of the License at
//
//     http://www.apache.org/licenses/LICENSE-2.0
//
// Unless required by applicable law or agreed to in writing, software
// distributed under the License is distributed on an "AS IS" BASIS,
// WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
// See the License for the specific language governing permissions and
// limitations under the License.

/**
 * To run this test, visit the URL:
 *     http://.../anthea.html?test=test-load-prior.js
 * and then click around through the rating process.
 */
const testProjectTSVData = `
This is the first​-​sentence​. 	This is its translation​.	doc-42	system-GL
This is the second sentence. It includes this long string that tests text-wrapping: http://01234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789​.	This is the translation (​of the second sentence​)​.	doc-42	system-GL
The third sentence​. 	A translation of the 3rd sentence​. 	doc-42	system-GL
# A sentence beginning with # 4​.	Translated sentence 4​.	doc-42	system-GL

A second paragraph​. This is a long sentence with meaninglessness embedded as an essential artifact that requires the reader to comtemplate their exact place in the vast expanse of existence​.	Translater had no clue on this one​.	doc-42	system-GL
The first sentence in the second document​.	The translation of the first sentence in the second document​.	doc-99	system-DL
The 2nd sentence in the second document​.	The translation of the doosra sentence in the second document​.	doc-99	system-DL
The third and final document​.	The translation​, of the opening sentence in the third document​.	doc-1531	system-DL
The last line​. The last word​. Waiting for whom​?	Given the existence as uttered forth in the public works of Puncher and Wattmann of a personal God quaquaquaqua with white beard quaquaquaqua outside time without extension who from the heights of divine apathia divine athambia divine aphasia loves us dearly with some exceptions for reasons unknown but time will tell and suffers like the divine Miranda with those who for reasons unknown .​.​.	doc-1531	system-DL
      `;
const testProjectName = 'Google-MQM-Test-Load-Prior-42';
const testTemplateName = 'MQM';
const activeName = antheaManager.activeName(testProjectName, testTemplateName);
try {
  const activeDataKey = antheaManager.ACTIVE_KEY_PREFIX_ + activeName;
  window.localStorage.removeItem(activeDataKey);
  const activeResultsKey =
      antheaManager.ACTIVE_RESULTS_KEY_PREFIX_ + activeName;
  window.localStorage.removeItem(activeResultsKey);
} catch (err) {
  console.log('Caught exception (harmless if for "no such item": ' + err);
}
const parameters = {
  "prior_results": [
    {
        "errors": [
            {
                "location": "source",
                "prefix": "This is the ",
                "selected": "first-sentence",
                "type": "source_error",
                "subtype": "",
                "display": "Source issue",
                "start": 6,
                "end": 8,
                "severity": "minor",
                "override_all_errors": false,
                "needs_note": false,
                "metadata": {
                    "sentence_index": 0,
                    "side": 0,
                    "timestamp": 1691699358223,
                    "timing": {},
                }
            }
        ],
        "doc": 0,
        "visited": true,
        "timestamp": 1691699363918,
        "feedback": {}
    },
    {
        "errors": [],
        "doc": 0,
        "visited": true,
        "timestamp": 1691699368942,
    },
    {
        "errors": [
            {
                "location": "translation",
                "prefix": "A translation of the ",
                "selected": "3rd sentence",
                "type": "accuracy",
                "subtype": "reinterpretation",
                "display": "Accuracy",
                "start": 8,
                "end": 10,
                "severity": "major",
                "override_all_errors": false,
                "needs_note": false,
                "metadata": {
                    "sentence_index": 0,
                    "side": 1,
                    "timestamp": 1691699380360,
                    "timing": {},
                }
            }
        ],
        "doc": 0,
        "visited": true,
        "timestamp": 1691699382695,
    },
    {
        "errors": [],
        "doc": 0,
        "visited": true,
        "timestamp": 1691699385184,
    },
    {
        "errors": [
            {
                "location": "translation",
                "prefix": "",
                "selected": "Translater had",
                "type": "fluency",
                "subtype": "inconsistency",
                "display": "Fluency",
                "start": 0,
                "end": 2,
                "severity": "minor",
                "override_all_errors": false,
                "needs_note": false,
                "metadata": {
                    "sentence_index": 0,
                    "side": 1,
                    "timestamp": 1691699397911,
                    "timing": {},
                }
            },
            {
                "location": "translation",
                "prefix": "Translater ",
                "selected": "had no clue on",
                "type": "style",
                "subtype": "awkward",
                "display": "Style",
                "start": 2,
                "end": 8,
                "severity": "major",
                "override_all_errors": false,
                "needs_note": false,
                "metadata": {
                    "sentence_index": 0,
                    "side": 1,
                    "timestamp": 1691699407997,
                    "timing": {},
                }
            }
        ],
        "doc": 0,
        "visited": true,
        "timestamp": 1691699407997,
        "timing": {},
    },
    {
        "errors": [],
        "doc": 1,
        "visited": false,
        "timestamp": 1691699316043,
        "timing": {},
        "hotw_list": [],
        "feedback": {}
    },
    {
        "errors": [],
        "doc": 1,
        "visited": false,
        "timestamp": 1691699316043,
        "timing": {},
    },
    {
        "errors": [],
        "doc": 2,
        "visited": false,
        "timestamp": 1691699316043,
        "timing": {},
        "hotw_list": [],
        "feedback": {}
    },
    {
        "errors": [],
        "doc": 2,
        "visited": false,
        "timestamp": 1691699316043,
        "timing": {},
    }
],
  "source_language": "en",
  "target_language": "en",
};
antheaManager.createActive(
    testTemplateName, testProjectName,
    JSON.stringify(parameters) + '\n' + testProjectTSVData,
    100  /** test that segments with prior annos do not get any hotw */);
