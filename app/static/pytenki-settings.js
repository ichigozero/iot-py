import {updateDropdown} from './helper.js';


function updateForecastAreaDropdowns(
    csrfToken, areasByRegionURL, areasByPrefecture, areasBySubprefecture) {
  document.addEventListener('input', function(event) {
    if (event.target.id == 'region') {
      const xhr = new XMLHttpRequest();

      xhr.onload = function() {
        if (this.status >= 200 && this.status < 300) {
          const data = JSON.parse(this.response);
          const choices = data.choices;

          updateDropdown('prefecture', choices['prefectures']);
          updateDropdown('subprefecture', choices['subprefectures']);
          updateDropdown('city', choices['cities']);
        }
      };
      xhr.open('POST', areasByRegionURL, true);
      xhr.setRequestHeader(
          'Content-Type', 'application/x-www-form-urlencoded; charset=UTF-8');
      xhr.setRequestHeader('X-CSRFToken', csrfToken);
      xhr.send('region=' + event.target.value);
    } else if (event.target.id == 'prefecture') {
      const xhr = new XMLHttpRequest();

      xhr.onload = function() {
        if (this.status >= 200 && this.status < 300) {
          const data = JSON.parse(this.response);
          const choices = data.choices;

          updateDropdown('subprefecture', choices['subprefectures']);
          updateDropdown('city', choices['cities']);
        }
      };
      xhr.open('POST', areasByPrefecture, true);
      xhr.setRequestHeader(
          'Content-Type', 'application/x-www-form-urlencoded; charset=UTF-8');
      xhr.setRequestHeader('X-CSRFToken', csrfToken);
      xhr.send('prefecture=' + event.target.value);
    } else if (event.target.id == 'subprefecture') {
      const xhr = new XMLHttpRequest();

      xhr.onload = function() {
        if (this.status >= 200 && this.status < 300) {
          const data = JSON.parse(this.response);
          const choices = data.choices;

          updateDropdown('city', choices['cities']);
        }
      };
      xhr.open('POST', areasBySubprefecture, true);
      xhr.setRequestHeader(
          'Content-Type', 'application/x-www-form-urlencoded; charset=UTF-8');
      xhr.setRequestHeader('X-CSRFToken', csrfToken);
      xhr.send('subprefecture=' + event.target.value);
    }
  });
}

export {updateForecastAreaDropdowns};
