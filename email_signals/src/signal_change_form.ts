
import autocomplete from './components/auto_complete_input';

class SignalChangeForm {

  CONTENT_TYPE_SELECT_ELEM = document.getElementById(
    'id_content_type'
  ) as HTMLSelectElement
  MODEL_ATTRS_API_URL = (document.getElementById(
    'model_attrs_api_url'
  ) as HTMLInputElement).value
  hasModelAttrsUrl: boolean
  inputOptions: string[] = []

  constructor() {
    this.hasModelAttrsUrl = this.MODEL_ATTRS_API_URL.length > 0;
  }

  setUpEventListeners() {
    if (!this.hasModelAttrsUrl) return

    this.CONTENT_TYPE_SELECT_ELEM.addEventListener('change', () => {
      this.updateInputOptions()
    })
  }

  updateInputOptions = () => {
    return this.callApi()
      .then(data => {
        this.inputOptions = this.getAvailableInputs(data);
        autocomplete(document.querySelector('#id_constraints-0-param_1')!, this.inputOptions);
      })
  }

  /**Currently selected content type. */
  getContentTypeId = () => this.CONTENT_TYPE_SELECT_ELEM.value

  /**Calls the API and returns the response as promise. */
  callApi = () => {
    const url = this.MODEL_ATTRS_API_URL.replace(
      '<content_type_id>',
      this.getContentTypeId()
    )
    return fetch(url)
      .then(response => response.json())
      .then(data => data)
  }

  /**The API returns a multi-level dictionary where each level contains all
   * attributes for a given model and it's value is a dictionary of attributes
   * for that model field.
   * This function flattens the dictionary into a single level dictionary where
   * each level is separated by a '.'.
   * This occurs recursively as long as the dictionary contains more than one
   * level.
   * 
   * @param {Object} all_inputs - The dictionary of all model attributes.
   * @param {string} prefix - The prefix to prepend to the attribute name.
   */
  getAvailableInputs = (all_inputs: any, prefix: string | null = null) => {
    const options: string[] = []
    for (const key in all_inputs) {
      const _prefix = prefix ? `${prefix}.${key}` : key
      options.push(_prefix)
      if (Object.keys(all_inputs[key]).length) {

        options.push(...this.getAvailableInputs(all_inputs[key], _prefix)
        )
      }
    }
    return options
  }
}

new SignalChangeForm().setUpEventListeners()