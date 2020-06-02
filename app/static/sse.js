function sse(streamURL) {
  const eventSource = new EventSource(streamURL);

  eventSource.addEventListener('pytenki', function(event) {
    const data = JSON.parse(event.data);

    if (!data) {
      return null;
    }

    updateContent('forecast-loc', data.fcast_loc);

    updateContent('today-weather', data.fcast.today.weather);
    updateContent('today-max-temp', data.fcast.today.temp.max);
    updateContent('today-min-temp', data.fcast.today.temp.min);

    updateContent('tomorrow-weather', data.fcast.tomorrow.weather);
    updateContent('tomorrow-max-temp', data.fcast.tomorrow.temp.max);
    updateContent('tomorrow-min-temp', data.fcast.tomorrow.temp.min);

    for (let i = 0; i < data.fcast_24_hours.length; i++) {
      updateContent('hour-' + (i + 1), data.fcast_24_hours[i]['time']);
      updateContent('weather-' + (i + 1), data.fcast_24_hours[i]['weather']);
      updateContent('temp-' + (i + 1), data.fcast_24_hours[i]['temp']);
    }
  }, false);

  eventSource.addEventListener('pydensha', function(event) {
    const data = JSON.parse(event.data);

    if (!data) {
      return null;
    }

    let i = 0;
    Object.keys(data).forEach(function(key) {
      updateContent('rail-line-' + (i + 1), data[key]['kanji_name']);
      updateContent('rail-status-' + (i + 1), data[key]['line_status']);
      updateContent(
          'rail-status-timestamp-' + (i + 1), data[key]['last_update']);
      i++;
    });
  }, false);
}

function updateContent(elementID, value) {
  document.getElementById(elementID).innerHTML = value;
}

export {sse};
