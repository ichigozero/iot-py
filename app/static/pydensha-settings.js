import {updateDropdown} from './helper.js';


function updateRailwayInfoDropdowns(
    csrfToken, infosByCategoryURL, infosByRegionURL, infosByCompanyURL) {
  document.addEventListener('input', function(event) {
    if (event.target.id == 'category') {
      const xhr = new XMLHttpRequest();

      xhr.onload = function() {
        if (this.status >= 200 && this.status < 300) {
          const data = JSON.parse(this.response);
          const choices = data.choices;

          updateDropdown('region', choices['regions']);
          updateDropdown('company', choices['companies']);
          updateDropdown('line', choices['lines']);
        }
      };
      xhr.open('POST', infosByCategoryURL, true);
      xhr.setRequestHeader(
          'Content-Type', 'application/x-www-form-urlencoded; charset=UTF-8');
      xhr.setRequestHeader('X-CSRFToken', csrfToken);
      xhr.send('category=' + event.target.value);
    } else if (event.target.id == 'region') {
      const categoryId = document.getElementById('category').value;
      const xhr = new XMLHttpRequest();

      xhr.onload = function() {
        if (this.status >= 200 && this.status < 300) {
          const data = JSON.parse(this.response);
          const choices = data.choices;

          updateDropdown('company', choices['companies']);
          updateDropdown('line', choices['lines']);
        }
      };
      xhr.open('POST', infosByRegionURL, true);
      xhr.setRequestHeader(
          'Content-Type', 'application/x-www-form-urlencoded; charset=UTF-8');
      xhr.setRequestHeader('X-CSRFToken', csrfToken);
      xhr.send('category=' + categoryId +
               '&region=' + event.target.value);
    } else if (event.target.id == 'company') {
      const categoryId = document.getElementById('category').value;
      const regionId = document.getElementById('region').value;
      const xhr = new XMLHttpRequest();

      xhr.onload = function() {
        if (this.status >= 200 && this.status < 300) {
          const data = JSON.parse(this.response);
          const choices = data.choices;

          updateDropdown('line', choices['lines']);
        }
      };
      xhr.open('POST', infosByCompanyURL, true);
      xhr.setRequestHeader(
          'Content-Type', 'application/x-www-form-urlencoded; charset=UTF-8');
      xhr.setRequestHeader('X-CSRFToken', csrfToken);
      xhr.send('category=' + categoryId +
               '&region=' + regionId +
               '&company=' + event.target.value);
    }
  });
}

export {updateRailwayInfoDropdowns};
