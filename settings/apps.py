from django.apps import AppConfig


class SettingsConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "settings"

    def ready(self):
        from accounting.models import PlanCategory, Plan, Main, FiscalYear
        from treasury.models import Currency, CurrencyDailyRate, CurrencyDiffrenceRate

        from .models import Journal

        import datetime

        groups = [
            {'category': 'actif', 'sub_categories': ['immobilisation incorporelle', 'immobilisation corporelle',
                                                     'immobilisation financière', 'actif circulant']},
            {'category': 'passif', 'sub_categories': ['capitaux propres', 'dettes', 'passif circulant']},
            {'category': 'charge',
             'sub_categories': ["charges d'exploitation", "charges financières", "charges exceptionnelles"]},
            {'category': 'produit',
             'sub_categories': ["produits d'exploitation", "produits financier", "produits exceptionnels"]}
        ]

        # create account categories
        for item in groups:
            if not PlanCategory.objects.filter(name=item['category']).exists():
                root = PlanCategory.add_root(name=item['category'])

                for sub_item in item['sub_categories']:
                    root.add_child(name=sub_item)

        # load main accounts children if any to the plan table
        if Main.objects.all().exists():
            main_accounts = Main.objects.all()

            for item in main_accounts:
                category = ''
                if item.account_type == 'encaissement':
                    category = PlanCategory.objects.get("produits d'exploitation")
                elif item.account_type == 'decaissement':
                    category = PlanCategory.objects.get("charges d'exploitation")

                root = Plan.add_root(account_number=item.account_number, account_name=item.account_name,
                                     category=category)

                # load sub accounts if any to the plan table
                if item.additional_set.all().exists():
                    sub_accounts = item.additional_set.all()

                    for sub_item in sub_accounts:
                        root.add_child(account_number=sub_item.account_number, account_name=sub_item.account_name)

                        sub_root = Plan.objects.get(account_number=sub_item.account_number,
                                                    account_name=sub_item.account_name)

                        # load sub account children if any to the plan table
                        if sub_item.adjunct_set.all().exists():
                            sub_item_sub_accounts = sub_item.adjunct_set.all()

                            for sub_item_child in sub_item_sub_accounts:
                                sub_root.add_root(account_number=sub_item_child.account_number,
                                                  account_name=sub_item_child.account_name)

        # create a default fiscal year if doesn't exists
        if not FiscalYear.objects.all().exists():
            year = datetime.datetime.now().year
            FiscalYear(year=year, rate=2200).save()

        # create currencies if doesn't exists
        if not Currency.objects.all().exists():
            countries = [
                {'country_code': 'us', 'name': 'Dollar Américain', 'symbol': 'usd', 'is_local': False},
                {'country_code': 'cd', 'name': 'Franc Congolais', 'symbol': 'cdf', 'is_local': True},
            ]

            for item in countries:
                Currency(country_code=item['country_code'], name=item['name'], symbol=item['symbol'],
                         is_local=item['is_local']).save()

        # create currency exchange différence rate

        if not CurrencyDiffrenceRate.objects.all().exists():
            categories = PlanCategory.objects.filter(name__in=['actif', 'passif']).all()

            account = {
                'actif': {
                    'root': {'number': '478', 'name': 'Écarts de conversion - actif'},
                    'children': [
                        {'number': '4781', 'name': 'Diminution des créances'},
                        {'number': '4782', 'name': 'Augmentation des dettes'},
                        {'number': '4788', 'name': 'Différences compensées par couverture de change'},
                    ],
                },
                'passif': {
                    'root': {'number': '479', 'name': 'Écarts de conversion - passif'},
                    'children': [
                        {'number': '4791', 'name': 'Diminution des créances'},
                        {'number': '4792', 'name': 'Augmentation des dettes'},
                        {'number': '4798', 'name': 'Différences compensées par couverture de change'},
                    ],
                },
            }

            for category in categories:
                if category.name == 'actif':
                    category = PlanCategory.objects.get(name='actif circulant')
                    root = Plan.add_root(account_number=account['actif']['root']['number'],
                                         account_name=account['actif']['root']['name'], category=category)

                    for child in account['actif']['children']:
                        root.add_child(account_number=child['number'], account_name=child['name'], category=category)

                    CurrencyDiffrenceRate(account=root, diff_category=category).save()
                elif category.name == 'passif':
                    category = PlanCategory.objects.get(name='passif circulant')
                    root = Plan.add_root(account_number=account['passif']['root']['number'], category=category,
                                         account_name=account['passif']['root']['name'])

                    for child in account['passif']['children']:
                        root.add_child(account_number=child['number'], account_name=child['name'], category=category)

                    CurrencyDiffrenceRate(account=root, diff_category=category).save()

        # set modules default accounting
        journals = [
            {'name': 'Banque', 'account_number': 56},
            {'name': 'Caisse', 'account_number': 57},
            {'name': 'Clients', 'account_number': 41},
            # {'name': 'Fiscalité', 'account_number': 44},
            {'name': 'Fournisseurs', 'account_number': 40},
            # {'name': 'Immobilisations', 'account_number': [x for x in range(20, 30)]},
            {'name': 'Personnel', 'account_number': 42},
            # {'name': 'Stock', 'account_number': [x for x in range(31, 40)]},

        ]

        for journal in journals:
            plan = Plan.objects.filter(account_number=journal['account_number'])

            if plan.exists():
                if not Journal.objects.filter(name=journal['name']).exists():
                    Journal.add_root(name=journal['name'], account=plan.get())
            else:
                categories = PlanCategory.objects.all()
                actif_circulant = categories.get(name="actif circulant")
                Plan.add_root(account_name=journal['name'], account_number=journal['account_number'],
                              category=actif_circulant)

                if not Journal.objects.filter(name=journal['name']).exists():
                    Journal.add_root(name=journal['name'], account=plan.get())

        # set default daily rate
        if not CurrencyDailyRate.objects.all().exists():
            cdf = Currency.objects.get(symbol='cdf')
            usd = Currency.objects.get(symbol='usd')

            rate = CurrencyDailyRate(from_currency=cdf, to_currency=usd, rate=2200)
            rate.save()
