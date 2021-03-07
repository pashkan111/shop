class CategoryManager(models.Manager):

    def get_queryset(self):
        return super().get_queryset()



    def get_category(self):
        
        DICT = {
            'Ноутбук': 'notebook__count',
            'Смартфон': 'smartphone__count'
        }     

        models = get_models_for_count('notebook', 'smartphone')
        qs = self.get_queryset().annotate(*models).values()
        return qs
        # return [dict(name = c['name'], slug = c['slug'], count = c[DICT[c['name']]]) for c in qs]
           
a = CategoryManager()
a.get_category()   