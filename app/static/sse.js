function sse(streamURL) {
  const eventSource = new EventSource(streamURL);

  eventSource.addEventListener('pytenki', function(event) {
    const data = JSON.parse(event.data);

    if (!data) {
      return null;
    }

    updateContent('forecast-loc', data.fcast_loc);

    updateContent('today-weather', data.fcast.today.weather);
    updateContent('today-max-temp', data.fcast.today.temps.high);
    updateContent('today-min-temp', data.fcast.today.temps.low);

    updateContent('tomorrow-weather', data.fcast.tomorrow.weather);
    updateContent('tomorrow-max-temp', data.fcast.tomorrow.temps.high);
    updateContent('tomorrow-min-temp', data.fcast.tomorrow.temps.low);

    for (let i = 0; i < data.fcast_24_hours.length; i++) {
      updateContent('hour-' + (i + 1), data.fcast_24_hours[i]['hour']);
      updateContent('weather-' + (i + 1), data.fcast_24_hours[i]['weather']);
      updateContent('temp-' + (i + 1), data.fcast_24_hours[i]['temp']);
    }
  }, false);

  eventSource.addEventListener('pydensha', function(event) {
    const data = JSON.parse(event.data);

    if (!data) {
      return null;
    }

    updateContent('rail-category', data.rail_category);

    const table = document.getElementById('rail-info');
    const dataKeys = Object.keys(data.rail_info);
    const lengthDiff = table.rows.length - dataKeys.length - 1;

    if (lengthDiff > 0) {
      for (let i = 0; i < lengthDiff; i++) {
        table.deleteRow(dataKeys.length + 1);
      }
    } else if (lengthDiff < 0) {
      for (let i = 0; i < Math.abs(lengthDiff); i++) {
        const index = table.rows.length;
        const row = table.insertRow(index);
        const cell1 = row.insertCell(0);
        const cell2 = row.insertCell(1);
        const cell3 = row.insertCell(2);

        cell1.id = 'rail-line-' + index;
        cell2.id = 'rail-status-' + index;
        cell3.id = 'rail-status-timestamp-' + index;
      }
    }

    let i = 1;
    dataKeys.forEach(function(key) {
      updateContent('rail-line-' + i, data['rail_info'][key]['kanji_name']);
      updateContent('rail-status-' + i, data['rail_info'][key]['line_status']);
      updateContent(
          'rail-status-timestamp-' + i, data['rail_info'][key]['last_update']);
      i++;
    });
  }, false);
}

function updateContent(elementID, value) {
  document.getElementById(elementID).innerHTML = value;
}

export {sse};
