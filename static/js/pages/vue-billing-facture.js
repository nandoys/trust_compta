const app=new Vue({el:"#app",delimiters:["${","}"],vuetify:new Vuetify,pinia:Pinia.createPinia(),data(){return{}},watch:{},methods:{capFirst(e){return e[0].toUpperCase()+e.slice(1)},formatDate(e){var t,a;return e?([e,t,a]=e.split("-"),a+`/${t}/`+e):null},parseDate(e){var t,a;return e?([e,t,a]=e.split("/"),`${t.padStart(2,"0")}-${e.padStart(2,"0")}-`+a):null},setOperationDate(){var[,,,]=new Date(Date.now()-6e4*(new Date).getTimezoneOffset()).toISOString().substr(0,10).split("-")},apiCall(e,t,a){return"get"===e?axios.get(t):"post"===e?axios.post(t,a):void 0},editItem(e){},deleteItem(e){},deleteItemConfirm(){account_id},close(){this.$nextTick(()=>{})},closeDelete(){this.$nextTick(()=>{})},setData(){},saveAndClose(){}},computed:{formTitle(){},computedDateIncomesFormatted(){},...Pinia.mapState(currencyStore,["currency_asset"])},created(){},mounted(){}});