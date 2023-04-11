/**
 * Utilise vuejs v.2 via cdn
 * Utilise vuetify v.2 via cdn
 * */

const app = new Vue({
    el: '#app',
    delimiters: ['${', '}'],
    vuetify: new Vuetify(),

    data () {
      return {
        comptes: [],
        classifications: [
            'actif',
            'passif'
        ],
        operations: [
            'encaissement',
            'decaissement'
        ],
        headers: [
          {
            text: 'Numéro du compte',
            align: 'start',
            sortable: true,
            value: 'number',
          },
          { text: 'Intitulé du compte', value: 'name' },
          { text: 'Classification', value: 'classification' },
          { text: 'Opération', value: 'operation' },
          { text: 'Description', value: 'description' },
          { text: 'Actions', value: 'actions', sortable: false },
        ],
        loading: false,
        dialog: false,
        dialogDelete: false,
        snackbar: false,
        multiLine: false,
        snacktext: '',
        snackcolor: '',
        timeout: 2000,
        search: '',
        options: {},
        editedIndex: -1,
        editedItem: {
          id: '',
          number: '',
          name: '',
          classification: '',
          operation: '',
          description: ''
        },
        defaultItem: {
          id: '',
          number: '',
          name: '',
          classification: '',
          operation: '',
          description: ''
      },
      }
    },

    watch: {
      options: {
        handler () {
          this.getDataFromApi()
        },
        deep: true,
      },

      dialog (val) {
        val || this.close()
      },
      dialogDelete (val) {
        val || this.closeDelete()
      },
    },

    methods: {
      getDataFromApi () {
        this.loading = true
        this.apiCall('get', '/api/accounting/plan/main/get').then(res => {
          let data = res.data
          let jsonData = []
          Array.from(data).forEach(item => {
            jsonData.push({
                  id: item.id,
                  number: item.account_number,
                  name: item.account_name,
                  operation: item.account_type,
                  classification: item.account_classification,
                  description: item.account_description
            })
          })
          this.comptes = jsonData
          this.loading = false
        })
      },
      /**
       * In a real application this would be a call to fetch() or axios.get()
       */
      apiCall (method, uri, data) {
        if(method === 'get') {
          return axios.get(uri)
        }
        else if(method === 'post') {
          return axios.post(uri, data)
        }

      },

      editItem (item) {
        this.editedIndex = this.comptes.indexOf(item)
        this.editedItem = Object.assign({}, item)
        this.dialog = true
      },

      deleteItem (item) {
        this.editedIndex = this.comptes.indexOf(item)
        this.editedItem = Object.assign({}, item)
        this.dialogDelete = true
      },

      deleteItemConfirm () {
        let account_id = this.editedItem.id

        this.loading = true
        let data = {
          id: account_id
        }

        this.apiCall('post', '/api/accounting/plan/main/delete', data).then(res => {
          this.loading = false
          this.snacktext = res.data.message
          this.snackbar = true
          this.snackcolor = 'green darken-3'
          this.comptes.splice(this.editedIndex, 1)
          this.dialogDelete = false
        })
      },

      close () {
        this.dialog = false
        this.$nextTick(() => {
          this.editedItem = Object.assign({}, this.defaultItem)
          this.editedIndex = -1
        })
      },

      closeDelete () {
        this.dialogDelete = false
        this.$nextTick(() => {
          this.editedItem = Object.assign({}, this.defaultItem)
          this.editedIndex = -1
        })
      },

      setData(){
        return {
            id: this.editedItem.id,
            account_number: this.editedItem.number,
            account_name: this.editedItem.name,
            account_classification: this.editedItem.classification,
            account_type: this.editedItem.operation,
            account_description: this.editedItem.description,
          }
      },

      save () {
        if (this.editedIndex > -1) {
          this.loading = true
          let data = this.setData()

          this.apiCall('post', '/api/accounting/plan/main/update', data).then(res => {
            let message = res.data.message
            this.snacktext = message
            this.snackcolor = 'green darken-3'
            this.snackbar = true
            this.dialog = false
            this.loading = false

            Object.assign(this.comptes[this.editedIndex], this.editedItem)

            this.$nextTick(() => {
              this.editedItem = Object.assign({}, this.defaultItem)
              this.editedIndex = -1
            })

          }).catch((err) => {
            let message = err.response.data.message
            this.loading = false
            this.snacktext = message
            this.snackbar = true
            this.snackcolor = 'red darken-3'
            this.dialog = false
          })
        } else {

          this.loading = true
          let data = this.setData()

          this.apiCall('post', '/api/accounting/plan/main/save', data).then(res => {
            let message = res.data.message
            this.snacktext = message
            this.snackcolor = 'green darken-3'
            this.comptes.push(this.editedItem)
            this.dialog = false
            this.snackbar = true
            this.loading = false

            this.$nextTick(() => {
              this.editedItem = Object.assign({}, this.defaultItem)
              this.editedIndex = -1
            })

          }).catch((err) => {
            let message = err.response.data.message
            this.loading = false
            this.snacktext = message
            this.snackbar = true
            this.snackcolor = 'red darken-3'
            this.dialog = false
          })
        }
      },

    },

    computed: {
      formTitle () {
        return this.editedIndex === -1 ? 'Nouveau Compte' : 'Modifier Compte'
      },
    },

    created () {
      this.getDataFromApi()
    },

  })