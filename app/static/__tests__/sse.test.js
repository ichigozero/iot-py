import {sse} from '../sse.js';

describe('Server-Sent Events test suite', () => {
  const oldDocumentBody = document.body.innerHTML;
  const oldEventSource = window.EventSource;
  const mockEvtSrc = {
    addEventListener: jest.fn(),
  };
  const mockEvt = {
    'data': JSON.stringify({
      'fcast': {
        'today': {
          'weather': 'Fine',
          'temp': {
            'max': '10C',
            'min': '1C',
          },
        },
        'tomorrow': {
          'weather': 'Rain',
          'temp': {
            'max': '5C',
            'min': '0C',
          },
        },
      },
      'fcast_24_hours': [
        {'time': '9', 'temp': '10C', 'weather': 'Fine'},
        {'time': '12', 'temp': '10C', 'weather': 'Fine'},
        {'time': '15', 'temp': '10C', 'weather': 'Fine'},
        {'time': '18', 'temp': '10C', 'weather': 'Fine'},
        {'time': '21', 'temp': '10C', 'weather': 'Fine'},
        {'time': '0', 'temp': '10C', 'weather': 'Fine'},
        {'time': '3', 'temp': '10C', 'weather': 'Fine'},
        {'time': '6', 'temp': '10C', 'weather': 'Fine'},
        {'time': '9', 'temp': '10C', 'weather': 'Fine'},
      ],
      'fcast_loc': '(Tokyo/Minato-ku)',
    }),
  };
  beforeEach(() => {
    window.EventSource = jest.fn(() => mockEvtSrc);
  });

  afterEach(() => {
    document.body.innerHTML = oldDocumentBody;
    window.EventSource = oldEventSource;
  });

  test('Process pytenki Server-Sent Events', () => {
    document.body.innerHTML =
      '<span id="forecast-loc"></span>' +
      '<table><tbody>' +
      '<tr>' +
      '<td id="today-weather"></td>' +
      '<td id="tomorrow-weather"></td>' +
      '</tr>' +
      '<tr>' +
      '<td id="today-max-temp"></td>' +
      '<td id="tomorrow-max-temp"></td>' +
      '</tr>' +
      '<tr>' +
      '<td id="today-min-temp"></td>' +
      '<td id="tomorrow-min-temp"></td>' +
      '</tr>' +
      '</tbody></table>' +
      '<table><tbody>' +
      '<tr>' +
      '<td id="hour-1"></td>' +
      '<td id="hour-2"></td>' +
      '<td id="hour-3"></td>' +
      '<td id="hour-4"></td>' +
      '<td id="hour-5"></td>' +
      '<td id="hour-6"></td>' +
      '<td id="hour-7"></td>' +
      '<td id="hour-8"></td>' +
      '<td id="hour-9"></td>' +
      '</tr>' +
      '<tr>' +
      '<td id="weather-1"></td>' +
      '<td id="weather-2"></td>' +
      '<td id="weather-3"></td>' +
      '<td id="weather-4"></td>' +
      '<td id="weather-5"></td>' +
      '<td id="weather-6"></td>' +
      '<td id="weather-7"></td>' +
      '<td id="weather-8"></td>' +
      '<td id="weather-9"></td>' +
      '</tr>' +
      '<tr>' +
      '<td id="temp-1"></td>' +
      '<td id="temp-2"></td>' +
      '<td id="temp-3"></td>' +
      '<td id="temp-4"></td>' +
      '<td id="temp-5"></td>' +
      '<td id="temp-6"></td>' +
      '<td id="temp-7"></td>' +
      '<td id="temp-8"></td>' +
      '<td id="temp-9"></td>' +
      '</tr>' +
      '</tbody></table>';

    const expected =
      '<span id="forecast-loc">(Tokyo/Minato-ku)</span>' +
      '<table><tbody>' +
      '<tr>' +
      '<td id="today-weather">Fine</td>' +
      '<td id="tomorrow-weather">Rain</td>' +
      '</tr>' +
      '<tr>' +
      '<td id="today-max-temp">10C</td>' +
      '<td id="tomorrow-max-temp">5C</td>' +
      '</tr>' +
      '<tr>' +
      '<td id="today-min-temp">1C</td>' +
      '<td id="tomorrow-min-temp">0C</td>' +
      '</tr>' +
      '</tbody></table>' +
      '<table><tbody>' +
      '<tr>' +
      '<td id="hour-1">9</td>' +
      '<td id="hour-2">12</td>' +
      '<td id="hour-3">15</td>' +
      '<td id="hour-4">18</td>' +
      '<td id="hour-5">21</td>' +
      '<td id="hour-6">0</td>' +
      '<td id="hour-7">3</td>' +
      '<td id="hour-8">6</td>' +
      '<td id="hour-9">9</td>' +
      '</tr>' +
      '<tr>' +
      '<td id="weather-1">Fine</td>' +
      '<td id="weather-2">Fine</td>' +
      '<td id="weather-3">Fine</td>' +
      '<td id="weather-4">Fine</td>' +
      '<td id="weather-5">Fine</td>' +
      '<td id="weather-6">Fine</td>' +
      '<td id="weather-7">Fine</td>' +
      '<td id="weather-8">Fine</td>' +
      '<td id="weather-9">Fine</td>' +
      '</tr>' +
      '<tr>' +
      '<td id="temp-1">10C</td>' +
      '<td id="temp-2">10C</td>' +
      '<td id="temp-3">10C</td>' +
      '<td id="temp-4">10C</td>' +
      '<td id="temp-5">10C</td>' +
      '<td id="temp-6">10C</td>' +
      '<td id="temp-7">10C</td>' +
      '<td id="temp-8">10C</td>' +
      '<td id="temp-9">10C</td>' +
      '</tr>' +
      '</tbody></table>';

    mockEvtSrc.addEventListener.mockImplementation((event, handler) => {
      if (event === 'pytenki') {
        handler(mockEvt);
      }
    });

    sse('/stream');
    expect(document.body.innerHTML).toBe(expected);
  });
});