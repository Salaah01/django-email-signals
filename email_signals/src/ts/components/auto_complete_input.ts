
/**Generate an ID to use for a dropdown list.
 * 
 * @param {HTMLInputElement} input - The input element to generate an ID for.
 * @returns {string} The ID to use for the dropdown list.
 */
const dropdownListID = (input: HTMLInputElement) => {
  let id = input.id;
  if (!id) {
    id = input.name;
  }
  return id + 'autocomplete-list';
}

const autocomplete = (input: HTMLInputElement, options: string[]) => {

  let currentFocus: number = -1;
  const inputID = dropdownListID(input);


  input.addEventListener("input", (event) => {
    const value = (event.target as HTMLInputElement).value;

    closeAllLists();

    if (!value) {
      return;
    }

    // Create a DIV element that will contain the items (values)
    const listDiv = document.createElement("DIV");
    listDiv.setAttribute("id", inputID);
    listDiv.setAttribute("class", "autocomplete-items");
    // Append the DIV element as a child of the autocomplete container
    input.parentNode!.appendChild(listDiv);
    for (const option of options) {
      // Check if the item starts with the same letters as the text field
      // value.
      if (option.substr(0, value.length).toUpperCase() === value.toUpperCase()) {
        // Create a DIV element for each matching element
        const itemDiv = document.createElement("DIV");

        // Make the matching letters bold
        itemDiv.innerHTML = "<strong>" + option.substr(0, value.length) + "</strong>";
        itemDiv.innerHTML += option.substr(value.length);

        // Insert a input field that will hold the current array item's value.
        itemDiv.innerHTML += `<input type="hidden" value="${option}">`;

        // Execute a function when someone clicks on the item value
        itemDiv.addEventListener("click", (e) => {
          // Insert the value for the autocomplete text field
          input.value = (e.target as HTMLDivElement).querySelector("input")!.value;

          // Close the list of autocompleted values,
          // (or any other open lists of autocompleted values)
          closeAllLists();
        });
        ;
        // Append the itemDiv to the listDiv
        listDiv.appendChild(itemDiv);
      }
    }
  });

  // Execute a function presses a key on the keyboard.
  input.addEventListener("keydown", (event) => {
    let listOptions = document.getElementById(
      inputID
    ) as HTMLElement | HTMLCollectionOf<HTMLElement>
    if (listOptions) {
      listOptions = (listOptions as HTMLElement).getElementsByTagName("div") as HTMLCollectionOf<HTMLElement>
    }

    if (event.key == 'ArrowDown') {
      currentFocus++;
      addActive(listOptions);

    } else if (event.key == 'ArrowUp') {
      currentFocus--;
      addActive(listOptions);

    } else if (event.key == 'Enter') {
      event.preventDefault();
      console.log(currentFocus);
      console.log(listOptions);
      if (currentFocus > -1) {
        if (listOptions[currentFocus]) {
          listOptions[currentFocus].click();
        }
      }
    }
  });

  const addActive = (listOptions: HTMLCollectionOf<HTMLElement>) => {

    removeActive(listOptions);

    if (currentFocus >= listOptions.length) {
      currentFocus = 0;
    }

    if (currentFocus < 0) {
      currentFocus = (listOptions.length - 1);
    }

    listOptions[currentFocus].classList.add("autocomplete-active");

  }


  const removeActive = (listOptions: HTMLCollectionOf<HTMLElement>) => {
    for (let i = 0; i < listOptions.length; i++) {
      listOptions[i].classList.remove("autocomplete-active");
    }
  }

  const closeAllLists = () => {
    const lists = document.getElementsByClassName("autocomplete-items");
    for (let i = 0; i < lists.length; i++) {
      lists[i].parentNode!.removeChild(lists[i]);
    }
  }

  document.addEventListener("click", closeAllLists);
}

export default autocomplete;
