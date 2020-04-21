import * as helper from '../helper.js';


describe('helper test suite', () => {
  const oldDocumentBody = document.body.innerHTML;

  afterEach(() => {
    document.body.innerHTML = oldDocumentBody;
  });

  test('Dropdown selections are updated to new values', () => {
    document.body.innerHTML =
      '<select id="dropdown">' +
      '<option value="bar">foo</option>' +
      '</select>';

    const choices = [
      {'value': 'val1', 'text': 'text1'},
      {'value': 'val2', 'text': 'text2'},
    ];

    const expected =
      '<select id="dropdown">' +
      '<option value="val1">text1</option>' +
      '<option value="val2">text2</option>' +
      '</select>';

    helper.updateDropdown('dropdown', choices);
    expect(document.body.innerHTML).toBe(expected);
  });

  test('New slider value is outputted upon chnage', () => {
    document.body.innerHTML =
      '<input id="fetch-intvl" type="range" value="35">' +
      '<span id="fetch-intvl-val"></span>';

    const slider = document.getElementById('fetch-intvl');
    const expected1 =
      '<input id="fetch-intvl" type="range" value="35">' +
      '<span id="fetch-intvl-val">35</span>';
    const expected2 =
      '<input id="fetch-intvl" type="range" value="35">' +
      '<span id="fetch-intvl-val">20</span>';

    const simulateInput = function(element) {
      const event = new Event('input', {
        bubbles: true,
        cancelable: true,
        view: window,
      });

      !element.dispatchEvent(event);
    };

    helper.outputSliderVal('fetch-intvl', 'fetch-intvl-val');
    expect(document.body.innerHTML).toBe(expected1);

    slider.value = 20;
    simulateInput(slider);
    expect(document.body.innerHTML).toBe(expected2);
  });
});
