import * as helper from '../helper.js';
import * as settings from '../pydensha-settings.js';


const createMockXHR = (responseJSON) => {
  const mockXHR = {
    open: jest.fn(),
    send: jest.fn(),
    status: 200,
    setRequestHeader: jest.fn(),
    response: JSON.stringify(responseJSON || {}),
  };
  return mockXHR;
};

describe('pydensha settings test suite', () => {
  const oldDocumentBody = document.body.innerHTML;
  const oldXMLHttpRequest = window.XMLHttpRequest;

  let mockXHR = null;
  const choices = {
    'regions': {'value': 1, 'text': 'rail_region_1'},
    'companies': {'value': 1, 'text': 'rail_company'},
    'lines': {'value': 1, 'text': 'rail_line_1'},
  };
  const simulateInput = function(element) {
    const event = new Event('input', {
      bubbles: true,
      cancelable: true,
      view: window,
    });

    !element.dispatchEvent(event);
  };

  beforeEach(() => {
    document.body.innerHTML =
      '<select id="category"></select>' +
      '<select id="region"></select>' +
      '<select id="company"></select>' +
      '<select id="line"></select>';

    mockXHR = createMockXHR();
    window.XMLHttpRequest = jest.fn(() => mockXHR);
  });

  afterEach(() => {
    document.body.innerHTML = oldDocumentBody;
    window.XMLHttpRequest = oldXMLHttpRequest;
  });

  test('Update related drop-downs if category drop-down val changed', () => {
    mockXHR.response = JSON.stringify({'choices': choices});

    const category = document.getElementById('category');
    const targetURL = 'localhost';
    const spy = jest.spyOn(helper, 'updateDropdown');

    spy.mockImplementation(() => {});
    settings.updateRailwayInfoDropdowns(targetURL, '', '');
    simulateInput(category);
    mockXHR.onload();

    expect(mockXHR.open).toHaveBeenCalledWith(
        'POST', targetURL, true);
    expect(mockXHR.send).toHaveBeenCalledWith('category=');
    expect(helper.updateDropdown).toHaveBeenCalledWith(
        'region', choices['regions']);
    expect(helper.updateDropdown).toHaveBeenCalledWith(
        'company', choices['companies']);
    expect(helper.updateDropdown).toHaveBeenCalledWith(
        'line', choices['lines']);
    spy.mockRestore();
  });

  test('Update related drop-downs if region drop-down val changed', () => {
    mockXHR.response = JSON.stringify({'choices': choices});

    const region = document.getElementById('region');
    const targetURL = 'localhost';
    const spy = jest.spyOn(helper, 'updateDropdown');

    spy.mockImplementation(() => {});
    settings.updateRailwayInfoDropdowns('', targetURL, '');
    simulateInput(region);
    mockXHR.onload();

    expect(mockXHR.open).toHaveBeenCalledWith(
        'POST', targetURL, true);
    expect(mockXHR.send).toHaveBeenCalledWith('category=&region=');
    expect(helper.updateDropdown).toHaveBeenCalledWith(
        'company', choices['companies']);
    expect(helper.updateDropdown).toHaveBeenCalledWith(
        'line', choices['lines']);
    spy.mockRestore();
  });

  test('Update related drop-downs if company drop-down val changed', () => {
    mockXHR.response = JSON.stringify({'choices': choices});

    const company = document.getElementById('company');
    const targetURL = 'localhost';
    const spy = jest.spyOn(helper, 'updateDropdown');

    spy.mockImplementation(() => {});
    settings.updateRailwayInfoDropdowns('', '', targetURL);
    simulateInput(company);
    mockXHR.onload();

    expect(mockXHR.open).toHaveBeenCalledWith(
        'POST', targetURL, true);
    expect(mockXHR.send).toHaveBeenCalledWith('category=&region=&company=');
    expect(helper.updateDropdown).toHaveBeenCalledWith(
        'line', choices['lines']);
    spy.mockRestore();
  });
});
