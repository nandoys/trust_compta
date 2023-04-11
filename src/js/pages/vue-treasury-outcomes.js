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
      return {
        incomes: [],
        outcomes: [],

        creditAccountsIncomes: [],
        creditAccountsOutcomes: [],

        debitAccountsIncomes: [],
        debitAccountsOutcomes: [],

        currenciesIncomes: [],

        countDebitAccountIncome: 1,
        countCreditAccountIncome: 1,

        creditIncomesCopy: [],
        creditOutcomesCopy: [],

        debitAccountsIncomesCopy: [],
        debitAccountsOutcomesCopy: [],

        typeDocuments:[],
        typeDocumentsCopy: [],

        headers: [
          {
            text: "Date de l'opération",
            align: 'start',
            sortable: true,
            value: 'dateOperation',
          },
          { text: 'Compte', value: 'accountname' },
          { text: 'Libellé', value: 'accountslip' },
          { text: 'Debit', value: 'debit' },
          { text: 'Crédit', value: 'credit', sortable: false },
        ],
        rules: {
          account: [
            v => !!v || 'Veuillez choisir un compte',
          ],
          currency: [
            v => !!v || 'Veuillez choisir une devise',
          ],
          rate: [
            v => !!v || 'Veuillez saisir un taux de changz',
          ],
          label: [
            v => !!v || 'Veuillez saisir un libellé',
          ],
          slip: [
            v => !!v || 'Veuillez choisir un type pour la pièce justificative',
          ],
          slipNumber: [
            v => !!v || 'Veuillez saisir un numéro de bordereau',
          ],
          amount: [
            v => !!v || 'Veuillez saisir un montant',
            v => /^-?[0-9]\d*(\.\d+)?$/.test(v) || 'Veuillez saisir un nombre',
          ],
          date: [
            v => !!v || 'Veuillez choisir une date',
          ]
        },
        tab: null,

        drawerHeight: '',

        menuIncomes: false,
        menuOutcomes: false,

        loadingIncomes: false,
        loadingOutcomes: false,

        creditIncomesLoading: false,
        creditOutcomesLoading: false,

        debitIncomesLoading: false,
        debitOutcomesLoading: false,

        currencyOperationIncomeLoading: false,
        isForeigncurrencyOperationIncome: false,

        typeDocumentLoading: false,

        dialogIncomes: false,
        dialogOutcomes: false,

        dialogIncomesDelete: false,
        dialogOutcomesDelete: false,

        dialogEntry: false,
        dialogInternTrans: false,

        snackbar: false,
        multiLine: false,
        moduleMenu: false,
        selectedModule: 1,

        items: [],
         search: '',
        filter: {},
        sortDesc: false,
        page: 1,
        itemsPerPage: 15,
        sortBy: 'text',
        keys: ['text', 'ref', 'number'],

        snacktext: '',
        snackcolor: '',
        timeout: 2000,
        searchIncomes: '',
        searchOutcomes: '',

        searchIncomesCredit: '',
        searchOutcomesCredit: '',

        searchIncomesDebit: '',
        searchOutcomesDebit: '',

        searchIncomesSlip: '',

        options: {},
        editedIncomeIndex: -1,
        editedOutcomeIndex: -1,

        editedItemIncome: {
          id: '',
          creditAccount: [],
          debitAccount: [],
          slip: '',
          slipNumber: '',
          label: '',
          currency: '',
          rate: '',
          amountDebit:[],
          amountCredit: [],
          dateOperation: '',
        },

        defaultItemIncomes: {
          id: '',
          creditAccount: [],
          debitAccount: [],
          slip: '',
          slipNumber: '',
          label: '',
          currency: '',
          rate: '',
          amountDebit:[],
          amountCredit: [],
          dateOperation: (new Date(Date.now() - (new Date()).getTimezoneOffset() * 60000)).toISOString().substr(0, 10),
        },

        editedItemOutcome: {
          id: '',
          creditAccount: [],
          debitAccount: [],
          slip: '',
          slipNumber: '',
          label: '',
          currency: '',
          rate: '',
          amountDebit:[],
          amountCredit: [],
          dateOperation: '',
        },

        defaultItemOutcomes: {
          id: '',
          creditAccount: [],
          debitAccount: [],
          slip: '',
          slipNumber: '',
          label: '',
          currency: '',
          rate: '',
          amountDebit:[],
          amountCredit: [],
          dateOperation: (new Date(Date.now() - (new Date()).getTimezoneOffset() * 60000)).toISOString().substr(0, 10),
        },
        minDate: '',
        maxDate: '',
        moduleId:'',
        moduleName:'',
        currentCurrency:'',
        currentMonth: '',
        currentYear: ''
      }
    },

    watch: {
      options: {
        handler () {
          this.getDataIncomes()
        },
        deep: true,
      },

      dialogIncomes (val) {
        val || this.close()
      },
      dialogIncomesDelete (val) {
        val || this.closeDelete()
      },

    },

    methods: {
      capFirst(name) {
        const capitalizedFirst = name[0].toUpperCase();
        const rest = name.slice(1);

        return capitalizedFirst + rest;
      },

      incrementCountDebitAccountIncome(){
        this.countDebitAccountIncome += 1
        this.editedItemIncome.amountDebit.push('')
        this.editedItemIncome.debitAccount.push('')
      },
      decrementCountDebitAccountIncome(index){
        this.countDebitAccountIncome -= 1
        this.editedItemIncome.amountDebit.splice(index-1, 1)
        this.editedItemIncome.debitAccount.splice(index-1, 1)
      },
      incrementCountCreditAccountIncome(){
        this.countCreditAccountIncome += 1
        this.editedItemIncome.amountCredit.push('')
        this.editedItemIncome.creditAccount.push('')
      },
      decrementCountCreditAccountIncome(index){
        this.countCreditAccountIncome -= 1
        this.editedItemIncome.amountCredit.splice(index-1, 1)
        this.editedItemIncome.creditAccount.splice(index-1, 1)
      },

      getUrlData(){
        const parse = window.location.pathname.split('/')
        this.moduleName = parse[2]
        this.moduleId= parse[3]
        this.currentCurrency = parse[4]
        this.currentMonth = parse[5]
        this.currentYear = parse[6]
      },

      getDataIncomes () {
        this.loading = true
        const currency = this.currentCurrency
        const month = this.currentMonth
        this.apiCall('get', `/api/treasury/incomes/${currency}/${month}/get?year=${this.currentYear}`).then(res => {
          let data = res.data
          let jsonData = []

          Array.from(data).forEach(item => {
            if (item.debit > 0) {
              jsonData.push({
                  id: item.id,
                  dateOperation: this.formatDate(item.date_at),
                  accountname: `${item.account__account_number} ${this.capFirst(item.account__account_name)}`,
                  accountslip: item.slip_number,
                  debit: `${item.debit} ${this.currentCurrency.toUpperCase()}`
              })
            }
          })

          this.incomes = jsonData

          this.loading = false
        })
      },

      getCreditAccounts(){
        this.creditIncomesLoading = true
        this.apiCall('get', `/api/accounting/plan/accounts-by-categories/get?categories=produit,passif`).then(res => {
          let data = res.data
          let jsonData = []
          if(data.length > 0) {
            Array.from(data).forEach(item => {
              jsonData.push({
                id: item.id,
                label: `${item.account_number}  ${item.account_name}`,
              })
            })
            this.creditAccountsIncomes = jsonData
            this.creditIncomesCopy = [...this.creditAccountsIncomes];
            this.creditIncomesLoading = false
          }

        })
      },

      getDebitAccounts(){
        this.debitIncomesLoading = true
        this.apiCall('get', `/api/accounting/plan/account/${this.moduleId}/get`).then(res => {
          let data = res.data
          let jsonData = []
          if(data.length > 0) {
            Array.from(data).forEach(item => {
              jsonData.push({
                id: item.id,
                label: `${item.account_number}  ${item.account_name}`,
              })
            })
            this.debitAccountsIncomes = jsonData
            this.editedItemIncome.debitAccount[0] = jsonData[0].id
            this.defaultItemIncomes.debitAccount[0] = jsonData[0].id
            this.debitAccountsIncomesCopy = [...this.debitAccountsIncomes];
            this.debitIncomesLoading = false
          }

        })
      },
      getTypeDocuments(){
        this.typeDocumentLoading = true
        this.apiCall('get', `/api/accounting/documents/type/get`).then(res => {
          let data = res.data
          let jsonData = []
          if(data.length > 0) {
            Array.from(data).forEach(item => {
              jsonData.push({
                id: item.id,
                label: `${item.name}`,
              })
            })
            this.typeDocuments = jsonData
            this.typeDocumentsCopy = [...this.typeDocuments];
            this.typeDocumentLoading = false
          }

        })
      },

      getCurrency(){
        this.currencyOperationIncomeLoading = true
        this.apiCall('get', `/api/treasury/currencies/get`).then(res => {
          let data = res.data
          let jsonData = []
          if(data.length > 0) {
            Array.from(data).forEach(item => {

              if (item.is_local){
                this.editedItemIncome.currency = item.id
                this.defaultItemIncomes.currency = item.id
              }

              jsonData.push({
                id: item.id,
                label: `${item.name}`,
                symbol: `${item.symbol}`,
                is_local: item.is_local,
                rate: item.rate
              })
            })
            this.currenciesIncomes = jsonData

            this.currencyOperationIncomeLoading = false
          }

        })
      },

      searchIncomesCreditAccounts(e) {
        if (!this.searchIncomesCredit) {
          this.creditAccountsIncomes = this.creditIncomesCopy;
        }

        this.creditAccountsIncomes = this.creditIncomesCopy.filter((item) => {
          return item.label.toLowerCase().indexOf(this.searchIncomesCredit.toLowerCase()) > -1;
        });
      },

      searchOutcomesCreditAccounts(e) {
        if (!this.searchIncomesCredit) {
          this.creditAccountsIncomes = this.creditIncomesCopy;
        }

        this.creditAccountsIncomes = this.creditIncomesCopy.filter((item) => {
          return item.label.toLowerCase().indexOf(this.searchIncomesCredit.toLowerCase()) > -1;
        });
      },

      searchIncomesDebitAccounts(e) {
        if (!this.searchIncomesDebit) {
          this.debitAccountsIncomes = this.debitAccountsIncomesCopy;
        }

        this.debitAccountsIncomes = this.debitAccountsIncomesCopy.filter((item) => {
          return item.label.toLowerCase().indexOf(this.searchIncomesDebit.toLowerCase()) > -1;
        });
      },

      searchIncomestypeDocuments(e) {
        if (!this.searchIncomesDebit) {
          this.typeDocuments = this.typeDocumentsCopy;
        }

        this.typeDocuments = this.typeDocumentsCopy.filter((item) => {
          return item.label.toLowerCase().indexOf(this.searchIncomesSlip.toLowerCase()) > -1;
        });
      },

      searchOutcomesDebitAccounts(e) {
        if (!this.searchIncomesDebit) {
          this.debitAccountsIncomes = this.debitAccountsIncomesCopy;
        }

        this.debitAccountsIncomes = this.debitAccountsIncomesCopy.filter((item) => {
          return item.label.toLowerCase().indexOf(this.searchIncomesDebit.toLowerCase()) > -1;
        });
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
        this.editedIncomeIndex = this.incomes.indexOf(item)
        this.editedItemIncome = Object.assign({}, item)
        this.dialogIncomes = true
      },

      deleteItem (item) {
        this.editedIncomeIndex = this.incomes.indexOf(item)
        this.editedItemIncome = Object.assign({}, item)
        this.dialogIncomesDelete = true
      },

      deleteItemConfirm () {
        let account_id = this.editedItemIncome.id

        this.loading = true
        let data = {
          id: account_id
        }

        this.apiCall('post', '/api/accounting/main/delete', data).then(res => {
          this.loading = false
          this.snacktext = res.data.message
          this.snackbar = true
          this.snackcolor = 'green darken-3'
          this.incomes.splice(this.editedIncomeIndex, 1)
          this.dialogIncomesDelete = false
        })
      },

      close () {
        this.dialogIncomes = false
        this.$nextTick(() => {
          this.editedItemIncome = Object.assign({}, this.defaultItemIncomes)
          this.editedIncomeIndex = -1
        })
      },

      closeDelete () {
        this.dialogIncomesDelete = false
        this.$nextTick(() => {
          this.editedItemIncome = Object.assign({}, this.defaultItemIncomes)
          this.editedIncomeIndex = -1
        })
      },

      closeDialogEntry () {
        this.dialogEntry = false
        this.$nextTick(() => {
          this.editedItemIncome = {
            id: '',
            creditAccount: [],
            debitAccount: [],
            slip: '',
            slipNumber: '',
            label: '',
            amountDebit:[],
            amountCredit: [],
            dateOperation: (new Date(Date.now() - (new Date()).getTimezoneOffset() * 60000)).toISOString().substr(0, 10),
          }
          this.editedItemIncome.debitAccount[0] = this.defaultItemIncomes.debitAccount[0]
          this.editedIncomeIndex = -1
          this.countDebitAccountIncome = 1
          this.countCreditAccountIncome = 1
        })
      },

      setData(){
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
      },

      saveAndClose () {
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
      },

      saveAndContinue () {
        if (this.editedIncomeIndex > -1) {
          this.loading = true
          let data = this.setData()

          this.apiCall('post', 'api/treasury/', data).then(res => {
            let message = res.data.message
            this.snacktext = message
            this.snackcolor = 'green darken-3'
            this.snackbar = true
            this.dialogIncomes = false
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
            this.dialogIncomes = false
          })
        } else {
          let data = this.setData()

          let debitIncomeSum
          let creditIncomeSum

          Array.from(data.amountDebit).forEach(amount => {
            debitIncomeSum += amount
          })

          Array.from(data.amountCredit).forEach(amount => {
            creditIncomeSum += amount
          })

          if (debitIncomeSum !== creditIncomeSum) {
             let message = "Il n'y a pas d'équilibre entre le compte débité et le(s) compte(s) crédités"

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
              this.dialogIncomes = false
            })
          }
        }
      },

      nextPage () {
        if (this.page + 1 <= this.numberOfPages) this.page += 1
      },
      formerPage () {
        if (this.page - 1 >= 1) this.page -= 1
      },

    },

    computed: {
      formTitle () {
        return this.editedIncomeIndex === -1 ? 'Nouveau Compte' : 'Modifier Compte'
      },

      symbolCurrency(){
        let found

        Array.from(this.currenciesIncomes).forEach(currency => {
          if(currency.id === this.editedItemIncome.currency) {
            found = currency.symbol.toUpperCase()

            if(!currency.is_local){
              this.isForeigncurrencyOperationIncome = true
              this.editedItemIncome.rate = currency.rate
            } else {
              this.isForeigncurrencyOperationIncome = false
              this.editedItemIncome.rate = ''
            }
          }
        })
        return `Montant en ${found}`
      },

      computedDateIncomesFormatted () {
        return this.formatDate(this.editedItemIncome.dateOperation)
      },

      computedDateOutcomesFormatted () {
        return this.formatDate(this.editedItemOutcome.dateOperation)
      },
      drawerHeight(){
        console.log(this.$el.clientHeight)
         return this.$el.clientHeight * 0.80
      },

      numberOfPages () {
        return Math.ceil(this.items.length / this.itemsPerPage)
      },
      filteredKeys () {
        return this.keys.filter(key => key !== 'Name')
      },

      ...Pinia.mapState(currencyStore, ['currency_asset'])
    },

    created () {
      this.getUrlData()
      this.getCurrency()
      this.setOperationDate()
      this.getCreditAccounts()
      this.getDebitAccounts()
      this.getTypeDocuments()
      this.getDataIncomes()
    },

    mounted() {
      for (let i = 0; i < 7000; i++) {
        this.items.push({text: `add ${i}`, ref: `ref ${i}`, number: `# ${i}`})
      }
    },

  })