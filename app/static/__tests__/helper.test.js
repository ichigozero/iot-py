import * as helper from '../helper.js';


describe('helper test suite', () => {
  const oldDocumentBody = document.body.innerHTML;

  beforeEach(() => {
    document.body.innerHTML =
      '<select id="dropdown">' +
      '<option value="bar">foo</option>' +
      '</select>';
  });

  afterEach(() => {
    document.body.innerHTML = oldDocumentBody;
  });

  test('Dropdown selections are updated to new values', () => {
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
});
