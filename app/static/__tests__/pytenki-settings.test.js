import * as helper from '../helper.js';
import * as settings from '../pytenki-settings.js';


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

describe('pytenki settings test suite', () => {
  const oldDocumentBody = document.body.innerHTML;
  const oldXMLHttpRequest = window.XMLHttpRequest;

  let mockXHR = null;
  const choices = {
    'prefectures': {'value': 1, 'text': 'pref_1'},
    'cities': {'value': 1, 'text': 'city_1'},
    'pinpoint_locs': {'value': 1, 'text': 'pinpoint_loc_1'},
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
      '<select id="region"></select>' +
      '<select id="prefecture"></select>' +
      '<select id="city"></select>' +
      '<select id="pinpoint_loc"></select>';

    mockXHR = createMockXHR();
    window.XMLHttpRequest = jest.fn(() => mockXHR);
  });

  afterEach(() => {
    document.body.innerHTML = oldDocumentBody;
    window.XMLHttpRequest = oldXMLHttpRequest;
  });

  test('Update related drop-downs if region drop-down val changed', () => {
    mockXHR.response = JSON.stringify({'choices': choices});

    const region = document.getElementById('region');
    const targetURL = 'localhost';
    const spy = jest.spyOn(helper, 'updateDropdown');

    spy.mockImplementation(() => {});
    settings.updateForecastAreaDropdowns(targetURL, '', '');
    simulateInput(region);
    mockXHR.onload();

    expect(mockXHR.open).toHaveBeenCalledWith(
        'POST', targetURL, true);
    expect(helper.updateDropdown).toHaveBeenCalledWith(
        'prefecture', choices['prefectures']);
    expect(helper.updateDropdown).toHaveBeenCalledWith(
        'city', choices['cities']);
    expect(helper.updateDropdown).toHaveBeenCalledWith(
        'pinpoint_loc', choices['pinpoints']);
    spy.mockRestore();
  });

  test('Update related drop-downs if prefecture drop-down val changed', () => {
    mockXHR.response = JSON.stringify({'choices': choices});

    const prefecture = document.getElementById('prefecture');
    const targetURL = 'localhost';
    const spy = jest.spyOn(helper, 'updateDropdown');

    spy.mockImplementation(() => {});
    settings.updateForecastAreaDropdowns('', targetURL, '');
    simulateInput(prefecture);
    mockXHR.onload();

    expect(mockXHR.open).toHaveBeenCalledWith(
        'POST', targetURL, true);
    expect(helper.updateDropdown).toHaveBeenCalledWith(
        'city', choices['cities']);
    expect(helper.updateDropdown).toHaveBeenCalledWith(
        'pinpoint_loc', choices['pinpoints']);
    spy.mockRestore();
  });

  test('Update related drop-downs if city drop-down val changed', () => {
    mockXHR.response = JSON.stringify({'choices': choices});

    const city = document.getElementById('city');
    const targetURL = 'localhost';
    const spy = jest.spyOn(helper, 'updateDropdown');

    spy.mockImplementation(() => {});
    settings.updateForecastAreaDropdowns('', '', targetURL);
    simulateInput(city);
    mockXHR.onload();

    expect(mockXHR.open).toHaveBeenCalledWith(
        'POST', targetURL, true);
    expect(helper.updateDropdown).toHaveBeenCalledWith(
        'pinpoint_loc', choices['pinpoints']);
    spy.mockRestore();
  });
});
