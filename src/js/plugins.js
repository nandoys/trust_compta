axios.defaults.baseURL = 'http://localhost:80/';

// extract value of sessionid from cookies

const cookies = document.cookie.split('; ')

Array.from(cookies).forEach(cookie => {
  if(cookie.startsWith('access_token=')){
    const access_token = cookie.split('=')
    axios.defaults.headers.common['Authorization'] = `Trust ${ access_token[1] }`
  }
})

//


const currencyStore = Pinia.defineStore('currency', {
  state() {
    return {
      currency_asset: 243
    }
  },
  actions: {
    increment() {
      this.currency_asset++
    }
  }
})

Vue.use(Pinia.PiniaVuePlugin)

//Common plugins
if(document.querySelectorAll("[toast-list]") || document.querySelectorAll('[data-choices]') || document.querySelectorAll("[data-provider]")){ 
  document.writeln("<script type='text/javascript' src='/static/libs/toastify-js/src/toastify.js'></script>");
  document.writeln("<script type='text/javascript' src='/static/libs/choices.js/public/assets/scripts/choices.min.js'></script>");
  document.writeln("<script type='text/javascript' src='/static/libs/flatpickr/dist/flatpickr.min.js'></script>");
   document.writeln("<script type='text/javascript' src='/static/libs/flatpickr/dist//l10n/fr.js'></script>");
}