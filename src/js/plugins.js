axios.defaults.baseURL = 'http://localhost:80/';

//Vue.component('vue-lottie', VueLottie)


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
