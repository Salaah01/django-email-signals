
import autocomplete from './components/auto_complete_input';


/**Contains a collections of param inputs. */
class ParamInputs {
  inputsRegistry: { [key: string]: HTMLInputElement } = {};
  deleteBtnsRegistry: Set<HTMLElement> = new Set();

  constructor() {
    this.setNewRowEventListener();
    this.rebuildAll()
  }

  /** Number of input rows. */
  inputRows = () => +(document.querySelector(
    '#id_constraints-TOTAL_FORMS'
  ) as HTMLInputElement).value;


  /** Adds a new param input item. */
  addInput = (input: HTMLInputElement) => {
    this.inputsRegistry[input.name] = input;
  }

  /** Removes a param input item. */
  deleteInput = (input: HTMLInputElement) => {
    delete this.inputsRegistry[input.name];
  }

  /** Returns the param input item with the given name. */
  getInput = (name: string) => {
    return this.inputsRegistry[name];
  }

  /** Returns a list of all input elements. */
  inputList = () => {
    return Object.values(this.inputsRegistry);
  }

  /** Resets the registry. */
  flushRegistry = () => {
    this.inputsRegistry = {};
    this.deleteBtnsRegistry = new Set();
  }


  /**Adds delete buttons to the registry and sets and event listener to
   * to handle the deletion of the param input rows.
   */
  private registerDeleteBtns = () => {
    const deleteBtns = document.querySelectorAll(
      '.inline-deletelink'
    ) as any as HTMLCollectionOf<HTMLElement>;

    for (let i = 0; i < deleteBtns.length; i++) {
      const btn = deleteBtns[i];
      if (!this.deleteBtnsRegistry.has(btn)) {
        this.deleteBtnsRegistry.add(btn);
        btn.addEventListener('click', this.rebuildAll);
      }
    }
  }


  /**Updates the inputs by flushing and rebuilding the inputs collection. */
  private addInputsToRegistry = () => {
    for (let i = 0; i < this.inputRows(); i++) {
      const param_1 = document.querySelector(
        `#id_constraints-${i}-param_1`
      ) as HTMLInputElement | null
      const param_2 = document.querySelector(
        `#id_constraints-${i}-param_2`
      ) as HTMLInputElement | null

      if (param_1) {
        this.addInput(param_1);
      }
      if (param_2) {
        this.addInput(param_2);
      }
    }
  }

  /**Sets the event listeners on the delete buttons. */
  private setDeleteBtnEventListeners = () => {
    this.deleteBtnsRegistry.forEach(btn => {
      btn.removeEventListener('click', this.rebuildAll);
      btn.addEventListener('click', this.rebuildAll);
    });
  }

  /**Sets the event listener on the new row button. */
  private setNewRowEventListener = () => {
    // Bit of a hack, but need to wait for the inline models to be rendered.
    document.querySelector(
      '.add-row a'
    )!.addEventListener('click', this.rebuildAll);
  }

  /**Flushes the registry and rebuilds all the event listeners. */
  rebuildAll = () => {
    this.flushRegistry();
    this.addInputsToRegistry();
    this.registerDeleteBtns();
    this.setDeleteBtnEventListeners();
  }
}


class ContentTypeSetup {

  CONTENT_TYPE_SELECT_ELEM = document.getElementById(
    'id_content_type'
  ) as HTMLSelectElement
  MODEL_ATTRS_API_URL = (document.getElementById(
    'model_attrs_api_url'
  ) as HTMLInputElement).value
  hasModelAttrsUrl: boolean
  inputElems: () => HTMLInputElement[]
  inputOptions: string[] = []

  constructor(inputElems: () => HTMLInputElement[]) {
    this.hasModelAttrsUrl = this.MODEL_ATTRS_API_URL.length > 0;
    this.inputElems = inputElems;
    this.setInputOptions();
  }

  setUpEventListener() {
    if (!this.hasModelAttrsUrl) return

    this.CONTENT_TYPE_SELECT_ELEM.addEventListener(
      'change',
      this.setInputOptions
    )

    document.querySelector(
      '.add-row a'
    )!.addEventListener('click', this.setInputOptions);
  }

  setInputOptions = () => {
    return this.callApi()
      .then(data => {
        this.inputOptions = this.getAvailableInputs(data);
        this.inputElems().forEach(input => {
          autocomplete(input, this.inputOptions);
        });
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

setTimeout(() => {
  const paramInputs = new ParamInputs();
  new ContentTypeSetup(paramInputs.inputList).setUpEventListener()
}, 500);