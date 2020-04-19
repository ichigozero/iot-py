function updateDropdown(elementId, choices) {
  const element = document.getElementById(elementId);

  while (element.firstChild) {
    element.removeChild(element.firstChild);
  }

  choices.forEach(function(item) {
    const option = document.createElement('option');

    option.setAttribute('value', item.value);
    option.textContent = item.text;

    element.appendChild(option);
  });
}

export {updateDropdown};
