/**
 * Utilise vuejs v.2 via cdn
 * Utilise vuetify v.2 via cdn
 * */

const app = new Vue({
    el: '#app',
    delimiters: ['${', '}'],
    vuetify: new Vuetify(),
    pinia: Pinia.createPinia(),

    data () {
      return {}
    },

    watch: {

    },

    methods: {
      capFirst(name) {
        const capitalizedFirst = name[0].toUpperCase();
        const rest = name.slice(1);

        return capitalizedFirst + rest;
      },

      formatDate (date) {
        if (!date) return null

        const [year, month, day] = date.split('-')
        return `${day}/${month}/${year}`
      },

      parseDate (date) {
        if (!date) return null

        const [month, day, year] = date.split('/')
        return `${day.padStart(2, '0')}-${month.padStart(2, '0')}-${year}`
      },

      setOperationDate(){
        const now  = (new Date(Date.now() - (new Date()).getTimezoneOffset() * 60000)).toISOString().substr(0, 10)
        const [year, month, day] = now.split('-')

        /*
        const selectedYear = this.currentYear
        const selectedMonth = `${this.currentMonth}`.length === 1 ? `0${this.currentMonth}` : this.currentMonth

        if(selectedYear === year && selectedMonth === month) {
          this.editedItemIncome.dateOperation = now
          this.minDate = `${selectedYear}-${selectedMonth}-01`
          this.maxDate = `${selectedYear}-${selectedMonth}-31`
        } else {
          this.editedItemIncome.dateOperation = `${selectedYear}-${selectedMonth}-01`
          this.minDate = `${selectedYear}-${selectedMonth}-01`
          this.maxDate = `${selectedYear}-${selectedMonth}-31`
        }
         */
      },

      apiCall (method, uri, data) {
        if(method === 'get') {
          return axios.get(uri)
        }
        else if(method === 'post') {
          return axios.post(uri, data)
        }

      },

      editItem (item) {
        // this.editedIncomeIndex = this.incomes.indexOf(item)
        // this.editedItemIncome = Object.assign({}, item)
        // this.dialogIncomes = true
      },

      deleteItem (item) {
        // this.editedIncomeIndex = this.incomes.indexOf(item)
        // this.editedItemIncome = Object.assign({}, item)
        // this.dialogIncomesDelete = true
      },

      deleteItemConfirm () {
        // let account_id = this.editedItemIncome.id

        //this.loading = true

        let data = {
          id: account_id
        }
        /*
        this.apiCall('post', '/api/accounting/main/delete', data).then(res => {
          this.loading = false
          this.snacktext = res.data.message
          this.snackbar = true
          this.snackcolor = 'green darken-3'
          this.incomes.splice(this.editedIncomeIndex, 1)
          this.dialogIncomesDelete = false
        })
        */
      },

      close () {
        // this.dialogIncomes = false
        this.$nextTick(() => {
         //  this.editedItemIncome = Object.assign({}, this.defaultItemIncomes)
          // this.editedIncomeIndex = -1
        })
      },

      closeDelete () {
        // this.dialogIncomesDelete = false
        this.$nextTick(() => {
          // this.editedItemIncome = Object.assign({}, this.defaultItemIncomes)
          // this.editedIncomeIndex = -1
        })
      },

      setData(){
        /*
        return {
            id: this.editedItemIncome.id,
            currency: this.editedItemIncome.currency,
            rate: this.editedItemIncome.rate,
            debit: this.editedItemIncome.debitAccount,
            credit: this.editedItemIncome.creditAccount,
            dateOperation: this.editedItemIncome.dateOperation,
            amountDebit: this.editedItemIncome.amountDebit,
            amountCredit: this.editedItemIncome.amountCredit,
            slip: this.editedItemIncome.slip,
            slipNumber: this.editedItemIncome.slipNumber,
            label: this.editedItemIncome.label
          }

         */
      },

      saveAndClose () {
        /*
        if (this.editedIncomeIndex > -1) {
          this.loading = true
          let data = this.setData()

          this.apiCall('post', 'api/treasury/', data).then(res => {
            let message = res.data.message
            this.snacktext = message
            this.snackcolor = 'green darken-3'
            this.snackbar = true
            this.dialogEntry = false
            this.loading = false

            Object.assign(this.incomes[this.editedIncomeIndex], this.editedItemIncome)

            this.$nextTick(() => {
              this.editedItemIncome = Object.assign({}, this.defaultItemIncomes)
              this.editedIncomeIndex = -1
            })

          }).catch((err) => {
            let message = err.response.data.message
            this.loading = false
            this.snacktext = message
            this.snackbar = true
            this.snackcolor = 'red darken-3'
          })
        } else {
          let data = this.setData()

          let debitIncomeSum
          let creditIncomeSum

          Array.from(data.amountDebit).forEach(amount => {
            debitIncomeSum+= amount
          })

          Array.from(data.amountCredit).forEach(amount => {
            creditIncomeSum += amount
          })

          if (debitIncomeSum !== creditIncomeSum) {
             let message = "Il n'y a pas d'équilibre entre le(s) compte(s) débités et le(s) compte(s) crédités"

              this.snacktext = message
              this.snackcolor = 'red darken-3'
              this.snackbar = true
          }

          if (this.$refs.formIncome.validate() && debitIncomeSum === creditIncomeSum){

            this.loading = true

            this.apiCall('post', '/api/treasury/entry/save', data).then(res => {
              let message = res.data.message

              this.snacktext = message
              this.snackcolor = 'green darken-3'

              this.dialogEntry = false
              this.snackbar = true
              this.loading = false

              this.$nextTick(() => {
                this.editedItemIncome = Object.assign({}, this.defaultItemIncomes)
                this.editedIncomeIndex = -1
              })

            }).catch((err) => {
              let message = err.response.data.message
              this.loading = false
              this.snacktext = message
              this.snackbar = true
              this.snackcolor = 'red darken-3'
            })
          }
        }
        */
      },

    },

    computed: {
      formTitle () {
        // return this.editedIncomeIndex === -1 ? 'Nouveau Compte' : 'Modifier Compte'
      },

      computedDateIncomesFormatted () {
        // return this.formatDate(this.editedItemIncome.dateOperation)
      },

      ...Pinia.mapState(currencyStore, ['currency_asset'])
    },

    created () {

    },

    mounted() {

    },

  })