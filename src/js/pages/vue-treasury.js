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
        income: {
          entries: [],
          debitAccounts: [],
          debitAccountsCopy: [],
          creditAccounts: [],
          creditAccountsCopy: [],
          currencies: [],
          currenciesCopy: [],
          partners: [],
          partnersCopy: [],
          statements: [],
          statementsCopy: [],
          headers: [
          {
            text: "Date de l'opération",
            align: 'start',
            sortable: true,
            value: 'dateTransaction',
          },
          { text: 'Compte', value: 'account' },
          { text: 'Libellé', value: 'label' },
          { text: 'Montant en devise', value: 'amountForeign' },
          { text: 'Debit', value: 'debit' },
          { text: 'Crédit', value: 'credit', sortable: false },
        ],
          countDebitAccount: 1,
          countCreditAccount: 1,
          menu: false,
          loading: false,
          creditLoading: false,
          debitLoading: false,
          statementsLoading: false,
          currencyOperationLoading: false,
          isForeigncurrencyOperation: false,
          partnerLoading: false,
          dialog: false,
          dialogDelete: false,
          dialogEntry: false,
          dialogIntern: false,
          selectedStatement: 0,
          search: '',
          searchCredit: '',
          searchDebit: '',
          searchPartner: '',
          searchCurrency: '',
          filter: {},
          sortDesc: false,
          page: 1,
          itemsPerPage: 15,
          sortBy: 'text',
          keys: ['text', 'ref', 'number'],
          editedIndex: -1,
          editedItem: {
            id: '',
            creditAccount: [],
            debitAccount: [],
            partner: '',
            reference: '',
            label: '',
            currency: '',
            rate: '',
            amountDebit:[],
            amountCredit: [],
            dateOperation: '',
          },
          defaultItem: {
          id: '',
          creditAccount: [],
          debitAccount: [],
          partner: '',
          reference: '',
          label: '',
          currency: '',
          rate: '',
          amountDebit:[],
          amountCredit: [],
          dateOperation: (new Date(Date.now() - (new Date()).getTimezoneOffset() * 60000)).toISOString().substr(0, 10),
        },
        },
        customer: {
          bills: [],
          billsCopy: [],
          selectedBill: [],
          headers: [
          {
            text: "Date de l'opération",
            align: 'start',
            sortable: true,
            value: 'dateOperation',
          },
          { text: 'Compte', value: 'account' },
          { text: 'Partenaire', value: 'partner' },
          { text: 'Libellé', value: 'label' },
          { text: 'Pièce comptable', value: 'reference', sortable: false },
          { text: 'Montant en devises', value: 'amountForeign' },
          { text: 'Montant', value: 'amount' },
        ],
          loading: false
        },
        test: [],
        minDate: '',
        maxDate: '',
        moduleId:'',
        moduleName:'',
        currentCurrency:'',
        currentMonth: '',
        currentYear: '',

        rules: {
          account: [
            v => !!v || 'Veuillez choisir un compte',
          ],
          currency: [
            v => !!v || 'Veuillez choisir une devise',
          ],
          rate: [
            v => !!v || 'Veuillez saisir un taux de change',
          ],
          label: [
            v => !!v || 'Veuillez saisir un libellé',
          ],
          slip: [
            v => !!v || 'Veuillez choisir un type pour la pièce justificative',
          ],
          reference: [
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
        tabLettering: null,

        drawerHeight: '',

        snackbar: false,
        multiLine: false,
        moduleMenu: false,

        snacktext: '',
        snackcolor: '',
        timeout: 2000,
      }
    },

    watch: {
      options: {
        handler () {
          this.getDataIncomes()
        },
        deep: true,
      },

      income: {
        handler (v, old) {
          const entries = v.entries.slice(1)
          Array.from(entries).forEach(entry => {
            const index = this.customer.bills.findIndex(bill => bill.id === entry.id)
            if (index > -1) {
              this.customer.bills[index].amountCalculated = this.customer.bills[index].amount - entry.credit
            }
          })
        },
        deep: true,
      },

      dialogIncomes (val) {
        val || this.close()
      },
      dialogIncomesDelete (val) {
        val || this.closeDelete()
      },

      watchSelectedBill(val, old) {
        let bill_new = Array.from(val)
        let bill_old = Array.from(old)

        if (bill_new.length === 0){

          if (bill_old.length === 1) {

             //reset the bill amount
            const item = this.income.entries[1]
            const index = this.customer.bills.findIndex(found => found.id === item.id)
            this.customer.bills[index].amountCalculated = this.customer.bills[index].amount

            // remove the entry when the bill is no longer selected
            this.income.entries.splice(1, 1)

            //remove header of bill table
            const indexBill = this.customer.headers.findIndex(header => header.value === 'amountCalculated')
            this.customer.headers.splice(indexBill, 1)
          } else if (bill_old.length > 1) {

             bill_old.forEach(bill => {

              const entry_found = this.income.entries.findIndex(entry => entry.id === bill.id)
              if (entry_found > 0) {
                //reset the bill amount
                const item = this.income.entries[entry_found]
                const index = this.customer.bills.findIndex(found => found.id === item.id)
                this.customer.bills[index].amountCalculated = this.customer.bills[index].amount

                // remove the entry when the bill is no longer selected
                this.income.entries.splice(entry_found, 1)
              }

            })

            //remove header of bill table
            const indexBill = this.customer.headers.findIndex(header => header.value === 'amountCalculated')
            this.customer.headers.splice(indexBill, 1)

          }
        }
        else if (bill_new.length < bill_old.length && bill_new.length >= 1){
          bill_old.forEach(bill => {

            const bill_found = bill_new.find(bill_found => bill_found.id === bill.id)
            // if no bill was found it should be delete from entries
            if (!bill_found) {
              const entry_found = this.income.entries.findIndex(entry => entry.id === bill.id)
               //reset the bill amount
              const item = this.income.entries[entry_found]
              const index = this.customer.bills.findIndex(found => found.id === item.id)
              this.customer.bills[index].amountCalculated = this.customer.bills[index].amount

              // remove the entry when the bill is no longer selected
              this.income.entries.splice(entry_found, 1)
            }
          })
        }


      }

    },

    methods: {
      capFirst(name) {
        const capitalizedFirst = name[0].toUpperCase();
        const rest = name.slice(1);

        return capitalizedFirst + rest;
      },

      incrementCountDebitAccountIncome(){
        this.countDebitAccountIncome += 1
        this.income.editedItem.amountDebit.push('')
        this.income.editedItem.debitAccount.push('')
      },
      decrementCountDebitAccountIncome(index){
        this.income.countDebitAccount -= 1
        this.income.editedItem.amountDebit.splice(index-1, 1)
        this.income.editedItem.debitAccount.splice(index-1, 1)
      },
      incrementCountCreditAccountIncome(){
        this.income.countCreditAccount += 1
        this.income.editedItem.amountCredit.push('')
        this.income.editedItem.creditAccount.push('')
      },
      decrementCountCreditAccountIncome(index){
        this.income.countCreditAccount -= 1
        this.income.editedItem.amountCredit.splice(index-1, 1)
        this.income.editedItem.creditAccount.splice(index-1, 1)
      },

      getUrlData(){
        const parse = window.location.pathname.split('/')
        this.moduleName = parse[2]
      },

      getModule(){

        this.apiCall('get', `/api/settings/journal?type=${this.moduleName}`).then(res => {
          const data = res.data
          this.moduleId = data['id']
          this.getStatements()
          this.getDebitAccounts()
        })
      },

      getStatements() {
        this.income.statementsLoading = true
        this.apiCall('get', `/api/treasury/statements/get?journal=${this.moduleId}`).then(res => {
          let data = res.data
          let jsonData = []
          Array.from(data).forEach(item => {

            jsonData.push({
              id: item.id,
              dateTransaction: this.formatDate(item.transaction_at),
              reference: item.reference,
              label: item.label,
              currencyId: item.currency_id,
              currencySymbol: item.currency__symbol,
              currencyName: item.currency__name,
              accountId: item.account_id,
              accountNumber: item.account__account_number,
              accountName: item.account__account_name,
              amount: item.amount !== null ? item.amount : '',
              rate: item.rate
            })
          })
          this.income.statements = jsonData
          this.income.statementsCopy = [...this.income.statements]
          this.income.statementsLoading = false
        }).catch(err => {

        })

      },

      getCreditAccounts(){
        this.income.creditLoading = true
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
            this.income.creditAccounts = jsonData
            this.income.creditCopy = [...this.income.creditAccounts];
            this.income.creditLoading = false
          }

        })
      },

      getDebitAccounts(){
        this.income.debitLoading = true
        this.apiCall('get', `/api/accounting/journal/${this.moduleId}/get`).then(res => {
          let data = res.data
          let jsonData = []
          if(data.length > 0) {
            Array.from(data).forEach(item => {
              jsonData.push({
                id: item.id,
                label: `${item.account_number}  ${item.account_name}`,
              })
            })
            this.income.debitAccounts= jsonData
            this.income.editedItem.debitAccount = jsonData[0].id
            this.income.defaultItem.debitAccount = jsonData[0].id
            this.income.debitAccountsCopy = [...this.income.debitAccounts];
            this.income.debitLoading = false
          }

        })
      },

      getPartners(){
        this.income.partnerLoading = true
        this.apiCall('get', `/api/billing/partners/get`).then(res => {
          let data = res.data
          let jsonData = []
          if(data.length > 0) {
            Array.from(data).forEach(item => {
              jsonData.push({
                id: item.id,
                label: `${item.name}`,
              })
            })
            this.income.partners = jsonData
            this.income.partnersCopy = [...this.income.partners];
            this.income.partnerLoading = false
          }

        })
      },

      savePartner(){
        if (this.income.searchPartner === ''){
          this.snacktext = 'Veuillez saisir un nom avant de créer un partenaire'
          this.snackbar = true
          this.snackcolor = 'red darken-3'
        } else {
          let data = {name: this.income.searchPartner }
          this.apiCall('post', '/api/billing/partner/save', data).then(res => {
            const partner = res.data.partner
            const message = res.data.message
            this.income.partnerloading = false
            this.snacktext = message
            this.snackbar = true
            this.income.partnerLoading = false
            this.snackcolor = 'green darken-3'
            this.income.editedItem.partner = partner
            this.income.searchPartner = ''
            this.income.partners.push(partner)
            this.income.partnersCopy = this.income.partners

          })
        }
      },

      savePartnerAndEdit(){},

      getCurrency(){
        this.income.currencyOperationLoading = true
        this.apiCall('get', `/api/treasury/currencies/get`).then(res => {
          let data = res.data
          let jsonData = []
          if(data.length > 0) {
            Array.from(data).forEach(item => {

              if (item.is_local){
                this.income.editedItem.currency = item.id
                this.income.defaultItem.currency = item.id
              }

              jsonData.push({
                id: item.id,
                label: `${item.name}`,
                symbol: `${item.symbol}`,
                is_local: item.is_local,
                rate: item.rate
              })
            })
            this.income.currencies = jsonData
            this.income.currenciesCopy = [...this.income.currencies];

            this.income.currencyOperationLoading = false
          }

        })
      },

      getBills(){
          this.customer.loading = true

          this.apiCall('get', `/api/billing/customer/bills/get?journal=${this.moduleId}`).then(res => {
            const data = res.data
            let jsonData = []
            Array.from(data).forEach(item => {
              jsonData.push({
                id: item.id,
                dateOperation: this.formatDate(item.bill_at),
                account: `${item.account__account_number} ${item.account__account_name}`,
                partner: item.partner__name,
                label: item.label,
                reference: item.reference,
                amountForeign: item.amount_foreign,
                amountForeignCalculated: item.amount_foreign,
                amount: item.amount,
                amountCalculated: item.amount,
              })
            })
            this.customer.bills = jsonData
            this.customer.billsCopy = [...this.customer.bills]
            this.customer.loading = false
          })
      },

      searchIncomesCreditAccounts(e) {
        if (!this.income.searchCredit) {
          this.income.creditAccounts = this.income.creditCopy;
        }

        this.income.creditAccounts = this.income.creditCopy.filter((item) => {
          return item.label.toLowerCase().indexOf(this.income.searchCredit.toLowerCase()) > -1;
        });
      },

      searchIncomesDebitAccounts(e) {
        if (!this.income.searchDebit) {
          this.income.debitAccounts= this.income.debitAccountsCopy;
        }

        this.income.debitAccounts = this.income.debitAccountsCopy.filter((item) => {
          return item.label.toLowerCase().indexOf(this.income.searchDebit.toLowerCase()) > -1;
        });
      },

      searchIncomesPartners(e) {
        if (!this.income.searchPartner) {
          this.income.partners = this.income.partnersCopy;
        }

        this.income.partners = this.income.partnersCopy.filter((item) => {
          if(this.income.searchPartner != null){
            return item.label.toLowerCase().indexOf(this.income.searchPartner.toLowerCase()) > -1;
          }
        });
      },

      searchIncomesCurrencies(e) {
        if (!this.income.searchCurrency) {
          this.income.currencies = this.income.currenciesCopy;
        }

        this.income.currencies = this.income.currenciesCopy.filter((item) => {
          if(this.income.searchCurrency != null){
            return item.label.toLowerCase().indexOf(this.income.searchCurrency.toLowerCase()) > -1;
          }
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

        /*
        const selectedYear = this.currentYear
        const selectedMonth = `${this.currentMonth}`.length === 1 ? `0${this.currentMonth}` : this.currentMonth

        if(selectedYear === year && selectedMonth === month) {
          this.income.editedItem.dateOperation = now
          this.minDate = `${selectedYear}-${selectedMonth}-01`
          this.maxDate = `${selectedYear}-${selectedMonth}-31`
        } else {
          this.income.editedItem.dateOperation = `${selectedYear}-${selectedMonth}-01`
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
        this.income.editedIndex = this.income.entries.indexOf(item)
        this.income.editedItem = Object.assign({}, item)
        this.income.dialog = true
      },

      deleteItem (item) {
        this.income.editedIndex = this.income.entries.indexOf(item)
        this.income.editedItem = Object.assign({}, item)
        this.income.dialogDelete = true
      },

      deleteItemConfirm () {
        let account_id = this.income.editedItem.id

        this.income.loading = true
        let data = {
          id: account_id
        }

        this.apiCall('post', '/api/accounting/main/delete', data).then(res => {
          this.income.loading = false
          this.snacktext = res.data.message
          this.snackbar = true
          this.snackcolor = 'green darken-3'
          this.income.entries.splice(this.income.editedIndex, 1)
          this.income.dialogDelete = false
        })
      },

      close () {
        this.income.dialog= false
        this.$nextTick(() => {
          this.income.editedItem = Object.assign({}, this.income.defaultItem)
          this.income.editedIndex = -1
        })
      },

      closeDelete () {
        this.income.dialogDelete = false
        this.$nextTick(() => {
          this.income.editedItem = Object.assign({}, this.income.defaultItem)
          this.income.editedIndex = -1
        })
      },

      closeDialogEntry () {
        this.income.dialogEntry = false
        this.$nextTick(() => {
          this.income.editedItem = {
            id: '',
            creditAccount: [],
            debitAccount: [],
            partner: '',
            reference: '',
            label: '',
            amountDebit:[],
            amountCredit: [],
            dateOperation: (new Date(Date.now() - (new Date()).getTimezoneOffset() * 60000)).toISOString().substr(0, 10),
          }
          this.income.editedItem.debitAccount[0] = this.income.defaultItem.debitAccount[0]
          this.income.editedIndex = -1
          this.income.countDebitAccount= 1
          this.income.countCreditAccount = 1
        })
      },

      setData(){
        return {
            id: this.income.editedItem.id,
            currency: this.income.editedItem.currency,
            rate: this.income.editedItem.rate,
            account: this.income.editedItem.debitAccount,
            dateOperation: this.income.editedItem.dateOperation,
            amount: this.income.editedItem.amountDebit,
            partner: this.income.editedItem.partner,
            reference: this.income.editedItem.reference,
            label: this.income.editedItem.label
          }
      },

      saveAndClose () {
        if (this.income.editedItem.editedIndex > -1) {
          this.income.loading = true
          let data = this.setData()

          this.apiCall('post', 'api/treasury/', data).then(res => {
            let message = res.data.message
            this.snacktext = message
            this.snackcolor = 'green darken-3'
            this.snackbar = true
            this.income.editedItem.dialogEntry = false
            this.income.loading = false

            Object.assign(this.income.entries[this.income.editedIndex], this.income.editedItem)

            this.$nextTick(() => {
              this.income.editedItem = Object.assign({}, this.income.defaultItem)
              this.income.editedIndex = -1
            })

          }).catch((err) => {
            let message = err.response.data.message
            this.income.loading = false
            this.snacktext = message
            this.snackbar = true
            this.snackcolor = 'red darken-3'
          })
        } else {
          let data = this.setData()

          if (this.$refs.formIncome.validate()){

            this.income.loading = true

            this.apiCall('post', '/api/treasury/statement/save', data).then(res => {
              let message = res.data.message

              this.snacktext = message
              this.snackcolor = 'green darken-3'

              this.income.dialogEntry = false
              this.snackbar = true
              this.income.loading = false

              this.$nextTick(() => {
                this.income.editedItem = Object.assign({}, this.income.defaultItem)
                this.income.editedIndex = -1
              })

            }).catch((err) => {
              let message = err.response.data.message
              this.income.loading = false
              this.snacktext = message
              this.snackbar = true
              this.snackcolor = 'red darken-3'
            })
          }
        }
      },

      saveAndContinue () {
        if (this.income.editedIndex > -1) {
          this.income.loading = true
          let data = this.setData()

          this.apiCall('post', 'api/treasury/', data).then(res => {
            let message = res.data.message
            this.snacktext = message
            this.snackcolor = 'green darken-3'
            this.snackbar = true
            this.income.dialog = false
            this.income.loading = false

            Object.assign(this.income.entries[this.income.editedIndex], this.income.editedItem)

            this.$nextTick(() => {
              this.income.editedItem = Object.assign({}, this.income.defaultItem)
              this.income.editedIndex = -1
            })

          }).catch((err) => {
            let message = err.response.data.message
            this.income.loading = false
            this.snacktext = message
            this.snackbar = true
            this.snackcolor = 'red darken-3'
            this.income.dialog = false
          })
        } else {
          let data = this.setData()

          if (this.$refs.formIncome.validate()){

            this.income.loading = true

            this.apiCall('post', '/api/treasury/statement/save', data).then(res => {
              let message = res.data.message

              this.snacktext = message
              this.snackcolor = 'green darken-3'

              this.snackbar = true
              this.income.loading = false

              this.$nextTick(() => {
                this.income.editedItem = Object.assign({}, this.income.defaultItem)
                this.income.editedIndex = -1
              })

            }).catch((err) => {
              let message = err.response.data.message
              this.income.loading = false
              this.snacktext = message
              this.snackbar = true
              this.snackcolor = 'red darken-3'
              this.income.dialog = false
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
        return this.income.editedIndex === -1 ? 'Nouveau Compte' : 'Modifier Compte'
      },

      thousandSeparator(){

      },

      getAccountingEntries() {
        const index = this.income.selectedStatement
        const statement = this.income.statements[index]
        if (statement !== undefined) {

          this.apiCall('get', `/api/treasury/incomes/get?statementId=${statement.id}`).then(res => {
            const data = res.data
            let jsonData = []
            Array.from(data).forEach(item => {

              jsonData.push({
                id: item.id,
                dateTransaction: this.formatDate(item.date_at),
                account: `${item.account__account_number} ${item.account__account_name}`,
                label: item.label,
                amountForeign: item.amount_foreign !== null ? item.amount_foreign : '',
                debit: item.debit !== null ? item.debit : '',
                credit: '',
                is_verified: item.is_verified
              })
            })
            this.income.entries = jsonData
            this.customer.selectedBill = []
            this.income.loading = false
            this.getBills()
          })
        }
      },

      getBillAccountingEntry(){
        let entries = []
        Array.from(this.customer.selectedBill).forEach(item => {
          const found = this.income.entries.find(entry => entry.id === item.id)

          if(!found){
            const incomeDebitAmount = this.income.entries[0].debit
            let amountCalculated

            if (incomeDebitAmount > item.amount){
              amountCalculated = item.amount
            } else if(incomeDebitAmount < item.amount) {
              amountCalculated = incomeDebitAmount
            }

            const found = this.customer.headers.find(header => header.value === 'amountCalculated')

            if (!found){
              this.customer.headers.push({
                text: "Reste à payer",
                align: 'start',
                sortable: true,
                value: 'amountCalculated',
              })
            }

            this.income.entries.push({
              id: item.id,
              dateTransaction: item.dateOperation,
              account: `${item.account}`,
              label: item.label,
              debit: '',
              credit: amountCalculated !== null ? amountCalculated : '',
            })
          }

        })
        if (this.income.entries.length > 1){
          Array.from(this.customer.selectedBill).forEach(item => {

          })
        }

      },

      watchSelectedBill(){
        return this.customer.selectedBill
      },

      watchIncomeEntry(){
        return this.income.entries.slice(1)
      },

      partnerPlaceholder () {
        return this.income.partners.length === 0 ? 'Exemple: Remya Tshipamba' : 'Rechercher partenaire'
      },

      partnerLabel (){
        return this.income.partners.length === 0 ? 'Créer un partenaire' : false
      },

      symbolCurrency(){
        let found

        Array.from(this.income.currencies).forEach(currency => {
          if(currency.id === this.income.editedItem.currency) {
            found = currency.symbol.toUpperCase()

            if(!currency.is_local){
              this.income.isForeigncurrencyOperation = true
              this.income.editedItem.rate = currency.rate
            } else {
              this.income.isForeigncurrencyOperation = false
              this.income.editedItem.rate = ''
            }
          }
        })
        return `Montant en ${found}`
      },

      computedDateIncomesFormatted () {
        return this.formatDate(this.income.editedItem.dateOperation)
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
      this.getModule()
      this.setOperationDate()
      this.getCreditAccounts()
      this.getPartners()
    },

    mounted() {

    },

  })