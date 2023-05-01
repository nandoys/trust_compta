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
        bill: {
          entries: [],
          debitAccounts: [],
          debitAccountsCopy: [],
          creditAccounts: [],
          creditAccountsCopy: [],
          debitAccountBalance: null,
          creditsAccountBalance: null,
          currencies: [],
          currenciesCopy: [],
          partners: [],
          partnersCopy: [],
          bills: [],
          billsCopy: [],
          selectedBill: 0,
          headers: [
          {
            text: "Date de l'opération",
            align: 'start',
            sortable: true,
            value: 'dateOperation',
          },
          { text: 'Compte', value: 'account' },
          { text: 'Libellé', value: 'label' },
          { text: 'Montant en devise', value: 'amount_foreign' },
          { text: 'Debit', value: 'debit' },
          { text: 'Crédit', value: 'credit', sortable: false },
        ],
          countDebitAccount: 1,
          countCreditAccount: 1,
          menuBill: false,
          menuDeadline: false,
          loading: false,
          creditLoading: false,
          debitLoading: false,
          billsLoading: false,
          currencyOperationLoading: false,
          isForeigncurrencyOperation: false,
          partnerLoading: false,
          dialog: false,
          dialogDelete: false,
          dialogEntry: false,
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
            dateBill: (new Date(Date.now() - (new Date()).getTimezoneOffset() * 60000)).toISOString().substr(0, 10),
            dateDeadline: (new Date(Date.now() - (new Date()).getTimezoneOffset() * 60000)).toISOString().substr(0, 10)
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
          dateBill: (new Date(Date.now() - (new Date()).getTimezoneOffset() * 60000)).toISOString().substr(0, 10),
          dateDeadline: (new Date(Date.now() - (new Date()).getTimezoneOffset() * 60000)).toISOString().substr(0, 10)
          }
        },
        lines: {
          items: [],
          itemsCopy: [],
          headers: [
          { text: "Libellé", align: 'start', sortable: true, value: 'label'},
          { text: 'Compte', value: 'account' },
          { text: 'Quantité', value: 'quantity' },
          { text: 'Prix HT', value: 'price' },
          { text: 'Taxes', value: 'taxes', sortable: false },
          { text: 'Prix TTC', value: 'priceWithTax' },
          { text: '', value: 'actions', sortable: false }
        ],
          loading: false,
        },
        taxes: [],
        total_amount: null, // i put this outside of lines var to avoid crash, infinite loop will be triggered in watch observer
        total_taxes: null, // i put this outside of lines var to avoid crash, infinite loop will be triggered in watch observer
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
            v => !!v || 'Veuillez saisir une référence',
          ],
          amount: [
            v => !!v || 'Veuillez saisir un montant',
            v => /^-?[0-9]\d*(\.\d+)?$/.test(v) || 'Veuillez saisir un nombre',
          ],
          price: [
            v => !!v || 'Veuillez saisir un prix',
            v => /^-?[0-9]\d*(\.\d+)?$/.test(v) || 'Veuillez saisir un nombre',
          ],
          quantity: [
            v => !!v || 'Veuillez saisir une quantité',
            v => v > 0 || 'Veuillez saisir une quantité supérieure à 0',
            v => /^-?[0-9]\d*(\.\d+)?$/.test(v) || 'Veuillez saisir un nombre',
          ],
          date: [
            v => !!v || 'Veuillez choisir une date',
          ]
        },
        tab: null,
        tabBillLines: null,
        tablStateBill: null,

        windowSize: {
          x: 0,
          y: 0,
        },

        snackbar: false,
        multiLine: false,
        moduleMenu: false,

        snacktext: '',
        snackcolor: '',
        timeout: 2000,

        disableValidate: true,
      }
    },

    watch: {

      // here i calculate amount with taxes, but watching changing data on lines data
      lines: {
        handler(v, old){
          const items = v.items

          // this code is to calculate the total sum of the bill at the bottom
          this.total_amount = null // amount without taxes
          const selected_bill_index = this.bill.selectedBill
          const selected_bill = this.bill.bills[selected_bill_index]

          if (selected_bill !== undefined) {
            selected_bill.amount = 0 // reset bill amount

            this.total_taxes = null // reset the tax value

            // resset tax entry
            this.resetTaxEntry()

            let count_tax = null

            items.forEach(item => {

            // bind label line to label entry
            const entry = this.bill.entries.find(entry => entry.line_ref === item.ref)

            if(entry !== undefined) {
              entry.label = item.label
            }

            // here we delete the tax amount if it's no longer selected
            // we do it before any calculation
            this.deleteTaxAmount(item)

            // here we calculate the taxes, prices for each lines
            if (!Number.isNaN(parseInt(item.quantity)) && !Number.isNaN(parseFloat(item.price))) {
              const total = parseInt(item.quantity) * parseFloat(item.price)

              let tax_amount = null

              //add tax to accounting entry, if not existing yet
              // for existing tax entry see outside of this items for loop, bill entries loop
               // increment count_selected
              Array.from(item.taxes).forEach(selected_tax => {

                const found_tax = this.taxes.find(taxe => taxe.id === selected_tax)

                found_tax.count_selected += 1

                const found_index = item.taxes.indexOf(selected_tax)

                // calculate the tax amount
                //add tax to accounting entry if not existing yet
                if (found_tax){
                  // calculate the tax amount
                  switch (found_tax.is_fixed) {
                    case true:
                      switch (found_tax.currency.is_local) {
                        case true:
                          switch (selected_bill.currency_is_local) {
                            case true:
                              tax_amount += found_tax.amount
                              break
                            case false:
                              tax_amount += found_tax.amount / selected_bill.rate
                          }
                          break
                        case false:
                          switch (selected_bill.currency_is_local) {
                            case true:
                              tax_amount += found_tax.amount * selected_bill.rate
                              break
                            case false:
                              tax_amount += found_tax.amount
                          }
                          break
                      }

                      item.taxes_amount[found_index] = {calculated: found_tax.amount, tax_ref: selected_tax}
                      break
                    case false:
                      if (item.price > 0) {
                        tax_amount += total * (found_tax.amount / 100)
                      }

                      // this bind to watch any changes when the user select a tax
                      item.taxes_amount[found_index] = {calculated: total * (found_tax.amount / 100), tax_ref: selected_tax}

                      break
                  }

                  //add tax to accounting entry if not existing yet
                  const  found_entry = this.bill.entries.find(entry => entry.account_id === found_tax.account_id &&
                      entry.label === found_tax.name)

                  if (!found_entry) {
                    let credit = null
                    let amount_foreign = null

                    item.taxes_amount.forEach(tax_amount=>{
                      if (tax_amount.tax_ref === found_tax.id) {
                        if (selected_bill.currency_is_local) {
                           credit += tax_amount.calculated
                        } else {
                          credit += tax_amount.calculated * selected_bill.rate
                          amount_foreign += tax_amount.calculated
                        }
                      }
                    })

                    this.bill.entries.push({
                        line_ref: found_tax.id,
                        dateOperation: selected_bill.bill_at,
                        account:`${found_tax.account_number} ${found_tax.account_name}`,
                        account_id: found_tax.account_id,
                        label: found_tax.name,
                        amount_foreign:  amount_foreign,
                        debit: null,
                        credit: credit,
                        is_customer_account: false,
                        is_tax_account: true,
                    })
                  }
                }
              })

              this.total_amount += total

              item.priceWithTax = total + tax_amount
              this.total_taxes += tax_amount

              selected_bill.amount += item.priceWithTax
            }

            // here we bind changing to see it in the accounting entries except taxes entry,
            // for tax  entry the if condition statement above
            if (!Number.isNaN(parseFloat(item.price))) {
              const index_entry = this.bill.entries.findIndex(entry => entry.line_ref === item.ref)

              const index_customer_account = this.bill.entries.findIndex(entry => entry.is_customer_account === true)

              const customer_entry = this.bill.entries[index_customer_account]

              const line_entry = this.bill.entries[index_entry]

              const total = parseInt(item.quantity) * parseFloat(item.price)

              if(selected_bill.currency_is_local) {

                customer_entry.amount_foreign = null
                customer_entry.amount = selected_bill.amount
                customer_entry.debit = selected_bill.amount

                line_entry.amount_foreign = null
                line_entry.amount =  isNaN(total) ? null : total
                line_entry.credit = isNaN(total) ? null : total
              } else {
                const rate =  selected_bill.rate

                const amount_customer = selected_bill.amount * rate
                customer_entry.amount_foreign = selected_bill.amount
                customer_entry.amount = amount_customer
                customer_entry.debit = amount_customer

                const amount = total * rate
                line_entry.amount_foreign = isNaN(total) ? null : total
                line_entry.amount = isNaN(amount) ? null : amount
                line_entry.credit = parseFloat(amount)
              }

            }

          })

            // here  we reset value of evevry tax in entry
            this.bill.entries.forEach(entry => {

              const tax_entry = this.taxes.find(tax => tax.account_id === entry.account_id && tax.name === entry.label)

              if(tax_entry){
                entry.credit = null
                items.forEach(item => {
                   item.taxes_amount.forEach(amount => {
                      if(amount.tax_ref === tax_entry.id) {
                        switch (selected_bill.currency_is_local) {
                          case true:
                            switch (tax_entry.currency.is_local) {
                              case true:
                                entry.credit += amount.calculated
                                break
                              case false:
                                entry.amount_foreign += amount.calculated
                                entry.credit += (amount.calculated * selected_bill.rate)
                                break
                              case null:
                                entry.amount_foreign = null
                                entry.credit += amount.calculated
                                break
                            }
                            break
                          case false:
                            switch (tax_entry.currency.is_local) {
                              case true:
                                entry.credit += amount.calculated
                                break
                              case false:
                                entry.amount_foreign += amount.calculated
                                entry.credit += (amount.calculated * selected_bill.rate)
                                break
                              case null:
                                entry.amount_foreign += amount.calculated
                                entry.credit += (amount.calculated * selected_bill.rate)
                                break
                            }
                            break
                        }
                      }
                   })
                })
              }

            })

            // disability of the validate button
            this.disableValidate = this.bill.entries.length === 0;
          }
        },
        deep: true,
      },

      selectedBill(value, old){

        if (value !== undefined) {
          this.lines.items.splice(0)
          this.bill.entries.splice(0)
        } else {
          if (this.lines.items.length > 0){
            this.lines.items.splice(0)
          }
          if (this.bill.entries.length > 0){
            this.bill.entries.splice(0)
          }
        }

        // disability of the validate button
        this.disableValidate = this.bill.entries.length === 0;
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

      // here we add the bill line and we create the debit entry for the customer if no one existing in bill entries array
      addLinesItem(){
        let default_account = ''

        Array.from(this.bill.creditAccounts).forEach(item => {
          if (item.depth === 1) {
            default_account = item
          }
        })

        this.lines.items.unshift({
          ref: Date.now(),
          label: '',
          account: default_account,
          quantity: 1,
          price: null,
          taxes: '',
          taxes_amount: []
        })

        // here we add accounting entries
        if (this.bill.entries.length === 0 && this.lines.items.length === 1){
          const index = this.bill.selectedBill
          const bill = this.bill.bills[index]
          const line = this.lines.items[0] // index is zero because every line is added using unshift method

          //add customer account to debit
          this.bill.entries.push({
            line_ref: '',
            dateOperation: bill.bill_at,
            account: bill.account,
            account_id: bill.account_id,
            label: bill.reference,
            amount_foreign: null,
            debit: null,
            credit: null,
            is_customer_account: true,
            is_tax_account: false,
          })

          // add credit entry
          this.bill.entries.push({
            line_ref: line.ref,
            dateOperation: bill.bill_at,
            account: line.account.label,
            account_id: line.account.id,
            label: '',
            amount_foreign: null,
            debit: null,
            credit: null,
            is_customer_account: false,
            is_tax_account: false,
          })

        }
          // add account to credit
         if (this.lines.items.length > 1){
          const index = this.bill.selectedBill
          const bill = this.bill.bills[index]
          const line = this.lines.items[0] // index is zero because every line is added using unshift method

          const found = this.bill.entries.find(entry => entry.line_ref === line.ref)

          if (!found){
            this.bill.entries.push({
              line_ref: line.ref,
              dateOperation: bill.bill_at,
              account: line.account.label,
              account_id: line.account.id,
              label: '',
              amount_foreign: null,
              debit: null,
              credit: null,
              is_customer_account: false,
              is_tax_account: false,
            })
          }
        }

      },

      resetTaxEntry(){
        this.taxes.forEach(tax => {
            const entry_index = this.bill.entries.findIndex(entry => entry.account_id === tax.account_id && entry.label === tax.name)
            tax.count_selected = null

            if (entry_index > -1){
               this.bill.entries.splice(entry_index, 1)
            }
          })
      },

      deleteTaxAmount(item){
        item.taxes_amount.forEach(amount => {
          const found_tax = item.taxes.find(selected_tax => amount.tax_ref === selected_tax)
          if (found_tax === undefined) {
            const unfound_tax_index = item.taxes_amount.findIndex(tax_amount => tax_amount.tax_ref === amount.tax_ref)
            item.taxes_amount.splice(unfound_tax_index, 1)
          }
        })
      },

      getUrlData(){
        const parse = window.location.pathname.split('/')
        this.moduleName = parse[2]
      },

      onResize () {
        this.windowSize = { x: window.innerWidth, y: window.innerHeight }
      },

      getModule(){
        this.apiCall('get', `/api/settings/journal?type=${this.moduleName}`).then(res => {
          const data = res.data
          this.moduleId = data['id']
        }).then(()=> {
          this.getBills() // this method is called to fill the left menu with all existing customers bill of this module
        }).then(()=> {
          this.getDebitAccounts() // this get all account that should be load in select field for debit amount
        }).then(()=> {
          this.getTaxes() // fill the tax for this journal
        })
      },

      getBills() {
        this.bill.billsLoading = true

        this.apiCall('get', `/api/billing/customer/bills/get?journal=${this.moduleId}`).then(res => {
          let data = res.data

          let jsonData = []
          Array.from(data).forEach(item => {

            jsonData.push({
              id: item.id,
              bill_at: this.formatDate(item.bill_at),
              deadline_at: this.formatDate(item.deadline_at),
              reference: item.reference,
              partner_id: item.partner !== null ? item.partner.id : null,
              partner: item.partner !== null ? item.partner.name : null,
              currency_id: item.currency.id,
              currency_name: item.currency.name,
              currency_is_local: item.currency.is_local,
              rate: item.rate,
              amount: this.thousandSeparator(item.amount),
              amount_foreign: this.thousandSeparator(item.amount_foreign),
              account_id: item.account.id,
              account: `${item.account.account_number} ${item.account.account_name}`

            })
          })
          this.bill.bills = jsonData
          this.bill.billsCopy = [...this.bill.bills]
          this.bill.billsLoading = false
        })

      },

      getCreditAccounts(){
        this.bill.creditLoading = true
        this.apiCall('get', `/api/accounting/plan/accounts-by-categories/get?categories=produit`).then(res => {
          let data = res.data
          let jsonData = []
          if(data.length > 0) {
            Array.from(data).forEach(item => {
              jsonData.push({
                id: item.id,
                label: `${item.account_number}  ${item.account_name}`,
                depth: item.depth
              })
            })
            this.bill.creditAccounts = jsonData
            this.bill.creditCopy = [...this.bill.creditAccounts];
            this.bill.creditLoading = false
          }

        })
      },

      getDebitAccounts(){
        this.bill.debitLoading = true
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
            this.bill.debitAccounts= jsonData
            this.bill.editedItem.debitAccount = jsonData[0].id
            this.bill.defaultItem.debitAccount = jsonData[0].id
            this.bill.debitAccountsCopy = [...this.bill.debitAccounts];
            this.bill.debitLoading = false
          }

        })
      },

      getTaxes(){
        this.apiCall('get', `/api/accounting/taxes/get?journal=${this.moduleId}`).then(res => {
          const data = res.data

          Array.from(data).forEach(item => {
            this.taxes.push({
              id: item.id,
              name: item.name,
              account_id: item.account_id,
              account_number: item.account__account_number,
              account_name: item.account__account_name,
              amount: item.amount,
              currency: {
                id: item.currency_id,
                name: item.currency__name,
                is_local: item.currency__is_local,
                symbol: item.currency__symbol,
              },
              is_fixed: item.is_fixed,
              count_selected: 0
            })
          })
        })
      },

      getPartners(){
        this.bill.partnerLoading = true
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
            this.bill.partners = jsonData
            this.bill.partnersCopy = [...this.bill.partners];
            this.bill.partnerLoading = false
          }

        })
      },

      savePartner(){
        if (this.bill.searchPartner === ''){
          this.snacktext = 'Veuillez saisir un nom avant de créer un partenaire'
          this.snackbar = true
          this.snackcolor = 'red darken-3'
        } else {
          let data = {name: this.bill.searchPartner }
          this.apiCall('post', '/api/billing/partner/save', data).then(res => {
            const partner = res.data.partner
            const message = res.data.message
            this.bill.partnerloading = false
            this.snacktext = message
            this.snackbar = true
            this.bill.partnerLoading = false
            this.snackcolor = 'green darken-3'
            this.bill.editedItem.partner = partner
            this.bill.searchPartner = ''
            this.bill.partners.push(partner)
            this.bill.partnersCopy = this.bill.partners

          })
        }
      },

      savePartnerAndEdit(){},

      saveBillEntries(){

        let lines = []
        let data = []
        const selected_bill_index = this.bill.selectedBill
        const selected_bill = this.bill.bills[selected_bill_index]

        this.bill.entries.forEach(entry => {

          const found_line = this.lines.items.find(item => item.ref === entry.line_ref)
          if (found_line === undefined) {

              if (entry.debit !== null || entry.credit !== null || entry.debit > 0 || entry.credit > 0) {

                data.push({
                  id: null,
                  currency: selected_bill.currency_id,
                  rate: selected_bill.rate,
                  ref_billing_customer: selected_bill.id,
                  ref_bill_line: null,
                  account: entry.account_id,
                  is_customer_account: entry.is_customer_account,
                  is_tax_account: false, //debug
                  date_at: selected_bill.bill_at,
                  label: entry.label,
                  partner: selected_bill.partner_id,
                  amount_foreign: entry.amount_foreign,
                  debit: entry.debit,
                  credit: entry.credit
              })
              }
          } else {
             data.push({
                  id: null,
                  currency: selected_bill.currency_id,
                  rate: selected_bill.rate,
                  ref_billing_customer: selected_bill.id,
                  ref_bill_line: {
                    account: found_line.account.id,
                    label: found_line.label,
                    quantity: found_line.quantity,
                    price: found_line.price,
                    priceWithTax: found_line.priceWithTax,
                    taxes: found_line.taxes_amount
                  },
                  account: entry.account_id,
                  is_customer_account: entry.is_customer_account,
                  is_tax_account: false, //debug
                  date_at: selected_bill.bill_at,
                  label: entry.label.toString() === '' ? selected_bill.reference : entry.label,
                  partner: selected_bill.partner_id,
                  amount_foreign: entry.amount_foreign,
                  debit: entry.debit,
                  credit: entry.credit
              })
          }
        })


        if (data.length > 0) {
          this.apiCall('post', `api/billing/customer/bill/entries/save`, data).then(res => {
            this.snacktext = res.data.message
            this.snackbar = true
            this.snackcolor = 'green darken-3'

          })
        }

        if (this.bill.entries.length === 0) {
          const message = `Aucune écriture comptable n'a été saisie. \r Commencez par entrer un ligne à à votre facture`
          this.snackcolor = 'red darken-4'
          this.snacktext = message
          this.multiLine = true
          this.snackbar = true
        }
      },

      getCurrency(){
        this.bill.currencyOperationLoading = true
        this.apiCall('get', `/api/treasury/currencies/get`).then(res => {
          let data = res.data
          let jsonData = []
          if(data.length > 0) {
            Array.from(data).forEach(item => {

              //set the local currency as default
              if (item.is_local){
                this.bill.editedItem.currency = item.id
                this.bill.defaultItem.currency = item.id
              }

              jsonData.push({
                id: item.id,
                label: `${item.name}`,
                symbol: `${item.symbol}`,
                is_local: item.is_local,
                rate: item.rate
              })
            })
            this.bill.currencies = jsonData
            this.bill.currenciesCopy = [...this.bill.currencies];

            this.bill.currencyOperationLoading = false
          }

        })
      },

      waitUpdate(){

        // bills-lines.html: sleclet account and tax no--data

        const message = 'Est indisponible... veuillez attendre la mise à jour'
        this.snackcolor = 'yellow darken-4'
        this.snacktext = message
        this.snackbar = true
      },

      searchIncomesCreditAccounts(e) {
        if (!this.bill.searchCredit) {
          this.bill.creditAccounts = this.bill.creditCopy;
        }

        this.bill.creditAccounts = this.bill.creditCopy.filter((item) => {
          return item.label.toLowerCase().indexOf(this.bill.searchCredit.toLowerCase()) > -1;
        });
      },

      searchIncomesDebitAccounts(e) {
        if (!this.bill.searchDebit) {
          this.bill.debitAccounts= this.bill.debitAccountsCopy;
        }

        this.bill.debitAccounts = this.bill.debitAccountsCopy.filter((item) => {
          return item.label.toLowerCase().indexOf(this.bill.searchDebit.toLowerCase()) > -1;
        });
      },

      searchIncomesPartners(e) {
        if (!this.bill.searchPartner) {
          this.bill.partners = this.bill.partnersCopy;
        }

        this.bill.partners = this.bill.partnersCopy.filter((item) => {
          if(this.bill.searchPartner != null){
            return item.label.toLowerCase().indexOf(this.bill.searchPartner.toLowerCase()) > -1;
          }
        });
      },

      searchIncomesCurrencies(e) {
        if (!this.bill.searchCurrency) {
          this.bill.currencies = this.bill.currenciesCopy;
        }

        this.bill.currencies = this.bill.currenciesCopy.filter((item) => {
          if(this.bill.searchCurrency != null){
            return item.label.toLowerCase().indexOf(this.bill.searchCurrency.toLowerCase()) > -1;
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

      thousandSeparator(item){
        if (item === null) {
          return null
        } else {
          const parse = parseFloat(item).toFixed(2)
          return parseFloat(parse).toLocaleString('fr-FR')
        }

      },

      setOperationDate(){
        const now  = (new Date(Date.now() - (new Date()).getTimezoneOffset() * 60000)).toISOString().substr(0, 10)
        const [year, month, day] = now.split('-')

        /*
        const selectedYear = this.currentYear
        const selectedMonth = `${this.currentMonth}`.length === 1 ? `0${this.currentMonth}` : this.currentMonth

        if(selectedYear === year && selectedMonth === month) {
          this.bill.editedItem.dateBill = now
          this.minDate = `${selectedYear}-${selectedMonth}-01`
          this.maxDate = `${selectedYear}-${selectedMonth}-31`
        } else {
          this.bill.editedItem.dateBill = `${selectedYear}-${selectedMonth}-01`
          this.minDate = `${selectedYear}-${selectedMonth}-01`
          this.maxDate = `${selectedYear}-${selectedMonth}-31`
        }
        */
      },

      deleteBill(item){
        this.bill.selectedBill = this.bill.bills.findIndex(bill => bill.id === item.id)
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
        this.bill.editedIndex = this.bill.entries.indexOf(item)
        this.bill.editedItem = Object.assign({}, item)
        this.bill.dialog = true
      },

      deleteItem (index, item) {
        this.lines.items.splice(index, 1)

        if (this.lines.items.length === 0) {
          this.bill.entries.splice(0)
        }

        const entry_index = this.bill.entries.findIndex(entry => entry.line_ref === item.ref)
        this.bill.entries.splice(entry_index, 1)
      },

      deleteItemConfirm () {
        let account_id = this.bill.editedItem.id

        this.bill.loading = true
        let data = {
          id: account_id
        }

        this.apiCall('post', '/api/accounting/main/delete', data).then(res => {
          this.bill.loading = false
          this.snacktext = res.data.message
          this.snackbar = true
          this.snackcolor = 'green darken-3'
          this.bill.entries.splice(this.bill.editedIndex, 1)
          this.bill.dialogDelete = false
        })
      },

      close () {
        this.bill.dialog= false
        this.$nextTick(() => {
          this.bill.editedItem = Object.assign({}, this.bill.defaultItem)
          this.bill.editedIndex = -1
        })
      },

      closeDelete () {
        this.bill.dialogDelete = false
        this.$nextTick(() => {
          this.bill.editedItem = Object.assign({}, this.bill.defaultItem)
          this.bill.editedIndex = -1
        })
      },

      closeDialogEntry () {
        this.bill.dialogEntry = false
        this.$nextTick(() => {
          this.bill.editedItem = {
            id: '',
            creditAccount: [],
            debitAccount: [],
            partner: '',
            reference: '',
            label: '',
            amountDebit:[],
            amountCredit: [],
            dateBill: (new Date(Date.now() - (new Date()).getTimezoneOffset() * 60000)).toISOString().substr(0, 10),
          }
          this.bill.editedItem.debitAccount[0] = this.bill.defaultItem.debitAccount[0]
          this.bill.editedIndex = -1
          this.bill.countDebitAccount= 1
          this.bill.countCreditAccount = 1
        })
      },

      setData(){
        return {
            id: this.bill.editedItem.id,
            currency: this.bill.editedItem.currency,
            rate: this.bill.editedItem.rate,
            account: this.bill.editedItem.debitAccount,
            dateBill: this.bill.editedItem.dateBill,
            dateDeadline: this.bill.editedItem.dateDeadline,
            partner: this.bill.editedItem.partner,
            reference: this.bill.editedItem.reference,
          }
      },

      saveAndClose () {
        if (this.bill.editedItem.editedIndex > -1) {
          this.bill.loading = true
          let data = this.setData()

        } else {
          let data = this.setData()

          if (this.$refs.formBill.validate()){

            this.bill.loading = true

            this.apiCall('post', '/api/billing/customer/bill/save', data).then(res => {
              let message = res.data.message

              this.snacktext = message
              this.snackcolor = 'green darken-3'

              this.bill.dialogEntry = false
              this.snackbar = true
              this.bill.loading = false

              this.$nextTick(() => {
                this.bill.editedItem = Object.assign({}, this.bill.defaultItem)
                this.bill.editedIndex = -1
              })


            }).catch((err) => {
              let message = err.response.data.message
              this.bill.loading = false
              this.snacktext = message
              this.snackbar = true
              this.snackcolor = 'red darken-3'
            })
          }
        }
      },

      saveAndContinue () {
        if (this.bill.editedIndex > -1) {
          this.bill.loading = true
          let data = this.setData()
        } else {
          let data = this.setData()

          if (this.$refs.formBill.validate()){

            this.bill.loading = true

            this.apiCall('post', '/api/billing/customer/bill/save', data).then(res => {
              let message = res.data.message

              this.snacktext = message
              this.snackcolor = 'green darken-3'

              this.snackbar = true
              this.bill.loading = false

              this.$nextTick(() => {
                this.bill.editedItem = Object.assign({}, this.bill.defaultItem)
                this.bill.editedIndex = -1
              })

            }).catch((err) => {
              let message = err.response.data.message
              this.bill.loading = false
              this.snacktext = message
              this.snackbar = true
              this.snackcolor = 'red darken-3'
              this.bill.dialog = false
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
        return this.bill.editedIndex === -1 ? 'Nouveau Compte' : 'Modifier Compte'
      },

      selectedBill(){
        return this.bill.selectedBill
      },

      // here i get the lines of the selectedBill
      getBillLines() {
        const index = this.bill.selectedBill
        const bill = this.bill.bills[index]
        if (bill !== undefined) {

          // here we fetch every existing accounting entry concerning this bill
          this.bill.loading = true

          this.apiCall('get', `/api/billing/customer/bill/${bill.id}/accounting/entries/get`).then(res => {
              this.bill.loading = false
              const data = res.data
              let jsonData = []
              Array.from(data).forEach(item => {

                jsonData.push({
                  id: item.id,
                  line_ref: item.ref_bill_line != null ? item.ref_bill_line.id : null,
                  dateOperation: this.formatDate(item.date_at),
                  account: `${item.account.account_number} ${item.account.account_name}`,
                  account_id: `${item.account.id}`,
                  label: item.label,
                  amount_foreign: item.amount_foreign,
                  debit: item.debit,
                  credit: item.credit,
                  rate: item.rate,
                  currency_is_local: item.currency.is_local,
                  partner: item.partner,
                  is_verified: item.is_verified
                })
              })
              this.bill.entries = jsonData

            }).then(() => {
              this.lines.loading = true
              // get every lines on the selected bill (on the left menu) and show them in bill lines table
              this.apiCall('get', `/api/billing/customer/bill/lines/get?billId=${bill.id}`).then(res => {
            const data = res.data
            let jsonData = []
            Array.from(data).forEach(item => {

             //bill_line__tax__amount , bill_line__tax__id

              const count = jsonData.push({
                id: item.id,
                ref: item.id,
                account: `${item.account.account_number} ${item.account.account_name}`,
                label: item.label,
                account: item.account.id,
                quantity: item.quantity,
                price: item.price,
                priceWithTax: item.price_with_tax,
                taxes: [],
                taxes_amount: []
              })

              //this fetch all taxes and tax amount of every line
              item.bill_line_tax.forEach(line_tax => {
                jsonData[count-1].taxes.push(line_tax.tax)
                jsonData[count-1].taxes_amount.push(line_tax.tax_amount)
              })
            })

            this.lines.items = jsonData
            this.lines.loading = false
          })
          })
        }
      },

      partnerPlaceholder () {
        return this.bill.partners.length === 0 ? 'Exemple: Remya Tshipamba' : 'Rechercher partenaire'
      },

      partnerLabel (){
        return this.bill.partners.length === 0 ? 'Créer un partenaire' : false
      },

      symbolCurrency(){
        let found

        Array.from(this.bill.currencies).forEach(currency => {
          if(currency.id === this.bill.editedItem.currency) {
            found = currency.symbol.toUpperCase()

            if(!currency.is_local){
              this.bill.isForeigncurrencyOperation = true
              this.bill.editedItem.rate = currency.rate
            } else {
              this.bill.isForeigncurrencyOperation = false
              this.bill.editedItem.rate = null
            }
          }
        })
        return `Montant en ${found}`
      },

      computedDateBillFormatted () {
        return this.formatDate(this.bill.editedItem.dateBill)
      },

      computedDateDeadlineFormatted () {
        return this.formatDate(this.bill.editedItem.dateDeadline)
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
      this.onResize()
      this.bill.selectedBill = undefined
    },

  })